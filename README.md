# 🌿 Portal de Comunicación y Recursos - Reserva de la Biosfera Sierra del Rincón (RBSR)
**Toolkit Digital para Técnicos Locales de Comunicación**

Este repositorio contiene el código fuente, los recursos editoriales y las herramientas de automatización del **Portal de Comunicación de la Reserva de la Biosfera Sierra del Rincón (RBSR)**. El portal centraliza el tono de marca, manuales visuales, estrategias y un generador interactivo de posts alineados con las directrices del plan estratégico.

*   🔗 **Portal online:** [datoscarlesgutierrez-stack.github.io/rbsr-comunicacion](https://datoscarlesgutierrez-stack.github.io/rbsr-comunicacion)
*   📁 **Repositorio:** [github.com/datoscarlesgutierrez-stack/rbsr-comunicacion](https://github.com/datoscarlesgutierrez-stack/rbsr-comunicacion)

---

## 🛠️ ¿Para qué sirve `generar_portal.py`?

El archivo `generar_portal.py` es el **compilador/generador estático del portal**. Se encarga de procesar los archivos de contenido en formato Markdown y empaquetarlos en la web final. Sus funciones específicas son:

1.  **Conversión de Contenidos (Markdown ➔ HTML)**:
    *   Lee los archivos origen (`.md`) dentro de la carpeta `recursos/` (esencia, sistema visual, plantillas, estrategia, Q&A).
    *   Analiza y convierte elementos markdown (títulos, tablas, citas, listas, enlaces, alertas especiales) en código HTML estilizado con Tailwind CSS mediante expresiones regulares optimizadas.
2.  **Extracción Dinámica de Enlaces Canva**:
    *   Escanea `recursos/3_canales_y_plantillas.md` buscando los enlaces a plantillas Canva y genera un objeto JSON que inyecta en el portal.
3.  **Generación de Tarjetas Q&A**:
    *   Parsea el documento de preguntas frecuentes (`6_qna.md`) y crea tarjetas dinámicas interactivas listas para el buscador del portal.
4.  **Ensamblaje del Portal (`index.html`)**:
    *   Carga todo el contenido procesado, los prompts de IA y la estructura web, y los empaqueta en un único archivo HTML autocontenido (`index.html`) en la raíz del proyecto.

---

## ⚙️ ¿Cómo funciona este portal web?

El portal está diseñado bajo la filosofía de **Single Page Application (SPA)** y es completamente estático y autocontenido. Funciona de la siguiente manera:

*   **Sin Servidor (Client-side)**: No requiere bases de datos ni backends. Todo el portal se ejecuta localmente en el navegador del usuario a partir del archivo `index.html`.
*   **Diseño Premium con Tailwind CSS**: Carga Tailwind CSS desde un CDN para ofrecer una interfaz moderna y adaptativa (responsive) para móviles, tablets y ordenadores con paletas cromáticas naturales adaptadas a la Reserva.
*   **Navegación Dinámica (Tabs)**: Utiliza Vanilla JavaScript para conmutar las pestañas instantáneamente sin recargar la página. Al pulsar los menús o el logo `SBSR`, el sitio cambia de sección de forma suave y limpia.
*   **Generador de Post Seguro y Privado**: El formulario de generación de posts procesa la información localmente en tu ordenador. Construye copys optimizados para WhatsApp, Instagram y LinkedIn, y redacta prompts de imágenes y textos alternativos (ALT text) sin enviar ningún dato a APIs externas.
*   **Persistencia de Enlaces**: Permite a los técnicos modificar los enlaces de Canva en caliente; estos cambios se guardan localmente en el `localStorage` del navegador para futuras sesiones.

---

## 📁 Estructura del Repositorio

```text
.
├── index.html                            # Portal web final compilado (no editar a mano)
├── generar_portal.py                     # Script compilador (Markdown ➔ HTML)
├── skill_comunicacion_rbsr.md            # Archivo de contexto del Agente de IA en Antigravity
├── Instrucciones_GEM_ComunicaciónRBSR.md # Instrucciones listas para inyectar en Google Gemini (GEM)
├── README.md                             # Este manual explicativo
│
├── recursos/                             # Documentos fuente editables (fuente de verdad)
│   ├── 1_esencia_y_valores.md            # Identidad, visión, valores y tono de voz
│   ├── 2_sistema_visual.md               # Paleta oficial de marca, tipografías y reglas del logo
│   ├── 3_canales_y_plantillas.md         # Directrices de canales de red social y enlaces Canva
│   ├── 4_estrategia_y_planificacion.md   # Los 7 ejes estratégicos, secciones fijas y checklist
│   ├── 5_instrucciones_plataformas.md    # Prompts de sistema para GEM, ChatGPT y Canva
│   └── 6_qna.md                          # Base de conocimiento (Preguntas y Respuestas)
│
└── Fuentes/                              # Documentación original e histórica del proyecto
    ├── Plan Estrategico Biosfera de la Sierra del Rincon (BSR) - Feb 2- 2026-1.pdf
    └── Prompt Ejemplo Rerva del Rincón.pdf
```

---

## 🚀 Guía de Actualización y Despliegue

Si necesitas realizar un cambio en los textos oficiales o añadir información al Q&A, el flujo es el siguiente:

1.  **Edita el archivo fuente**: Modifica el archivo correspondiente dentro de la carpeta `recursos/` (por ejemplo, `recursos/6_qna.md` para añadir una nueva pregunta).
2.  **Compila el portal**: Abre tu terminal en la carpeta raíz y ejecuta:
    ```bash
    python3 generar_portal.py
    ```
    *(Esto actualizará automáticamente `index.html` con tus cambios)*.
3.  **Sube los cambios a GitHub**:
    ```bash
    git add -A
    git commit -m "Actualizar recursos del portal"
    git push
    ```
4.  **Publicación automática**: GitHub Pages detectará la actualización en la rama `main` y publicará los cambios online de forma automática en pocos segundos.

---

## 👥 Desarrollo y Autoría

Este portal y su sistema de automatización y compilación ha sido conceptualizado y desarrollado por:

*   **Desarrollo Tecnológico y Digital**: **[Carles Gutiérrez Vallès](https://carlesgutierrez.github.io/consultoria-digital/)** (Consultoría Tecnológica, Desarrollo Web y Automatización).
*   **Marketing y Comunicación**: **Nicolas Serna** (Estrategia de Marketing Digital y Comunicación Territorial).

Diseñado específicamente como un toolkit digital avanzado para la Mancomunidad y el equipo técnico de la **Reserva de la Biosfera Sierra del Rincón**, declarada por la UNESCO el 26 de junio de 2005.

---

## 📞 Contacto

**Reserva de la Biosfera Sierra del Rincón**  
Calle Iglesia nº10, Prádena del Rincón — Madrid (28191), España  
📧 [reservabiosferasierradelrincon@gmail.com](mailto:reservabiosferasierradelrincon@gmail.com)
