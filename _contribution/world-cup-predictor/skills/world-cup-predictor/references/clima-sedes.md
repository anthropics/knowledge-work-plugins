# Capa 8 — Impacto Climático Mundial 2026

## Por qué el clima es un factor de predicción real

<cite>Un estudio de Brunel University encontró que 14 de las 16 sedes superarán
28°C diariamente en junio y julio, y 4 podrían alcanzar 32°C.</cite>

<cite>El defensor de Inglaterra Reece James, tras jugar la Club World Cup en EE.UU.,
advirtió que serán "condiciones super difíciles" — y Tuchel dijo: "El sufrimiento
es uno de los titulares de este Mundial."</cite>

Los europeos juegan toda su temporada entre 8-18°C. Llegan a un torneo donde
Dallas, Houston, Miami, Atlanta y Monterrey tienen 33-40°C con humedad extrema.
Eso tiene impacto medible en:
- Distancia recorrida por partido (cae entre 8-12% en calor extremo)
- Sprints de alta intensidad (caen hasta 20%)
- Tiempo de recuperación entre partidos (se extiende)
- Riesgo de calambres y lesiones musculares

---

## MAPA CLIMÁTICO — Las 16 sedes del Mundial 2026

### 🔴 ZONA ROJA — Calor extremo (>33°C, alta humedad)
*Penaliza fuertemente a equipos europeos del norte*

| Ciudad | Estadio | Temp. promedio junio | Humedad | WBGT |
|---|---|---|---|---|
| **Dallas** | AT&T Stadium | 35°C | 60% | **>32°C — peligroso** |
| **Houston** | NRG Stadium | 34°C | 72% | **>32°C — peligroso** |
| **Miami** | Hard Rock Stadium | 32°C | 78% | **>30°C — muy alto** |
| **Atlanta** | Mercedes-Benz | 30°C | 74% | >28°C — alto |
| **Monterrey** | Estadio BBVA | 36°C | 55% | **>32°C — peligroso** |

*WBGT (Wet Bulb Globe Temperature) = temperatura real que siente el cuerpo*
*FIFA protocola pausas de hidratación cuando WBGT > 28°C*

### 🟡 ZONA AMARILLA — Calor moderado (25-32°C)
*Afecta parcialmente — equipos de clima templado tienen desventaja menor*

| Ciudad | Estadio | Temp. junio | Nota |
|---|---|---|---|
| **Kansas City** | Arrowhead Stadium | 29°C | Humedad variable |
| **Guadalajara** | Estadio Akron | 28°C | + temporada de lluvias |
| **Philadelphia** | Lincoln Financial | 28°C | Humedad costera |
| **Boston** | Gillette Stadium | 26°C | Confortable |
| **Ciudad de México** | Azteca | 22°C | ⚠️ Altitud 2,240 msnm |

### 🟢 ZONA VERDE — Clima favorable (18-25°C)
*Condiciones similares a Europa — sin desventaja climática*

| Ciudad | Estadio | Temp. junio | Nota |
|---|---|---|---|
| **Seattle** | Lumen Field | 22°C | Fresco, cómodo |
| **Los Ángeles** | SoFi Stadium | 24°C | Seco, manejable |
| **San Francisco** | Levi's Stadium | 20°C | Fresco costero |
| **Vancouver** | BC Place | 19°C | + techo retráctil |
| **Toronto** | BMO Field | 24°C | Cómodo |
| **Nueva Jersey** | MetLife Stadium | 27°C | Final 19 julio — caluroso |

---

## AJUSTES AL MODELO POR CLIMA

### Regla base: ¿En qué zona juegan?

```
Zona Roja + Equipo europeo del norte (UK, Alemania, Países Bajos, Bélgica):
  → xG visitante × 0.88 (penalización real por calor)
  → IF del equipo × 0.92 (fatiga acumulada)
  → Nota en factores de riesgo: "Calor extremo — desventaja física"

Zona Roja + Equipo de clima cálido (Brasil, Senegal, Marruecos, México):
  → Sin ajuste negativo — ya están adaptados
  → Puede ser ventaja: xG × 1.03

Zona Amarilla + Equipo europeo:
  → xG × 0.94 (penalización menor)

Zona Verde + Cualquier equipo:
  → Sin ajuste — condiciones neutras
```

### Equipos que MÁS sufren el calor (peor adaptación histórica)

| Selección | Liga de origen | Clima habitual | Riesgo |
|---|---|---|---|
| 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra | Premier League | 10-18°C, lluvia | 🔴 Muy alto |
| 🇩🇪 Alemania | Bundesliga | 8-16°C | 🔴 Muy alto |
| 🇧🇪 Bélgica | Pro League | 8-15°C | 🔴 Muy alto |
| 🇳🇱 Países Bajos | Eredivisie | 10-17°C | 🔴 Muy alto |
| 🇸🇪 Suecia | Allsvenskan | 5-15°C | 🔴 Muy alto |
| 🇨🇭 Suiza | SL + ligas top | 10-18°C | 🟡 Alto |
| 🇫🇷 Francia | Ligue 1 | 15-22°C | 🟡 Moderado |
| 🇪🇸 España | La Liga | 18-28°C | 🟡 Moderado |
| 🇵🇹 Portugal | Primeira Liga | 18-25°C | 🟡 Moderado |
| 🇮🇹 Italia | Serie A | 20-28°C | 🟡 Leve |

### Equipos MEJOR adaptados al calor (ventaja)

| Selección | Razón |
|---|---|
| 🇧🇷 Brasil | Clima tropical permanente |
| 🇸🇳 Senegal | África Occidental — 30°C+ habitual |
| 🇲🇦 Marruecos | Norte de África, calor seco |
| 🇲🇽 México | Juega en Guadalajara y Ciudad de México |
| 🇺🇸 USA | Locales — ya adaptados |
| 🇸🇦 Arabia Saudita | Calor extremo permanente |
| 🇬🇭 Ghana | Clima tropical |

---

## PARTIDOS CON MAYOR IMPACTO CLIMÁTICO

Estos partidos tienen el mayor riesgo de que el clima cambie el resultado:

### Zona Roja — Europa vs Sudamérica/África

```
Alemania vs Costa de Marfil — Houston (34°C, 72% humedad)
→ Costa de Marfil: ventaja climática real. Ajustar xG.

Inglaterra vs Ghana — Boston (26°C) → Zona verde, sin impacto

Francia vs Senegal — Nueva Jersey (27°C) → Leve impacto

Países Bajos vs Japón — Dallas (35°C)
→ Ambos sufren el calor. Japón más acostumbrado (veranos húmedos).
→ Ajuste leve para ambos.
```

### Casos especiales

**Ciudad de México (Azteca) — 2,240 msnm + calor moderado:**
- Combinación letal para europeos: altitud + calor
- Equipos que juegan ahí necesitan adaptación mínima de 5-7 días
- Ajuste adicional: xG europeo × 0.85

**Monterrey (BBVA) — El más extremo:**
- 36°C + humedad = WBGT >32°C
- Cualquier equipo europeo jugando aquí recibe penalización máxima

---

## PROTOCOLO FIFA PARA EL CALOR

FIFA implementó reglas específicas para 2026:

```
WBGT 28-32°C → Pausa de hidratación obligatoria en minutos 30 y 75
WBGT >32°C   → Pausa adicional en tiempo extra
Kickoff tardío → Partidos en Dallas, Houston, Miami se juegan de noche
               para reducir temperatura (pero la humedad sigue alta)
```

**Nota importante:** muchos partidos de fase de grupos están programados
para las 3:00 PM ET o 6:00 PM ET — no de noche. Eso significa calor pleno.

---

## CÓMO INTEGRAR LA CAPA 8 EN EL OUTPUT

Agregar esta sección al análisis de cada partido:

```
--- FACTOR CLIMÁTICO (CAPA 8) ---

Sede: [ciudad] — Zona [Roja/Amarilla/Verde]
Condiciones: [temp]°C / [humedad]% / [WBGT]°C estimado
Hora del partido: [hora] ET — [¿Pleno sol o noche?]

Impacto en [Equipo A]: [Penalización xG si aplica] — [razón]
Impacto en [Equipo B]: [Ventaja/neutral/penalización] — [razón]

Ajuste al xG:
  [Equipo A]: [xG base] × [multiplicador] = [xG ajustado]
  [Equipo B]: [xG base] × [multiplicador] = [xG ajustado]

Nota: [si hay pausa de hidratación FIFA prevista]
```

**Peso en el modelo final: 8%**
*(Distribución actualizada: Capa 0=15%, Capa 2=22%, Capa 3=22%,
Capa 3B=9%, Capa 4=17%, Capa 5=7%, Capa 6=calc., Capa 8=8%)*
