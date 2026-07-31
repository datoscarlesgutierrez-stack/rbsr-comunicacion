# Directrices de Redacción y Plantillas de Texto: Canales RBSR

Este documento establece las estructuras, longitudes recomendadas y plantillas de redacción adaptadas para cada uno de los canales de comunicación de la **Reserva de la Biosfera Sierra del Rincón (RBSR)**.

---

## 📁 Guía del Excel de Plantillas y Protocolo Estacional

Disponemos de una **Matriz de Mensajes en Excel** que sirve como guía unificada de acceso a las plantillas de redes y Canva, y como protocolo para redactar textos adaptados al ritmo y tono de la Sierra.


> [!IMPORTANT]
> 🔗 **[ACCEDER AL EXCEL DE PLANTILLAS Y PROTOCOLO DE LA RESERVA](https://docs.google.com/spreadsheets/d/1ZWrurZqTga1lSKKCR7BXOUxXwOrvge-eUrd5y-vPkBw/edit?gid=81569507#gid=81569507)**
> *(Nota: El documento se encuentra en modo Comentador. Si necesitas permisos de edición directa para tu área, solicita el acceso a través del propio enlace de Google Drive).*

---

### 🎨 Enlaces a las Plantillas de Diseño en Canva (Resoluciones)

*   **Plantilla 1:1 (Meta)**: `https://canva.link/metarsrb`
*   **Plantilla 4:5**: `https://canva.link/933xncglzshcqxy`
*   **Plantilla 16:9**: `https://canva.link/fgesdrt0q2oji1v`
*   **Plantilla 9:16 (Story)**: `https://canva.link/ql314ijqwb1k2qe`

<details class="bg-stone-50 border border-stone-200 rounded-2xl p-6 my-6 group">
    <summary class="font-title font-bold text-sm text-reserve-forest cursor-pointer hover:text-reserve-olive transition-colors flex items-center justify-between">
        <span class="flex items-center gap-2">🔧 PERSONALIZACIÓN: Configuración de Enlaces Canva (Guardado en Navegador)</span>
        <span class="text-xs text-stone-400 group-open:rotate-180 transition-transform">▼</span>
    </summary>
    <div class="mt-4 pt-4 border-t border-stone-200/60 space-y-4">
        <p class="text-base text-stone-500">Puedes personalizar y modificar los enlaces de Canva aquí abajo. Se guardarán en el almacenamiento local de tu navegador para futuras sesiones sin alterar los archivos de origen.</p>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Generica -->
            <div class="space-y-1">
                <label class="block text-3xs font-bold text-stone-500 uppercase tracking-wider">Plantilla Genérica Post</label>
                <input type="text" id="canva-edit-generica_post" class="w-full px-3 py-2 rounded-lg border border-stone-200 text-xs focus:ring-1 focus:ring-reserve-forest">
            </div>
            <div class="space-y-1">
                <label class="block text-3xs font-bold text-stone-500 uppercase tracking-wider">Plantilla Genérica Story</label>
                <input type="text" id="canva-edit-generica_story" class="w-full px-3 py-2 rounded-lg border border-stone-200 text-xs focus:ring-1 focus:ring-reserve-forest">
            </div>
            <!-- Primavera -->
            <div class="space-y-1">
                <label class="block text-3xs font-bold text-pink-600 uppercase tracking-wider">🌸 Primavera Post</label>
                <input type="text" id="canva-edit-primavera_post" class="w-full px-3 py-2 rounded-lg border border-stone-200 text-xs focus:ring-1 focus:ring-reserve-forest">
            </div>
            <div class="space-y-1">
                <label class="block text-3xs font-bold text-pink-600 uppercase tracking-wider">🌸 Primavera Story</label>
                <input type="text" id="canva-edit-primavera_story" class="w-full px-3 py-2 rounded-lg border border-stone-200 text-xs focus:ring-1 focus:ring-reserve-forest">
            </div>
            <!-- Verano -->
            <div class="space-y-1">
                <label class="block text-3xs font-bold text-amber-600 uppercase tracking-wider">☀️ Verano Post</label>
                <input type="text" id="canva-edit-verano_post" class="w-full px-3 py-2 rounded-lg border border-stone-200 text-xs focus:ring-1 focus:ring-reserve-forest">
            </div>
            <div class="space-y-1">
                <label class="block text-3xs font-bold text-amber-600 uppercase tracking-wider">☀️ Verano Story</label>
                <input type="text" id="canva-edit-verano_story" class="w-full px-3 py-2 rounded-lg border border-stone-200 text-xs focus:ring-1 focus:ring-reserve-forest">
            </div>
            <!-- Otoño -->
            <div class="space-y-1">
                <label class="block text-3xs font-bold text-orange-600 uppercase tracking-wider">🍁 Otoño Post</label>
                <input type="text" id="canva-edit-otono_post" class="w-full px-3 py-2 rounded-lg border border-stone-200 text-xs focus:ring-1 focus:ring-reserve-forest">
            </div>
            <div class="space-y-1">
                <label class="block text-3xs font-bold text-orange-600 uppercase tracking-wider">🍁 Otoño Story</label>
                <input type="text" id="canva-edit-otono_story" class="w-full px-3 py-2 rounded-lg border border-stone-200 text-xs focus:ring-1 focus:ring-reserve-forest">
            </div>
            <!-- Invierno -->
            <div class="space-y-1">
                <label class="block text-3xs font-bold text-sky-600 uppercase tracking-wider">❄️ Invierno Post</label>
                <input type="text" id="canva-edit-invierno_post" class="w-full px-3 py-2 rounded-lg border border-stone-200 text-xs focus:ring-1 focus:ring-reserve-forest">
            </div>
            <div class="space-y-1">
                <label class="block text-3xs font-bold text-sky-600 uppercase tracking-wider">❄️ Invierno Story</label>
                <input type="text" id="canva-edit-invierno_story" class="w-full px-3 py-2 rounded-lg border border-stone-200 text-xs focus:ring-1 focus:ring-reserve-forest">
            </div>
        </div>

        <div class="flex justify-end gap-3 pt-2">
            <button onclick="resetCanvaTemplates()" class="px-4 py-2 rounded-xl border border-stone-300 text-xs font-bold text-stone-600 hover:bg-stone-100 transition-colors">
                🔄 Restaurar Originales
            </button>
            <button onclick="saveCanvaTemplates()" class="px-5 py-2 rounded-xl bg-reserve-forest text-white text-xs font-bold hover:bg-stone-800 transition-all">
                💾 Guardar Enlaces
            </button>
        </div>
    </div>
</details>

---

### 🗺️ Paso a Paso para Crear Nuevos Contenidos
Cuando necesites comunicar una actividad, un evento o una noticia, **no empieces desde cero**. Sigue este sencillo protocolo de 5 pasos para garantizar la coherencia visual y el espíritu de la Reserva:

1. **Seleccionar la pestaña adecuada**: Entra en el Excel y elige la pestaña correspondiente a la estación actual (🌸 Primavera, ☀️ Verano, 🍁 Otoño, ❄️ Invierno) o la pestaña **Genérico** si el mensaje no depende del clima.
2. **Duplicar una sección base**: Busca el bloque temático que más se parezca a tu objetivo (ej. dar la bienvenida, proponer una ruta o invitar a un taller) y cópialo.
3. **Adaptar el Titular**: Modifica el titular de forma sugerente para capturar la atención, manteniendo la brevedad.
4. **Redactar la Descripción y el Texto Largo**: Ajusta los campos al contenido concreto de tu actividad. **Respeta los límites de caracteres** indicados en el Excel para evitar que se corten en el feed.
5. **Aplicar la Estética Visual**: Accede al **enlace de Canva** asociado a ese bloque de mensaje (en las columnas derechas del Excel) para maquetar la pieza visual con la paleta de colores de esa estación.

---

### 🗂️ ¿Cómo está Organizado el Excel?

El documento se divide en pestañas estacionales y una pestaña transversal:
*   **Primavera / Verano / Otoño / Invierno**: Mensajes que respiran el cambio de la naturaleza, adaptados a la temperatura, los colores del bosque y los sentimientos de cada época.
*   **Pestaña "Genérico"**: Mensajes institucionales, recordatorios permanentes de buenas prácticas en el medio natural, invitaciones generales y comunicaciones sobre los valores, el cuidado y el respeto por el territorio.

#### Estructura de Cada Sección
Dentro de cada pestaña, cada bloque de comunicación se compone estrictamente de tres partes:
*   **Titular**: Frase corta que resume y define el propósito del mensaje de forma directa.
*   **Descripción**: Breve texto de 1 o 2 frases que acompaña, contextualiza y añade valor.
*   **Texto Largo (Caption)**: El mensaje principal del post, pensado para comunicar con calma, claridad y profundidad.

---

### 🌿 El Tono de Voz que debemos Cuidar Siempre
Cada mensaje es una pequeña puerta de entrada a la Sierra del Rincón. No comunicamos simplemente folletos de actividades; **comunicamos una forma respetuosa de habitar el territorio**. Todo texto debe ser:

*   **Cercano y humano**: Hablar de tú a tú, conectando con las personas.
*   **Claro y fácil de entender**: Evitar los tecnicismos burocráticos y la palabrería excesiva.
*   **Vinculado al territorio**: Conectar el mensaje con los nombres de nuestros seis municipios, nuestros oficios y nuestros productores locales.
*   **Sin exageraciones**: Comunicación sincera y calmada, sin usar lenguaje comercial agresivo.
*   **Que invite a cuidar**: Antes de publicar, hazte siempre esta pregunta clave:
    > *¿Este texto invita a venir con respeto y a quedarse un poco más en nuestra tierra?*

---

## 1. Instagram & Facebook: "La Sierra se siente"

*   **Propósito**: Inspirar, conectar emocionalmente y mostrar el latido diario del territorio (paisajes, productores, actividades).
*   **Frecuencia**: 1–2 publicaciones semanales en feed + 3–5 stories (especialmente en semanas de actividad).
*   **Longitud**: 100–180 palabras (los captions largos bien narrados funcionan mejor que las descripciones escuetas).
*   **Reglas**:
    *   **Gancho Emocional**: Las 2 primeras líneas deben capturar el espíritu de la sierra (sensaciones, estaciones, curiosidades).
    *   **Llamada a la Acción (CTA)**: Siempre clara e inmediata (ej. *"Inscripciones abiertas en el enlace de la biografía"*).
    *   **Hashtags**: Uso **prudente y coherente**. Se recomienda no utilizar más de **3 a 5 hashtags** por publicación. El uso masivo o indiscriminado de etiquetas resulta contraproducente y es penalizado por el algoritmo actual de Instagram, reduciendo la visibilidad de las publicaciones. Agruparlos siempre limpios al final (ej: `#SierraDelRincon #ReservaDeLaBiosfera #TurismoSostenible #CEA`).
    *   **Imagen**: Priorizar fotografía real del territorio. Si se usa IA, generar un fondo botánico/naturaleza en vertical 9:16 con los detalles estacionales del municipio (hojas, flores, textura de pizarra, etc.).

### Plantilla de Post de Actividad (Instagram)
> 🌿 **[Gancho Emocional - Sentir la Sierra]**
> ¿Sabías que el hayedo no duerme en verano? Bajo su denso manto de hojas, la vida serrana late en forma de pequeños arroyos que cantan y sendas sombrías que nos dan un respiro del calor de la gran ciudad.
> 
> Este sábado te invitamos a redescubrir el Hayedo de Montejo con una mirada diferente. No solo caminaremos bajo sus copas centenarias; aprenderemos a escuchar su silencio y a comprender los secretos de su equilibrio natural.
> 
> 📍 **Senda Interpretativa: El Alma del Hayedo**
> 📅 Sábado, [Fecha] | ⏰ 10:00h
> ⏳ Duración: 2.5 horas
> 👥 Dirigido a: Público familiar
> 
> Ven a compartir saberes y a respirar el aire más puro de Madrid.
> 
> 👉 **Inscripción gratuita pero con plazas limitadas**. Haz tu reserva directa en el enlace de nuestra biografía o entra en nuestra página web oficial.
> 
> ---
> `#SierraDelRincon #HayedodeMontejo #TurismoSostenible #EducacionAmbiental`
> *(Texto alternativo para accesibilidad: Fotografía de un grupo de familias caminando sonrientes por una senda forestal rodeada de hayas centenarias, guiados por una técnica con uniforme verde oliva.)*

---

## 2. LinkedIn: "La Sierra que construye futuro"

*   **Propósito**: Posicionar la Reserva como referente en gobernanza, desarrollo socioeconómico sostenible, investigación aplicada y alianzas institucionales.
*   **Frecuencia**: 2–3 publicaciones al mes (enfocadas en impacto y reputación, no en cantidad).
*   **Longitud**: 600–1000 caracteres.
*   **Reglas**:
    *   **Enfoque de Impacto**: Estructurado, profesional y enfocado en datos reales, alianzas con universidades, fomento del empleo local y sostenibilidad ambiental.
    *   **Tono**: Riguroso pero cercano, constructivo, mostrando el modelo de gestión local de "innovación desde lo pequeño".
    *   **Mención Activa**: Etiquetar siempre a las universidades, fundaciones, empresas locales o ayuntamientos involucrados.

### Plantilla de Post Institucional (LinkedIn)
> 👥 **[Titular de Impacto - Desarrollo y Conservación]**
> ¿Cómo se puede revitalizar la economía rural cuidando a la vez un ecosistema protegido por la UNESCO? La respuesta está en la cooperación y en el apoyo al productor local.
> 
> Esta semana hemos finalizado la formación técnica del programa **[Nombre del Programa]**, diseñado en colaboración con [Entidad Colaboradora], donde [Cifra] emprendedores de los municipios de la Sierra del Rincón han compartido metodologías de economía circular aplicada al sector agroalimentario.
> 
> El fomento del empleo local y el desarrollo rural no están reñidos con la conservación. De hecho, son sus mejores aliados. Al priorizar el talento de nuestro territorio, garantizamos que los recursos y los beneficios se queden donde nace la materia prima.
> 
> Agradecemos la participación de todos los técnicos y artesanos locales que hacen de la Sierra del Rincón un laboratorio vivo de sostenibilidad.
> 
> Infórmate más sobre los resultados del programa en nuestra sección web técnica: [enlace]
> 
> `#SierraDelRincon #DesarrolloRural #Sostenibilidad #EconomiaCircular #ProgramaMaB #UNESCO`

---

## 3. WhatsApp & Telegram: "El tablón vivo de la Sierra"

*   **Propósito**: Canal de servicio directo, ágil y de acción inmediata para los vecinos de la comarca y visitantes recurrentes.
*   **Frecuencia**: 1–3 mensajes por semana (evitar saturación para que no silencien el canal).
*   **Longitud**: 3–6 líneas de lectura rápida y escaneable.
*   **Reglas**:
    *   **Título corto + Emoji**: Identificación visual del contenido al instante.
    *   **Estructura fija**: Fecha/Hora + Lugar + Breve descripción + Enlace directo de reserva.
    *   **No repetir**: Si una actividad está llena, enviar un aviso con la lista de espera. Siempre incluir el enlace limpio.

### Plantilla de Mensaje Directo (WhatsApp)
> 🌿 **Taller de Cestería Tradicional en Horcajuelo**
> 📅 Sábado 18 | ⏰ 10:30h
> 📍 Centro Cultural de Horcajuelo de la Sierra
> 🧺 Aprende a tejer mimbre con técnicas tradicionales guiado por artesanos del territorio. Plazas limitadas (prioridad a residentes).
> 
> 👉 **Inscríbete gratis aquí:** [enlace]

---

## 4. Blog & Web: "Historias del Bosque y el Viento"

*   **Propósito**: Desarrollar contenidos de fondo (artículos, entrevistas, reportajes) que queden indexados, aporten valor educativo y mejoren el posicionamiento SEO.
*   **Longitud**: 500–800 palabras.
*   **Estructura Recomendada**:
    1.  **Título Poético**: Inspirado en la sierra (ej: *Donde el agua aprende a cantar*, *El mapa del silencio*).
    2.  **Entrada Estratégica**: Párrafo de 3-4 líneas resumiendo el valor conceptual de lo que se va a narrar.
    3.  **Bloques Modulares**: Subtítulos descriptivos con párrafos cortos (máx. 5 líneas por párrafo) combinando curiosidades de naturaleza con el impacto de la comunidad local.
    4.  **Cierre con Alma**: Una reflexión vinculada al territorio, la custodia y el futuro.
    5.  **Anexo del Lector**: Ficha de datos prácticos.

### Plantilla de SEO para Entradas de Blog
*   **Título SEO**: `[Tema del Artículo] | Reserva Biosfera Sierra del Rincón` (Máx. 60 caracteres).
*   **Meta Descripción**: Un resumen cautivador de 140-155 caracteres que contenga llamada a la acción y palabras clave como "sostenibilidad", "senderismo responsable" o "Sierra del Rincón".
*   **Encabezados (H1, H2, H3)**: Un solo H1 por página (el título del post), y secciones separadas por H2 con títulos sugerentes.

---

## 🎥 Video Tutoriales y Formación
Para asimilar el uso de las plantillas y el flujo de trabajo en la Reserva, dispones de los siguientes video tutoriales explicativos:

*   **Elegir y guardar una PLANTILLA para comunicación**: [Ver en Loom](https://www.loom.com/share/25fd2d8b8feb4dc3969bbacbe9052c7b)
*   **Matriz de Mensajes de la RBSR Comunicación**: [Ver Presentación Google Slides](https://docs.google.com/presentation/d/1G6qysB5xTwcyReyiHJ7HnxBQECbucpSCnHlLozRybAA/edit?usp=sharing)
*   **Como hacer publicación PARTE 1 (Canva, Edición de Textos)**: [Ver en Loom](https://www.loom.com/share/b118740a435a4f028474da3212ebf607)
*   **Como hacer publicación PARTE 2 (Caso Meta, Sheets, Canva)**: [Ver en Loom](https://www.loom.com/share/a5719f254b5a44248b286fdee2fe161c)

