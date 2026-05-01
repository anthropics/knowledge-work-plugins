# Template Completo — Fluxograma Swimlane

Este arquivo contém o código-fonte completo e funcional de um fluxograma swimlane,
já com todos os padrões da skill aplicados. Use como ponto de partida e adapte
ACTORS, PHASES, NODES e EDGES para o processo do usuário.

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Fluxograma – [Título do Processo]</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: Arial, sans-serif; background: #eef2f7; }
  .page { max-width: 1500px; margin: 0 auto; padding: 20px 14px; }
  .header { background: #1F3864; color: white; border-radius: 10px; padding: 18px 24px;
    margin-bottom: 14px; display: flex; align-items: center; justify-content: space-between; }
  .header h1 { font-size: 18px; font-weight: 700; }
  .header p  { font-size: 12px; color: #b0c4de; margin-top: 4px; }
  .header-right { text-align: right; font-size: 11px; color: #b0c4de; line-height: 1.8; }
  .legend { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 14px; align-items: center; }
  .legend-item { display: flex; align-items: center; gap: 6px; font-size: 11px; color: #444; }
  .legend-dot { width: 26px; height: 16px; border-radius: 3px; flex-shrink: 0; }
  .diagram-wrap { background: white; border-radius: 10px;
    box-shadow: 0 2px 14px rgba(0,0,0,.13); overflow-x: auto; }
  svg { display: block; }
  svg text { font-family: Arial, sans-serif; }
  /* Opcional: nota de alerta acima do diagrama */
  .alert-note { background: #fff3cd; border: 1.5px solid #E67E22; border-radius: 6px;
    padding: 8px 14px; font-size: 11px; color: #7D3C0A; margin-bottom: 12px; }
</style>
</head>
<body>
<div class="page">

  <div class="header">
    <div>
      <h1>Fluxograma – [Nome do Processo]</h1>
      <p>[Responsável] | [Empresa]</p>
    </div>
    <div class="header-right">
      <div>[N] Fases &nbsp;|&nbsp; Versão 1</div>
      <div>[N] Atores</div>
    </div>
  </div>

  <!-- Remova se não houver nota de alerta -->
  <div class="alert-note">
    ⚠️ <strong>[Título da nota]:</strong> [Texto da nota de alerta.]
  </div>

  <div class="legend" id="legend"></div>

  <div class="diagram-wrap">
    <svg id="diagram"></svg>
  </div>
</div>

<script>
// ═══════════════════════════════════════════════════════
// 1. CONSTANTES DE LAYOUT
// ═══════════════════════════════════════════════════════
const LBL_W  = 140;   // largura da coluna de fases
const LANE_W = 162;   // largura de cada raia de ator
const ROW_H  = 92;    // altura de cada linha
const NW     = 138;   // largura dos nós retangulares
const NH     = 54;    // altura dos nós retangulares
const DH     = 32;    // meia-altura do diamante
const DW     = 46;    // meia-largura do diamante
const HDR_H  = 65;    // altura do cabeçalho
const PAD    = 22;    // espaço interno superior

// Canais de roteamento para loops
const LMARGIN  = 108;  // canal esquerdo primário
const LMARGIN2 = 96;   // canal esquerdo secundário
const RMARGIN_FN = () => LBL_W + ACTORS.length * LANE_W + 22; // canal direito

// ═══════════════════════════════════════════════════════
// 2. ATORES (raias, da esquerda para a direita)
// ═══════════════════════════════════════════════════════
const ACTORS = [
  { id:'ator1', label:['ATOR 1','Descrição'],  color:'#1F3864', bg:'#EBF0F8' },
  { id:'ator2', label:['ATOR 2',''],           color:'#2E75B6', bg:'#E3EFF9' },
  { id:'ator3', label:['ATOR 3',''],           color:'#C0392B', bg:'#FDECEA' },
  // Adicione mais atores conforme necessário
];
const AI = {};
ACTORS.forEach((a,i) => AI[a.id] = i);

// Posição X do centro de uma raia
function lx(actor) { return LBL_W + AI[actor] * LANE_W + LANE_W / 2; }
// Posição Y do centro de uma linha
function ry(row)   { return HDR_H + PAD + (row - 1) * ROW_H + ROW_H / 2; }

// Bounds de um nó {cx, cy, top, bottom, left, right}
function nb(id) {
  const n = NODES.find(x => x.id === id);
  if (!n) return null;
  const cx = lx(n.actor), cy = ry(n.row);
  if (n.type === 'diamond' || n.type === 'diamond3') {
    return { cx, cy, top:cy-DH, bottom:cy+DH, left:cx-DW, right:cx+DW };
  }
  return { cx, cy, top:cy-NH/2, bottom:cy+NH/2, left:cx-NW/2, right:cx+NW/2 };
}

// ═══════════════════════════════════════════════════════
// 3. FASES
// ═══════════════════════════════════════════════════════
const PHASES = [
  { label:'FASE 1 – Nome da fase', rows:[1,3], border:'#1F3864', bg:'#EBF0F8' },
  { label:'FASE 2 – Nome da fase', rows:[4,6], border:'#2E75B6', bg:'#E3EFF9' },
  // ...
];

// ═══════════════════════════════════════════════════════
// 4. NÓS
// ═══════════════════════════════════════════════════════
// Tipos: 'start' | 'rect' | 'diamond' | 'diamond3' | 'oval' | 'oval_end'
// Propriedades: cancel:true → fundo rosado (cancelamento/alerta)
const NODES = [
  { id:'n01', actor:'ator1', row:1, type:'start',   label:['INÍCIO'] },
  { id:'n02', actor:'ator1', row:2, type:'rect',    label:['Atividade normal','segunda linha'] },
  { id:'n03', actor:'ator2', row:3, type:'rect',    label:['Atividade em','outro ator'] },
  { id:'n04', actor:'ator2', row:4, type:'diamond', label:['Decisão?'] },
  // decision 2-way: SIM sai por um lado, NÃO pelo outro
  { id:'n05', actor:'ator1', row:5, type:'rect',    label:['Se NÃO','volta aqui'] },
  { id:'n06', actor:'ator3', row:5, type:'rect',    label:['Se SIM','vai aqui'], cancel:true },
  { id:'n07', actor:'ator2', row:6, type:'oval',    label:['PROCESSO','CONCLUÍDO'] },
  { id:'n08', actor:'ator3', row:6, type:'oval_end',label:['ENCERRADO',''] },
];

// ═══════════════════════════════════════════════════════
// 5. SETAS (EDGES)
// ═══════════════════════════════════════════════════════
// explicit: usa a função explicitPath() para roteamento especial
// dashed: true → linha tracejada (loops, retornos)
// lbl: rótulo da seta (ex.: 'SIM', 'NÃO', 'CANCELAR')
const EDGES = [
  { f:'n01', t:'n02', lbl:'',     color:'#2E75B6' },
  { f:'n02', t:'n03', lbl:'',     color:'#2E75B6' },
  { f:'n03', t:'n04', lbl:'',     color:'#2E75B6' },
  // n04 diamond: SIM→RIGHT(n06), NÃO→LEFT(n05)
  { f:'n04', t:'n06', lbl:'SIM',  color:'#1E8449', explicit:'n04_n06' },
  { f:'n04', t:'n05', lbl:'NÃO',  color:'#E67E22', explicit:'n04_n05' },
  // n05 loop back → LEFT de n03
  { f:'n05', t:'n03', lbl:'retorna', color:'#E67E22', explicit:'n05_n03', dashed:true },
  { f:'n06', t:'n08', lbl:'',     color:'#C0392B' },
  { f:'n03', t:'n07', lbl:'',     color:'#117A65' }, // (após processar SIM, via n06)
];

// ═══════════════════════════════════════════════════════
// 6. ROTAS EXPLÍCITAS
// ═══════════════════════════════════════════════════════
// Implemente um case para cada seta com explicit:'chave'
// lx, ly = CENTRO do rótulo da seta
function explicitPath(key) {
  const RMARGIN = RMARGIN_FN();
  switch(key) {

    // PADRÃO: saída pelo lado direito do diamante → horizontal → desce até o nó
    case 'n04_n06': {
      const b = nb('n04'), t = nb('n06');
      const d = `M ${b.right} ${b.cy} L ${t.cx} ${b.cy} L ${t.cx} ${t.top}`;
      return { d, lx: (b.right + t.cx)/2, ly: b.cy - 10 };
    }

    // PADRÃO: saída pelo lado esquerdo do diamante → horizontal → desce até o nó
    case 'n04_n05': {
      const b = nb('n04'), t = nb('n05');
      const d = `M ${b.left} ${b.cy} L ${t.cx} ${b.cy} L ${t.cx} ${t.top}`;
      return { d, lx: (b.left + t.cx)/2, ly: b.cy - 10 };
    }

    // PADRÃO: loop via margem esquerda → chega pelo LEFT do destino
    case 'n05_n03': {
      const b = nb('n05'), t = nb('n03');
      const d = `M ${b.left} ${b.cy} L ${LMARGIN} ${b.cy} L ${LMARGIN} ${t.cy} L ${t.left} ${t.cy}`;
      return { d, lx: (b.left + LMARGIN)/2, ly: b.cy - 10 };
    }

    // PADRÃO: loop via margem direita → chega pelo RIGHT do destino
    // case 'nX_nY': {
    //   const b = nb('nX'), t = nb('nY');
    //   const d = `M ${b.right} ${b.cy} L ${RMARGIN} ${b.cy} L ${RMARGIN} ${t.cy} L ${t.right} ${t.cy}`;
    //   return { d, lx: (b.right + RMARGIN)/2, ly: b.cy - 10 };
    // }

    // PADRÃO: saída pelo BOTTOM do diamante → desce diretamente (mesma raia)
    // case 'nX_nY': {
    //   const b = nb('nX'), t = nb('nY');
    //   const d = `M ${b.cx} ${b.bottom} L ${b.cx} ${t.top}`;
    //   return { d, lx: b.cx + 8, ly: b.bottom + 14 };
    // }

    // PADRÃO: saída pelo BOTTOM do diamante → desce e depois vai para outra raia
    // case 'nX_nY': {
    //   const b = nb('nX'), t = nb('nY');
    //   const safeY = ry(LINHA_SEGURA) + NH/2 + 20; // abaixo dos nós intermediários
    //   const d = `M ${b.cx} ${b.bottom} L ${b.cx} ${safeY} L ${t.cx} ${safeY} L ${t.cx} ${t.top}`;
    //   return { d, lx: b.cx + 8, ly: b.bottom + 16 };
    // }

    default: return null;
  }
}

// ═══════════════════════════════════════════════════════
// 7. DIMENSÕES DO SVG (calculadas automaticamente)
// ═══════════════════════════════════════════════════════
const totalRows = Math.max(...NODES.map(n => n.row));
const svgW = LBL_W + ACTORS.length * LANE_W + 42;
const svgH = HDR_H + PAD + totalRows * ROW_H + PAD + 20;

// ═══════════════════════════════════════════════════════
// 8. UTILITÁRIOS DE RENDERIZAÇÃO SVG
// ═══════════════════════════════════════════════════════
const svg = document.getElementById('diagram');
svg.setAttribute('width', svgW);
svg.setAttribute('height', svgH);
svg.setAttribute('viewBox', `0 0 ${svgW} ${svgH}`);

function el(tag, attrs, parent) {
  const e = document.createElementNS('http://www.w3.org/2000/svg', tag);
  for (const [k,v] of Object.entries(attrs)) e.setAttribute(k,v);
  if (parent) parent.appendChild(e);
  return e;
}

function txt(content, x, y, opts, parent) {
  const t = el('text', {
    x, y,
    'text-anchor': opts.anchor || 'middle',
    'dominant-baseline': opts.base || 'middle',
    'font-size': opts.size || 10,
    fill: opts.fill || '#222',
    'font-weight': opts.bold ? 'bold' : 'normal',
    'font-family': 'Arial,sans-serif'
  }, parent);
  t.textContent = content;
  return t;
}

// Texto multi-linha COM clip para não transbordar o nó
function mTxtClipped(lines, cx, cy, opts, parent, clipId) {
  const lh = opts.lh || 13;
  const sy = cy - ((lines.length - 1) * lh) / 2;
  const g = el('g', { 'clip-path': `url(#${clipId})` }, parent);
  lines.forEach((l, i) => txt(l, cx, sy + i*lh, opts, g));
}

// ═══════════════════════════════════════════════════════
// 9. DEFS: MARCADORES DE SETA + CLIPPATH POR NÓ
// ═══════════════════════════════════════════════════════
const defs = el('defs', {}, svg);

// Marcadores de seta coloridos
const arrowColors = {
  blue:'#2E75B6', green:'#1E8449', orange:'#E67E22',
  red:'#C0392B', teal:'#117A65', brown:'#D35400'
};
Object.entries(arrowColors).forEach(([name, color]) => {
  const m = el('marker', {
    id:`arr-${name}`, markerWidth:'9', markerHeight:'7',
    refX:'8', refY:'3.5', orient:'auto'
  }, defs);
  el('polygon', { points:'0 0, 9 3.5, 0 7', fill:color }, m);
});

function markerForColor(c) {
  if (c === '#1E8449') return 'url(#arr-green)';
  if (c === '#E67E22') return 'url(#arr-orange)';
  if (c === '#C0392B') return 'url(#arr-red)';
  if (c === '#117A65') return 'url(#arr-teal)';
  if (c === '#D35400') return 'url(#arr-brown)';
  return 'url(#arr-blue)';
}

// ClipPath para cada nó (impede text overflow)
NODES.forEach(n => {
  const cx = lx(n.actor), cy = ry(n.row);
  const cp = el('clipPath', { id: `clip-${n.id}` }, defs);
  if (n.type === 'diamond' || n.type === 'diamond3') {
    el('rect', { x: cx-DW+6, y: cy-DH+4, width: (DW-6)*2, height: (DH-4)*2 }, cp);
  } else if (n.type === 'start' || n.type === 'oval' || n.type === 'oval_end') {
    el('rect', { x: cx-NW/2+8, y: cy-NH/2, width: NW-16, height: NH }, cp);
  } else {
    el('rect', { x: cx-NW/2+8, y: cy-NH/2+2, width: NW-12, height: NH-4 }, cp);
  }
});

// ═══════════════════════════════════════════════════════
// 10. RENDERIZAÇÃO (ordem importa!)
// ═══════════════════════════════════════════════════════

// 10.1 Fundos de fase + rótulos laterais + linha tracejada de topo
const phG = el('g', {}, svg);
PHASES.forEach(ph => {
  const y1 = HDR_H + PAD + (ph.rows[0]-1) * ROW_H;
  const y2 = HDR_H + PAD + ph.rows[1] * ROW_H;
  el('rect', { x:LBL_W, y:y1, width:ACTORS.length*LANE_W, height:y2-y1,
    fill:ph.bg, opacity:'0.4' }, phG);
  // Rótulo vertical da fase
  const fo = document.createElementNS('http://www.w3.org/2000/svg','foreignObject');
  fo.setAttribute('x', 0); fo.setAttribute('y', y1);
  fo.setAttribute('width', LBL_W-2); fo.setAttribute('height', y2-y1);
  const d = document.createElement('div');
  d.style.cssText = `height:${y2-y1}px;display:flex;align-items:center;
    justify-content:center;writing-mode:vertical-rl;transform:rotate(180deg);
    font-size:9px;font-weight:700;color:${ph.border};font-family:Arial;
    padding:2px;text-align:center;line-height:1.2;overflow:hidden;`;
  d.textContent = ph.label;
  fo.appendChild(d); phG.appendChild(fo);
  el('line', { x1:LBL_W, y1, x2:LBL_W+ACTORS.length*LANE_W, y2:y1,
    stroke:ph.border, 'stroke-width':'1.5', 'stroke-dasharray':'5 3', opacity:'0.7' }, phG);
});

// 10.2 Fundos e linhas divisórias das raias
const laneG = el('g', {}, svg);
ACTORS.forEach((a,i) => {
  const x = LBL_W + i*LANE_W;
  el('rect', { x, y:HDR_H, width:LANE_W, height:svgH-HDR_H, fill:a.bg, opacity:'0.38' }, laneG);
  el('line', { x1:x, y1:0, x2:x, y2:svgH, stroke:'#ccc', 'stroke-width':'0.7' }, laneG);
});
el('line', { x1:LBL_W+ACTORS.length*LANE_W, y1:0,
  x2:LBL_W+ACTORS.length*LANE_W, y2:svgH, stroke:'#aaa', 'stroke-width':'1' }, laneG);

// 10.3 Cabeçalho de atores
const hG = el('g', {}, svg);
el('rect', { x:0, y:0, width:svgW, height:HDR_H, fill:'#1F3864' }, hG);
ACTORS.forEach((a,i) => {
  const cx = LBL_W + i*LANE_W + LANE_W/2;
  el('rect', { x:LBL_W+i*LANE_W+3, y:3, width:LANE_W-6, height:HDR_H-6,
    fill:a.color, rx:'5' }, hG);
  const lines = a.label;
  const sy = HDR_H/2 - ((lines.length-1)*13)/2;
  lines.forEach((l,idx) => {
    const t = el('text', { x:cx, y:sy+idx*13, 'text-anchor':'middle',
      'dominant-baseline':'middle', 'font-size':'10.5', fill:'white',
      'font-weight':'bold', 'font-family':'Arial,sans-serif' }, hG);
    t.textContent = l;
  });
});
const lt = el('text', { x:LBL_W/2, y:HDR_H/2, 'text-anchor':'middle',
  'dominant-baseline':'middle', 'font-size':'8.5', fill:'#aaa',
  'font-weight':'bold', 'font-family':'Arial,sans-serif' }, hG);
lt.textContent = 'ATOR / FASE';

// 10.4 SETAS (desenhadas ANTES dos nós — ficam atrás)
const eG = el('g', {}, svg);
EDGES.forEach(edge => {
  const fn = NODES.find(n=>n.id===edge.f);
  const tn = NODES.find(n=>n.id===edge.t);
  if (!fn||!tn) return;
  const fb = nb(edge.f), tb = nb(edge.t);
  const color = edge.color || '#2E75B6';
  const marker = markerForColor(color);
  const dashed = edge.dashed ? '6 3' : 'none';
  let d, lblX, lblY;

  if (edge.explicit) {
    const ep = explicitPath(edge.explicit);
    if (ep) { d = ep.d; lblX = ep.lx; lblY = ep.ly; }
  }

  if (!d) {
    // Roteamento automático
    if (fn.actor === tn.actor && tn.row > fn.row) {
      d = `M ${fb.cx} ${fb.bottom} L ${tb.cx} ${tb.top}`;
      lblX = fb.cx + 8; lblY = (fb.bottom + tb.top) / 2;
    } else if (fn.actor !== tn.actor && tn.row === fn.row) {
      const goR = AI[tn.actor] > AI[fn.actor];
      d = goR ? `M ${fb.right} ${fb.cy} L ${tb.left} ${tb.cy}`
              : `M ${fb.left} ${fb.cy} L ${tb.right} ${tb.cy}`;
      lblX = (fb.cx + tb.cx)/2; lblY = fb.cy - 10;
    } else {
      const midY = fb.bottom + (tb.top - fb.bottom) * 0.45;
      d = `M ${fb.cx} ${fb.bottom} L ${fb.cx} ${midY} L ${tb.cx} ${midY} L ${tb.cx} ${tb.top}`;
      lblX = (fb.cx + tb.cx)/2; lblY = midY - 8;
    }
  }

  el('path', { d, stroke:color, 'stroke-width':'2',
    fill:'none', 'stroke-dasharray':dashed, 'marker-end':marker }, eG);

  if (edge.lbl && lblX != null) {
    // ✅ Largura dinâmica — nunca trunca o texto
    const lblW = Math.max(34, edge.lbl.length * 5.6 + 14);
    const bgC = color === '#1E8449' ? '#E9F7EF'
              : color === '#C0392B' ? '#FDECEA' : '#FEF9E7';
    el('rect', { x:lblX-lblW/2, y:lblY-8, width:lblW, height:15, rx:3,
      fill:bgC, stroke:color, 'stroke-width':'0.9' }, eG);
    const lt = el('text', { x:lblX, y:lblY, 'text-anchor':'middle',
      'dominant-baseline':'middle', 'font-size':'7.5', fill:color,
      'font-weight':'bold', 'font-family':'Arial,sans-serif' }, eG);
    lt.textContent = edge.lbl;
  }
});

// 10.5 NÓS (desenhados por último — ficam na frente das setas)
const nG = el('g', {}, svg);
NODES.forEach(n => {
  const actor = ACTORS[AI[n.actor]];
  const cx = lx(n.actor), cy = ry(n.row);
  const clipId = `clip-${n.id}`;

  if (n.type === 'start') {
    el('rect', { x:cx-NW/2, y:cy-NH/2, width:NW, height:NH, rx:27, fill:actor.color }, nG);
    mTxtClipped(n.label, cx, cy, { fill:'white', size:9.5, bold:true, lh:13 }, nG, clipId);

  } else if (n.type === 'oval') {
    el('rect', { x:cx-NW/2, y:cy-NH/2-4, width:NW, height:NH+8, rx:30, fill:'#1E8449' }, nG);
    mTxtClipped(n.label, cx, cy, { fill:'white', size:8.8, bold:true, lh:12 }, nG, clipId);

  } else if (n.type === 'oval_end') {
    el('rect', { x:cx-NW/2, y:cy-NH/2-4, width:NW, height:NH+8, rx:30, fill:'#C0392B' }, nG);
    mTxtClipped(n.label, cx, cy, { fill:'white', size:9.5, bold:true, lh:13 }, nG, clipId);

  } else if (n.type === 'diamond' || n.type === 'diamond3') {
    const pts = `${cx},${cy-DH} ${cx+DW},${cy} ${cx},${cy+DH} ${cx-DW},${cy}`;
    const fillC = n.cancel ? '#FADBD8' : '#FFF8E1';
    const bordC = n.type==='diamond3' ? '#6C3483' : actor.color;
    el('polygon', { points:pts, fill:fillC, stroke:bordC, 'stroke-width':'2' }, nG);
    if (n.type === 'diamond3') {
      // Anel tracejado extra para diferenciar diamante de 3 saídas
      const pts2 = `${cx},${cy-DH-5} ${cx+DW+7},${cy} ${cx},${cy+DH+5} ${cx-DW-7},${cy}`;
      el('polygon', { points:pts2, fill:'none', stroke:'#6C3483',
        'stroke-width':'0.9', 'stroke-dasharray':'3 2', opacity:'0.5' }, nG);
    }
    mTxtClipped(n.label, cx, cy, { fill:bordC, size:8.8, bold:true, lh:12 }, nG, clipId);

  } else {
    // rect padrão
    const fillC = n.cancel ? '#FADBD8' : 'white';
    const bordC = n.cancel ? '#C0392B' : actor.color;
    el('rect', { x:cx-NW/2, y:cy-NH/2, width:NW, height:NH, rx:5,
      fill:fillC, stroke:bordC, 'stroke-width':'1.8' }, nG);
    // Barra colorida lateral esquerda
    el('rect', { x:cx-NW/2, y:cy-NH/2, width:5, height:NH, rx:3, fill:bordC }, nG);
    mTxtClipped(n.label, cx+4, cy,
      { fill: n.cancel ? '#7B241C' : '#222', size:9, lh:13 }, nG, clipId);
  }
});

// ═══════════════════════════════════════════════════════
// 11. LEGENDA (gerada automaticamente)
// ═══════════════════════════════════════════════════════
const legendEl = document.getElementById('legend');
ACTORS.forEach(a => {
  const item = document.createElement('div');
  item.className = 'legend-item';
  item.innerHTML = `<div class="legend-dot" style="background:${a.color}"></div>
    <span>${a.label.join(' ')}</span>`;
  legendEl.appendChild(item);
});
[
  ['Atividade normal', '#2E75B6', 'rect'],
  ['Decisão 2 saídas', '#1E8449', 'diamond'],
  ['Decisão 3 saídas', '#6C3483', 'diamond3'],
  ['Cancelamento',     '#C0392B', 'cancel'],
  ['Início / Fim',     '#1F3864', 'oval'],
].forEach(([lbl, c, t]) => {
  const item = document.createElement('div');
  item.className = 'legend-item';
  item.style.marginLeft = '6px';
  let icon = '';
  if (t==='rect')     icon = `<div class="legend-dot" style="background:${c};border-radius:3px;border-left:4px solid ${c}"></div>`;
  if (t==='diamond')  icon = `<div style="width:16px;height:16px;background:#FFF8E1;border:2px solid ${c};transform:rotate(45deg);flex-shrink:0;"></div>`;
  if (t==='diamond3') icon = `<div style="width:16px;height:16px;background:#FFF8E1;border:2px solid ${c};transform:rotate(45deg);flex-shrink:0;outline:1px dashed ${c};outline-offset:2px;"></div>`;
  if (t==='cancel')   icon = `<div class="legend-dot" style="background:#FADBD8;border:2px solid ${c};border-radius:3px;"></div>`;
  if (t==='oval')     icon = `<div class="legend-dot" style="background:${c};border-radius:20px"></div>`;
  item.innerHTML = `${icon}<span>${lbl}</span>`;
  legendEl.appendChild(item);
});
</script>
</body>
</html>
```
