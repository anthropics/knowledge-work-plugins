# Fluxograma Builder

Plugin para criação de fluxogramas swimlane profissionais em HTML/SVG — sem dependências externas.

## O que faz

Gera arquivos HTML auto-contidos com fluxogramas swimlane interativos a partir da descrição de um processo. Ideal para mapear processos com múltiplos responsáveis como RH, aprovações, onboarding e recrutamento.

## Funcionalidades

- **Raias por ator** — cada responsável tem sua própria faixa visual
- **Fases numeradas** — agrupamento visual por etapa do processo
- **Tipos de nó** — atividade, decisão 2-vias, decisão 3-vias, início, fim
- **Roteamento sem sobreposição** — regra de ponto único por conexão (cada lado do nó: TOP/BOTTOM/LEFT/RIGHT é usado por no máximo uma seta)
- **Loops via canais de margem** — retornos a etapas anteriores nunca sobrepõem nós
- **Texto clipado** — labels sempre dentro dos cartões, sem transbordo
- **Labels dinâmicas** — caixas de rótulo de seta com largura automática

## Exemplo de uso

> "Crie um fluxograma do processo de abertura de vagas. Os atores são Gestor, Sistema, Aprovadores e RH. O Gestor abre a solicitação, o Sistema encaminha para aprovação, os Aprovadores decidem (SIM / NÃO / CANCELAR)..."

## Instalação

1. No Cowork, acesse o marketplace de plugins
2. Busque por **fluxograma-builder**
3. Clique em instalar

## Estrutura

```
fluxograma-builder/
├── .claude-plugin/plugin.json
├── .mcp.json
├── README.md
└── skills/
    └── fluxograma-builder/
        ├── SKILL.md
        └── references/
            └── template.md   ← código-fonte completo como referência
```

## Autor

Rodrigo Moraes — rmoraes3008@gmail.com

## Licença

Apache-2.0
