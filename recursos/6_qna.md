# Base de Conocimiento Q&A: Agente de Comunicación RBSR

Este documento acumula preguntas frecuentes y sus respuestas validadas para el agente de comunicación de la **Reserva de la Biosfera Sierra del Rincón (RBSR)**. Es una fuente viva: se irá ampliando con cada duda relevante de los técnicos. El agente debe consultarlo antes de responder preguntas sobre tipografía, imagen, estilo, estrategia o herramientas.

---

## Q&A_004: ¿Qué requisitos de legibilidad debe cumplir el portal web de comunicación?

**Fecha:** Junio 2026

### Respuesta

El técnico ha indicado que el portal debe ser **más ligero de leer** para facilitar su uso cotidiano. Los requisitos de legibilidad para el portal son:

- **Texto de cuerpo más grande**: mínimo `text-base` (16px) para párrafos, nunca `text-sm` (14px) como tamaño principal de lectura.
- **Contraste alto**: los textos de cuerpo deben usar `text-stone-800` (casi negro pizarra cálido) en lugar de `text-stone-600` (gris medio). Los textos de apoyo usan `text-stone-600`.
- **Interlineado generoso**: `leading-relaxed` o `leading-loose` para párrafos. Nunca compactar el interlineado.
- **Headings prominentes**: H2 en `text-2xl`, H3 en `text-xl`, H4 en `text-base` con peso bold.
- **Listas escaneables**: ítems de lista en `text-base text-stone-800` con espaciado vertical `space-y-2`.

> *Este requisito debe tenerse en cuenta siempre que se modifique el parser de Markdown o el diseño del portal.*

---

## Q&A_001: ¿La fuente "News Cycle" de Canva es adecuada para la marca RBSR?

**Preguntado por:** Carles (técnico de comunicación)
**Fecha:** Junio 2026

### Respuesta

**News Cycle** es una fuente serif de palo seco humanista (humanist slab-serif) de diseño periodístico clásico, limpia y legible. Comparada con las fuentes oficiales de la Reserva, este es el análisis:

| Criterio | News Cycle | Montserrat Bold (oficial) | VSV Alergia (oficial) |
| :--- | :--- | :--- | :--- |
| **Familia tipográfica** | Slab-serif (serifa cuadrada) | Sans-serif geométrica | Sans-serif personalizada |
| **Personalidad** | Periodística, sobria, editorial | Moderna, clara, institucional | Orgánica, territorial, única |
| **Legibilidad en titulares** | Alta | Muy alta | Alta |
| **Legibilidad en texto corrido** | Muy alta | Media-alta | Media |
| **Alineamiento con la marca RBSR** | Parcial — evoca naturaleza y tradición pero no es la fuente oficial | Sí — es la tipografía de titulares oficial | Sí — es la tipografía corporativa exclusiva de la Reserva |
| **Disponibilidad en Canva** | ✅ Nativa en Canva | ✅ Disponible en Canva (Google Fonts) | ❌ No disponible en Canva (fuente propietaria) |

### Veredicto

**News Cycle es una opción aceptable como fuente secundaria o de cuerpo de texto en Canva**, especialmente para textos explicativos dentro de carteles o plantillas. Su carácter editorial y orgánico armoniza bien con el territorio rural de la Sierra. Sin embargo, **no debe usarse como tipografía principal de titulares**, ya que ese rol le corresponde a **Montserrat Bold** (que sí está disponible en Canva de forma nativa como fuente de Google Fonts).

### Recomendación de combinación tipográfica en Canva

La siguiente combinación respeta la identidad de marca y es 100% ejecutable en Canva:

- **Titulares principales (H1)**: `Montserrat Bold` — fuerza, modernidad, coherencia institucional.
- **Subtítulos (H2/H3)**: `Montserrat SemiBold` — jerarquía clara y visual.
- **Texto de lectura / cuerpo**: `News Cycle Regular` — legibilidad editorial cálida y cercana a la tradición impresa del territorio.

Esta combinación **Montserrat + News Cycle** ofrece el contraste visual adecuado entre lo geométrico y limpio (institucional) y lo orgánico y editorial (territorial), complementándose sin competir. Es un emparejamiento semánticamente coherente con la Reserva.

### Lo que debes evitar

- No uses News Cycle en titulares de portada o cabeceras de imagen digital (demasiado pequeña a distancia).
- No uses News Cycle Bold en combinación con Montserrat Bold en el mismo bloque — saturará el peso visual.
- No mezcles más de dos familias tipográficas en una misma pieza gráfica.

---

## Q&A_002: ¿Cuándo usar el logo en negativo (blanco) vs. el logo en color?

**Fecha:** Junio 2026

### Respuesta

- **Logo en color (verde oliva sobre fondo claro)**: úsalo sobre fondos crema (`#f4f3ed`), blancos o fotográficos muy luminosos con zonas claras.
- **Logo en negativo (blanco puro)**: úsalo sobre fondos oscuros (verde bosque `#2e4d3e`, pizarra `#262923`) o sobre fotografías de tonos medios-oscuros del territorio.
- **Regla de oro**: si hay duda sobre la legibilidad del logo, coloca siempre una banda semitransparente de color sólido detrás del logo para garantizar el contraste mínimo de lectura.

---

## Q&A_003: ¿Cuántos hashtags usar en Instagram y cuáles son los fijos de la marca?

**Fecha:** Junio 2026

### Respuesta

El manual de la Reserva establece entre **3 y 5 hashtags** por publicación (máximo 8 en casos excepcionales de alta difusión). El uso excesivo de hashtags penaliza el alcance orgánico en el algoritmo actual de Instagram (2024–2026).

**Hashtags fijos de marca (siempre presentes):**
- `#SierraDelRincon`
- `#ReservaDeLaBiosfera`

**Hashtags rotativos por sección:**
- `#AgendaRBSR` — actividades del CEA y OT
- `#SabíasQue` — píldoras de divulgación
- `#GenteDelBosque` — historias de productores y vecinos

**Hashtags estacionales sugeridos:**
- Primavera: `#PrimaveraSerrana`, `#HayedoMontejo`
- Verano: `#VeranoSerrano`, `#NaturalezaMadrid`
- Otoño: `#OtoñoSerrano`, `#BosquesMadrid`
- Invierno: `#InviernoSerrano`, `#SierraDeMadrid`

---

> *¿Tienes una nueva pregunta? Añádela en este archivo con el formato `## Q&A_XXX: Pregunta` y ejecuta `python3 generar_portal.py` para que aparezca automáticamente en el portal.*
