---
name: fluxograma-builder
description: >
  Cria fluxogramas swimlane profissionais em HTML/SVG com raias por ator (swimlanes),
  fases numeradas, nós coloridos por tipo e roteamento de setas sem sobreposição.
  Use esta skill sempre que o usuário pedir um fluxograma, diagrama de processo,
  mapa de fluxo, swimlane, diagrama de atores, BPM visual, ou qualquer representação
  gráfica de um processo com múltiplos responsáveis — mesmo que não mencione HTML ou SVG.
  Também use ao reconstruir ou corrigir fluxogramas existentes com problemas de sobreposição,
  setas mal roteadas, texto transbordando ou pontos de conexão duplicados.
---

# Construtor de Fluxogramas Swimlane

Este skill produz fluxogramas swimlane profissionais como arquivos HTML auto-contidos,
renderizados em SVG puro via JavaScript. Nenhuma biblioteca externa é necessária.

Antes de começar, leia `references/template.md` — ele contém o código-base completo
com todos os padrões já implementados. Adapte ACTORS, PHASES, NODES e EDGES para o
processo descrito pelo usuário.

---

## 1. Constantes de Layout

```javascript
const LBL_W  = 140;   // largura da coluna de fases
const LANE_W = 162;   // largura de cada raia de ator
const ROW_H  = 92;    // altura de cada linha
const NW     = 138;   // largura dos nós retangulares
const NH     = 54;    // altura dos nós retangulares
const DH     = 32;    // meia-altura do diamante
const DW     = 46;    // meia-largura do diamante
const HDR_H  = 65;    // altura do cabeçalho
const PAD    = 22;    // espaço interno superior

const LMARGIN  = 108; // canal esquerdo primário para loops
const LMARGIN2 = 96;  // canal esquerdo secundário
const RMARGIN_FN = () => LBL_W + ACTORS.length * LANE_W + 22;
```

---

## 2. Estrutura de Dados

### ACTORS — Raias (esquerda para direita)
```javascript
{ id:'nome', label:['LINHA 1','linha 2'], color:'#HEX', bg:'#HEX' }
```

### PHASES — Fases do processo
```javascript
{ label:'FASE 1 – Nome', rows:[1,3], border:'#HEX', bg:'#HEX' }
```

### NODES — Tipos disponíveis

| type | Forma | Uso |
|------|-------|-----|
| `start` | Cápsula colorida | Início |
| `rect` | Retângulo com barra lateral | Atividade normal |
| `diamond` | Losango | Decisão 2 saídas |
| `diamond3` | Losango + anel tracejado | Decisão 3 saídas |
| `oval` | Cápsula verde | Fim positivo |
| `oval_end` | Cápsula vermelha | Encerramento |

Adicione `cancel: true` em nós de alerta/cancelamento → fundo rosado `#FADBD8`.

---

## 3. Regra de Ouro: Ponto Único por Conexão

**Nenhum nó pode ter 2 setas chegando ou saindo pelo mesmo ponto (top/bottom/left/right).**

Mapeie antecipadamente:
- **TOP** → entrada do fluxo principal (nó acima)
- **BOTTOM** → saída principal ou decisão direta
- **LEFT** → loop de retorno via margem esquerda ou saída de decisão
- **RIGHT** → loop de retorno via margem direita ou saída de decisão

### Diamantes com 3 saídas — atribuição obrigatória

```
         TOP ← entrada
          │
  LEFT ◄──◆──► RIGHT
          │
        BOTTOM
```

Exemplo: NÃO→LEFT, SIM→RIGHT (ou LEFT se destino é mais à esquerda), CANCELAR→BOTTOM.
Nunca coloque duas saídas no mesmo vértice.

---

## 4. Roteamento de Loops

Loops que voltam a etapas anteriores usam **canais de margem** para não sobrepor nós.

### Via margem esquerda → chega pelo LEFT do destino
```javascript
case 'nA_nB': {
  const b = nb('nA'), t = nb('nB');
  const d = `M ${b.left} ${b.cy} L ${LMARGIN} ${b.cy} L ${LMARGIN} ${t.cy} L ${t.left} ${t.cy}`;
  return { d, lx: (b.left + LMARGIN)/2, ly: b.cy - 10 };
}
```

### Via margem direita → chega pelo RIGHT do destino
```javascript
case 'nA_nB': {
  const b = nb('nA'), t = nb('nB');
  const d = `M ${b.right} ${b.cy} L ${RMARGIN} ${b.cy} L ${RMARGIN} ${t.cy} L ${t.right} ${t.cy}`;
  return { d, lx: (b.right + RMARGIN)/2, ly: b.cy - 10 };
}
```

Se dois loops chegam ao mesmo nó, use `LMARGIN` para um e `LMARGIN2` (96) para o outro.

**Posicione o rótulo no meio do segmento horizontal** (não no vertical):
```javascript
lx: (b.left + LMARGIN)/2, ly: b.cy - 10
```

---

## 5. Labels de Setas — Largura Dinâmica

Nunca use largura fixa. Labels como "PEDIR AJUSTES" transbordam caixas pequenas:

```javascript
const lblW = Math.max(34, edge.lbl.length * 5.6 + 14);
// Box sempre centrado em (lblX, lblY)
el('rect', { x:lblX-lblW/2, y:lblY-8, width:lblW, height:15, rx:3, ... });
```

---

## 6. Clipping de Texto nos Nós

Todo texto de nó deve ser clipado com `<clipPath>` para não transbordar o card:

```javascript
// Em defs — um clipPath por nó:
NODES.forEach(n => {
  const cp = el('clipPath', { id:`clip-${n.id}` }, defs);
  if (n.type === 'diamond' || n.type === 'diamond3') {
    el('rect', { x:cx-DW+6, y:cy-DH+4, width:(DW-6)*2, height:(DH-4)*2 }, cp);
  } else {
    el('rect', { x:cx-NW/2+8, y:cy-NH/2+2, width:NW-12, height:NH-4 }, cp);
  }
});

// Ao renderizar texto:
const g = el('g', { 'clip-path':`url(#clip-${n.id})` }, parent);
lines.forEach((l,i) => txt(l, cx, sy+i*lh, opts, g));
```

---

## 7. Ordem de Renderização (obrigatória)

1. `<defs>` — marcadores de seta + clipPaths
2. Fundos de fase
3. Fundos e linhas das raias
4. Cabeçalho de atores
5. **Setas** — desenhadas ANTES dos nós (ficam atrás)
6. **Nós** — desenhados por último (ficam na frente)

---

## 8. Padrão de Cores por Semântica

| Cor | Uso |
|-----|-----|
| `#2E75B6` | Fluxo principal / sistema |
| `#1E8449` | Aprovação / sucesso (SIM) |
| `#E67E22` | Revisão / retorno (NÃO) |
| `#C0392B` | Cancelamento / alerta |
| `#D35400` | Parceiro externo |
| `#117A65` | Onboarding / TI |

---

## 9. Checklist de Qualidade

- [ ] Nenhum nó com 2 setas no mesmo ponto (TOP/BOTTOM/LEFT/RIGHT)
- [ ] Todos os loops usam canal LMARGIN ou RMARGIN
- [ ] Texto de nó com `clip-path` aplicado
- [ ] Labels de seta com largura dinâmica
- [ ] Setas desenhadas antes dos nós no SVG
- [ ] Diamantes `diamond3` com anel tracejado extra
- [ ] Nós `cancel:true` com fundo rosado
- [ ] SVG auto-dimensionado pelos dados (não fixo)
- [ ] Legenda gerada automaticamente

---

## Referência de Código

Para o template completo funcional com todos os padrões implementados, leia:
`references/template.md`
