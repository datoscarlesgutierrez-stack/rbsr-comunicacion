# 🌿 Portal de Comunicación RBSR
### Reserva de la Biosfera Sierra del Rincón — Toolkit Digital para Técnicos

Portal web interactivo y sistema modular de recursos para la gestión de la comunicación de la **Reserva de la Biosfera Sierra del Rincón (RBSR)**, declarada por la UNESCO en 2005 bajo el programa MaB (Hombre y Biosfera).

🔗 **Versión en línea:** [https://datoscarlesgutierrez-stack.github.io/rbsr-comunicacion](https://datoscarlesgutierrez-stack.github.io/rbsr-comunicacion)

---

## ¿Qué es este proyecto?

Este repositorio contiene todo lo necesario para que los técnicos de la Reserva de la Biosfera Sierra del Rincón puedan comunicar de manera coherente, eficaz y alineada con la identidad de marca del territorio. Incluye:

- **Directrices editoriales y visuales** de la marca RBSR (colores, tipografías, logotipo, tono de voz).
- **Plantillas multicanal** listas para usar en Instagram, LinkedIn, WhatsApp y Blog.
- **Instrucciones para Agentes de IA** adaptadas para Google Gemini (GEM), ChatGPT Custom GPT y Canva (Voz de la marca).
- **Generador interactivo de copys** que produce en segundos textos optimizados para cada red social.
- **Base de conocimiento Q&A** consultable y buscable en tiempo real.

Todo compilado en un único archivo `index.html` autocontenido — sin servidores ni dependencias externas.

---

## Estructura del Repositorio

```
.
├── index.html                          # Portal web interactivo (autogenerado)
├── generar_portal.py                   # Script compilador (Markdown → HTML)
├── skill_comunicacion_rbsr.md          # SKILL raíz del Agente de IA
├── Instrucciones_GEM_ComunicaciónRBSR.md  # Instrucciones completas para GEM
├── README.md                           # Este archivo
│
├── recursos/                           # Módulos editables (fuente de verdad)
│   ├── 1_esencia_y_valores.md          # Propósito, visión, valores y tono de voz
│   ├── 2_sistema_visual.md             # Colores, tipografías, logotipo e imagen
│   ├── 3_canales_y_plantillas.md       # Directrices por canal + plantillas
│   ├── 4_estrategia_y_planificacion.md # 7 ejes, secciones fijas y checklist
│   ├── 5_instrucciones_plataformas.md  # GEM, ChatGPT y Canva (voz de marca)
│   └── 6_qna.md                        # Base de conocimiento Q&A
│
└── Fuentes/                            # Documentos origen del proyecto
    ├── Plan Estrategico Biosfera de la Sierra del Rincon (BSR) - Feb 2- 2026-1.pdf
    └── Prompt Ejemplo Rerva del Rincón.pdf
```

---

## Cómo Actualizar el Portal

1. Edita cualquier archivo `.md` de la carpeta `recursos/` con un editor de texto.
2. Ejecuta el compilador desde la carpeta raíz del proyecto:
   ```bash
   python3 generar_portal.py
   ```
3. El archivo `index.html` se regenera automáticamente con todos los cambios.
4. Sube los cambios a GitHub:
   ```bash
   git add -A && git commit -m "Actualización de recursos" && git push
   ```

> El portal se publica automáticamente en GitHub Pages al hacer `push` a la rama `main`.

---

## Funcionalidades del Portal

| Sección | Descripción |
| :--- | :--- |
| 🌸 **Esencia** | Propósito, visión, valores y tono de voz de la marca |
| 🎨 **Manual Visual** | Paleta de colores interactiva (clic para copiar HEX), tipografías y directrices de imagen |
| 📝 **Plantillas** | Estructuras de texto listas para Instagram, LinkedIn, WhatsApp y Blog |
| 📊 **Estrategia** | 7 ejes temáticos, secciones fijas del calendario y checklist de calidad |
| ⚙️ **Generador de Post** | Formulario que genera al instante copys multicanal + prompt de IA + ALT TEXT |
| 📋 **Instrucciones IA** | Versiones adaptadas para GEM, ChatGPT y Canva con botón "Copiar todo" |
| ❓ **Q&A** | Base de conocimiento buscable con preguntas y respuestas validadas |
| 🤖 **SKILL Agente** | Referencia técnica del SKILL raíz del agente de comunicación |

---

## Identidad Visual (Resumen Rápido)

| Token | Valor | Uso |
| :--- | :--- | :--- |
| Verde Brote | `#b8be3f` (Pantone 583C) | Acentos, CTA, iconos |
| Olivo Oscuro | `#585615` (Pantone 581C) | Textos secundarios, contornos |
| Verde Bosque | `#4d7c67` (Pantone 624C) | Cabeceras institucionales |
| Crema Orgánico | `#f4f3ed` | Fondo principal (nunca blanco puro) |
| Negro Pizarra | `#1c1e1a` | Texto principal |
| Tipografía Titulares | Montserrat Bold | H1, H2, botones |
| Tipografía Cuerpo | Calibri / News Cycle | Párrafos y texto largo |

---

## Contacto

**Reserva de la Biosfera Sierra del Rincón**
Calle Iglesia nº10, Prádena del Rincón — Madrid (28191), España
📧 reservabiosferasierradelrincon@gmail.com

---

*Desarrollado como toolkit digital de comunicación territorial. Declarada Reserva de la Biosfera por la UNESCO el 26 de junio de 2005.*
