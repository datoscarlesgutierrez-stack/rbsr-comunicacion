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

## Q&A_001: ¿Qué tipografía se utiliza en Canva para las publicaciones de redes sociales?

**Preguntado por:** Carles (técnico de comunicación)  
**Fecha:** Junio 2026 / Actualizado Julio 2026

### Respuesta

Para todas las plantillas de Redes Sociales en Canva, se ha decidido utilizar la tipografía **News Cycle** (Regular / Bold) para **todos los niveles de texto** (titulares, subtítulos y cuerpo de texto), tal y como está configurado en las plantillas oficiales de Canva.

### Razón y Beneficios

- **Unificación y Simplicidad**: Facilita el trabajo diario de los técnicos sin necesidad de combinar múltiples fuentes.
- **Estética Editorial y Tradición**: Aporta un tono periodístico, sobrio y orgánico muy cercano a la tradición impresa y al espíritu natural del territorio.
- **100% Nativa en Canva**: No requiere instalar ni subir licencias de fuentes externas.

> ⚠️ **Nota de Gobernanza de Diseño**: Esta decisión es la norma operativa actual acordada para dar agilidad al equipo. No obstante, **puede sufrir modificaciones o refinamientos a futuro** según los criterios y decisiones finales que determine el equipo formal de diseño de la Reserva.

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

## Q&A_005: ¿El Generador de Post usa inteligencia artificial para escribir los textos?

**Fecha:** Junio 2026

### Respuesta

**No.** El Generador de Post es una herramienta de **combinación de plantillas**, no un modelo de lenguaje. Funciona completamente en el navegador, sin conexión a ninguna API de IA ni servidor externo.

### ¿Cómo funciona realmente?

Cuando rellenas el formulario y pulsas **"Generar"**, el sistema toma los datos que has introducido (título, fecha, lugar, descripción, enlace y estación del año) y los inserta en una estructura de texto base predefinida diferente según el tipo de contenido elegido:

- **Actividad / Taller Directo** → Genera copys de convocatoria con la logística estructurada en viñetas (fecha, lugar, inscripción) y un tono emocional evocador.
- **Reverberación / Noticia Externa** → Genera copys en estilo "Gente del Bosque": pone en valor la iniciativa local con un tono cercano y comunitario.

A cada tipo se le añaden automáticamente los **metadatos estacionales** elegidos (metáfora literaria de la estación, hashtags correspondientes y estilo visual para el prompt de imagen).

### ¿Qué genera en concreto?

| Salida | Descripción |
| :--- | :--- |
| `Instagram / FB` | Texto largo evocador con emoji, logística, CTA y hashtags de marca |
| `WhatsApp` | Versión corta y escaneable con los datos esenciales |
| `LinkedIn` | Versión institucional y extensa con lenguaje de impacto social |
| `Prompt de IA` | Descripción visual en inglés lista para usar en Midjourney, DALL·E o Gemini |
| `ALT TEXT` | Texto alternativo de accesibilidad para la imagen |

### ¿Para qué sirve entonces?

El generador produce un **borrador estructurado y alineado con la identidad de la Reserva** en cuestión de segundos. Los textos resultantes:
1. **Se pueden publicar directamente** si el contenido encaja bien con los datos introducidos.
2. **Se pueden copiar y pegar en GEM, ChatGPT o similar** como base para que la IA los refine, personalice o amplíe con más detalle.

> **Flujo recomendado**: Genera → Revisa el resultado → Si quieres más profundidad, cópialo en tu GEM de la Reserva y pídele que lo mejore manteniendo el tono y la identidad de la Sierra.

> [!IMPORTANT]
> 📋 Instrucciones para Copiando el texto en el QnA: El generador NO accede a Internet, NO usa ningún modelo de IA externo y NO envía ningún dato a ningún servidor. Todo el procesamiento ocurre localmente en tu propio navegador.

---

## Q&A_006: ¿Dónde está alojada esta web y cómo se realiza su mantenimiento o migración?

**Preguntado por:** Equipo de Comunicación RBSR  
**Fecha:** Julio 2026

### Respuesta

1. **Alojamiento Gratuito e Indefinido**: Esta web está alojada de forma totalmente **gratuita** por parte de [Carles Gutiérrez Vallès](https://carlesgutierrez.github.io/consultoria-digital/) en la infraestructura de GitHub Pages (mientras la plataforma lo permita, en principio de forma indefinida).

2. **Cambio de Dominio**: Si en el futuro se desea asociar la web a un dominio web oficial propio (ej: `comunicacion.sierradelrincon.org`), es una configuración ágil que se puede realizar rápidamente en GitHub contactando con [Carles Gutiérrez](https://carlesgutierrez.github.io/consultoria-digital/).

3. **Migración a otro Servidor o Repositorio**: Si la Reserva o la entidad gestora decide en el futuro migrar esta web a sus propios servidores o a una cuenta de GitHub institucional, se puede solicitar la asistencia técnica a Carles Gutiérrez.

4. **Código Abierto y Repositorio Público**: Todo el código fuente del portal, las plantillas y el generador están disponibles de forma **libre y abierta** en el repositorio público de GitHub:
   - 📁 **Repositorio oficial**: [https://github.com/datoscarlesgutierrez-stack/rbsr-comunicacion](https://github.com/datoscarlesgutierrez-stack/rbsr-comunicacion)

> *Cualquier persona o técnico del equipo puede clonar, descargar o desplegar libremente este proyecto en otra cuenta de GitHub o servidor corporativo en cualquier momento.*

---

## Q&A_007: ¿Cómo funciona la arquitectura de este sitio web y cómo se modifican o actualizan sus contenidos?

**Preguntado por:** Equipo de Comunicación RBSR  
**Fecha:** Julio 2026

### Respuesta

Este portal web no utiliza un CMS complejo ni bases de datos externas; está construido con una arquitectura ligera basada en archivos **Markdown (`.md`)** compilados mediante un script automatizado en Python (`generar_portal.py`).

#### 1. ¿Cómo editar o modificar los contenidos de cada sección?
Cada pestaña del portal corresponde directamente a un archivo de texto en formato Markdown ubicado dentro de la carpeta `recursos/`:

| Pestaña del Portal | Archivo Fuente a Modificar |
| :--- | :--- |
| **🌸 Esencia** | `recursos/1_esencia_y_valores.md` |
| **🎨 Manual Visual** | `recursos/2_sistema_visual.md` |
| **📝 Plantillas** | `recursos/3_canales_y_plantillas.md` |
| **📊 Estrategia** | `recursos/4_estrategia_y_planificacion.md` |
| **🏛️ Manual Anterior** | `recursos/7_manual_uso_marca.md` |
| **❓ Q&A** | `recursos/6_qna.md` |

#### 2. Sintaxis Markdown
Los archivos se editan utilizando formato Markdown simple (encabezados `#`, negritas `**`, listas `-`, enlaces `[texto](url)` y tablas). Puedes aprender la sintaxis rápidamente con estas guías recomendadas:
- 📖 [Guía Básica de Sintaxis Markdown (Markdown Guide)](https://www.markdownguide.org/basic-syntax/)
- 📖 [Tutorial y Sintaxis de Markdown en Español (Markdown.es)](https://markdown.es/sintaxis-markdown/)

#### 3. Flujo de Trabajo para Actualizar la Web (Local)
Para aplicar cualquier cambio o añadir nuevos contenidos al portal:
1. **Descargar / Clonar la Web**: Descargar el proyecto o clonar el repositorio de GitHub a tu equipo local.
2. **Editar los Archivos**: Modificar los textos deseados en la carpeta `recursos/` utilizando cualquier editor de texto o código.
3. **Recompilar el Portal**: Ejecutar la instrucción `python3 generar_portal.py` en la terminal local. Esto generará y actualizará automáticamente el archivo `index.html`.
4. **Publicar los Cambios**: Subir los cambios (*git push*) al repositorio de GitHub para que la web se despliegue actualizada en Internet.

> **Nota sobre el mantenimiento actual y formación futura**:  
> Por el momento, este trabajo de modificación técnica y recompilación en local es realizado por el desarrollador ([Carles Gutiérrez](https://carlesgutierrez.github.io/consultoria-digital/)). No obstante, si el equipo de la Reserva necesita gestionar estas actualizaciones de forma autónoma en el futuro, se puede impartir **capacitación, formación práctica e instrucciones detalladas al equipo** en una próxima sesión de consultoría.

---

> *¿Tienes una nueva pregunta? Añádela en este archivo con el formato `## Q&A_XXX: Pregunta` y ejecuta `python3 generar_portal.py` para que aparezca automáticamente en el portal.*
