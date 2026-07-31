import os
import re
import json

def parse_markdown_to_html(md_text):
    # Renders markdown headings, bold text, lists, and tables into beautiful HTML.
    
    # Clean up Windows newlines
    md_text = md_text.replace('\r\n', '\n')
    
    # Render Alerts
    def render_alert(match):
        alert_type = match.group(1).upper()
        content = re.sub(r'^>\s*', '', match.group(2), flags=re.M).strip()
        classes = "border-l-4 p-4 my-6 rounded-r-lg "
        icon = ""
        if alert_type == "IMPORTANT":
            classes += "bg-emerald-50 border-emerald-600 text-emerald-800"
            icon = "🌿"
        elif alert_type == "WARNING":
            classes += "bg-amber-50 border-amber-500 text-amber-800"
            icon = "⚠️"
        else:
            classes += "bg-stone-50 border-stone-400 text-stone-800"
            icon = "ℹ️"
        return f'<div class="{classes}"><p class="text-base leading-relaxed">{content}</p></div>'

    md_text = re.sub(r'>\s*\[!(IMPORTANT|WARNING|NOTE)\]\n((?:>\s*.*\n?)+)', 
                     render_alert, 
                     md_text)
    
    # Inline alerts simpler match
    md_text = re.sub(r'>\s*\[!(IMPORTANT|WARNING|NOTE)\]\s*(.*)', 
                     lambda m: f'<div class="border-l-4 border-emerald-600 bg-emerald-50/50 p-4 my-4 rounded-r-lg text-emerald-800"><p class="text-base mt-1">{m.group(2)}</p></div>', 
                     md_text)

    # Standard blockquotes
    def render_blockquote(match):
        content = match.group(1).strip()
        return f'<blockquote class="border-l-4 border-emerald-600 pl-4 py-1 my-4 italic text-stone-600 bg-emerald-50/20 rounded-r p-3 leading-relaxed">{content}</blockquote>'
    md_text = re.sub(r'(?:^>\s+(.*)\n?)+', render_blockquote, md_text, flags=re.M)

    # Tables
    lines = md_text.split('\n')
    in_table = False
    table_lines = []
    html_lines = []
    
    for line in lines:
        if re.match(r'^\s*\|.*\|\s*$', line):
            in_table = True
            table_lines.append(line)
        else:
            if in_table:
                # Render table
                if len(table_lines) >= 2:
                    headers = [c.strip() for c in table_lines[0].split('|')[1:-1]]
                    rows = []
                    for r_line in table_lines[2:]:
                        rows.append([c.strip() for c in r_line.split('|')[1:-1]])
                    
                    table_html = '<div class="overflow-x-auto my-6 rounded-lg border border-stone-200 shadow-sm"><table class="min-w-full divide-y divide-stone-200 text-left">'
                    table_html += '<thead class="bg-stone-50 text-emerald-900 font-semibold">'
                    table_html += '<tr>'
                    for h in headers:
                        table_html += f'<th class="px-6 py-4 font-bold text-sm border-b border-stone-200">{h}</th>'
                    table_html += '</tr></thead>'
                    table_html += '<tbody class="bg-white divide-y divide-stone-100 text-stone-800">'
                    for row in rows:
                        table_html += '<tr class="hover:bg-stone-50/50 transition-colors">'
                        for col in row:
                            # Parse inline formatting in table cells
                            col_parsed = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: f'<a href="{m.group(2)}" target="_blank" rel="noopener" class="text-emerald-700 underline hover:text-emerald-900 font-medium">{m.group(1)}</a>', col)
                            col_parsed = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', col_parsed)
                            col_parsed = re.sub(r'`(.*?)`', r'<code class="px-1 py-0.5 bg-stone-100 rounded text-emerald-800 font-mono text-xs">\1</code>', col_parsed)
                            col_parsed = re.sub(r'(?<!href=")(https?://[^\s<>"]+)', lambda m: f'<a href="{m.group(1)}" target="_blank" rel="noopener" class="text-emerald-700 underline text-xs break-all">{m.group(1)}</a>', col_parsed)
                            table_html += f'<td class="px-6 py-4 text-base border-b border-stone-100">{col_parsed}</td>'
                        table_html += '</tr>'
                    table_html += '</tbody></table></div>'
                    html_lines.append(table_html)
                in_table = False
                table_lines = []
            
            # Simple line parsing
            html_lines.append(line)
            
    md_text = '\n'.join(html_lines)

    # Headings
    md_text = re.sub(r'^#### (.*?)$', r'<h4 class="text-base font-bold text-stone-900 mt-5 mb-2">\1</h4>', md_text, flags=re.M)
    md_text = re.sub(r'^### (.*?)$', r'<h3 class="text-xl font-bold text-emerald-800 mt-8 mb-3 border-b border-stone-200 pb-2">\1</h3>', md_text, flags=re.M)
    md_text = re.sub(r'^## (.*?)$', r'<h2 class="text-2xl font-bold text-emerald-900 mt-10 mb-4 border-l-4 border-emerald-600 pl-4">\1</h2>', md_text, flags=re.M)
    md_text = re.sub(r'^# (.*?)$', r'<h1 class="text-3xl font-black text-emerald-950 mb-6 hidden">\1</h1>', md_text, flags=re.M)

    # Markdown links [text](url) — must run BEFORE bold, code, and auto-URL
    def render_md_link(m):
        label = m.group(1).strip()
        href = m.group(2).strip()
        return f'<a href="{href}" target="_blank" rel="noopener" class="text-emerald-700 underline underline-offset-2 hover:text-emerald-900 transition-colors font-medium">{label}</a>'
    md_text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', render_md_link, md_text)

    # Bold
    md_text = re.sub(r'\*\*(.*?)\*\*', r'<strong class="font-bold text-stone-900">\1</strong>', md_text)

    # Italic (single asterisk, not preceded by * and followed by non-whitespace to avoid matching bullet markers)
    md_text = re.sub(r'(?<!\*)\*(?![\*\s])(.*?)(?<!\*)\*(?!\*)', r'<em class="italic text-stone-700">\1</em>', md_text)

    # Helper: apply all inline formatting (links already done above)
    def inline_format(text):
        # Markdown links [text](url) already done globally above
        # Bold
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong class="font-bold text-stone-900">\1</strong>', text)
        # Italic (non-whitespace after opening * to avoid matching bullet markers)
        text = re.sub(r'(?<!\*)\*(?![\*\s])(.*?)(?<!\*)\*(?!\*)', r'<em class="italic text-stone-700">\1</em>', text)
        # Inline code
        text = re.sub(r'`(.*?)`', lambda m: f'<code class="px-1.5 py-0.5 bg-stone-100 rounded text-emerald-800 font-mono text-sm">{m.group(1)}</code>', text)
        # Auto-link bare https:// URLs inside list items
        text = re.sub(r'(?<!href=")(?<!src=")(https?://[^\s<>"]+)', lambda m: f'<a href="{m.group(1)}" target="_blank" rel="noopener" class="text-emerald-700 underline underline-offset-2 hover:text-emerald-900 transition-colors font-medium break-all">{m.group(1)}</a>', text)
        return text

    # Numbered / Ordered Lists — Processed FIRST to keep their sub-content together
    def render_ordered_list_block(lines_block):
        list_html = '<ol class="list-decimal pl-6 my-5 space-y-3 text-stone-800 leading-relaxed">'
        current_item_lines = []

        def flush_item(item_lines):
            if not item_lines:
                return ''
            first = re.sub(r'^\s*\d+\.\s*', '', item_lines[0]).strip()
            first_html = inline_format(first)
            sub_lines = [l.strip() for l in item_lines[1:] if l.strip()]
            if sub_lines:
                # Check if sub-lines are bullet points
                is_bullet_sub = all(re.match(r'^[\*\-]\s', l) or l.startswith(('*', '-')) for l in sub_lines)
                if is_bullet_sub:
                    sub_html = '<ul class="list-disc pl-5 mt-2 space-y-1.5 text-stone-600">'
                    for sl in sub_lines:
                        sc = re.sub(r'^[\*\-]\s*', '', sl).strip()
                        sub_html += '<li class="text-base">' + inline_format(sc) + '</li>'
                    sub_html += '</ul>'
                else:
                    sub_html = ''.join('<p class="mt-1 text-base text-stone-600">' + inline_format(sl) + '</p>' for sl in sub_lines)
                inner = first_html + sub_html
            else:
                inner = first_html
            return '<li class="text-base">' + inner + '</li>'

        for line in lines_block:
            if re.match(r'^\s*\d+\.', line):
                if current_item_lines:
                    list_html += flush_item(current_item_lines)
                current_item_lines = [line]
            elif current_item_lines and (line.startswith('    ') or line.startswith('\t') or re.match(r'^\s+[\*\-]', line)):
                current_item_lines.append(line)
            else:
                if current_item_lines:
                    list_html += flush_item(current_item_lines)
                    current_item_lines = []

        if current_item_lines:
            list_html += flush_item(current_item_lines)

        list_html += '</ol>'
        return list_html

    # Split text into lines, group ordered list blocks, render them
    ol_lines = md_text.split('\n')
    ol_output = []
    ol_block = []
    in_ol = False

    for line in ol_lines:
        is_num = bool(re.match(r'^\s*\d+\.', line))
        is_sub = bool(in_ol and (line.startswith('    ') or line.startswith('\t') or re.match(r'^\s{2,}[\*\-]', line)))
        if is_num or is_sub:
            in_ol = True
            ol_block.append(line)
        else:
            if in_ol:
                ol_output.append(render_ordered_list_block(ol_block))
                ol_block = []
                in_ol = False
            ol_output.append(line)

    if ol_block:
        ol_output.append(render_ordered_list_block(ol_block))

    md_text = '\n'.join(ol_output)

    # Bullet / Unordered Lists — Processed SECOND
    def render_bullet_block(lines_block):
        list_html = '<ul class="list-disc pl-6 my-5 space-y-3 text-stone-800 leading-relaxed">'
        current_item_lines = []

        def flush_bullet(item_lines):
            if not item_lines:
                return ''
            first = re.sub(r'^\s*[\*\-]\s*', '', item_lines[0]).strip()
            first_html = inline_format(first)
            sub_lines = item_lines[1:]
            if sub_lines:
                sub_paras = ''.join('<p class="text-base text-stone-600">' + inline_format(l.strip().lstrip('*').lstrip('-').strip()) + '</p>' for l in sub_lines if l.strip())
                inner = first_html + ('<div class="mt-1">' + sub_paras + '</div>' if sub_paras else '')
            else:
                inner = first_html
            return '<li class="text-base">' + inner + '</li>'

        for line in lines_block:
            is_bullet = bool(re.match(r'^\s*[\*\-]\s', line))
            is_sub = bool(current_item_lines and (line.startswith('    ') or line.startswith('\t')))
            if is_bullet:
                if current_item_lines:
                    list_html += flush_bullet(current_item_lines)
                current_item_lines = [line]
            elif is_sub:
                current_item_lines.append(line)
            else:
                if current_item_lines:
                    list_html += flush_bullet(current_item_lines)
                    current_item_lines = []

        if current_item_lines:
            list_html += flush_bullet(current_item_lines)

        list_html += '</ul>'
        return list_html

    ul_lines = md_text.split('\n')
    ul_output = []
    ul_block = []
    in_ul = False

    for line in ul_lines:
        is_bullet = bool(re.match(r'^\s*[\*\-]\s', line))
        is_sub = bool(in_ul and (line.startswith('    ') or line.startswith('\t')))
        if is_bullet or is_sub:
            in_ul = True
            ul_block.append(line)
        else:
            if in_ul:
                ul_output.append(render_bullet_block(ul_block))
                ul_block = []
                in_ul = False
            ul_output.append(line)

    if ul_block:
        ul_output.append(render_bullet_block(ul_block))

    md_text = '\n'.join(ul_output)

    # Inline code (for any backticks not yet converted inside other blocks)
    md_text = re.sub(r'`(.*?)`', lambda m: f'<code class="px-1.5 py-0.5 bg-stone-100 rounded text-emerald-800 font-mono text-sm">{m.group(1)}</code>', md_text)

    # Auto-link remaining bare https:// URLs (outside blocks already processed)
    md_text = re.sub(r'(?<!href=")(?<!src=")(https?://[^\s<>"]+)', lambda m: f'<a href="{m.group(1)}" target="_blank" rel="noopener" class="text-emerald-700 underline underline-offset-2 hover:text-emerald-900 transition-colors font-medium break-all">{m.group(1)}</a>', md_text)

    # Checklist checkboxes (optional)
    md_text = re.sub(r'- \[ \]\s+(.*?)$', r'<label class="flex items-start gap-3 my-3 p-3 bg-stone-50 border border-stone-200 rounded-lg cursor-pointer hover:bg-stone-100/50 transition-colors"><input type="checkbox" class="w-4 h-4 mt-1 rounded border-stone-300 text-emerald-600 focus:ring-emerald-500"><span class="text-base text-stone-700 leading-relaxed">\1</span></label>', md_text, flags=re.M)

    # Strip markdown horizontal rules (--- lines) — no se muestran como guiones
    md_text = re.sub(r'^\s*[-]{3,}\s*$', '', md_text, flags=re.M)

    # Paragraphs (excluding tags already created)
    blocks = md_text.split('\n\n')
    processed_blocks = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        if block.startswith('<h') or block.startswith('<div') or block.startswith('<ul') or block.startswith('<ol') or block.startswith('<table') or block.startswith('<block') or block.startswith('<label') or block.startswith('<thead') or block.startswith('<tbody'):
            processed_blocks.append(block)
        else:
            # Body paragraphs: base size, high contrast, generous line-height
            processed_blocks.append(f'<p class="text-stone-800 leading-loose my-5 text-base">{block}</p>')
            
    return '\n'.join(processed_blocks)

def extract_platform_block(md_text, platform_tag):
    """Extract text between PLATAFORMA_XXX_START and PLATAFORMA_XXX_END markers."""
    pattern = rf'## PLATAFORMA_{platform_tag}_START\s*\n(.*?)\n## PLATAFORMA_{platform_tag}_END'
    match = re.search(pattern, md_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return f"(Bloque {platform_tag} no encontrado en 5_instrucciones_plataformas.md)"

def compile_portal():
    recursos_path = "recursos"
    files = {
        "esencia": "1_esencia_y_valores.md",
        "visual": "2_sistema_visual.md",
        "plantillas": "3_canales_y_plantillas.md",
        "estrategia": "4_estrategia_y_planificacion.md",
        "manual": "7_manual_uso_marca.md"
    }
    
    contents = {}
    for key, filename in files.items():
        full_path = os.path.join(recursos_path, filename)
        if os.path.exists(full_path):
            with open(full_path, "r", encoding="utf-8") as f:
                md_text = f.read()
                contents[key] = parse_markdown_to_html(md_text)
        else:
            contents[key] = f"<p class='text-amber-600'>Error: Archivo {filename} no encontrado en recursos/</p>"

    # Let's read the root skill to display as a helper sheet
    skill_path = "skill_comunicacion_rbsr.md"
    if os.path.exists(skill_path):
        with open(skill_path, "r", encoding="utf-8") as f:
            contents["skill"] = parse_markdown_to_html(f.read())
    else:
        contents["skill"] = "<p class='text-amber-600'>Error: Archivo skill_comunicacion_rbsr.md no encontrado en raíz.</p>"

    # Read GEM instructions (full text for copy-paste)
    gem_path = "Instrucciones_GEM_ComunicaciónRBSR.md"
    gem_raw = ""
    if os.path.exists(gem_path):
        with open(gem_path, "r", encoding="utf-8") as f:
            gem_raw = f.read()
    else:
        gem_raw = "(Archivo Instrucciones_GEM_ComunicaciónRBSR.md no encontrado)"

    # Read platform instructions resource and extract blocks
    plat_path = os.path.join(recursos_path, "5_instrucciones_plataformas.md")
    chatgpt_raw = ""
    canva_raw = ""
    if os.path.exists(plat_path):
        with open(plat_path, "r", encoding="utf-8") as f:
            plat_md = f.read()
        chatgpt_raw = extract_platform_block(plat_md, "CHATGPT")
        canva_raw = extract_platform_block(plat_md, "CANVA")
    else:
        chatgpt_raw = "(Archivo 5_instrucciones_plataformas.md no encontrado)"
        canva_raw = chatgpt_raw

    # Escape raw texts for safe JS embedding (backslash, backtick, dollar)
    def escape_for_js(text):
        return text.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')

    contents["gem_raw_js"] = escape_for_js(gem_raw)
    contents["chatgpt_raw_js"] = escape_for_js(chatgpt_raw)
    contents["canva_raw_js"] = escape_for_js(canva_raw)

    # Read SKILL raw for the advanced Antigravity panel
    skill_raw = ""
    if os.path.exists(skill_path):
        with open(skill_path, "r", encoding="utf-8") as f:
            skill_raw = f.read()
    else:
        skill_raw = "(Archivo skill_comunicacion_rbsr.md no encontrado)"
    contents["skill_raw_js"] = escape_for_js(skill_raw)

    # Extract Canva templates dynamically from 3_canales_y_plantillas.md
    canva_links = {}

    plantillas_file = os.path.join(recursos_path, "3_canales_y_plantillas.md")
    if os.path.exists(plantillas_file):
        with open(plantillas_file, "r", encoding="utf-8") as f:
            plantillas_text = f.read()
        # Find: *   **Key**: `url`
        matches = re.findall(r'\*\*\s*([^:\n]+?)\s*\*\*\s*:\s*`(https?://[^\s`<>"]+)`', plantillas_text, re.IGNORECASE)
        for key, url in matches:
            k = key.lower()
            if "1:1" in k or "meta" in k:
                canva_links["template_1_1"] = url.strip()
            elif "4:5" in k:
                canva_links["template_4_5"] = url.strip()
            elif "16:9" in k:
                canva_links["template_16_9"] = url.strip()
            elif "9:16" in k or "story" in k:
                canva_links["template_9_16"] = url.strip()

    # Fallbacks in case formatting is broken or lines are missing
    defaults = {
        "template_1_1": "https://canva.link/metarsrb",
        "template_4_5": "https://canva.link/933xncglzshcqxy",
        "template_16_9": "https://canva.link/fgesdrt0q2oji1v",
        "template_9_16": "https://canva.link/ql314ijqwb1k2qe"
    }
    for k, v in defaults.items():
        if k not in canva_links:
            canva_links[k] = v

    contents["canva_links_json"] = json.dumps(canva_links)


    # Read & parse QnA resource — split into individual Q&A blocks
    qna_path = os.path.join(recursos_path, "6_qna.md")
    qna_cards_html = ""
    if os.path.exists(qna_path):
        with open(qna_path, "r", encoding="utf-8") as f:
            qna_full = f.read()
        # Split on Q&A_XXX headings
        qna_blocks = re.split(r'(?=## Q&A_\d+:)', qna_full)
        for block in qna_blocks:
            block = block.strip()
            if not block or not block.startswith('## Q&A_'):
                continue
            # Extract question from heading
            title_match = re.match(r'## Q&A_(\d+):\s*(.*)', block)
            if not title_match:
                continue
            q_num = title_match.group(1)
            q_num_int = int(q_num)
            q_text = title_match.group(2).strip()
            # Render body (strip the heading line, parse rest as markdown)
            body_md = block[title_match.end():].strip()
            body_html = parse_markdown_to_html(body_md)
            qna_cards_html += f"""
<div id="qna-{q_num_int}" class="qna-card bg-white p-6 rounded-2xl border border-stone-200 shadow-sm space-y-4 transition-all" data-q="{q_text.lower()}" data-qnum="{q_num_int}">
    <div class="flex items-start justify-between gap-3">
        <button onclick="toggleQnA(this)" class="flex-grow text-left flex items-start justify-between gap-4 group">
            <div class="flex items-center gap-3">
                <span class="bg-reserve-olive/20 text-reserve-olivedark font-title font-black text-sm px-3 py-1.5 rounded-lg shrink-0">#{q_num}</span>
                <h3 class="text-base font-bold text-reserve-forest group-hover:text-reserve-olive transition-colors leading-snug">{q_text}</h3>
            </div>
            <span class="qna-arrow text-reserve-forest text-lg transition-transform shrink-0 mt-0.5">▼</span>
        </button>
        <button onclick="copyQnALink('{q_num_int}')" title="Copiar enlace directo a esta pregunta (#{q_num})" class="p-1.5 rounded-lg text-stone-400 hover:text-reserve-forest hover:bg-stone-100 transition-colors shrink-0 text-sm">
            🔗
        </button>
    </div>
    <div class="qna-body hidden pt-2 border-t border-stone-100 space-y-4">
        {body_html}
    </div>
</div>"""
    else:
        qna_cards_html = "<p class='text-amber-600'>Archivo 6_qna.md no encontrado en recursos/</p>"

    contents["qna_cards"] = qna_cards_html

    # Define HTML Template
    html_template = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RBSR - Portal de Comunicación e Identidad de Marca</title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;900&family=News+Cycle:wght@400;700&family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <!-- TailwindCSS CDN (Premium UI development standard) -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['News Cycle', 'sans-serif'],
                        title: ['News Cycle', 'Montserrat', 'sans-serif'],
                    }},
                    colors: {{
                        reserve: {{
                            light: '#fbfaf5',
                            cream: '#f5f3e9',
                            olive: '#b8be3f',
                            olivedark: '#585615',
                            forest: '#2e4d3e',
                            slate: '#262923',
                            accent: '#a7b50b'
                        }}
                    }}
                }}
            }}
        }}
    </script>
    <style>
        /* ─── Tipografía global forzada: News Cycle ─────────────────────────── */
        *, *::before, *::after {{
            font-family: 'News Cycle', Arial, sans-serif;
        }}
        h1, h2, h3, h4, h5, h6,
        .font-title,
        button, .tab-btn, nav {{
            font-family: 'News Cycle', Arial, sans-serif;
        }}
        code, pre, .font-mono {{
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        }}
        /* ─── Modo Alto Contraste y Accesibilidad ────────────────────────────── */
        html.accessibility-mode {{
            font-size: 112% !important;
        }}
        html.accessibility-mode body {{
            background-color: #f4f2e6 !important;
            color: #111111 !important;
        }}
        html.accessibility-mode *, 
        html.accessibility-mode *::before, 
        html.accessibility-mode *::after {{
            font-weight: 500 !important;
        }}
        html.accessibility-mode main p:not(.text-white):not(.text-stone-200):not(.text-stone-300), 
        html.accessibility-mode main span:not(.text-white):not(.text-stone-200):not(.text-stone-300), 
        html.accessibility-mode main li:not(.text-white), 
        html.accessibility-mode main td:not(.text-white), 
        html.accessibility-mode main label:not(.text-white) {{
            color: #111111 !important;
        }}
        /* Mantener legibilidad blanca dentro de contenedores y botones oscuros */
        html.accessibility-mode .bg-reserve-forest *,
        html.accessibility-mode .bg-stone-800 *,
        html.accessibility-mode .bg-stone-900 *,
        html.accessibility-mode .bg-reserve-slate *,
        html.accessibility-mode footer *,
        html.accessibility-mode .bg-\[\#737a00\] *,
        html.accessibility-mode .bg-emerald-800 *,
        html.accessibility-mode .bg-amber-600 *,
        html.accessibility-mode .active-tab,
        html.accessibility-mode .text-white {{
            color: #ffffff !important;
        }}
        html.accessibility-mode main .text-stone-500,
        html.accessibility-mode main .text-stone-600,
        html.accessibility-mode main .text-stone-400,
        html.accessibility-mode main .text-stone-700 {{
            color: #1a1a1a !important;
            font-weight: 600 !important;
        }}
        /* Fuerza absoluta de texto blanco legible en el Footer */
        html.accessibility-mode footer,
        html.accessibility-mode footer *,
        html.accessibility-mode footer p,
        html.accessibility-mode footer span,
        html.accessibility-mode footer div,
        html.accessibility-mode footer a,
        html.accessibility-mode footer h4 {{
            color: #ffffff !important;
        }}
        html.accessibility-mode .glass,
        html.accessibility-mode section,
        html.accessibility-mode .rounded-2xl:not(button):not(#btn-accessibility),
        html.accessibility-mode .rounded-3xl {{
            border-color: #555555 !important;
        }}
        /* El logo del header nunca recibe borde en ningún modo */
        html.accessibility-mode header button img,
        html.accessibility-mode header button {{
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
        }}
        html.accessibility-mode button,
        html.accessibility-mode .tab-btn {{
            border: 2px solid #222222 !important;
        }}
        /* ─── Estilos de Selección de Texto (Mouse Highlight) ───────────────── */
        ::selection {{
            background-color: #1e3b2e !important; /* Fondo verde oscuro de alto contraste */
            color: #ffffff !important;            /* Texto blanco cristalino garantizado */
        }}
        ::-moz-selection {{
            background-color: #1e3b2e !important;
            color: #ffffff !important;
        }}
        /* ─────────────────────────────────────────────────────────────────────── */
        .custom-scrollbar::-webkit-scrollbar {{
            width: 6px;
            height: 6px;
        }}
        .custom-scrollbar::-webkit-scrollbar-track {{
            background: #f5f3e9;
        }}
        .custom-scrollbar::-webkit-scrollbar-thumb {{
            background: #cbd5e1;
            border-radius: 4px;
        }}
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {{
            background: #2e4d3e;
        }}
        .tab-content {{
            display: none;
            opacity: 0;
            transition: opacity 0.3s ease-in-out;
        }}
        .tab-content.active {{
            display: block;
            opacity: 1;
        }}
        .glass {{
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(226, 223, 213, 0.7);
        }}
    </style>
</head>
<body class="bg-reserve-light text-reserve-slate min-h-screen flex flex-col font-sans relative">

    <!-- Top Premium Brand Header -->
    <header class="glass sticky top-0 z-40 px-4 md:px-6 py-2.5 shadow-sm flex flex-col xl:flex-row items-center justify-between gap-2 xl:gap-3">
        <button onclick="switchTab('esencia'); window.scrollTo({{top: 0, behavior: 'smooth'}});" class="flex items-center text-left gap-2.5 hover:opacity-90 active:scale-[0.99] transition-all focus:outline-none group shrink-0">
            <!-- Isotipo logo oficial RBSR (sin borde en ningún modo) -->
            <img src="recursos/img/logo_solo.png" alt="Logo Sierra del Rincón" class="w-9 h-9 md:w-10 md:h-10 object-contain select-none group-hover:scale-105 transition-all" style="border:none !important; box-shadow:none !important;">
            <div class="leading-tight">
                <h1 class="font-title font-black text-base md:text-lg tracking-tight text-reserve-forest group-hover:text-reserve-olive transition-colors">
                    <span class="hidden xl:inline">Reserva de la Biosfera </span>Sierra del Rincón
                </h1>
            </div>
        </button>
        
        <!-- Navigation Menu -->
        <nav class="flex flex-wrap items-center gap-1 bg-stone-100/90 p-1.5 rounded-2xl border border-stone-300/80 shadow-inner">
            <button onclick="switchTab('esencia')" id="btn-esencia" class="tab-btn px-3 py-1.5 text-xs md:text-sm font-bold rounded-xl text-reserve-slate hover:bg-stone-200/70 transition-all active-tab bg-reserve-forest text-white shadow-sm">
                🌸 Esencia
            </button>
            <button onclick="switchTab('visual')" id="btn-visual" class="tab-btn px-3 py-1.5 text-xs md:text-sm font-bold rounded-xl text-reserve-slate hover:bg-stone-200/70 transition-all">
                🎨 Manual Visual
            </button>
            <button onclick="switchTab('plantillas')" id="btn-plantillas" class="tab-btn px-3 py-1.5 text-xs md:text-sm font-bold rounded-xl text-reserve-slate hover:bg-stone-200/70 transition-all">
                📝 Plantillas
            </button>
            <button onclick="switchTab('estrategia')" id="btn-estrategia" class="tab-btn px-3 py-1.5 text-xs md:text-sm font-bold rounded-xl text-reserve-slate hover:bg-stone-200/70 transition-all">
                📊 Estrategia
            </button>
            <button onclick="switchTab('manual')" id="btn-manual" class="tab-btn px-3 py-1.5 text-xs md:text-sm font-bold rounded-xl text-reserve-slate hover:bg-stone-200/70 transition-all">
                🏛️ Manual Anterior
            </button>
            <button onclick="switchTab('tutoriales')" id="btn-tutoriales" class="tab-btn px-3 py-1.5 text-xs md:text-sm font-bold rounded-xl text-reserve-slate hover:bg-stone-200/70 transition-all">
                🎥 Tutoriales
            </button>
            <button onclick="switchTab('generador')" id="btn-generador" class="tab-btn px-3 py-1.5 text-xs md:text-sm font-bold rounded-xl text-reserve-slate hover:bg-stone-200/70 transition-all">
                ⚙️ Generador de Post
            </button>
            <button onclick="switchTab('instrucciones')" id="btn-instrucciones" class="tab-btn px-3 py-1.5 text-xs md:text-sm font-bold rounded-xl text-reserve-slate hover:bg-stone-200/70 transition-all">
                📋 Instrucciones IA
            </button>
            <button onclick="switchTab('qna')" id="btn-qna" class="tab-btn px-3 py-1.5 text-xs md:text-sm font-bold rounded-xl text-reserve-slate hover:bg-stone-200/70 transition-all">
                ❓ Q&amp;A
            </button>
        </nav>
    </header>

    <!-- Main Container -->
    <main class="flex-grow max-w-7xl w-full mx-auto p-4 md:p-8 flex flex-col gap-8">
        
        <!-- Welcome Floating Banner -->
        <div class="rounded-2xl bg-gradient-to-r from-reserve-forest to-stone-800 p-6 md:p-8 text-white shadow-lg relative overflow-hidden flex flex-col md:flex-row justify-between items-center gap-6">
            <div class="absolute inset-0 opacity-10 bg-[radial-gradient(#b8be3f_1px,transparent_1px)] [background-size:16px_16px]"></div>
            <div class="relative z-10 space-y-2">
                <span class="px-2.5 py-1 rounded bg-reserve-olive text-reserve-forest font-title font-bold text-xs uppercase tracking-wider select-none">
                    Toolkit de los Técnicos
                </span>
                <h2 class="text-2xl md:text-3xl font-black font-title tracking-tight">Manual de Comunicación y Recursos de la Reserva</h2>
                <p class="text-stone-200 text-sm md:text-base max-w-2xl leading-relaxed">
                    Portal de consulta activa para los técnicos de comunicación. Encuentra la guía visual, mensajes clave por municipio, plantillas directas y el generador multicanal.
                </p>
                <div class="pt-2">
                    <a href="https://docs.google.com/presentation/d/1G6qysB5xTwcyReyiHJ7HnxBQECbucpSCnHlLozRybAA/edit?usp=sharing" target="_blank" rel="noopener" class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-white/10 hover:bg-white/20 text-white text-xs font-bold transition-all border border-white/20 shadow-sm group">
                        <span>📊</span> Ver Presentación Análisis Colectivo (Esencia, Sistema Visual y Estrategia) <span class="group-hover:translate-x-0.5 transition-transform">↗</span>
                    </a>
                </div>
            </div>
            
            <div class="relative z-10 flex flex-col items-center md:items-end gap-2 shrink-0">
                <span class="text-xs uppercase font-bold text-stone-300 tracking-wider">Estación del Año Activa</span>
                <div id="current-season-badge" class="font-title font-black text-sm uppercase px-3.5 py-1.5 rounded-full bg-white/10 text-white border border-white/20">
                    🌿 Cargando...
                </div>
            </div>
        </div>

        <!-- Tab 1: Esencia -->
        <div id="tab-esencia" class="tab-content active space-y-6">
            <div class="glass p-6 md:p-10 rounded-3xl shadow-sm space-y-8">
                {contents["esencia"]}
            </div>
        </div>

        <!-- Tab 2: Visual -->
        <div id="tab-visual" class="tab-content space-y-6">
            <div class="glass p-6 md:p-10 rounded-3xl shadow-sm space-y-8">
                
                <!-- Quick interactive color palettes -->
                <h3 class="text-2xl font-bold text-emerald-900 border-b border-stone-200 pb-3 flex items-center gap-2">
                    <span>🎨</span> Paletas de Colores para Redes Sociales
                </h3>
                
                <div class="space-y-6">
                    <!-- Paletas Canva (Redes Sociales y Estacionalidad) -->
                    <div class="space-y-4">
                        <h4 class="text-base font-bold uppercase tracking-wider text-emerald-950 flex items-center gap-2">
                            <span class="inline-block w-3 h-3 rounded-full bg-violet-600"></span>
                            Paletas Canva (Redes Sociales y Estacionalidad)
                        </h4>
                        <p class="text-sm md:text-base font-medium text-stone-800 bg-emerald-50/80 border-l-4 border-emerald-600 p-4 rounded-r-xl leading-relaxed shadow-sm">
                            Combinaciones estacionales optimizadas para las plantillas de Canva. Haz clic sobre cualquier color para copiar su código HEX al portapapeles.
                        </p>
                        
                        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
                            <!-- Paleta Genérica -->
                            <div class="bg-white p-5 rounded-2xl border border-stone-200 shadow-sm flex flex-col justify-between space-y-4">
                                <span class="text-sm font-bold text-stone-900 flex items-center gap-1.5">🔘 Genérica (Principal)</span>
                                <div class="grid grid-cols-3 gap-2.5">
                                    <div onclick="copyToClipboard('#88ab81', 'HEX Verde Musgo Canva')" title="Verde Musgo Suave (#88ab81) - Transversal y recordatorios permanentes." class="group cursor-pointer text-center">
                                        <div class="w-full h-14 rounded-xl bg-[#88ab81] shadow-inner transition-all hover:scale-105"></div>
                                        <span class="text-xs font-bold font-mono text-stone-800 block mt-1.5">#88ab81</span>
                                    </div>
                                    <div onclick="copyToClipboard('#fefaed', 'HEX Crema Hueso Canva')" title="Crema Hueso (#fefaed) - Fondo general para publicaciones limpias." class="group cursor-pointer text-center">
                                        <div class="w-full h-14 rounded-xl bg-[#fefaed] border border-stone-300 shadow-inner transition-all hover:scale-105"></div>
                                        <span class="text-xs font-bold font-mono text-stone-800 block mt-1.5">#fefaed</span>
                                    </div>
                                    <div onclick="copyToClipboard('#92b115', 'HEX Verde Brote Canva')" title="Verde Brote Canva (#92b115) - Acentuación y llamadas a la acción." class="group cursor-pointer text-center">
                                        <div class="w-full h-14 rounded-xl bg-[#92b115] shadow-inner transition-all hover:scale-105"></div>
                                        <span class="text-xs font-bold font-mono text-stone-800 block mt-1.5">#92b115</span>
                                    </div>
                                </div>
                            </div>

                            <!-- Paleta Primavera -->
                            <div class="bg-white p-5 rounded-2xl border border-stone-200 shadow-sm flex flex-col justify-between space-y-4">
                                <span class="text-sm font-bold text-stone-900 flex items-center gap-1.5">🌸 Primavera</span>
                                <div class="grid grid-cols-4 gap-2">
                                    <div onclick="copyToClipboard('#ff8ac7', 'HEX Rosa Floración')" title="Rosa Cerezo / Floración (#ff8ac7) - Tono estacional primaveral." class="group cursor-pointer text-center">
                                        <div class="w-full h-12 rounded-xl bg-[#ff8ac7] shadow-inner transition-all hover:scale-105"></div>
                                        <span class="text-[10px] font-mono font-bold text-stone-700 block mt-1.5">#ff8ac7</span>
                                    </div>
                                    <div onclick="copyToClipboard('#f1efe2', 'HEX Crema Primavera')" title="Crema Primavera (#f1efe2) - Fondo suave estacional." class="group cursor-pointer text-center">
                                        <div class="w-full h-12 rounded-xl bg-[#f1efe2] border border-stone-300 shadow-inner transition-all hover:scale-105"></div>
                                        <span class="text-[10px] font-mono font-bold text-stone-700 block mt-1.5">#f1efe2</span>
                                    </div>
                                    <div onclick="copyToClipboard('#92b115', 'HEX Verde Brote')" title="Verde Brote (#92b115) - Evoca el renacimiento silvestre." class="group cursor-pointer text-center">
                                        <div class="w-full h-12 rounded-xl bg-[#92b115] shadow-inner transition-all hover:scale-105"></div>
                                        <span class="text-[10px] font-mono font-bold text-stone-700 block mt-1.5">#92b115</span>
                                    </div>
                                    <div onclick="copyToClipboard('#103f2b', 'HEX Verde Pino')" title="Verde Pino Oscuro (#103f2b) - Estructura y fondo oscuro." class="group cursor-pointer text-center">
                                        <div class="w-full h-12 rounded-xl bg-[#103f2b] shadow-inner transition-all hover:scale-105"></div>
                                        <span class="text-[10px] font-mono font-bold text-stone-700 block mt-1.5">#103f2b</span>
                                    </div>
                                </div>
                            </div>
                            <!-- Paleta Verano -->
                            <div class="bg-white p-5 rounded-2xl border border-stone-200 shadow-sm flex flex-col justify-between space-y-4">
                                <span class="text-sm font-bold text-stone-900 flex items-center gap-1.5">☀️ Verano</span>
                                <div class="grid grid-cols-4 gap-2">
                                    <div onclick="copyToClipboard('#65b9f0', 'HEX Azul Río')" title="Azul Río / Frescor (#65b9f0) - Agua y cielo estival." class="group cursor-pointer text-center">
                                        <div class="w-full h-12 rounded-xl bg-[#65b9f0] shadow-inner transition-all hover:scale-105"></div>
                                        <span class="text-[10px] font-mono font-bold text-stone-700 block mt-1.5">#65b9f0</span>
                                    </div>
                                    <div onclick="copyToClipboard('#e7b43f', 'HEX Amarillo Sol')" title="Amarillo Sol / Trigo (#e7b43f) - Luz y madurez." class="group cursor-pointer text-center">
                                        <div class="w-full h-12 rounded-xl bg-[#e7b43f] shadow-inner transition-all hover:scale-105"></div>
                                        <span class="text-[10px] font-mono font-bold text-stone-700 block mt-1.5">#e7b43f</span>
                                    </div>
                                    <div onclick="copyToClipboard('#d7bf99', 'HEX Arena')" title="Arena de Río (#d7bf99) - Fondo y texturas terrosas." class="group cursor-pointer text-center">
                                        <div class="w-full h-12 rounded-xl bg-[#d7bf99] shadow-inner transition-all hover:scale-105"></div>
                                        <span class="text-[10px] font-mono font-bold text-stone-700 block mt-1.5">#d7bf99</span>
                                    </div>
                                    <div onclick="copyToClipboard('#103f2b', 'HEX Verde Pino')" title="Verde Pino Oscuro (#103f2b) - Estructura y legibilidad." class="group cursor-pointer text-center">
                                        <div class="w-full h-12 rounded-xl bg-[#103f2b] shadow-inner transition-all hover:scale-105"></div>
                                        <span class="text-[10px] font-mono font-bold text-stone-700 block mt-1.5">#103f2b</span>
                                    </div>
                                </div>
                            </div>

                            <!-- Paleta Invierno -->
                            <div class="bg-white p-5 rounded-2xl border border-stone-200 shadow-sm flex flex-col justify-between space-y-4">
                                <span class="text-sm font-bold text-stone-900 flex items-center gap-1.5">❄️ Invierno</span>
                                <div class="grid grid-cols-3 gap-2.5">
                                    <div onclick="copyToClipboard('#006a3e', 'HEX Verde Acebo')" title="Verde Acebo Oscuro (#006a3e) - Follaje invernal y acebos." class="group cursor-pointer text-center">
                                        <div class="w-full h-14 rounded-xl bg-[#006a3e] shadow-inner transition-all hover:scale-105"></div>
                                        <span class="text-xs font-bold font-mono text-stone-800 block mt-1.5">#006a3e</span>
                                    </div>
                                    <div onclick="copyToClipboard('#9eb3c5', 'HEX Gris Ventisca')" title="Gris Ventisca / Pizarra (#9eb3c5) - Cumbres y roca fría." class="group cursor-pointer text-center">
                                        <div class="w-full h-14 rounded-xl bg-[#9eb3c5] shadow-inner transition-all hover:scale-105"></div>
                                        <span class="text-xs font-bold font-mono text-stone-800 block mt-1.5">#9eb3c5</span>
                                    </div>
                                    <div onclick="copyToClipboard('#ffffff', 'HEX Blanco Nieve')" title="Blanco Nieve (#ffffff) - Claridad y nieve de las cumbres." class="group cursor-pointer text-center">
                                        <div class="w-full h-14 rounded-xl bg-[#ffffff] border border-stone-300 shadow-inner transition-all hover:scale-105"></div>
                                        <span class="text-xs font-bold font-mono text-stone-800 block mt-1.5">#ffffff</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {contents["visual"]}
            </div>
        </div>

        <!-- Tab 3: Plantillas -->
        <div id="tab-plantillas" class="tab-content space-y-6">
            <div class="glass p-6 md:p-10 rounded-3xl shadow-sm space-y-8">
                <!-- Instructions alert -->
                <div class="bg-amber-50 border-l-4 border-amber-500 text-amber-800 p-4 rounded-r-lg">
                    <p class="font-bold text-base">📋 Espacio de Trabajo y Seguimiento</p>
                    <p class="text-base mt-1 leading-relaxed">Como ya se menciona en esta web, disponemos de un <strong>Excel de Google</strong> con todas las pautas para que podáis adaptarlo y usarlo como plantilla, guía y registro de vuestras publicaciones. Para agilizar esa tarea del Excel, se ha creado en la web el <strong>Generador Multicanal de Publicaciones</strong> (pestaña ⚙️ Generador de Post).</p>
                </div>

                <!-- Parse plantillas but also add inline interactive widgets to copy -->
                <div class="prose max-w-none text-stone-700">
                    {contents["plantillas"]}
                </div>

                <!-- Canva Templates Manager (Browser storage editable presets) — placed here so it appears next to the Canva links section -->
                <details class="bg-stone-50 border border-stone-200 rounded-2xl p-6 group">
                    <summary class="font-title font-bold text-sm text-reserve-forest cursor-pointer hover:text-reserve-olive transition-colors flex items-center justify-between">
                        <span class="flex items-center gap-2">🔧 Configuración de Enlaces Canva (Guardado en Navegador)</span>
                        <span class="text-xs text-stone-400 group-open:rotate-180 transition-transform">▼</span>
                    </summary>
                    <div class="mt-4 pt-4 border-t border-stone-200/60 space-y-4">
                        <p class="text-base text-stone-500">Puedes modificar los enlaces de Canva aquí abajo. Se guardarán en el almacenamiento local de tu navegador para futuras sesiones sin alterar los archivos de origen.</p>
                        
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
            </div>
        </div>

        <!-- Tab 4: Estrategia -->
        <div id="tab-estrategia" class="tab-content space-y-6">
            <div class="glass p-6 md:p-10 rounded-3xl shadow-sm space-y-8">
                {contents["estrategia"]}
            </div>
        </div>

        <!-- Tab: Manual Anterior -->
        <div id="tab-manual" class="tab-content space-y-6">
            <div class="glass p-6 md:p-10 rounded-3xl shadow-sm space-y-8">

                <!-- Nota de Contexto y Referencia Histórica -->
                <div class="bg-amber-50 border border-amber-200 p-6 rounded-2xl space-y-4">
                    <div class="flex items-start gap-4">
                        <span class="text-3xl">🏛️</span>
                        <div class="space-y-2">
                            <h4 class="text-base font-bold text-amber-900">Manual de Marca Institucional &amp; Referencias Históricas</h4>
                            <p class="text-xs text-amber-800 leading-relaxed">
                                Este bloque recopila las directrices oficiales basadas en el 
                                <a href="https://drive.google.com/file/d/1mPFJfUtaEvCKvsQ_ZgsfwfyJwHD6Ez6d/view?usp=sharing" target="_blank" rel="noopener" class="underline font-bold hover:text-amber-950">📄 Manual de Estilo de la Marca (2024)</a>.
                                Las referencias a los <strong>«Anexos»</strong> citadas a continuación proceden directamente de dicho documento oficial y se mantienen íntegras para preservar su concordancia técnica.
                            </p>
                        </div>
                    </div>

                    <div class="pt-3 border-t border-amber-200/80 grid grid-cols-1 md:grid-cols-2 gap-4 text-xs text-amber-800">
                        <div class="bg-white/70 p-3.5 rounded-xl border border-amber-200/60">
                            <p class="font-bold text-amber-900 mb-1">📱 Evolución del Diseño para Redes Sociales</p>
                            <p class="leading-relaxed">
                                En la página final del manual de estilo original se incluye una breve pincelada sobre el uso gráfico en Redes Sociales. Desde este portal, hemos restaurado, ampliado y evolucionado esa idea en una propuesta visual ágil, estacional y adaptada a las necesidades reales de comunicación digital de la Reserva.
                            </p>
                        </div>
                        <div class="bg-white/70 p-3.5 rounded-xl border border-amber-200/60">
                            <p class="font-bold text-amber-900 mb-1">⚖️ Recomendación de Revisión Institucional</p>
                            <p class="leading-relaxed">
                                Recomendamos que la Reserva de la Biosfera y su equipo gestor revisen y validen todas estas decisiones de diseño junto a su equipo de diseño formal. Este portal proporciona reglas para dotar de estabilidad y coherencia a las publicaciones, siendo la Reserva quien finalmente adapte y aplique su criterio definitivo.
                            </p>
                        </div>
                    </div>
                </div>

                <!-- Logo Institucional -->
                <div class="space-y-4">
                    <h3 class="text-xl font-bold text-emerald-800 border-b border-stone-100 pb-2 flex items-center gap-2">
                        <span>🖼️</span> Logotipo Oficial
                    </h3>
                    <div class="bg-stone-50 border border-stone-200 rounded-2xl p-6 flex flex-col md:flex-row items-center gap-8">
                        <!-- Logo on white bg — version natural (PNG oficial) -->
                        <div class="flex flex-col gap-3 items-center">
                            <div class="bg-white border border-stone-200 rounded-xl p-8 shadow-sm flex items-center justify-center" style="min-width:300px;">
                                <img src="recursos/img/logo_rbsr_oficial.png" alt="Logo oficial Sierra del Rincón - Reserva de la Biosfera" class="w-64 h-auto" style="max-height:120px; object-fit:contain;">
                            </div>
                            <span class="text-xs text-stone-500">Versión original sobre fondo blanco (uso estándar)</span>
                        </div>
                        <!-- Logo on dark corporate bg -->
                        <div class="flex flex-col gap-3 items-center">
                            <div class="rounded-xl p-8 shadow-md flex items-center justify-center" style="min-width:300px; background:#737a00;">
                                <img src="recursos/img/logo_rbsr_oficial.png" alt="Logo oficial Sierra del Rincón sobre fondo corporativo" class="w-64 h-auto" style="max-height:120px; object-fit:contain; filter: brightness(0) invert(1);">
                            </div>
                            <span class="text-xs text-stone-500">Versión negativo (blanco) sobre fondo corporativo verde</span>
                        </div>
                    </div>
                </div>

                <!-- Paleta Oficial de Marca -->
                <div class="space-y-4">
                    <h3 class="text-xl font-bold text-emerald-800 border-b border-stone-100 pb-2 flex items-center gap-2">
                        <span>🎨</span> Paleta Cromática Oficial (Cartelería Institucional)
                    </h3>
                    <div class="bg-stone-50 border border-stone-200/80 p-6 rounded-2xl">
                        <p class="text-xs text-stone-500 mb-4">Identidad cromática oficial para cartelería física, papelería corporativa, señalética y comunicaciones institucionales impresas. Haz clic en cada color para copiar su código HEX.</p>
                        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                            <!-- Verde Raíz -->
                            <div onclick="copyToClipboard('#737a00', 'HEX Verde Raíz')" title="Verde Raíz (#737a00) - Pantone 583C. Color principal del logotipo y fondos institucionales." class="group cursor-pointer flex items-center gap-3 bg-white p-4 rounded-xl border border-stone-200 hover:border-emerald-600 shadow-sm transition-all hover:-translate-y-0.5">
                                <div class="w-14 h-14 rounded-xl shadow-inner flex-shrink-0" style="background:#737a00;"></div>
                                <div class="text-left">
                                    <p class="text-sm font-bold text-stone-800 leading-none">Verde Raíz</p>
                                    <span class="text-xs text-stone-500 block mt-1">Color principal del logotipo</span>
                                    <span class="text-[11px] font-mono text-stone-400 block mt-1">#737a00 · Pantone 583C</span>
                                </div>
                            </div>
                            <!-- Verde Brote -->
                            <div onclick="copyToClipboard('#b8be3f', 'HEX Verde Brote')" title="Verde Brote (#b8be3f) - Pantone 583C variación. Acentos, iconos y llamadas a la acción." class="group cursor-pointer flex items-center gap-3 bg-white p-4 rounded-xl border border-stone-200 hover:border-emerald-600 shadow-sm transition-all hover:-translate-y-0.5">
                                <div class="w-14 h-14 rounded-xl shadow-inner flex-shrink-0" style="background:#b8be3f;"></div>
                                <div class="text-left">
                                    <p class="text-sm font-bold text-stone-800 leading-none">Verde Brote</p>
                                    <span class="text-xs text-stone-500 block mt-1">Acentos e iconografía</span>
                                    <span class="text-[11px] font-mono text-stone-400 block mt-1">#b8be3f · Pantone 583C</span>
                                </div>
                            </div>
                            <!-- Olivo Oscuro -->
                            <div onclick="copyToClipboard('#585615', 'HEX Olivo Oscuro')" title="Olivo Oscuro (#585615) - Pantone 581C. Textos secundarios y contornos." class="group cursor-pointer flex items-center gap-3 bg-white p-4 rounded-xl border border-stone-200 hover:border-emerald-600 shadow-sm transition-all hover:-translate-y-0.5">
                                <div class="w-14 h-14 rounded-xl shadow-inner flex-shrink-0" style="background:#585615;"></div>
                                <div class="text-left">
                                    <p class="text-sm font-bold text-stone-800 leading-none">Olivo Oscuro</p>
                                    <span class="text-xs text-stone-500 block mt-1">Textos y contornos</span>
                                    <span class="text-[11px] font-mono text-stone-400 block mt-1">#585615 · Pantone 581C</span>
                                </div>
                            </div>
                            <!-- Verde Bosque RERB -->
                            <div onclick="copyToClipboard('#4d7c67', 'HEX Verde Bosque RERB')" title="Verde Bosque RERB (#4d7c67) - Pantone 624C. Red Española de Reservas de la Biosfera." class="group cursor-pointer flex items-center gap-3 bg-white p-4 rounded-xl border border-stone-200 hover:border-emerald-600 shadow-sm transition-all hover:-translate-y-0.5">
                                <div class="w-14 h-14 rounded-xl shadow-inner flex-shrink-0" style="background:#4d7c67;"></div>
                                <div class="text-left">
                                    <p class="text-sm font-bold text-stone-800 leading-none">Verde Bosque RERB</p>
                                    <span class="text-xs text-stone-500 block mt-1">Red Española Reservas Biosfera</span>
                                    <span class="text-[11px] font-mono text-stone-400 block mt-1">#4d7c67 · Pantone 624C</span>
                                </div>
                            </div>
                            <!-- Blanco institucional -->
                            <div onclick="copyToClipboard('#ffffff', 'HEX Blanco Institucional')" title="Blanco (#ffffff) - Para logotipo en negativo y textos sobre fondos oscuros." class="group cursor-pointer flex items-center gap-3 bg-white p-4 rounded-xl border border-stone-200 hover:border-emerald-600 shadow-sm transition-all hover:-translate-y-0.5">
                                <div class="w-14 h-14 rounded-xl shadow-inner flex-shrink-0 border border-stone-300" style="background:#ffffff;"></div>
                                <div class="text-left">
                                    <p class="text-sm font-bold text-stone-800 leading-none">Blanco Institucional</p>
                                    <span class="text-xs text-stone-500 block mt-1">Logotipo en negativo</span>
                                    <span class="text-[11px] font-mono text-stone-400 block mt-1">#ffffff · White</span>
                                </div>
                            </div>
                            <!-- Negro tipográfico -->
                            <div onclick="copyToClipboard('#1a1a18', 'HEX Negro Tipográfico')" title="Negro tipográfico (#1a1a18) - Para textos sobre fondos claros en documentos impresos." class="group cursor-pointer flex items-center gap-3 bg-white p-4 rounded-xl border border-stone-200 hover:border-emerald-600 shadow-sm transition-all hover:-translate-y-0.5">
                                <div class="w-14 h-14 rounded-xl shadow-inner flex-shrink-0" style="background:#1a1a18;"></div>
                                <div class="text-left">
                                    <p class="text-sm font-bold text-stone-800 leading-none">Negro Tipográfico</p>
                                    <span class="text-xs text-stone-500 block mt-1">Textos en impresos</span>
                                    <span class="text-[11px] font-mono text-stone-400 block mt-1">#1a1a18</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Contenido del archivo 7_manual_uso_marca.md -->
                {contents["manual"]}

                <!-- Normas clave de aplicación -->
                <div class="space-y-4">
                    <h3 class="text-xl font-bold text-emerald-800 border-b border-stone-100 pb-2 flex items-center gap-2">
                        <span>📐</span> Normas Clave de Aplicación del Logotipo
                    </h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="bg-red-50 border border-red-100 p-5 rounded-2xl">
                            <p class="text-sm font-bold text-red-700 mb-3 flex items-center gap-2">🚫 Usos Prohibidos</p>
                            <ul class="space-y-2 text-xs text-red-700">
                                <li class="flex items-start gap-2"><span class="mt-0.5">✗</span> Aplastar, estirar o rotar el logotipo</li>
                                <li class="flex items-start gap-2"><span class="mt-0.5">✗</span> Cambiar los colores corporativos por otros no autorizados</li>
                                <li class="flex items-start gap-2"><span class="mt-0.5">✗</span> Colocar el logo sobre fondos con texturas fuertes o imágenes complejas</li>
                                <li class="flex items-start gap-2"><span class="mt-0.5">✗</span> Usar versión color sobre fondos oscuros (usar siempre el negativo blanco)</li>
                                <li class="flex items-start gap-2"><span class="mt-0.5">✗</span> Superar en tamaño visual al escudo/logo del socio colaborador principal</li>
                                <li class="flex items-start gap-2"><span class="mt-0.5">✗</span> Añadir efectos de sombra, bisel o degradados al logotipo</li>
                            </ul>
                        </div>
                        <div class="bg-emerald-50 border border-emerald-100 p-5 rounded-2xl">
                            <p class="text-sm font-bold text-emerald-700 mb-3 flex items-center gap-2">✅ Buenas Prácticas</p>
                            <ul class="space-y-2 text-xs text-emerald-700">
                                <li class="flex items-start gap-2"><span class="mt-0.5">✓</span> Mantener siempre un margen mínimo de <strong>1 cm</strong> en impresión / <strong>20px</strong> en digital</li>
                                <li class="flex items-start gap-2"><span class="mt-0.5">✓</span> Sobre fondos claros → versión color corporativo</li>
                                <li class="flex items-start gap-2"><span class="mt-0.5">✓</span> Sobre fondos oscuros → versión negativo en blanco puro</li>
                                <li class="flex items-start gap-2"><span class="mt-0.5">✓</span> Alinear al mismo nivel horizontal que escudos municipales colaboradores</li>
                                <li class="flex items-start gap-2"><span class="mt-0.5">✓</span> Bloquear proporción de aspecto al redimensionar</li>
                                <li class="flex items-start gap-2"><span class="mt-0.5">✓</span> Usar solo sobre fondos lisos o texturas muy tenues</li>
                            </ul>
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <!-- Tab 5: Generador de Copys (Interactive UI) -->
        <div id="tab-generador" class="tab-content space-y-6">
            <div class="glass p-6 md:p-10 rounded-3xl shadow-sm space-y-6">
                <div>
                    <h2 class="text-2xl font-bold font-title text-reserve-forest">Generador de Copy e Imágenes Multicanal</h2>
                    <p class="text-sm text-stone-500 mt-1">Rellena la ficha técnica del taller o noticia y el sistema formateará instantáneamente los textos optimizados para cada red social con prompts de IA a juego.</p>
                </div>

                <!-- Input Form -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 bg-stone-50 p-6 rounded-2xl border border-stone-200">
                    <div class="space-y-4">
                        <div>
                            <label class="block text-xs font-bold text-stone-600 uppercase tracking-wider mb-1.5">Tipología de Contenido</label>
                            <select id="gen-type" onchange="toggleFormInputs()" class="w-full px-4 py-2.5 rounded-lg border border-stone-300 focus:outline-none focus:ring-2 focus:ring-reserve-forest text-sm font-semibold">
                                <option value="actividad">🌿 Actividad / Taller Directo de la Reserva (CEA/OT)</option>
                                <option value="reverberacion">📢 Reverberación / Noticia Externa ("Gente del Bosque")</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-xs font-bold text-stone-600 uppercase tracking-wider mb-1.5">Título de la Comunicación</label>
                            <input type="text" id="gen-title" placeholder="Ej: Taller de Cestería de Mimbre" class="w-full px-4 py-2.5 rounded-lg border border-stone-300 focus:outline-none focus:ring-2 focus:ring-reserve-forest text-sm">
                        </div>
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="block text-xs font-bold text-stone-600 uppercase tracking-wider mb-1.5">Fecha y Hora</label>
                                <input type="text" id="gen-datetime" placeholder="Ej: Sábado 18 de Julio | 10:30h" class="w-full px-4 py-2.5 rounded-lg border border-stone-300 focus:outline-none focus:ring-2 focus:ring-reserve-forest text-sm">
                            </div>
                            <div>
                                <label class="block text-xs font-bold text-stone-600 uppercase tracking-wider mb-1.5">Municipio / Lugar</label>
                                <input type="text" id="gen-location" placeholder="Ej: Horcajuelo de la Sierra" class="w-full px-4 py-2.5 rounded-lg border border-stone-300 focus:outline-none focus:ring-2 focus:ring-reserve-forest text-sm">
                            </div>
                        </div>
                    </div>

                    <div class="space-y-4">
                        <div>
                            <label class="block text-xs font-bold text-stone-600 uppercase tracking-wider mb-1.5">Descripción de lo que se va a Vivir / Hacer</label>
                            <textarea id="gen-description" rows="3" placeholder="Ej: Aprenderemos las técnicas tradicionales para tejer mimbre, tocando las texturas, guiados por expertos cesteros de la Sierra del Rincón." class="w-full px-4 py-2 rounded-lg border border-stone-300 focus:outline-none focus:ring-2 focus:ring-reserve-forest text-sm"></textarea>
                        </div>
                        <div id="input-link-container">
                            <label class="block text-xs font-bold text-stone-600 uppercase tracking-wider mb-1.5">Enlace de Inscripción / Info</label>
                            <input type="text" id="gen-link" placeholder="Ej: www.sierradelrincon.org/agenda.html" class="w-full px-4 py-2.5 rounded-lg border border-stone-300 focus:outline-none focus:ring-2 focus:ring-reserve-forest text-sm">
                        </div>
                    </div>
                </div>

                <div class="flex justify-center">
                    <button onclick="generatePosts()" class="px-8 py-3 rounded-full bg-reserve-forest text-white font-title font-black hover:bg-stone-800 transition-all shadow-md flex items-center gap-2">
                        <span>✨</span> GENERAR CONTENIDOS A MEDIDA
                    </button>
                </div>

                <!-- Output Display Areas -->
                <div id="gen-results" class="hidden space-y-6">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        
                        <!-- Instagram Result Card -->
                        <div class="bg-white p-5 rounded-2xl border border-stone-200 flex flex-col justify-between shadow-sm">
                            <div>
                                <div class="flex justify-between items-center mb-3">
                                    <span class="text-xs font-bold uppercase tracking-widest text-pink-600 bg-pink-50 px-2.5 py-1 rounded">📸 Instagram / FB Post</span>
                                    <button onclick="copyToClipboard(document.getElementById('out-ig').innerText, 'Instagram Copy')" class="text-xs font-bold text-reserve-forest hover:text-reserve-olive flex items-center gap-1">📋 Copiar Copy</button>
                                </div>
                                <div id="out-ig" class="text-xs text-stone-700 leading-relaxed whitespace-pre-wrap select-all font-sans bg-stone-50 p-4 rounded-xl border border-stone-200/50 max-h-96 overflow-y-auto custom-scrollbar"></div>
                            </div>
                            <div class="mt-4 pt-3 border-t border-stone-100 flex flex-wrap gap-2 items-center justify-between text-2xs text-stone-400">
                                <div class="flex flex-wrap gap-1.5 items-center">
                                    <span>Canva:</span>
                                    <a id="link-canva-1-1" href="#" target="_blank" class="text-pink-600 underline font-semibold hover:text-pink-800 transition-colors">Plantilla 1:1 (Meta)</a>
                                    <span class="text-stone-300">|</span>
                                    <a id="link-canva-4-5" href="#" target="_blank" class="text-pink-600 underline font-semibold hover:text-pink-800 transition-colors">Plantilla 4:5</a>
                                </div>
                                <span class="font-mono text-3xs">News Cycle / Montserrat</span>
                            </div>
                        </div>

                        <!-- Stories Result Card -->
                        <div class="bg-white p-5 rounded-2xl border border-stone-200 flex flex-col justify-between shadow-sm">
                            <div>
                                <div class="flex justify-between items-center mb-3">
                                    <span class="text-xs font-bold uppercase tracking-widest text-violet-600 bg-violet-50 px-2.5 py-1 rounded">📱 Stories (IG / WA)</span>
                                    <button onclick="copyToClipboard(document.getElementById('out-story').innerText, 'Stories Copy')" class="text-xs font-bold text-reserve-forest hover:text-reserve-olive flex items-center gap-1">📋 Copiar Guión</button>
                                </div>
                                <div id="out-story" class="text-xs text-stone-700 leading-relaxed whitespace-pre-wrap select-all font-sans bg-stone-50 p-4 rounded-xl border border-stone-200/50 max-h-96 overflow-y-auto custom-scrollbar"></div>
                            </div>
                            <div class="mt-4 pt-3 border-t border-stone-100 flex items-center justify-between text-2xs text-stone-400">
                                <span>Canva: <a id="link-canva-9-16" href="#" target="_blank" class="text-violet-600 underline font-semibold hover:text-violet-800 transition-colors">Plantilla 9:16 (Story)</a></span>
                                <span class="font-mono text-3xs">Páginas según longitud</span>
                            </div>
                        </div>

                        <!-- WhatsApp Result Card -->
                        <div class="bg-white p-5 rounded-2xl border border-stone-200 flex flex-col justify-between shadow-sm">
                            <div>
                                <div class="flex justify-between items-center mb-3">
                                    <span class="text-xs font-bold uppercase tracking-widest text-emerald-600 bg-emerald-50 px-2.5 py-1 rounded">🌿 WhatsApp / Tel</span>
                                    <button onclick="copyToClipboard(document.getElementById('out-wa').innerText, 'WhatsApp Copy')" class="text-xs font-bold text-reserve-forest hover:text-reserve-olive flex items-center gap-1">📋 Copiar</button>
                                </div>
                                <div id="out-wa" class="text-xs text-stone-700 leading-relaxed whitespace-pre-wrap select-all font-sans bg-stone-50 p-4 rounded-xl border border-stone-200/50 max-h-96 overflow-y-auto custom-scrollbar"></div>
                            </div>
                            <div class="mt-4 pt-3 border-t border-stone-100 flex flex-col gap-1 text-2xs text-stone-400">
                                <span>Canva: <a id="link-canva-wa-1-1" href="#" target="_blank" class="text-emerald-600 underline font-semibold hover:text-emerald-800 transition-colors">Plantilla 1:1 (Meta)</a></span>
                                <span class="text-stone-300">Enlace limpio + Estructura fija directa</span>
                            </div>
                        </div>

                        <!-- LinkedIn Result Card -->
                        <div class="bg-white p-5 rounded-2xl border border-stone-200 flex flex-col justify-between shadow-sm">
                            <div>
                                <div class="flex justify-between items-center mb-3">
                                    <span class="text-xs font-bold uppercase tracking-widest text-blue-600 bg-blue-50 px-2.5 py-1 rounded">👥 LinkedIn / Web</span>
                                    <button onclick="copyToClipboard(document.getElementById('out-li').innerText, 'LinkedIn Copy')" class="text-xs font-bold text-reserve-forest hover:text-reserve-olive flex items-center gap-1">📋 Copiar</button>
                                </div>
                                <div id="out-li" class="text-xs text-stone-700 leading-relaxed whitespace-pre-wrap select-all font-sans bg-stone-50 p-4 rounded-xl border border-stone-200/50 max-h-96 overflow-y-auto custom-scrollbar"></div>
                            </div>
                            <div class="mt-4 pt-3 border-t border-stone-100 flex flex-col gap-1 text-2xs text-stone-400">
                                <span>Canva: <a id="link-canva-16-9" href="#" target="_blank" class="text-blue-600 underline font-semibold hover:text-blue-800 transition-colors">Plantilla 16:9</a></span>
                                <span>Tono profesional, desarrollo y gobernanza rural</span>
                            </div>
                        </div>
                    </div>

                    <!-- Prompt de Redacción de Textos con IA Card -->
                    <div class="bg-violet-50/50 p-6 rounded-2xl border-2 border-violet-200 shadow-sm space-y-4">
                        <div class="flex justify-between items-center border-b border-violet-100 pb-2">
                            <h4 class="font-title font-bold text-violet-800 text-sm flex items-center gap-1.5">🤖 Prompt de Redacción para cualquier IA (Gemini / ChatGPT / Claude)</h4>
                            <button onclick="copyToClipboard(document.getElementById('out-text-prompt').innerText, 'Prompt de Redacción')" class="px-4 py-2 rounded-full bg-violet-600 text-white text-xs font-bold hover:bg-violet-700 transition-all shadow-sm flex items-center gap-1.5">
                                📋 Copiar Prompt
                            </button>
                        </div>
                        <p class="text-xs text-stone-600">Copia y pega este bloque en tu modelo de lenguaje favorito para generar variaciones de tono, captions y textos alternativos refinados.</p>
                        <div id="out-text-prompt" class="text-xs text-stone-700 bg-white p-4 rounded-xl border border-stone-200/60 leading-relaxed select-all max-h-96 overflow-y-auto custom-scrollbar whitespace-pre-wrap"></div>
                    </div>

                    <!-- Visual Prompt Result Card -->
                    <div class="bg-white p-6 rounded-2xl border border-stone-200 shadow-sm space-y-4">
                        <div class="flex justify-between items-center border-b border-stone-100 pb-2">
                            <h4 class="font-title font-bold text-reserve-forest text-sm flex items-center gap-1.5">🎨 Prompt de Imagen Sugerido</h4>
                            <button onclick="copyToClipboard(document.getElementById('out-prompt').innerText, 'Prompt de IA')" class="text-xs font-bold text-reserve-forest hover:text-reserve-olive flex items-center gap-1">📋 Copiar Prompt</button>
                        </div>
                        <div>
                            <p class="text-xs font-bold text-stone-500 uppercase tracking-widest mb-1">Prompt de Generación de Fondo / Naturaleza (Gemini / Imagen 3)</p>
                            <div id="out-prompt" class="text-xs font-mono text-stone-600 bg-stone-50 p-3 rounded-lg border border-stone-100 leading-relaxed select-all"></div>
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <!-- Tab 6: Instrucciones IA (GEM, ChatGPT, Canva) -->
        <div id="tab-instrucciones" class="tab-content space-y-6">
            <div class="glass p-6 md:p-10 rounded-3xl shadow-sm space-y-8">
                <div>
                    <h2 class="text-2xl font-bold font-title text-reserve-forest">Instrucciones para Plataformas de IA</h2>
                    <p class="text-sm text-stone-500 mt-1 max-w-3xl">Cada plataforma tiene su propio formato y límites. A continuación encontrarás la versión adaptada y lista para copiar de las instrucciones del agente de comunicación RBSR para <strong>Google Gemini (GEM)</strong>, <strong>ChatGPT (Custom GPT / Proyecto)</strong> y <strong>Canva (Voz de la Marca, máx. 500 caracteres)</strong>.</p>
                </div>

                <!-- GEM Card -->
                <div class="bg-white p-6 rounded-2xl border border-stone-200 shadow-sm space-y-4">
                    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-3">
                        <div class="flex items-center gap-3">
                            <span class="text-2xl">💎</span>
                            <div>
                                <h3 class="font-title font-bold text-reserve-forest text-lg">Google Gemini — GEM</h3>
                                <p class="text-xs text-stone-500">Copia íntegro en el campo "Instrucciones" de tu GEM en gemini.google.com</p>
                            </div>
                        </div>
                        <button onclick="copyToClipboard(gemInstructions, 'Instrucciones GEM')" class="px-5 py-2 rounded-full bg-reserve-forest text-white text-xs font-bold hover:bg-stone-800 transition-all shadow-sm flex items-center gap-1.5 shrink-0">
                            📋 Copiar Todo al Portapapeles
                        </button>
                    </div>
                    <!-- GEM textarea - full selectable/copyable -->
                    <textarea id="gem-content" readonly class="w-full mt-3 bg-stone-50 p-4 rounded-xl border border-stone-200 text-xs text-stone-700 font-sans leading-relaxed resize-none focus:outline-none focus:ring-2 focus:ring-reserve-forest custom-scrollbar" rows="14" style="field-sizing:content;max-height:420px;" spellcheck="false"></textarea>
                </div>

                <!-- ChatGPT Card -->
                <div class="bg-white p-6 rounded-2xl border border-stone-200 shadow-sm space-y-4">
                    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-3">
                        <div class="flex items-center gap-3">
                            <span class="text-2xl">🤖</span>
                            <div>
                                <h3 class="font-title font-bold text-stone-800 text-lg">OpenAI — ChatGPT Custom GPT / Proyecto</h3>
                                <p class="text-xs text-stone-500">Copia en el campo "Instructions" de tu Custom GPT o Proyecto</p>
                            </div>
                        </div>
                        <button onclick="copyToClipboard(chatgptInstructions, 'Instrucciones ChatGPT')" class="px-5 py-2 rounded-full bg-stone-800 text-white text-xs font-bold hover:bg-stone-700 transition-all shadow-sm flex items-center gap-1.5 shrink-0">
                            📋 Copiar Todo al Portapapeles
                        </button>
                    </div>
                    <!-- ChatGPT textarea - full selectable/copyable -->
                    <textarea id="chatgpt-content" readonly class="w-full mt-3 bg-stone-50 p-4 rounded-xl border border-stone-200 text-xs text-stone-700 font-sans leading-relaxed resize-none focus:outline-none focus:ring-2 focus:ring-stone-400 custom-scrollbar" rows="14" style="max-height:420px;" spellcheck="false"></textarea>
                </div>

                <!-- Canva Brand Voice Card -->
                <div class="bg-white p-6 rounded-2xl border-2 border-violet-200 shadow-sm space-y-4">
                    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-3">
                        <div class="flex items-center gap-3">
                            <span class="text-2xl">🎨</span>
                            <div>
                                <h3 class="font-title font-bold text-violet-700 text-lg">Canva — Voz de la Marca</h3>
                                <p class="text-xs text-stone-500">Pega en el campo "Voz de la marca" del Kit de Marca de Canva (máx. 500 caracteres)</p>
                            </div>
                        </div>
                        <div class="flex items-center gap-3 shrink-0">
                            <span id="canva-char-count" class="text-xs font-mono text-stone-500"></span>
                            <button onclick="copyToClipboard(canvaInstructions, 'Voz de Marca Canva')" class="px-5 py-2 rounded-full bg-violet-600 text-white text-xs font-bold hover:bg-violet-700 transition-all shadow-sm flex items-center gap-1.5">
                                📋 Copiar al Portapapeles
                            </button>
                        </div>
                    </div>
                    <div class="bg-violet-50/50 p-4 rounded-xl border border-violet-100">
                        <pre id="canva-content" class="text-sm text-violet-900 whitespace-pre-wrap font-sans leading-relaxed cursor-text"></pre>
                    </div>
                </div>

                <!-- Info box -->
                <div class="border-l-4 border-emerald-600 bg-emerald-50/50 p-4 rounded-r-lg text-emerald-800">
                    <p class="font-bold text-sm">🌿 Sincronización Automática</p>
                    <p class="text-xs mt-1">Cada vez que modifiques los archivos de la carpeta <code class="px-1 py-0.5 bg-stone-100 rounded text-emerald-800 font-mono text-xs">recursos/</code>, ejecuta <code class="px-1 py-0.5 bg-stone-100 rounded text-emerald-800 font-mono text-xs">python3 generar_portal.py</code> para regenerar este portal y actualizar automáticamente las instrucciones de todas las plataformas.</p>
                </div>
            </div>
        </div>

        <!-- Tab 7: Q&A Knowledge Base -->
        <div id="tab-qna" class="tab-content space-y-6">
            <div class="glass p-6 md:p-10 rounded-3xl shadow-sm space-y-8">
                <div>
                    <h2 class="text-2xl font-bold font-title text-reserve-forest">Base de Conocimiento Q&amp;A</h2>
                    <p class="text-sm text-stone-500 mt-1 max-w-3xl">Preguntas frecuentes resueltas sobre tipografía, imagen, estrategia y herramientas. El agente las consulta automáticamente. Para añadir una nueva, edita <code class="px-1 py-0.5 bg-stone-100 rounded text-emerald-800 font-mono text-xs">recursos/6_qna.md</code> y regenera el portal.</p>
                </div>

                <!-- Live Search -->
                <div class="relative">
                    <span class="absolute left-4 top-1/2 -translate-y-1/2 text-stone-400 text-lg">🔍</span>
                    <input type="text" id="qna-search" oninput="filterQnA(this.value)" placeholder="Busca una pregunta... (ej: tipografía, logo, hashtags)" class="w-full pl-11 pr-5 py-3 rounded-xl border border-stone-300 focus:outline-none focus:ring-2 focus:ring-reserve-forest text-sm shadow-sm">
                </div>

                <!-- Q&A Cards -->
                <div id="qna-list" class="space-y-4">
                    {contents["qna_cards"]}
                </div>

                <!-- Empty state -->
                <div id="qna-empty" class="hidden text-center py-10 text-stone-400">
                    <span class="text-3xl">🌲</span>
                    <p class="mt-2 text-sm">No se encontraron preguntas que coincidan.</p>
                </div>

                <!-- Add Question Tip -->
                <div class="border-l-4 border-amber-500 bg-amber-50/50 p-4 rounded-r-lg text-amber-800">
                    <p class="font-bold text-sm">💡 ¿Tienes una nueva pregunta?</p>
                    <p class="text-xs mt-1">Añádela en <code class="px-1 py-0.5 bg-stone-100 rounded font-mono text-xs">recursos/6_qna.md</code> con el formato <code class="px-1 py-0.5 bg-stone-100 rounded font-mono text-xs">## Q&A_XXX: Tu pregunta</code> y ejecuta <code class="px-1 py-0.5 bg-stone-100 rounded font-mono text-xs">python3 generar_portal.py</code> para actualizarla aquí automáticamente.</p>
                </div>
            </div>
        </div>

        <!-- Tab 8: Video Tutoriales e Inducción -->
        <div id="tab-tutoriales" class="tab-content space-y-6">
            <div class="glass p-6 md:p-10 rounded-3xl shadow-sm space-y-8">
                <div>
                    <h2 class="text-2xl font-bold font-title text-reserve-forest">🎥 Centro de Formación y Video Tutoriales</h2>
                    <p class="text-sm text-stone-500 mt-1 max-w-3xl">Vídeos explicativos paso a paso y recursos formativos para asimilar el uso de la identidad visual de la Reserva de la Biosfera Sierra del Rincón y agilizar el flujo de trabajo diario.</p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <!-- Loom 1: Plantilla Canva -->
                    <div class="bg-white rounded-2xl border border-stone-200 p-5 shadow-sm hover:shadow-md transition-all flex flex-col justify-between group">
                        <div class="space-y-3">
                            <div class="flex items-center justify-between">
                                <span class="text-2xs font-bold uppercase tracking-widest text-emerald-600 bg-emerald-50 px-2.5 py-1 rounded">Canva / Diseño</span>
                                <span class="text-xs text-stone-400">Duración: ~5 min</span>
                            </div>
                            <h3 class="font-title font-bold text-stone-800 text-lg group-hover:text-reserve-forest transition-colors">Elegir y guardar una plantilla para comunicación</h3>
                            <p class="text-xs text-stone-500 leading-relaxed">Aprende a acceder a las nuevas plantillas unificadas de Canva (4:5, 16:9, 1:1, 9:16) y guardarlas correctamente en tu espacio de trabajo para edición recurrente.</p>
                        </div>
                        <div class="mt-6 pt-4 border-t border-stone-100 flex justify-between items-center">
                            <span class="text-stone-400 text-xs">🎥 Vídeo en Loom</span>
                            <a href="https://www.loom.com/share/25fd2d8b8feb4dc3969bbacbe9052c7b" target="_blank" rel="noopener" class="px-4 py-2 bg-reserve-forest hover:bg-stone-800 text-white rounded-lg text-xs font-bold transition-all shadow-sm">Ver Tutorial</a>
                        </div>
                    </div>

                    <!-- Slides: Matriz de Mensajes -->
                    <div class="bg-white rounded-2xl border border-stone-200 p-5 shadow-sm hover:shadow-md transition-all flex flex-col justify-between group">
                        <div class="space-y-3">
                            <div class="flex items-center justify-between">
                                <span class="text-2xs font-bold uppercase tracking-widest text-amber-600 bg-amber-50 px-2.5 py-1 rounded">Estrategia / Mensaje</span>
                                <span class="text-xs text-stone-400">Presentación Oficial</span>
                            </div>
                            <h3 class="font-title font-bold text-stone-800 text-lg group-hover:text-reserve-forest transition-colors">Matriz de Mensajes de la RBSR</h3>
                            <p class="text-xs text-stone-500 leading-relaxed">Presentación conceptual completa sobre la matriz de comunicación de la Reserva: los 7 ejes de contenido, las secciones fijas y las pautas estratégicas del programa.</p>
                        </div>
                        <div class="mt-6 pt-4 border-t border-stone-100 flex justify-between items-center">
                            <span class="text-stone-400 text-xs">📊 Diapositivas</span>
                            <a href="https://docs.google.com/presentation/d/1G6qysB5xTwcyReyiHJ7HnxBQECbucpSCnHlLozRybAA/edit?usp=sharing" target="_blank" rel="noopener" class="px-4 py-2 bg-amber-600 hover:bg-amber-700 text-white rounded-lg text-xs font-bold transition-all shadow-sm">Ver Presentación</a>
                        </div>
                    </div>

                    <!-- Loom 2: Publicar Parte 1 -->
                    <div class="bg-white rounded-2xl border border-stone-200 p-5 shadow-sm hover:shadow-md transition-all flex flex-col justify-between group">
                        <div class="space-y-3">
                            <div class="flex items-center justify-between">
                                <span class="text-2xs font-bold uppercase tracking-widest text-sky-600 bg-sky-50 px-2.5 py-1 rounded">Edición / Redes</span>
                                <span class="text-xs text-stone-400">Duración: ~8 min</span>
                            </div>
                            <h3 class="font-title font-bold text-stone-800 text-lg group-hover:text-reserve-forest transition-colors">Cómo hacer una publicación (Parte 1)</h3>
                            <p class="text-xs text-stone-500 leading-relaxed">Guía práctica que cubre la selección de imágenes del territorio, la redacción de los copys multicanal adaptados y la edición de textos en Canva.</p>
                        </div>
                        <div class="mt-6 pt-4 border-t border-stone-100 flex justify-between items-center">
                            <span class="text-stone-400 text-xs">🎥 Vídeo en Loom</span>
                            <a href="https://www.loom.com/share/b118740a435a4f028474da3212ebf607" target="_blank" rel="noopener" class="px-4 py-2 bg-reserve-forest hover:bg-stone-800 text-white rounded-lg text-xs font-bold transition-all shadow-sm">Ver Tutorial</a>
                        </div>
                    </div>

                    <!-- Loom 3: Publicar Parte 2 -->
                    <div class="bg-white rounded-2xl border border-stone-200 p-5 shadow-sm hover:shadow-md transition-all flex flex-col justify-between group">
                        <div class="space-y-3">
                            <div class="flex items-center justify-between">
                                <span class="text-2xs font-bold uppercase tracking-widest text-indigo-600 bg-indigo-50 px-2.5 py-1 rounded">Automatización / Sheets</span>
                                <span class="text-xs text-stone-400">Duración: ~7 min</span>
                            </div>
                            <h3 class="font-title font-bold text-stone-800 text-lg group-hover:text-reserve-forest transition-colors">Cómo hacer una publicación (Parte 2)</h3>
                            <p class="text-xs text-stone-500 leading-relaxed">Flujo de trabajo avanzado utilizando el generador automático de posts, la carga de datos de Google Sheets y la exportación final en Canva.</p>
                        </div>
                        <div class="mt-6 pt-4 border-t border-stone-100 flex justify-between items-center">
                            <span class="text-stone-400 text-xs">🎥 Vídeo en Loom</span>
                            <a href="https://www.loom.com/share/a5719f254b5a44248b286fdee2fe161c" target="_blank" rel="noopener" class="px-4 py-2 bg-reserve-forest hover:bg-stone-800 text-white rounded-lg text-xs font-bold transition-all shadow-sm">Ver Tutorial</a>
                        </div>
                    </div>
                </div>

                <div class="border-l-4 border-sky-500 bg-sky-50/50 p-4 rounded-r-lg text-sky-800">
                    <p class="font-bold text-sm">💡 ¿Quieres sugerir un nuevo videotutorial?</p>
                    <p class="text-xs mt-1">Si detectas dudas recurrentes o quieres grabar una inducción sobre un nuevo proceso, ponte en contacto con la coordinación para añadirlo aquí.</p>
                </div>
            </div>
        </div>

    <!-- 🤖 ADVANCED PANEL: Antigravity SKILL (hidden, triggered by robot button) -->
    <div id="advanced-panel" class="hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-end justify-end p-6" onclick="if(event.target===this)closeAdvanced()">
        <div class="bg-stone-900 text-stone-100 rounded-2xl shadow-2xl w-full max-w-3xl max-h-[85vh] flex flex-col overflow-hidden border border-stone-700">
            <!-- Panel Header -->
            <div class="flex items-center justify-between px-6 py-4 border-b border-stone-700 shrink-0">
                <div class="flex items-center gap-3">
                    <span class="text-2xl">🤖</span>
                    <div>
                        <h3 class="font-title font-bold text-white text-base">MODO AVANZADO — SKILL Antigravity</h3>
                        <p class="text-xs text-stone-500 mt-0.5">⚠️ Solo continúa si tienes conocimientos de Antigravity y del ecosistema de este proyecto.</p>
                    </div>
                </div>
                <button onclick="closeAdvanced()" class="text-stone-500 hover:text-white transition-colors text-xl font-bold px-2" title="Cerrar">✕</button>
            </div>

            <!-- Repo link + instructions -->
            <div class="px-6 py-4 border-b border-stone-800 space-y-3 shrink-0">
                <p class="text-xs text-stone-400 leading-relaxed">Este SKILL define el comportamiento del agente cuando trabajas en <strong class="text-stone-200">Antigravity</strong>. Copia el contenido y úsalo como SKILL del proyecto en tu instancia de Antigravity. Para continuar trabajando o clonar el proyecto completo, accede al repositorio.</p>
                <div class="flex flex-wrap gap-3">
                    <a href="https://github.com/datoscarlesgutierrez-stack/rbsr-comunicacion" target="_blank" rel="noopener" class="flex items-center gap-2 px-4 py-2 rounded-lg bg-stone-700 hover:bg-stone-600 text-white text-xs font-bold transition-colors border border-stone-600">
                        <span>📁</span> Ver Repositorio en GitHub
                    </a>
                    <a href="https://github.com/datoscarlesgutierrez-stack/rbsr-comunicacion/archive/refs/heads/main.zip" target="_blank" rel="noopener" class="flex items-center gap-2 px-4 py-2 rounded-lg bg-stone-700 hover:bg-stone-600 text-white text-xs font-bold transition-colors border border-stone-600">
                        <span>⬇️</span> Descargar ZIP
                    </a>
                </div>
                <div class="bg-stone-800 rounded-lg px-4 py-2 font-mono text-xs text-stone-400 select-all">git clone https://github.com/datoscarlesgutierrez-stack/rbsr-comunicacion.git</div>
            </div>

            <!-- SKILL Textarea -->
            <div class="flex items-center justify-between px-6 py-3 border-b border-stone-800 shrink-0">
                <span class="text-xs font-bold text-stone-400 uppercase tracking-wider">SKILL Content — Selecciona todo y copia (Ctrl+A / Cmd+A)</span>
                <button onclick="copyToClipboard(skillContent, 'SKILL Antigravity')" class="px-4 py-1.5 rounded-full bg-reserve-olive text-reserve-forest text-xs font-bold hover:opacity-80 transition-all flex items-center gap-1.5">📋 Copiar SKILL Completo</button>
            </div>
            <div class="flex-1 overflow-hidden px-6 py-4">
                <textarea id="skill-textarea" readonly class="w-full h-full min-h-[300px] bg-stone-950 text-stone-300 font-mono text-xs p-4 rounded-xl border border-stone-700 resize-none focus:outline-none focus:ring-1 focus:ring-reserve-olive custom-scrollbar leading-relaxed" spellcheck="false"></textarea>
            </div>
        </div>
    </div>

    <!-- 🤖 Robot trigger button (bottom-right, hidden until hover) -->
    <button id="robot-trigger" onclick="openAdvanced()" title="Modo Avanzado — SKILL Antigravity" class="fixed bottom-20 right-6 z-40 w-12 h-12 rounded-full bg-stone-900/80 backdrop-blur-sm border border-stone-700 text-xl flex items-center justify-center shadow-lg transition-all duration-300 opacity-0 hover:opacity-100 focus:opacity-100 hover:scale-110 hover:bg-stone-800 cursor-pointer">
        🤖
    </button>

    <!-- 👁️ Accessibility / High Contrast Floating Button (bottom-right) -->
    <button id="btn-accessibility" onclick="toggleAccessibility()" title="Modo Legibilidad y Alto Contraste" class="fixed bottom-6 right-6 z-50 w-12 h-12 rounded-full bg-white text-stone-900 border-2 border-stone-400 shadow-xl flex items-center justify-center text-xl hover:scale-110 active:scale-95 transition-all cursor-pointer select-none">
        <span id="accessibility-icon">👁️</span>
    </button>

    </main>

    <!-- Footer -->
    <footer class="mt-12 bg-reserve-slate text-stone-300 py-10 border-t border-stone-800">
        <div class="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-6 text-sm">
            <div class="space-y-2 text-center md:text-left">
                <h4 class="font-title font-bold text-white text-base">Reserva de la Biosfera Sierra del Rincón</h4>
                <p class="text-xs text-stone-400 max-w-md">
                    Declarada el 26 de junio de 2005. Coordinada por la Dirección General de Biodiversidad y Áreas Protegidas de la Comunidad de Madrid.
                </p>
            </div>
            
            <div class="flex flex-col items-center md:items-end gap-2.5">
                <div class="flex flex-wrap items-center justify-center md:justify-end gap-2">
                    <a href="https://docs.google.com/presentation/d/1G6qysB5xTwcyReyiHJ7HnxBQECbucpSCnHlLozRybAA/edit?usp=sharing" target="_blank" rel="noopener" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded bg-stone-800 hover:bg-stone-700 text-stone-200 hover:text-white font-mono text-xs transition-colors border border-stone-700" title="Ver Presentación de Análisis Colectivo en Google Slides">
                        <span>📊</span> Análisis Colectivo (Google Slides)
                    </a>
                    <span class="px-3 py-1.5 rounded bg-stone-800 text-stone-300 font-mono text-xs select-none">
                        v1.0.0 Stable | MD-to-HTML Compiled
                    </span>
                </div>
                <p class="text-xs text-stone-400 text-center md:text-right">
                    Co-desarrollado por <a href="https://carlesgutierrez.github.io/consultoria-digital/" target="_blank" rel="noopener" class="text-stone-300 hover:text-white underline underline-offset-2 transition-colors font-semibold">Carles Gutiérrez Vallès</a> con la ayuda de Nicolas Serna (Marketing Digital).
                </p>
            </div>
        </div>
    </footer>

    <!-- Interactive JS Utilities -->
    <script>
        // Platform Instructions Raw Text (injected by compiler)
        const gemInstructions = `{contents["gem_raw_js"]}`;
        const chatgptInstructions = `{contents["chatgpt_raw_js"]}`;
        const canvaInstructions = `{contents["canva_raw_js"]}`;
        const skillContent = `{contents["skill_raw_js"]}`;

        // Populate instruction panels on load
        document.addEventListener('DOMContentLoaded', () => {{
            document.getElementById('gem-content').value = gemInstructions;
            document.getElementById('chatgpt-content').value = chatgptInstructions;
            document.getElementById('canva-content').textContent = canvaInstructions;
            document.getElementById('skill-textarea').value = skillContent;
            const charCount = document.getElementById('canva-char-count');
            charCount.textContent = `${{canvaInstructions.length}}/500 chars`;
            charCount.className = canvaInstructions.length > 500
                ? 'text-xs font-mono text-red-500 font-bold'
                : 'text-xs font-mono text-emerald-600 font-bold';
            // Load custom Canva editor presets
            populateCanvaEditorInputs();

            // Load form field presets
            const formPresets = ['gen-type', 'gen-title', 'gen-datetime', 'gen-location', 'gen-description', 'gen-link'];
            formPresets.forEach(id => {{
                const saved = localStorage.getItem('rbsr_preset_' + id);
                if (saved !== null) {{
                    const elem = document.getElementById(id);
                    if (elem) elem.value = saved;
                }}
            }});
            if (typeof toggleFormInputs === 'function') {{
                toggleFormInputs();
            }}
        }});

        // Advanced panel (robot button)
        function openAdvanced() {{
            document.getElementById('advanced-panel').classList.remove('hidden');
            document.body.style.overflow = 'hidden';
        }}
        function closeAdvanced() {{
            document.getElementById('advanced-panel').classList.add('hidden');
            document.body.style.overflow = '';
        }}
        document.addEventListener('keydown', e => {{ if (e.key === 'Escape') closeAdvanced(); }});

        // Q&A Accordion toggle
        function toggleQnA(btn) {{
            const body = btn.closest('.qna-card').querySelector('.qna-body');
            const arrow = btn.querySelector('.qna-arrow');
            body.classList.toggle('hidden');
            arrow.style.transform = body.classList.contains('hidden') ? '' : 'rotate(180deg)';
        }}

        // Q&A Live Search filter
        function filterQnA(query) {{
            const cards = document.querySelectorAll('.qna-card');
            const q = query.toLowerCase().trim();
            let visible = 0;
            cards.forEach(card => {{
                const text = (card.dataset.q + ' ' + card.innerText).toLowerCase();
                const show = !q || text.includes(q);
                card.style.display = show ? '' : 'none';
                if (show) visible++;
            }});
            document.getElementById('qna-empty').classList.toggle('hidden', visible > 0);
        }}

        // Canva templates config parsed from documentation
        const canvaTemplates = {contents["canva_links_json"]};

        // Load custom templates from localStorage or fallback to defaults
        const customTemplates = localStorage.getItem('rbsr_canva_custom_links');
        if (customTemplates) {{
            try {{
                const parsed = JSON.parse(customTemplates);
                Object.keys(parsed).forEach(k => {{
                    canvaTemplates[k] = parsed[k];
                }});
            }} catch(e) {{
                console.error("Error parsing custom links", e);
            }}
        }}

        function populateCanvaEditorInputs() {{
            Object.keys(canvaTemplates).forEach(k => {{
                const input = document.getElementById(`canva-edit-${{k}}`);
                if (input) input.value = canvaTemplates[k];
            }});
        }}

        function saveCanvaTemplates() {{
            Object.keys(canvaTemplates).forEach(k => {{
                const input = document.getElementById(`canva-edit-${{k}}`);
                if (input) {{
                    canvaTemplates[k] = input.value.trim();
                }}
            }});
            localStorage.setItem('rbsr_canva_custom_links', JSON.stringify(canvaTemplates));
            copyToClipboard('', 'Enlaces de plantillas actualizados y guardados en tu navegador.');
            // Re-generate if results are already visible
            if (!document.getElementById('gen-results').classList.contains('hidden')) {{
                generatePosts();
            }}
        }}

        function resetCanvaTemplates() {{
            localStorage.removeItem('rbsr_canva_custom_links');
            copyToClipboard('', 'Restaurando enlaces predeterminados...');
            setTimeout(() => {{
                location.reload();
            }}, 1000);
        }}

        // Season Detection
        const seasons = {{
            'primavera': {{ emoji: '🌸', text: 'Primavera', badge: 'text-pink-600 bg-pink-50' }},
            'verano': {{ emoji: '☀️', text: 'Verano', badge: 'text-amber-600 bg-amber-50' }},
            'otono': {{ emoji: '🍁', text: 'Otoño', badge: 'text-orange-600 bg-orange-50' }},
            'invierno': {{ emoji: '❄️', text: 'Invierno', badge: 'text-sky-600 bg-sky-50' }}
        }};
        
        function getSeason(date = new Date()) {{
            const month = date.getMonth();
            if (month >= 2 && month <= 4) return 'primavera';
            if (month >= 5 && month <= 8) return 'verano';
            if (month >= 9 && month <= 10) return 'otono';
            return 'invierno';
        }}
        
        const activeSeason = getSeason();
        const seasonInfo = seasons[activeSeason];
        const badgeElem = document.getElementById('current-season-badge');
        badgeElem.innerText = `${{seasonInfo.emoji}} ${{seasonInfo.text}}`;
        badgeElem.className = `font-title font-black text-sm uppercase px-3 py-1.5 rounded-full bg-white/10 text-white border border-white/20`;

        // Navigation Tabs switching & Hash Routing
        function switchTab(tabId, updateHash = true) {{
            // Hide all tabs
            const tabs = document.querySelectorAll('.tab-content');
            tabs.forEach(tab => {{
                tab.classList.remove('active');
            }});
            
            // Show selected tab
            const targetTab = document.getElementById(`tab-${{tabId}}`);
            if (!targetTab) return;
            targetTab.classList.add('active');
            
            // Reset all buttons to default state
            const btns = document.querySelectorAll('.tab-btn');
            btns.forEach(btn => {{
                btn.className = "tab-btn px-3 py-1.5 text-xs md:text-sm font-bold rounded-xl text-reserve-slate hover:bg-stone-200/70 transition-all";
            }});
            
            // Set active button
            const activeBtn = document.getElementById(`btn-${{tabId}}`);
            if (activeBtn) {{
                activeBtn.className = "tab-btn px-3 py-1.5 text-xs md:text-sm font-bold rounded-xl bg-reserve-forest text-white shadow-sm transition-all";
            }}

            if (updateHash) {{
                history.replaceState(null, null, `#${{tabId}}`);
                window.scrollTo({{ top: 280, behavior: 'smooth' }});
            }}
        }}

        // Copy Q&A direct link
        function copyQnALink(qNum) {{
            const url = window.location.origin + window.location.pathname + '#qna-' + parseInt(qNum);
            copyToClipboard(url, 'Enlace directo a la pregunta #' + qNum + ' copiado');
        }}

        // Deep linking hash handler for tabs and Q&A questions
        function handleHashChange() {{
            const hash = window.location.hash.replace('#', '').trim();
            if (!hash) return;

            // Direct link to Q&A question (e.g. #qna-5, #qna-005, #qna_5)
            if (hash.startsWith('qna-') || hash.startsWith('qna_')) {{
                switchTab('qna', false);
                const numPart = hash.replace(/qna[-_]/, '');
                const numInt = parseInt(numPart);
                const targetCard = document.getElementById(`qna-${{numInt}}`) || document.getElementById(`qna-${{numPart}}`);
                
                if (targetCard) {{
                    const body = targetCard.querySelector('.qna-body');
                    const arrow = targetCard.querySelector('.qna-arrow');
                    if (body && body.classList.contains('hidden')) {{
                        body.classList.remove('hidden');
                        if (arrow) arrow.style.transform = 'rotate(180deg)';
                    }}
                    setTimeout(() => {{
                        targetCard.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                        targetCard.classList.add('ring-2', 'ring-reserve-forest', 'shadow-md');
                        setTimeout(() => targetCard.classList.remove('ring-2', 'ring-reserve-forest', 'shadow-md'), 3000);
                    }}, 150);
                }}
                return;
            }}

            // Direct link to main tabs (e.g. #visual, #generador, #qna)
            const tabElem = document.getElementById(`tab-${{hash}}`);
            if (tabElem) {{
                switchTab(hash, false);
                setTimeout(() => {{
                    window.scrollTo({{ top: 280, behavior: 'smooth' }});
                }}, 100);
            }}
        }}

        window.addEventListener('hashchange', handleHashChange);
        window.addEventListener('DOMContentLoaded', handleHashChange);

        // Accessibility & High Contrast Toggle
        function toggleAccessibility() {{
            const isAccess = document.documentElement.classList.toggle('accessibility-mode');
            localStorage.setItem('rbsr_accessibility', isAccess ? 'true' : 'false');
            updateAccessibilityBtn(isAccess);
        }}

        function updateAccessibilityBtn(active) {{
            const icon = document.getElementById('accessibility-icon');
            const btn = document.getElementById('btn-accessibility');
            if (active) {{
                if (icon) icon.innerText = '👁️‍🗨️';
                if (btn) {{
                    btn.className = "fixed bottom-6 right-6 z-50 w-12 h-12 rounded-full bg-emerald-800 text-white border-2 border-emerald-400 shadow-2xl flex items-center justify-center text-xl hover:scale-110 active:scale-95 transition-all cursor-pointer ring-4 ring-emerald-300/50";
                    btn.title = "Desactivar Alto Contraste (Modo Normal)";
                }}
            }} else {{
                if (icon) icon.innerText = '👁️';
                if (btn) {{
                    btn.className = "fixed bottom-6 right-6 z-50 w-12 h-12 rounded-full bg-white text-stone-900 border-2 border-stone-400 shadow-xl flex items-center justify-center text-xl hover:scale-110 active:scale-95 transition-all cursor-pointer";
                    btn.title = "Activar Modo Legibilidad y Alto Contraste";
                }}
            }}
        }}

        // Initialize Accessibility mode on load
        if (localStorage.getItem('rbsr_accessibility') === 'true') {{
            document.documentElement.classList.add('accessibility-mode');
            updateAccessibilityBtn(true);
        }}

        // Toggle Form Inputs based on selected typolology
        function toggleFormInputs() {{
            const type = document.getElementById('gen-type').value;
            const linkContainer = document.getElementById('input-link-container');
            const datetimeInput = document.getElementById('gen-datetime');
            const locationInput = document.getElementById('gen-location');

            if (type === 'reverberacion') {{
                linkContainer.querySelector('label').innerText = 'Enlace a la Noticia / Productor';
                datetimeInput.placeholder = 'Opcional (Ej: Publicado esta semana)';
                locationInput.placeholder = 'Pueblo de origen (Ej: La Hiruela)';
            }} else {{
                linkContainer.querySelector('label').innerText = 'Enlace de Inscripción / Info';
                datetimeInput.placeholder = 'Ej: Sábado 18 de Julio | 10:30h';
                locationInput.placeholder = 'Ej: Horcajuelo de la Sierra';
            }}
        }}

        // Copy-to-Clipboard Utility
        function copyToClipboard(text, message = 'Texto copiado') {{
            navigator.clipboard.writeText(text).then(() => {{
                const bubble = document.createElement('div');
                bubble.innerText = `✔️ ${{message}} con éxito`;
                bubble.className = 'fixed bottom-5 right-5 bg-reserve-forest text-white px-5 py-3 rounded-xl shadow-lg border border-reserve-olive/30 text-sm font-semibold z-50 animate-bounce transition-all';
                document.body.appendChild(bubble);
                setTimeout(() => {{ bubble.remove(); }}, 3000);
            }}).catch(err => {{
                console.error('Error al copiar: ', err);
            }});
        }}

        // Dynamic Post Copy Generator Algorithm
        function generatePosts() {{
            const type = document.getElementById('gen-type').value;
            const title = document.getElementById('gen-title').value.trim() || 'Actividad Especial en la Reserva';
            const datetime = document.getElementById('gen-datetime').value.trim() || 'Fecha por confirmar';
            const location = document.getElementById('gen-location').value.trim() || 'Municipio de la Sierra';
            const description = document.getElementById('gen-description').value.trim() || 'Una propuesta para conectar con nuestro entorno y descubrir la magia del paisaje serrano en un taller guiado por personas expertas.';
            const link = document.getElementById('gen-link').value.trim() || 'www.sierradelrincon.org';
            const season = getSeason();

            // Save form presets to localStorage
            const presetMap = {{ 'gen-type': type, 'gen-title': title, 'gen-datetime': datetime, 'gen-location': location, 'gen-description': description, 'gen-link': link }};
            Object.keys(presetMap).forEach(k => localStorage.setItem('rbsr_preset_' + k, presetMap[k]));

            // Seasonal sensory details & natural botanical elements
            const seasonData = {{
                'primavera': {{
                    metaphor: 'Donde la floración despierta los prados y los arroyos cantan con la luz que regresa.',
                    adjective: 'fresco y primaveral',
                    hashtags: '#PrimaveraSerrana #ReservaRincon',
                    natureDetails: 'hojas verdes vibrantes de roble melojo (Quercus pyrenaica), flores de jara pringosa blanca (Cistus ladanifer), cantueso silvestre y gotas de agua fresca de arroyo de montaña',
                    promptStyle: 'luz matutina primaveral, detalles de floración fresca, ambiente limpio de montaña serrana, fotografía documental y texturas orgánicas'
                }},
                'verano': {{
                    metaphor: 'Sentir el frescor del refugio de las dehesas sombrías bajo los robles centenarios.',
                    adjective: 'cálido y luminoso',
                    hashtags: '#VeranoSerrano #ReservaRincon',
                    natureDetails: 'sombra de la copa de robles melojos, textura de hierba seca dorada de montaña, zarzamoras silvestres maduras y calidez sobre piedra de pizarra',
                    promptStyle: 'luz de atardecer filtrada entre las ramas del roble, brisa fresca serrana, ambiente rústico con texturas naturales ricas'
                }},
                'otono': {{
                    metaphor: 'Caminar sobre el estallido dorado y ocre de las hojas que anuncian la cosecha del año.',
                    adjective: 'dorado y otoñal',
                    hashtags: '#OtoñoSerrano #Montejo #Ocre',
                    natureDetails: 'hojas de haya doradas y cobrizas (Fagus sylvatica) del Hayedo de Montejo, bellotas caídas, musgo húmedo sobre pizarra y niebla matutina de montaña',
                    promptStyle: 'luz cálida otoñal, tonos ámbar y ocre, suavidad y profundidad de bruma matutina, atmósfera rústica cinematográfica'
                }},
                'invierno': {{
                    metaphor: 'Disfrutar de la quietud reconfortante del bosque helado y la calidez tradicional de los hogares.',
                    adjective: 'quieto y acogedor',
                    hashtags: '#InviernoSerrano #SilencioRBSR',
                    natureDetails: 'piñas con escarcha, bayas rojas de acebo (Ilex aquifolium), ramas desnudas de roble cubiertas de leve nieve y liquen húmedo sobre piedra de pizarra',
                    promptStyle: 'fondo de quietud helada invernal, texturas de arquitectura tradicional de pizarra, luz cálida de montaña'
                }}
            }}[season];

            // Define target copy texts
            let igCopy = '';
            let waCopy = '';
            let liCopy = '';
            let storyCopy = '';
            let promptText = '';
            let altText = '';
            let textPrompt = '';

            // Canva links resolution
            document.getElementById('link-canva-1-1').href = canvaTemplates['template_1_1'];
            document.getElementById('link-canva-4-5').href = canvaTemplates['template_4_5'];
            document.getElementById('link-canva-9-16').href = canvaTemplates['template_9_16'];
            document.getElementById('link-canva-16-9').href = canvaTemplates['template_16_9'];
            document.getElementById('link-canva-wa-1-1').href = canvaTemplates['template_1_1'];

            // Calculate Story length dynamics
            const descLength = description.length;
            let numSlides = 2;
            if (descLength > 150) numSlides = 3;
            if (descLength > 280) numSlides = 4;

            if (type === 'actividad') {{
                // INTERNAL ACTIVITY COPIES
                igCopy = `🌿 **${{title.toUpperCase()}}**\\n\\n${{seasonData.metaphor}}\\n\\nTe invitamos a vivir una experiencia única en pleno corazón de la Sierra del Rincón. ${{description}}\\n\\nEs un momento idóneo para detener el ritmo apresurado del día a día, respirar aire limpio de montaña y aprender de la mano de personas expertas y apasionadas que cuidan el territorio.\\n\\n📍 **Lugar:** ${{location}}\\n📅 **Fecha:** ${{datetime}}\\n👥 **Dirigido a:** Todos los públicos (plazas limitadas)\\n\\n👉 **Inscripción gratuita:** Reserva tu plaza ya en nuestra web oficial o directamente en el enlace de la bio.\\n\\n---\\n#SierraDelRincon #TurismoSostenible #CEA ${{seasonData.hashtags}}`;
                
                waCopy = `🌿 *${{title}}*\\n📅 ${{datetime}}\\n📍 ${{location}}\\n\\n${{description}}\\n\\n¡Plazas limitadas! Inscríbete gratis ya en el enlace directo 👉 ${{link}}`;
                
                liCopy = `👥 **Fomento de la Educación Ambiental: ${{title}} en la Sierra del Rincón**\\n\\nLa educación y la concienciación sobre el terreno son las herramientas más poderosas de conservación. Dentro de nuestro compromiso bajo el marco del programa Hombre y Biosfera (MaB) de la UNESCO, nos alegra anunciar el taller "${{title}}".\\n\\nEsta sesión interpretativa está diseñada para acercar de forma rigurosa y directa el modelo de sostenibilidad rural a todos los ciudadanos, fomentando dinámicas circulares y el respeto activo hacia nuestro patrimonio natural.\\n\\n📍 Ubicación: ${{location}}\\n📅 Calendario: ${{datetime}}\\n\\nIniciativas locales que tejen futuro y cohesión social en los seis municipios de la Mancomunidad. Descubre los resultados del programa en el siguiente enlace: ${{link}}\\n\\n#SierraDelRincon #DesarrolloSostenible #ProgramaMaB #UNESCO #ComunidadMadrid`;
                
                promptText = `Fotografía macro en formato vertical 9:16 capturando detalles naturales auténticos de ${{location}}, Sierra del Rincón, Madrid. Enfoque en ${{seasonData.natureDetails}}. Estilo: ${{seasonData.promptStyle}}. Composición orgánica con espacio limpio superior para superponer texto de redes sociales, alta resolución, texturas ricas de la naturaleza y luz suave sin personas ni elementos artificiales.`;
                
                altText = `Fotografía vertical en plano detalle de elementos naturales de la Sierra del Rincón en ${{location}} (${{seasonData.natureDetails.substring(0, 70)}}...), mostrando texturas orgánicas y ambiente propio de la estación para usar de fondo.`;

                // Stories Copy Dynamic Construction
                storyCopy = `📌 GUION DE STORY (${{numSlides}} Diapositivas)\\n[Usa la plantilla Story de Canva para ${{season.toUpperCase()}}]\\n\\n`;
                if (numSlides === 2) {{
                    storyCopy += `• Página 1 (Portada)\\n  Visual: Fondo vertical con elementos de naturaleza autóctona de ${{location}}.\\n  Texto principal: ¿Te apetece conectar con la Sierra? 🌿\\n  Detalles: Taller "${{title}}" en ${{location}}.\\n\\n• Página 2 (Detalle & Registro)\\n  Visual: Cuadro de texto limpio e iconos estacionales.\\n  Texto principal: 📅 ${{datetime}}\\n  Detalles: ${{description.substring(0, 120)}}...\\n  👉 ¡Reserva tu plaza gratuita! Enlace en la bio.`;
                }} else if (numSlides === 3) {{
                    storyCopy += `• Página 1 (Portada)\\n  Visual: Fondo de naturaleza serrana en vertical con logo RBSR.\\n  Texto principal: NUEVA ACTIVIDAD 🌿\\n  Detalles: ${{title}} | En ${{location}}.\\n\\n• Página 2 (Qué Viviremos)\\n  Visual: Listado limpio con la paleta de color de la estación.\\n  Texto principal: Experiencia guiada:\\n  Detalles: ${{description.substring(0, 160)}}...\\n  📅 ${{datetime}}\\n\\n• Página 3 (Llamada a la Acción)\\n  Visual: Botón y enlace destacado.\\n  Texto principal: Plazas gratuitas y limitadas. 🎒\\n  Detalles: Regístrate ya en el enlace directo de nuestra biografía.`;
                }} else {{
                    storyCopy += `• Página 1 (Portada)\\n  Visual: Tipografía Montserrat grande sobre fondo de naturaleza vertical.\\n  Texto principal: ${{title}} 🌲\\n  Detalles: Siente el latido y la calma de la Sierra del Rincón.\\n\\n• Página 2 (Inspiración y Tono)\\n  Visual: Fotografía evocativa del suelo/bosque serrano.\\n  Texto principal: "${{seasonData.metaphor}}"\\n\\n• Página 3 (Detalles de la Cita)\\n  Visual: Bloques informativos ordenados.\\n  Texto principal: 📅 ${{datetime}}\\n  Detalles: ${{location}}\\n  Info: ${{description.substring(0, 165)}}...\\n\\n• Página 4 (CTA Final)\\n  Visual: Sticker de enlace o botón en Canva.\\n  Texto principal: Plazas limitadas. 📢\\n  Detalles: No te quedes sin tu plaza. Haz clic en el enlace de la bio para reservar.`;
                }}

            }} else {{
                // EXTERNAL REVERBERATION COPIES ("Gente del Bosque")
                igCopy = `📢 **HISTORIAS DEL BOSQUE: ${{title.toUpperCase()}}**\\n\\nLa Sierra del Rincón no solo es paisaje; es la gente que la habita, la trabaja y la protege día a día. Hoy queremos compartir el admirable trabajo realizado con la iniciativa "${{title}}" en el municipio de ${{location}}.\\n\\n${{description}}\\n\\nEste tipo de proyectos locales demuestra que la innovación brota de la tradición, logrando que el patrimonio agroalimentario y cultural continúe vivo y con impacto positivo en nuestra comarca.\\n\\nNos enorgullece ser un altavoz de la sabiduría y empuje de nuestros vecinos serranos.\\n\\n👉 Conoce toda la historia de este y otros productores rurales en la sección de relatos de nuestra web o en el enlace: ${{link}}\\n\\n---\\n#GenteDelBosque #SierraDelRincon #DesarrolloRural #Cercania ${{seasonData.hashtags}}`;
                
                waCopy = `📢 *Noticias Serranas: ${{title}}*\\n📍 Municipio: ${{location}}\\n\\nEl admirable proyecto de nuestros vecinos que pone en valor la tradición y economía de cercanía en el territorio.\\n\\nConoce toda la historia completa aquí 👉 ${{link}}`;
                
                liCopy = `📢 **Desarrollo Local y Gobernanza Rural: ${{title}}**\\n\\nEn la Reserva de la Biosfera Sierra del Rincón (RBSR), entendemos la sostenibilidad como un equilibrio tripartito entre conservación ecológica, cohesión social y viabilidad económica rural. El proyecto "${{title}}", desarrollado en el municipio de ${{location}}, es un magnífico ejemplo de este modelo.\\n\\nAl dar soporte y visibilizar estas iniciativas, impulsamos la economía de proximidad, fortalecemos el tejido comunitario local y demostramos que la innovación aplicada a los oficios de raíz es el motor de desarrollo para frenar la despoblación en el norte de Madrid.\\n\\nUn caso de estudio inspirador sobre el impacto de la declaración MaB de la UNESCO.\\n\\nMás información y análisis de impacto en la red: ${{link}}\\n\\n#SierraDelRincon #DesarrolloRural #EconomiaRural #EmpoderamientoComunitario #PymeRural`;
                
                promptText = `Fotografía de fondo en formato vertical 9:16 mostrando texturas en primer plano de elementos naturales en ${{location}}, Sierra del Rincón, Madrid. Enfoque en ${{seasonData.natureDetails}}. Estilo: ${{seasonData.promptStyle}}. Luz suave, detalles orgánicos ricos de madera, piedra de pizarra y hojas, encuadre vertical óptimo como fondo de publicaciones y stories de redes sociales. Sin personas.`;
                
                altText = `Fotografía de fondo en formato vertical con texturas y detalles de la naturaleza en ${{location}} (${{seasonData.natureDetails.substring(0, 70)}}...), perfecta para acompañar la publicación de la iniciativa "${{title}}".`;

                // Stories Copy Dynamic Construction
                storyCopy = `📌 GUION DE STORY (${{numSlides}} Diapositivas)\\n[Usa la plantilla Story de Canva para ${{season.toUpperCase()}}]\\n\\n`;
                if (numSlides === 2) {{
                    storyCopy += `• Página 1 (Portada)\\n  Visual: Retrato cálido del productor artesano de la Sierra.\\n  Texto principal: HISTORIAS DEL BOSQUE 📢\\n  Detalles: Conoce el empuje de "${{title}}" en ${{location}}.\\n\\n• Página 2 (La Esencia & Enlace)\\n  Visual: Diseño minimalista con textura rústica.\\n  Texto principal: ${{description.substring(0, 120)}}...\\n  👉 Lee la historia completa en el enlace de la bio.`;
                }} else if (numSlides === 3) {{
                    storyCopy += `• Página 1 (Portada)\\n  Visual: Foto de detalle de producto o labor tradicional.\\n  Texto principal: GENTE DEL BOSQUE 📢\\n  Detalles: Iniciativa: ${{title}} | ${{location}}.\\n\\n• Página 2 (El Oficio)\\n  Visual: Bloque de texto destacado sobre fondo estacional.\\n  Texto principal: Tradición y relevo rural:\\n  Detalles: ${{description.substring(0, 160)}}...\\n\\n• Página 3 (CTA)\\n  Visual: Logotipo MaB de la UNESCO con botón de enlace.\\n  Texto principal: Valoramos el comercio local. 💚\\n  Detalles: Visita nuestra web y conoce su historia (enlace en bio).`;
                }} else {{
                    storyCopy += `• Página 1 (Portada)\\n  Visual: Retrato con luz natural y logo de la Reserva.\\n  Texto principal: Historias con Raíces: ${{title}} 📢\\n  Detalles: Tradición viva en el municipio de ${{location}}.\\n\\n• Página 2 (La Filosofía)\\n  Visual: Frase del productor en Canva con fuentes News Cycle.\\n  Texto principal: "Cuando la innovación brota de la tradición, nuestro patrimonio sigue vivo."\\n\\n• Página 3 (Impacto Local)\\n  Visual: Detalles visuales del proyecto rural.\\n  Texto principal: Proyecto de cercanía:\\n  Detalles: ${{description.substring(0, 165)}}...\\n\\n• Página 4 (CTA Final)\\n  Visual: Sticker interactivo de encuesta o enlace.\\n  Texto principal: Conoce su trayectoria. 🌿\\n  Detalles: Reportaje completo disponible en nuestra web (enlace en bio).`;
                }}
            }}

            // Generate AI Redaction Prompt with brand rules and exploratory questions
            textPrompt = `Actúa como especialista en Redacción de Contenidos y Social Media Manager para la Reserva de la Biosfera Sierra del Rincón (RBSR). Redacta contenidos adaptados que capten la esencia natural y humana del territorio.

---
REGLAS DE MARCA & TONO:
- Tono: Conectado con la naturaleza, local, riguroso, pero sumamente acogedor e inspirador.
- Palabras clave estacionales a integrar o emular: "${{seasonData.metaphor}}".
- Evita el turismo masivo (ej: No uses frases sobre "escapadas de fin de semana para huir de la gran ciudad" o que centren todo el interés solo en visitar el Hayedo masificado). Fomenta descubrir los pueblos, artesanos y el patrimonio natural del resto de los municipios de la reserva.
- Fuentes de Inspiración: Estrategias del Plan Estratégico (conservación de la biodiversidad, cohesión social, desarrollo rural sostenible y desestacionalización).

---
DATOS DEL POST:
- Tipo: ${{type === 'actividad' ? 'Taller / Actividad de Educación Ambiental' : 'Historia Local / Productor ("Gente del Bosque")'}}
- Título: ${{title}}
- Ubicación: ${{location}}
- Fecha / Hora: ${{datetime}}
- Enlace de referencia: ${{link}}
- Descripción base: ${{description}}

---
TAREA DE REDACCIÓN:
1. Redacta 3 propuestas creativas alternativas de "Copy" para un post de Instagram (una de enfoque emocional, otra de carácter informativo y otra muy directa y corta con emojis).
2. Redacta 1 copy directo y estructurado para WhatsApp.
3. Redacta 1 copy formal de gobernanza para LinkedIn, enfocado en el valor institucional del programa MaB de la UNESCO y la Mancomunidad.

---
PREGUNTAS EXPLORATORIAS:
Para afinar aún más este texto, sugiéreme 2 preguntas exploratorias al final de tu respuesta (por ejemplo, si hay algún productor/artesano local involucrado por su nombre, o si hay que recordar a la gente llevar calzado específico o transporte compartido).`;

            // Inject to HTML elements
            document.getElementById('out-ig').innerText = igCopy;
            document.getElementById('out-story').innerText = storyCopy;
            document.getElementById('out-wa').innerText = waCopy;
            document.getElementById('out-li').innerText = liCopy;
            document.getElementById('out-prompt').innerText = promptText;
            document.getElementById('out-text-prompt').innerText = textPrompt;

            // Show results container
            document.getElementById('gen-results').classList.remove('hidden');
            
            // Scroll smoothly to results
            setTimeout(() => {{
                document.getElementById('gen-results').scrollIntoView({{ behavior: 'smooth' }});
            }}, 200);
        }}
    </script>
</body>
</html>"""

    output_file = "index.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_template)
        
    print(f"[OK] Portal web compilado con exito en: '{output_file}'!")

if __name__ == "__main__":
    compile_portal()
