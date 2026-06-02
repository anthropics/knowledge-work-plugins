---
name: world-cup-predictor
description: >
  Analiza y predice partidos del Mundial FIFA 2026 (USA/Canada/México) usando datos actuales,
  modelo Poisson, forma reciente, plantilla, contexto de sede, cuotas de mercado y cobertura
  mediática. Activar cuando el usuario pregunte por pronósticos, marcador probable, probabilidades
  de victoria, análisis de grupos, simulaciones de bracket o evaluación de favoritos.
  Después de cada predicción completa, preguntar siempre si el usuario quiere armar el plan
  de apuesta en Betcris. Activar la Capa 7 únicamente cuando el usuario confirme que quiere
  el plan y proporcione el capital disponible. El plan debe incluir edge, semáforo de riesgo,
  stop loss y distribución proporcional, sin prometer ganancias.
---

# 🌍 World Cup 2026 Predictor — Metodología Profesional

## Filosofía del skill

Este skill replica la metodología de las principales casas de apuestas y modelos estadísticos
profesionales (Opta, FiveThirtyEight, Gracenote, Goldman Sachs Football Model), **combinada
con el análisis cualitativo de los principales medios deportivos del mundo**:

> **Predicción = Modelo Poisson + forma reciente + plantilla + contexto + pulso mediático**

Los números dicen qué tan bueno es un equipo históricamente. Los medios dicen cómo está
*ahora mismo* — tensiones internas, confianza del vestuario, presión de la prensa, estado
anímico del técnico. Ambas fuentes son necesarias para una predicción completa.


## Tabla de pesos normalizados del modelo (suman 100%)

| Capa | Factor | Peso |
|---|---|---|
| Capa 0 | Pulso mediático (ESM) | 12% |
| Capa 1 | Contexto del partido | — (cualitativo, sin peso numérico) |
| Capa 2 | DNA histórico / clasificatorias | 20% |
| Capa 3 | Plantilla y jugadores clave | 20% |
| Capa 3B | Momentum de club y nivel de liga | 8% |
| Capa 4 | Forma reciente (IF) | 18% |
| Capa 5 | Mercado de apuestas | 14% |
| Capa 6 | Modelo Poisson (xG) | calculado con los anteriores |
| Capa 8 | Impacto climático | 8% |
| **TOTAL** | | **100%** |

> Los ajustes de Capa 6 se calculan usando los inputs de todas las capas anteriores.
> El clima (Capa 8) aplica solo cuando la diferencia de adaptación es significativa.

---

## Proceso de predicción — 9 pasos ordenados (Capas 0 a 8)

Ejecutar **siempre en este orden**. No saltar capas.

### CAPA 0 — Pulso mediático (qué dicen los grandes medios)

**Esta capa va PRIMERO porque puede cambiar todo lo demás.**

Buscar qué dicen los medios más influyentes sobre cada equipo en el contexto actual del
Mundial. Capturar el "sentimiento" periodístico: ¿el equipo llega confiado o con dudas?
¿Hay polémica? ¿El técnico está bajo presión?

**Medios a priorizar por región del equipo:**

| Región | Medios prioritarios |
|---|---|
| Global / inglés | ESPN FC, The Athletic, BBC Sport, The Guardian, Sky Sports |
| España / Latinoamérica | Marca, AS, Mundo Deportivo, GOAL.com, Infobae Deportes |
| Francia | L'Équipe |
| Alemania | Kicker, Sport Bild |
| Italia | Gazzetta dello Sport, Corriere dello Sport |
| Brasil / Portugal | Lance!, Record |
| Argentina | TyC Sports, Olé, Clarín Deportes |
| México / CONCACAF | TUDN, Medio Tiempo, Record MX |

**Búsquedas para la Capa 0:**
```
[PAIS] seleccion mundial 2026 analisis ESPN
[PAIS] national team World Cup 2026 preview The Athletic BBC
[PAIS] mundial 2026 opinion prensa critica
[EQUIPO A] vs [EQUIPO B] World Cup 2026 preview media
[PAIS] seleccion estado animo vestuario 2026
[TECNICO] [PAIS] World Cup 2026 tactics formation
[PAIS] World Cup 2026 Marca AS GOAL preview
```

**Qué extraer de los medios:**

1. **Tono general** — ¿optimismo, dudas, alarma, euforia?
2. **Problemas reportados** — lesiones no confirmadas, conflictos internos, sanciones
3. **Narrativa táctica** — ¿el equipo tiene sistema claro o hay debate sobre la formación?
4. **Factor psicológico** — ¿llegó ganando o perdiendo partidos amistosos/preparatorios?
5. **Declaraciones del técnico o jugadores** — confianza pública vs señales de tensión
6. **Historial H2H** — ¿qué dice la prensa del historial entre estos dos rivales?
7. **Expectativa del país** — ¿la afición y medios locales presionan o apoyan?

**Escala de Sentimiento Mediático (ESM):**
```
+2 = Narrativa muy positiva (favorito claro, equipo en racha, vestuario unido)
+1 = Narrativa positiva con matices menores
 0 = Neutral o señales contradictorias
-1 = Dudas importantes (forma irregular, tensiones, críticas al técnico)
-2 = Narrativa negativa fuerte (crisis, escándalos, lesiones masivas, vestuario roto)
```

El ESM ajusta las probabilidades finales en ±5% por equipo.

**Citar siempre la fuente del medio al mencionar cualquier opinión editorial.**

**Peso ajustado: 12% del modelo normalizado**

---

### CAPA 1 — Contexto del partido
Identificar antes de buscar datos:
- ¿Es fase de grupos, octavos, cuartos, semi, final?
- ¿Hay presión extra (eliminación directa, primer partido, rival histórico)?
- ¿Sede del partido? (aunque en 2026 no hay ventaja de local por sedes compartidas, la distancia de viaje importa)
- ¿Cuántos días de descanso tiene cada equipo?

### CAPA 2 — DNA histórico del equipo (Mundial 2022 + Clasificatorias 2026)

**Buscar con web_search:**
```
[PAIS] FIFA World Cup 2022 stats results
[PAIS] FIFA World Cup 2026 qualifiers standings goals
[PAIS] clasificatorias mundial 2026 resultados
```

**Datos clave a extraer:**
| Métrica | Fuente preferida |
|---|---|
| Puntos en clasificatorias | FIFA.com, CONMEBOL, UEFA, etc. |
| Goles a favor / en contra | Transfermarkt, Fbref.com |
| Partidos G/E/P | SofaScore, FlashScore |
| Rendimiento Mundial 2022 | Wikipedia, ESPN |
| Diferencia de goles clasificatorias | 11v11.com |

**Peso ajustado: 20% del modelo normalizado**

### CAPA 3 — Análisis de plantilla y jugadores clave

**Criterio para decidir profundidad de análisis:**
- Si el equipo tiene jugadores en Top 5 ligas europeas con >20 partidos/temporada → análisis individual de top 5 jugadores
- Si el equipo es mayoritariamente de ligas locales → análisis colectivo (sin individuos)
- Siempre analizar: portero titular, capitán, máximo goleador de clasificatorias

**Buscar con web_search:**
```
[PAIS] squad World Cup 2026 key players form
[JUGADOR CLAVE] 2024-25 season stats goals assists
[PAIS] seleccion nacional convocados 2025 2026
```

**Métricas de jugadores clave:**
- Goles + asistencias en temporada de club (2024-25)
- Minutos jugados (forma física)
- Valor de mercado actual vs hace 4 años (Transfermarkt)
- ¿Están en su mejor momento? ¿O en declive?
- Lesiones recientes o suspensiones para este partido

**Peso ajustado: 20% del modelo normalizado**

### CAPA 3B — Momentum de club y nivel de liga

**Esta capa se ejecuta JUNTO a la Capa 3, no separada.**

Es el factor que más se subestima: un jugador no llega solo con sus estadísticas individuales
— llega con el estado emocional, físico y de confianza que le dejó su temporada con el club.
Un campeón de Champions llega diferente a uno que quedó eliminado en grupos.

**Pregunta central: ¿De qué contexto viene cada jugador clave?**

#### Paso 1 — Identificar el "núcleo de club" de la selección

Buscar cuántos jugadores del equipo titular provienen del mismo club:
```
[SELECCION] convocados 2026 [CLUB] jugadores
[SELECCION] World Cup 2026 squad [CLUB] players
```

Un núcleo de 4+ jugadores del mismo club es significativo — ya vienen
rodados juntos, con automatismos y lenguaje compartido. Eso vale.

Ejemplos relevantes para Mundial 2026:
- Francia: eje PSG (Mbappé, Dembélé, Doué, Zaire-Emery) — campeones Champions 2024-25
- Inglaterra: eje Arsenal (Saka, Rice, Saliba, Havertz) — finalistas Champions 2025-26
- España: mezcla Real Madrid + Barcelona + Atlético
- Alemania: eje Bayern (Kimmich, Goretzka, Gnabry, Müller si convocado)

#### Paso 2 — Clasificar el nivel de liga de origen

**Tabla de peso por liga (para ajustar xG):**
```
Nivel A (multiplicador 1.10):
  Premier League, La Liga, Bundesliga, Serie A, Ligue 1
  → jugadores compiten semana a semana al máximo nivel

Nivel B (multiplicador 1.00):
  Eredivisie, Liga Portuguesa, Liga Turca, Liga Belga,
  Saudi Pro League (jugadores top), MLS (jugadores top)

Nivel C (multiplicador 0.90):
  Ligas de Sudamérica (CONMEBOL — excepto Brasil/Argentina A)
  Ligas de África, Asia, Oceanía

Nivel D (multiplicador 0.80):
  Ligas locales / semiprofesionales
  Jugadores sin actividad reciente
```

Si el equipo tiene >60% de jugadores en ligas Nivel A → ajuste xG +0.1
Si el equipo tiene >60% en ligas C o D → ajuste xG -0.15

#### Paso 3 — Evaluar el momentum colectivo del club

**Buscar resultado final de temporada del club principal:**
```
[CLUB] Champions League 2025-26 resultado
[CLUB] [LIGA] temporada 2025-26 campeón posición final
[CLUB] season 2025-26 title winner result
```

**Escala de Momentum de Club (MCM):**
```
+3 = Ganó Champions League / Copa del Mundo de Clubes
+2 = Finalista Champions / Ganó liga con dominio claro
+1 = Cuartos o semis de Champions / Campeón de liga ajustado
 0 = Octavos de Champions / Top 4 de liga sin título
-1 = Eliminado pronto / Mitad de tabla
-2 = Temporada de crisis / Descenso / Conflictos internos
```

El MCM del núcleo principal ajusta las probabilidades ±3% por equipo.

**Casos concretos para Mundial 2026:**
```
PSG (eje Francia): Campeón Champions 2024-25 → MCM +3 → +3% a Francia
Arsenal (eje Inglaterra): Finalista Champions 2025-26 → MCM +2 → +2% a Inglaterra
Real Madrid: Eliminado semifinales 2025-26 → MCM +1 → +1% a España
Bayern Munich: Semifinalista 2025-26 → MCM +1 → +1% a Alemania
```

#### Paso 4 — Detectar el "efecto Champions fatiga"

Jugadores que llegaron a la final de Champions (30 mayo 2026) tienen
solo 12 días hasta el inicio del Mundial (11 junio). Eso es un arma
de doble filo: llegan con confianza máxima PERO con el cuerpo al límite.

```
Señal positiva: ganaron la final → confianza, cohesión, momentum
Señal negativa: perdieron la final → posible bajón emocional + fatiga
Riesgo físico: cualquier finalista → 12 días de descanso mínimo
```

**Ajuste por fatiga Champions:**
- Ganadores de la final: +3% confianza, -2% físico neto = +1% neto
- Perdedores de la final: -3% confianza, -2% físico = -5% neto

**Búsquedas para esta capa:**
```
[LIGA] 2025-26 champion winner season
[CLUB] UCL 2025-26 result eliminated
[SELECCION] players Champions League 2026 finalist
Champions League final 2026 winner result
```

**Peso ajustado: 8% del modelo normalizado (Capa 3 + 3B = 28% total plantilla)**

---

### CAPA 4 — Forma reciente — Forma reciente (últimos 6 partidos oficiales)

**Buscar con web_search:**
```
[PAIS] national team last 6 matches results 2025
[PAIS] seleccion resultados recientes 2025
```

**Calcular el Índice de Forma (IF):**
```
Victoria = 3 puntos
Empate = 1 punto
Derrota = 0 puntos
Goles a favor = +0.2 por gol
Goles en contra = -0.1 por gol

IF = (suma de puntos + ajuste goles) / 6 partidos
Escala: 0 a 3.5
```

**Peso ajustado: 18% del modelo normalizado**

### CAPA 5 — Contraste con el mercado de apuestas actual

**Esto es OBLIGATORIO. Siempre buscar odds actuales.**

```
web_search: [EQUIPO A] vs [EQUIPO B] World Cup 2026 odds prediction
web_search: [EQUIPO A] [EQUIPO B] apuestas cuotas pronostico
web_search: [EQUIPO A] vs [EQUIPO B] betting odds Bet365 William Hill
```

**Interpretar las cuotas así:**
```
Cuota decimal → Probabilidad implícita = 1 / cuota × 100

Ejemplo:
- Local gana: cuota 1.85 → prob = 54%
- Empate: cuota 3.40 → prob = 29%
- Visita gana: cuota 4.50 → prob = 22%
(Suman >100% por el margen de la casa)
```

Comparar con modelos predictivos citados (ESPN, Opta, Gracenote si aparecen).

**Peso ajustado: 14% del modelo normalizado**

### CAPA 6 — Modelo Poisson simplificado

Calcular goles esperados (xG) por equipo:

```
xG_equipo = (promedio_goles_anotados_clasificatorias × 0.4) 
           + (promedio_goles_rival_en_su_últimos_6 × 0.3)
           + (ajuste_plantilla: 0 a 0.5 según Capa 3)
           + (ajuste_forma: IF × 0.1)
```

Con los xG calculados, estimar probabilidades:
- **Poisson(k, λ)** donde λ = xG del equipo
- Calcular P(gana), P(empata), P(pierde) sumando distribución

Si no se puede calcular exacto, usar esta tabla aproximada:
```
xG diferencia > 0.8 → favorito claro (60-70% prob de ganar)
xG diferencia 0.4-0.8 → favorito moderado (52-60%)
xG diferencia < 0.4 → partido equilibrado (45-55%)
```

---

## CAPA 8 — Impacto climático y de sede

**Esta capa va después de la Capa 3B y antes de la Capa 4.**
No es opcional — el clima del Mundial 2026 es el más extremo en la historia del torneo.

### Paso 1 — Identificar la zona climática de la sede

Consultar `references/clima-sedes.md` para el mapa completo de las 16 sedes.

```
🔴 Zona Roja  → Dallas, Houston, Miami, Atlanta, Monterrey (>33°C)
🟡 Zona Amarilla → Kansas City, Guadalajara, Philadelphia (25-32°C)
🟢 Zona Verde → Seattle, Los Ángeles, San Francisco, Vancouver, Toronto (<25°C)
⚠️ Especial   → Ciudad de México (altitud 2,240 msnm + calor moderado)
```

### Paso 2 — Determinar la hora del partido

La hora importa tanto como la temperatura. Un partido a las 3PM ET en Dallas
en junio es muy diferente a uno a las 9PM ET en el mismo estadio.

Consultar `references/grupos-y-calendario.md` para hora exacta de cada partido.

### Paso 3 — Aplicar ajuste por origen del equipo

```
Zona Roja + Equipo norte de Europa (UK, Alemania, Países Bajos, Bélgica, Suecia):
  → xG × 0.88 | IF × 0.92 | Nota: "calor extremo — desventaja física real"

Zona Roja + Equipo de clima cálido (Brasil, Senegal, Marruecos, México, Ghana):
  → xG × 1.03 | Ventaja climática

Zona Amarilla + Equipo norte de Europa:
  → xG × 0.94

Zona Verde + Cualquier equipo:
  → Sin ajuste — condiciones neutras

Ciudad de México + Equipo europeo:
  → xG × 0.85 (altitud + calor combinados)
```

### Paso 4 — Incluir en el output

Siempre mostrar el factor climático en el análisis:
- Zona de la sede
- Temperatura estimada al momento del partido
- Qué equipo tiene ventaja/desventaja
- Ajuste aplicado al xG

**Peso ajustado: 8% del modelo normalizado**

Consultar `references/clima-sedes.md` para tabla completa de sedes,
temperaturas, humedad, WBGT y equipos más afectados.

---

## Formato de output — SIEMPRE usar esta estructura

**REGLA CRÍTICA: El output de predicción NUNCA se omite ni se reduce.
La Capa 7 (Betcris) se agrega AL FINAL, no reemplaza nada.**

El output tiene DOS partes obligatorias:

### PARTE 1 — Predicción completa (SIEMPRE, sin excepción)
### PARTE 2 — Pregunta de apuesta Betcris (SIEMPRE al final)

---

```
## [EQUIPO A] vs [EQUIPO B] — Mundial 2026
Fecha · Sede · Grupo / Fase

--- PULSO MEDIATICO ---

[Equipo A] — ESM: [+2/+1/0/-1/-2]
Resumen del tono predominante en medios
- ESPN / Marca / The Athletic / etc: lo que dice (parafrasado, nunca copiado)
- Narrativa: optimismo / dudas / euforia / crisis

[Equipo B] — ESM: [+2/+1/0/-1/-2]
Resumen del tono predominante en medios
- [Medio local]: lo que dice (parafrasado)
- Narrativa: optimismo / dudas / euforia / crisis

--- ANALISIS ESTADISTICO ---

| Factor              | [Equipo A] | [Equipo B] |
|---------------------|------------|------------|
| Puntos clasificat.  | X          | X          |
| GF / GC             | X / X      | X / X      |
| Forma reciente (IF) | X.X / 3.5  | X.X / 3.5  |
| Sentimiento (ESM)   | X          | X          |
| Nivel liga (A/B/C)  | X          | X          |
| Momentum club (MCM) | +X         | +X         |
| Núcleo de club      | X de [Club]| X de [Club]|
| Valor plantilla     | X€M        | X€M        |
| xG esperados        | X.X        | X.X        |

Jugadores a seguir:
[Equipo A]: Nombre — razón con stats concretos
[Equipo B]: Nombre — razón con stats concretos

--- PROBABILIDADES ---

| Resultado         | Modelo Poisson | + Ajuste ESM | Mercado apuestas |
|-------------------|----------------|--------------|------------------|
| Victoria [Eq. A]  | XX%            | XX%          | XX%              |
| Empate            | XX%            | XX%          | XX%              |
| Victoria [Eq. B]  | XX%            | XX%          | XX%              |

Marcador más probable: X - X
(distribución Poisson con xG calculados y ajuste mediático)

--- VEREDICTO FINAL ---
2-3 líneas integrando datos + narrativa mediática.
Mencionar si los medios refuerzan o contradicen lo que dicen los números.
Concluir con el resultado más probable y el factor decisivo.

Factores de riesgo:
- [Factor estadístico]
- [Factor mediático / psicológico / situacional]

Fuentes: estadísticas · medios consultados · casas de apuestas

--- PREGUNTA OBLIGATORIA AL FINAL (PARTE 2) ---

"¿Quieres que arme el plan de apuesta en Betcris?
 Si es así, dime cuánto tienes disponible para invertir y cuánto llevás perdido este mes en total."
```

**Esta pregunta aparece SIEMPRE después de cada predicción completa.
NUNCA antes. NUNCA en vez de la predicción. SIEMPRE después.**

---

## Reglas de calidad

1. **Nunca predecir sin buscar medios deportivos primero (Capa 0)** — el sentimiento
   mediático puede invalidar lo que dicen los números solos
2. **Nunca predecir sin buscar odds actuales** — el mercado tiene sabiduría colectiva
3. **Citar siempre los medios por nombre** — nunca decir "los medios dicen" sin especificar
   cuál medio (ESPN, Marca, The Athletic, etc.)
4. **Parafrasear siempre las opiniones de los medios**, nunca copiar texto literal
5. **Si los datos de un equipo son escasos**, señalarlo y dar más peso al mercado y medios
6. **Separar confianza alta vs baja:**
   - Alta: datos estadísticos + cobertura mediática abundante (Europa, Sudamérica)
   - Media: solo estadísticas o solo cobertura mediática disponible
   - Baja: poca data y poca cobertura (ligas de CAF menor, AFC menor)
7. **No fabricar estadísticas ni opiniones** — si no se encuentra un dato, decirlo y omitirlo
8. **Actualidad**: priorizar datos de 2025-2026 sobre datos anteriores
9. **Lesiones y suspensiones** tienen peso de hasta +/- 10% en probabilidades
10. **Cuando medios y números se contradicen**, mencionarlo explícitamente en el veredicto
    y explicar cuál fuente se pondera más y por qué

---

## Búsquedas de referencia rápida por confederación

### CONMEBOL (Sudamérica)
```
site:conmebol.com eliminatorias sudamericanas 2026 tabla
[pais] eliminatorias sudamericanas 2026 estadisticas
```

### UEFA (Europa)
```
UEFA Nations League 2024-25 [pais] results
[pais] Euro 2024 performance stats
```

### CONCACAF (Norte y Centro América + Caribe)
```
CONCACAF Nations League 2024-25 [pais] 
Octagonal CONCACAF 2026 qualifiers [pais]
```

### CAF (África) / AFC (Asia) / OFC (Oceanía)
```
CAF World Cup 2026 qualifiers [pais] standings
AFC third round qualifiers 2026 [pais]
```

---

## Referencias externas a consultar


---

## CAPA 7 — Gestión de Apuesta Betcris (post-predicción)

**Flujo obligatorio — siempre en este orden:**

### Paso 1 — Entregar el pronóstico completo (Capas 0-6)
Dar la predicción completa: probabilidades, marcador más probable, veredicto.

### Paso 2 — Preguntar el capital SIEMPRE
Al final de CADA predicción, preguntar exactamente:

> "¿Quieres que arme el plan de apuesta en Betcris?
>  Si es así, dime cuánto tienes disponible para invertir y cuánto llevás perdido este mes en total."

**NUNCA asumir un monto. NUNCA usar el monto de una conversación anterior.
El usuario decide cuánto invertir cada vez — puede ser Q100, Q500, Q1000 o cualquier cantidad.**

---

### SEMÁFORO DE EDGE — Mostrar SIEMPRE antes del plan de apuesta

Antes de entregar el plan, calcular el edge promedio de las apuestas seleccionadas
y mostrar el semáforo. El edge es la diferencia entre la probabilidad del modelo
y la probabilidad implícita de Betcris.

```
Edge promedio = promedio de (prob_modelo - prob_betcris) de las 4 apuestas
```

**Mostrar así, sin excepción:**

🟢 Edge +7% o más
  → "Señal fuerte. El modelo tiene ventaja clara sobre el mercado. Apostá con confianza."
  → Usar distribución completa (40/27/20/13)

🟡 Edge 4-6%
  → "Señal moderada. Hay ventaja pero no es contundente. Reducí los montos a la mitad."
  → Reducir distribución al 50%: (20/13/10/7)

🔴 Edge menor a 4%
  → "El mercado está más informado que el modelo en este partido. No apostés."
  → NO entregar plan de apuesta. Decirlo claramente y explicar por qué.

**Regla crítica:** Si el semáforo es 🔴, el skill NO presenta el plan de apuesta
aunque el usuario lo pida. En ese caso responder:
"El edge calculado es insuficiente para apostar con ventaja real. En este partido
el mercado ya incorporó toda la información disponible. Esperá un partido con
mejor oportunidad."

---

### STOP LOSS — Preguntar SIEMPRE antes de entregar el plan

Junto con la pregunta del monto, preguntar también:

Con esa respuesta, comparar contra el bankroll total declarado:

```
Si pérdida_del_mes > 15% del bankroll total → STOP LOSS activado
Si pérdida_del_mes entre 10-15%             → ALERTA, reducir stake al 50%
Si pérdida_del_mes < 10%                    → Continuar normal
```

**Si el stop loss se activa:**
"Llevás perdido más del 15% de tu bankroll este mes. La regla es clara:
pausá esta semana. No es debilidad — es lo que separa a un apostador
disciplinado del resto. Volvé la próxima semana con la cabeza fría."

**Esta regla no se negocia. Si el usuario insiste, repetir el mensaje.
El skill nunca entrega un plan de apuesta cuando el stop loss está activo.**

---

### Paso 3 — Recibir el monto y calcular

Con el monto que diga el usuario:

**3A — Calcular distribución proporcional:**
```
40% → Apuesta Recuperación (mayor probabilidad, menor riesgo)
27% → Apuesta Ancla (doble oportunidad o mercado seguro)
20% → Apuesta Cobertura (mercado opuesto — el seguro)
13% → Apuesta Valor (cuota más alta con ventaja real)
```

**3B — Seleccionar mercados con títulos EXACTOS de Betcris:**
Usar los títulos tal como aparecen en Betcris para que el usuario
sepa exactamente dónde hacer click. Ejemplo:
- "📋 PSG vs Arsenal FC: PSG Ganará Alguna Mitad"
- "📋 Arsenal FC vs PSG: Doble Oportunidad"
- "📋 PSG vs Arsenal FC: Arsenal FC Ganará Alguna Mitad"
- "📋 PSG vs Arsenal FC: Total de Goles PSG"

**3C — Aplicar Kelly Fraccionado (25%) para validar:**
```
f* = (b×p - q) / b  →  f_seguro = f* × 0.25
Solo incluir apuesta si f_seguro > 3%
```

**3D — Calcular montos exactos en la moneda del usuario**
Si dice Q300 → Q120 / Q81 / Q60 / Q39
Si dice Q1000 → Q400 / Q270 / Q200 / Q130
Si dice Q50 → Q20 / Q13.50 / Q10 / Q6.50

### Paso 4 — Mostrar el plan con 5 secciones claras

```
0. SEMÁFORO DE EDGE (SIEMPRE primero)
   🟢/🟡/🔴 Edge calculado: X% — [mensaje según color]

1. STOP LOSS (si aplica — mostrar ANTES del plan)
   ✅ Sin alerta / ⚠️ Alerta / 🛑 STOP LOSS ACTIVADO

2. DISTRIBUCIÓN VISUAL (barra con los 4 montos)
   Solo si semáforo es 🟢 o 🟡 y no hay stop loss activo

3. LAS 4 APUESTAS con:
   - Título exacto de Betcris (📋)
   - Selección exacta (ej: "Sí", "Paris Saint-Germain/Draw")
   - Cuota americana y decimal
   - Monto exacto a apostar
   - Ganancia si acierta / pérdida si falla

4. ESCENARIOS (qué pasa en cada resultado posible)

5. RESUMEN FINAL (peor caso, retorno estimado en escenario probable, probabilidad de terminar positivo)
   — Aclarar siempre que los retornos son estimaciones del modelo, no garantías
```

### Paso 5 — Recordar siempre

- La cobertura (Apuesta 3) va en dirección OPUESTA a las demás — es el seguro
- En el peor caso el usuario pierde la inversión pero NO más que eso
- El capital que NO invierte queda disponible para otros partidos
- Nunca juzgar el monto — Q50 o Q5000 reciben el mismo análisis serio
---

Ver `references/momentum-de-club.md` para el mapa completo de núcleos de club,
niveles de liga y MCM ya calculados para las 48 selecciones del Mundial 2026.
Consultar antes de ejecutar la Capa 3B — ahorra tiempo de búsqueda.

Ver `references/medios-deportivos.md` para la lista completa de medios prioritarios
por país y región, con las búsquedas recomendadas para la Capa 0.

Ver `references/grupos-y-calendario.md` para los 12 grupos completos, todos los partidos
de la fase de grupos con fechas, horarios ET y sedes. **Consultar SIEMPRE antes de predecir**
para confirmar la fecha y sede correcta del partido.

Ver `references/fuentes-datos.md` para lista completa de URLs de fuentes de estadísticas
y casas de apuestas confiables por confederación.

Ver `references/modelo-poisson.md` para la explicación matemática completa del modelo
si necesitas profundizar en los cálculos.
