# Modelo Poisson para predicción de fútbol — Referencia técnica

## ¿Por qué Poisson?

Los goles en fútbol siguen aproximadamente una distribución de Poisson:
- Los goles son eventos raros e independientes
- Ocurren a una tasa promedio (λ) en un tiempo fijo (90 min)
- Este modelo es usado por Bet365, Opta, y la mayoría de casas serias

## Fórmula de Poisson

```
P(k goles) = (e^(-λ) × λ^k) / k!

Donde:
- λ = goles esperados (xG del equipo)
- k = número de goles a estimar
- e = 2.71828 (constante de Euler)
```

## Cómo calcular xG para selecciones nacionales

### Paso 1: Base histórica
```
xG_base = (goles_a_favor_clasificatorias / partidos_clasificatorias)
```

### Paso 2: Ajuste por calidad de rivales
- Si la mayoría de rivales fueron equipos débiles (FIFA rank >80): reducir xG_base × 0.85
- Si enfrentó equipos Top 20 FIFA frecuentemente: mantener o aumentar × 1.05

### Paso 3: Ajuste por forma reciente
```
multiplicador_forma = 0.85 + (IF / 3.5 × 0.30)
xG_ajustado = xG_base × multiplicador_forma
```

### Paso 4: Ajuste defensivo del rival
```
xG_final = xG_ajustado × (1 - (rating_defensivo_rival / 10))
```
El rating defensivo del rival va de 0 (muy permisivo) a 5 (muy sólido).
Puedes estimarlo por goles recibidos por partido: <0.8 = fuerte, >1.5 = débil

## Tabla de probabilidades aproximadas (referencia rápida)

Cuando no puedes calcular Poisson exacto, usa esta tabla:

| xG Local | xG Visita | % Local gana | % Empate | % Visita gana |
|---|---|---|---|---|
| 2.0 | 0.8 | 68% | 19% | 13% |
| 1.8 | 1.0 | 60% | 22% | 18% |
| 1.5 | 1.2 | 52% | 25% | 23% |
| 1.3 | 1.3 | 43% | 28% | 29% |
| 1.2 | 1.5 | 37% | 27% | 36% |
| 1.0 | 1.8 | 28% | 24% | 48% |
| 0.8 | 2.0 | 20% | 22% | 58% |

## Marcador más probable

El marcador más probable es la combinación de goles con mayor probabilidad conjunta:
```
P(A gana X-Y) = P(A anota X goles) × P(B anota Y goles)
```

Los marcadores más frecuentes en Mundiales históricamente:
- 1-0 (partido cerrado, favorito claro)
- 2-1 (partido abierto, diferencia de nivel)
- 1-1 (equilibrio, ambos anotan)
- 2-0 (dominador claro)
- 0-0 (fase de grupos, mucha presión, defensas fuertes)

## Ajustes situacionales importantes

| Situación | Ajuste |
|---|---|
| Eliminación directa (no puede perder) | -5% prob de empate, +5% al favorito |
| Primer partido del grupo (tensión) | +3% prob de empate |
| Rival con jugador clave lesionado/suspendido | +8% al equipo contrario |
| Partido en sede cercana a su país | +3% al equipo local culturalmente |
| 3 días de descanso vs 4+ días | -3% al equipo con menos descanso |

## Calibración con el mercado

El mercado de apuestas es eficiente a largo plazo. Si tu modelo da:
- **< 5% diferencia con el mercado**: Predicción robusta, alta confianza
- **5-15% diferencia**: Revisar si hay información que el mercado ya incorporó (lesión, clima)
- **> 15% diferencia**: Muy probable que el mercado tenga información que tú no, revisar fuentes

## Escala de confianza del modelo

```
ALTA CONFIANZA (★★★★★):
- Ambos equipos de CONMEBOL o UEFA con data abundante
- Diferencia de xG > 0.7
- Consistente con el mercado (< 8% diferencia)

MEDIA CONFIANZA (★★★☆☆):
- Un equipo de CAF, AFC, o CONCACAF menor
- Diferencia de xG 0.3-0.7
- Diferencia con mercado 8-15%

BAJA CONFIANZA (★★☆☆☆):
- Ambos equipos con poca data disponible
- Diferencia de xG < 0.3 (partido muy equilibrado)
- Diferencia con mercado > 15%
```
