# Betcris — Estructura de Mercados y Gestión de Capital

## Arquitectura de mercados Betcris (extraída del sistema real)

Betcris ofrece 4 niveles de mercado por partido, clasificados aquí
por riesgo de capital de menor a mayor.

---

## NIVEL 1 — MERCADOS DE BAJO RIESGO (ancla del capital)
*Probabilidad alta, retorno moderado. Base de cualquier apuesta inteligente.*

| Mercado | Descripción | Cuándo usar |
|---|---|---|
| **Doble Oportunidad** | Cubre 2 de 3 resultados: Local/Empate, Local/Visita, Visita/Empate | Cuando el favorito tiene 55-70% de probabilidad — no es certeza total |
| **Under 2.5 goles** | El partido termina con 0, 1 o 2 goles | Cuando xG combinado < 2.2 (partidos cerrados, defensas fuertes) |
| **Over 2.5 goles** | El partido termina con 3+ goles | Cuando xG combinado > 2.8 (ambos equipos atacan) |
| **Ambos Equipos Anotan - No** | Al menos un equipo hace valla invicta | Cuando xG del rival débil < 0.8 |
| **Ambos Equipos Anotan - Sí** | Ambos equipos marcan | Cuando ambos xG > 1.0 y defensa permisiva |
| **Bajas de 1.5 en Ambas Mitades** | Menos de 2 goles por tiempo | Partidos muy tácticos/cerrados |
| **Par/Impar Total** | Número total de goles es par o impar | Complemento táctico de bajo riesgo |

---

## NIVEL 2 — MERCADOS DE RIESGO MEDIO (cuerpo de la apuesta)
*Balance entre probabilidad y retorno. El núcleo de la estrategia.*

| Mercado | Descripción | Cuándo usar |
|---|---|---|
| **1X2 Resultado** | Victoria local / Empate / Victoria visitante | Favorito con >60% según modelo |
| **Handicap Asiático** | 0/-0.5 al favorito, 0/+0.5 al desfavorecido | Partidos con diferencia moderada (xG diff 0.4-0.8) |
| **Valla Invicta (Clean Sheet)** | Un equipo no recibe goles | Cuando xG rival < 0.7 |
| **Ganar Alguna Mitad** | El equipo gana al menos un tiempo | Favorito claro que puede arrancar tarde |
| **Rango de Goles 2-3** | El partido termina con 2 o 3 goles en total | El escenario más frecuente en Mundiales (40% de partidos) |
| **Medio Tiempo/Tiempo Completo** | Resultado al descanso + resultado final | Cuando el modelo predice partido parejo en primera mitad |
| **Resultado + BTTS combinado** | Combina ganador con si ambos anotan | Cuando ambos xG son altos pero hay favorito claro |

---

## NIVEL 3 — MERCADOS DE RIESGO ALTO (especulativos)
*Cuotas altas, menor probabilidad. Solo con fracción pequeña del capital.*

| Mercado | Descripción | Cuándo usar |
|---|---|---|
| **Marcador Correcto** | Resultado exacto del partido | Solo cuando el marcador más probable tiene >15% |
| **Marcador Correcto 1ª Mitad** | Resultado exacto al descanso | Partidos muy predecibles tácticamente |
| **Goles Exactos por Equipo** | Cuántos goles marca cada equipo | Nunca como apuesta principal |
| **Primer Gol + Resultado Final** | Quién anota primero y quién gana | Cuando hay dominador claro desde inicio |
| **Método de Victoria** | Regular time / Tiempo extra / Penales | Solo en partidos eliminatorios |
| **Minuto del Primer Gol** | Rango de tiempo del primer gol | Especulativo puro, complemento pequeño |
| **Margen de Victoria** | Por cuántos goles gana | Cuando la diferencia de xG es >1.0 |

---

## NIVEL 4 — MERCADOS DE MUY ALTO RIESGO (no recomendados)
*Solo para apostadores con tolerancia extrema al riesgo.*

| Mercado | Descripción |
|---|---|
| Gana Ambas Mitades | El equipo gana los dos tiempos — muy improbable |
| Marcador 3-0 o más | Goleadas — ocurren <8% de partidos |
| 7+ goles | Prácticamente imposible en fútbol de élite |
| Arsenal/PSG Gana Ambas Mitades | Cuotas de +525 a +800 |

---

## CONVERSIÓN DE CUOTAS AMERICANAS A PROBABILIDAD REAL

```
Cuota POSITIVA (+XXX):
  Prob implícita = 100 / (XXX + 100)
  Ejemplo: +126 → 100/226 = 44.2%

Cuota NEGATIVA (-XXX):
  Prob implícita = XXX / (XXX + 100)
  Ejemplo: -146 → 146/246 = 59.3%

Margen de la casa (vig):
  Suma de todas las probabilidades implícitas > 100%
  La diferencia es el margen de Betcris (~5-8% en mercados principales)

Probabilidad REAL ajustada:
  Prob real = Prob implícita / (suma total de probabilidades del mercado)
```

---

## SISTEMA KELLY CRITERION — DISTRIBUCIÓN DE CAPITAL

El Kelly Criterion es la fórmula matemática que usan los apostadores
profesionales para determinar qué porcentaje del bankroll apostar.

### Fórmula Kelly Completo:
```
f* = (b×p - q) / b

Donde:
  f* = fracción del bankroll a apostar
  b  = cuota decimal - 1 (ganancia neta por unidad)
  p  = probabilidad del modelo (nuestra estimación)
  q  = 1 - p (probabilidad de perder)
```

### Conversión cuota americana a decimal:
```
Positiva (+XXX): decimal = (XXX/100) + 1
Negativa (-XXX): decimal = (100/XXX) + 1

Ejemplo:
  +126 → (126/100) + 1 = 2.26
  -146 → (100/146) + 1 = 1.685
```

### Kelly Fraccionado (SIEMPRE usar 25% del Kelly completo):
```
f_seguro = f* × 0.25

¿Por qué 25%? Porque el Kelly completo asume probabilidades exactas.
Nuestro modelo tiene un margen de error del 5-10%, así que usar el
25% del Kelly elimina el riesgo de ruina del bankroll.
```

### Ejemplo con Q500, PSG vs Arsenal:

```
Apuesta: PSG gana (-146)
  Cuota decimal: 1.685
  b = 1.685 - 1 = 0.685
  p_modelo = 0.62 (62% según modelo)
  q = 1 - 0.62 = 0.38

  Kelly completo = (0.685 × 0.62 - 0.38) / 0.685
                = (0.4247 - 0.38) / 0.685
                = 0.0447 / 0.685
                = 6.5% del bankroll

  Kelly fraccionado (25%) = 6.5% × 0.25 = 1.6%
  Sobre Q500 = Q8 → demasiado bajo, no vale la pena

Apuesta: Doble Oportunidad PSG/Draw (-301)
  Cuota decimal: (100/301) + 1 = 1.332
  b = 0.332
  p_modelo = 0.62 + 0.18 = 0.80 (PSG gana O empata)
  q = 0.20

  Kelly completo = (0.332 × 0.80 - 0.20) / 0.332
                = (0.2656 - 0.20) / 0.332
                = 0.0656 / 0.332
                = 19.8% del bankroll

  Kelly fraccionado (25%) = 19.8% × 0.25 = 4.9%
  Sobre Q500 = Q24.5 → apuesta válida con retorno seguro
```

---

## PROTOCOLO DE DISTRIBUCIÓN DE CAPITAL — 3 NIVELES

Después de recibir el monto del usuario, distribuir SIEMPRE así:

### Distribución base:
```
60% → Apuesta ANCLA (Nivel 1-2, menor riesgo, Kelly confirma valor)
30% → Apuesta VALOR (Nivel 2-3, retorno medio, hay ventaja vs mercado)
10% → Apuesta ESPECULATIVA (Nivel 3, cuota alta, fracción mínima)
```

### Reglas de selección:
1. La apuesta ANCLA solo si Kelly fraccionado > 3% del bankroll
2. La apuesta VALOR solo si hay "valor" (prob modelo > prob implícita Betcris)
3. La apuesta ESPECULATIVA NUNCA si la cuota es menor a +200
4. Si no hay valor claro en ningún mercado → recomendar NO APOSTAR
5. El total apostado NUNCA debe superar el 15% del bankroll en un partido
6. Si el capital dado es < Q200 → apostar solo al mercado ANCLA

---

## TABLA DE VALOR (cuándo hay ventaja vs Betcris)

```
Hay VALOR cuando:
  Probabilidad del modelo > Probabilidad implícita de Betcris + 3%

Ejemplo:
  Modelo dice PSG gana: 62%
  Betcris implica PSG gana: 59.3% (cuota -146)
  Diferencia: 2.7% → NO hay valor suficiente (umbral es 3%)

  Modelo dice Under 2.5: 55%
  Betcris implica Under 2.5: -116 → 53.7%
  Diferencia: 1.3% → NO hay valor

  Modelo dice Empate: 25%
  Betcris implica Empate: 225 → 30.8% normalizado = 22.9%
  Diferencia: 2.1% → NO hay valor suficiente

  Modelo dice Doble oportunidad PSG/Draw: 80%
  Betcris implica: -301 → 75.1%
  Diferencia: 4.9% → SÍ hay valor ✓
```

---

## FORMATO DE OUTPUT — PLAN DE APUESTA BETCRIS

Después de dar la predicción y recibir el monto, mostrar siempre:

```
💰 PLAN DE APUESTA — [PARTIDO] — Betcris

Capital disponible: Q[MONTO]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🟢 APUESTA RECUPERACIÓN (40% = Q[monto×0.40])
  Mercado: [nombre del mercado Betcris]
  Selección: [qué se apuesta]
  Cuota: [americana] → [decimal]
  Prob modelo: [X]% vs Betcris implica: [Y]%
  Edge: [+Z%]
  Retorno estimado si acierta: Q[X] | Pérdida si falla: Q[Y]

🔵 APUESTA ANCLA (27% = Q[monto×0.27])
  Mercado: [nombre]
  Selección: [qué]
  Cuota: [americana] → [decimal]
  Retorno estimado si acierta: Q[X] | Pérdida si falla: Q[Y]

🛡 APUESTA COBERTURA (20% = Q[monto×0.20])
  Mercado: [nombre — dirección opuesta a las anteriores]
  Selección: [qué]
  Cuota: [americana]
  Retorno estimado si acierta: Q[X] | Pérdida si falla: Q[Y]

🟡 APUESTA VALOR (13% = Q[monto×0.13])
  Mercado: [nombre]
  Selección: [qué]
  Cuota: [americana]
  Advertencia: cuota alta, probabilidad menor

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ESCENARIO MÁS PROBABLE:
  Retorno estimado si el modelo acierta: Q[X]
  ⚠️ Estimación matemática — no garantía de resultado

ESCENARIO PEOR CASO (todo falla):
  Pérdida máxima: Q[suma apostada]
  Capital restante: Q[monto - apostado]

⚠️ Este plan distribuye el riesgo pero no elimina la posibilidad de pérdida.
   Apostá solo lo que podés perder sin afectar tu economía.
```

---

## REGLA DE ORO — CUÁNDO NO APOSTAR

El skill debe recomendar NO APOSTAR cuando:
- El modelo tiene confianza baja (★★☆☆☆ o menos)
- La diferencia entre prob modelo y prob Betcris < 2% en todos los mercados
- El partido es muy impredecible (xG diferencia < 0.3)
- La cuota del ancla no supera el umbral mínimo de Kelly
- El bankroll dado es < Q100 (no hay capital suficiente para distribuir)

En ese caso, el mensaje es:
"No encontré valor real en los mercados de Betcris para este partido.
Las cuotas reflejan correctamente las probabilidades — apostar sería
jugar en contra del margen de la casa sin ventaja. Recomiendo observar."

---

## DISTRIBUCIÓN PROPORCIONAL — CUALQUIER MONTO

El skill adapta los montos automáticamente según lo que diga el usuario.
Los porcentajes son fijos, los montos cambian.

```
MONTO USUARIO × 40% = Apuesta Recuperación
MONTO USUARIO × 27% = Apuesta Ancla  
MONTO USUARIO × 20% = Apuesta Cobertura (el seguro)
MONTO USUARIO × 13% = Apuesta Valor

TOTAL = 100% del monto indicado
```

### Ejemplos de distribución

| Usuario dice | Recuperación (40%) | Ancla (27%) | Cobertura (20%) | Valor (13%) |
|---|---|---|---|---|
| Q100 | Q40 | Q27 | Q20 | Q13 |
| Q200 | Q80 | Q54 | Q40 | Q26 |
| Q300 | Q120 | Q81 | Q60 | Q39 |
| Q500 | Q200 | Q135 | Q100 | Q65 |
| Q1000 | Q400 | Q270 | Q200 | Q130 |
| Q2000 | Q800 | Q540 | Q400 | Q260 |

### Monto mínimo recomendado: Q100
Por debajo de Q100, los montos individuales son tan pequeños
que las ganancias no justifican el análisis. Si el usuario
dice menos de Q100, informarlo y preguntar si quiere proceder.

### El seguro (Cobertura) es siempre el 20%
Sin importar el monto total, el 20% siempre va en dirección
OPUESTA a las apuestas principales. Eso es lo que protege
el capital en el peor escenario.

---

## TÍTULOS EXACTOS DE BETCRIS — REFERENCIA

Usar estos títulos tal como aparecen en la plataforma:

### Sección principal
- UEFA - Champions League - To Lift The Trophy
- Líneas de juego

### Mercados de resultado
- Arsenal FC vs PSG: Doble Oportunidad
- Arsenal FC vs PSG: Margen de Victoria

### Mercados de mitades  
- Arsenal FC vs PSG: 1ª Mitad
- Arsenal FC vs PSG: 2ª Mitad
- Arsenal FC vs PSG: Mitad Con Más Anotaciones

### Mercados de goles por equipo
- PSG vs Arsenal FC: PSG Ganará Alguna Mitad
- PSG vs Arsenal FC: Arsenal FC Ganará Alguna Mitad
- PSG vs Arsenal FC: PSG Gana Sin Encajar
- PSG vs Arsenal FC: PSG Valla Invicta
- PSG vs Arsenal FC: Arsenal FC Valla Invicta
- PSG vs Arsenal FC: Total de Goles PSG
- PSG vs Arsenal FC: Total de Goles Arsenal FC
- Arsenal FC vs PSG: Anotarán Ambos Equipos

### Formato de selección en el output
Siempre mostrar así:
  📋 [Título exacto de Betcris]
  Selección: [opción exacta tal como aparece: "Sí", "No", "Paris Saint-Germain/Draw", etc.]
  Cuota: [americana] → decimal [X.XX]
