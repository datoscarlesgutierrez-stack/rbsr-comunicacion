import os
import re

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
        return f'<div class="{classes}"><p class="font-bold flex items-center gap-2 mb-1"><span>{icon}</span> {alert_type}</p><p class="text-sm leading-relaxed">{content}</p></div>'

    md_text = re.sub(r'>\s*\[!(IMPORTANT|WARNING|NOTE)\]\n((?:>\s*.*\n?)+)', 
                     render_alert, 
                     md_text)
    
    # Inline alerts simpler match
    md_text = re.sub(r'>\s*\[!(IMPORTANT|WARNING|NOTE)\]\s*(.*)', 
                     lambda m: f'<div class="border-l-4 border-emerald-600 bg-emerald-50/50 p-4 my-4 rounded-r-lg text-emerald-800"><p class="font-bold text-sm">🌿 {m.group(1)}</p><p class="text-sm mt-1">{m.group(2)}</p></div>', 
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
                            # Parse bold in columns
                            col_parsed = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', col)
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

    # Bold
    md_text = re.sub(r'\*\*(.*?)\*\*', r'<strong class="font-bold text-stone-900">\1</strong>', md_text)
    
    # Bullet Lists
    def render_list(match):
        items = match.group(0).strip().split('\n')
        list_html = '<ul class="list-disc pl-6 my-5 space-y-3 text-stone-800 leading-relaxed">'
        for item in items:
            cleaned = re.sub(r'^\s*[\*\-]\s*', '', item).strip()
            # Replace inline formatting
            cleaned = re.sub(r'`(.*?)`', r'<code class="px-1.5 py-0.5 bg-stone-100 rounded text-emerald-800 font-mono text-sm">\1</code>', cleaned)
            cleaned = re.sub(r'\*\*(.*?)\*\*', r'<strong class="font-bold text-stone-900">\1</strong>', cleaned)
            list_html += f'<li class="text-base">{cleaned}</li>'
        list_html += '</ul>'
        return list_html
    md_text = re.sub(r'(?:^\s*[\*\-]\s+.*\n?)+', render_list, md_text, flags=re.M)

    # Simple inline code block
    md_text = re.sub(r'`(.*?)`', r'<code class="px-1.5 py-0.5 bg-stone-100 rounded text-emerald-800 font-mono text-sm">\1</code>', md_text)

    # Checklist checkboxes (optional)
    md_text = re.sub(r'- \[ \]\s+(.*?)$', r'<label class="flex items-start gap-3 my-3 p-3 bg-stone-50 border border-stone-200 rounded-lg cursor-pointer hover:bg-stone-100/50 transition-colors"><input type="checkbox" class="w-4 h-4 mt-1 rounded border-stone-300 text-emerald-600 focus:ring-emerald-500"><span class="text-sm text-stone-700 leading-relaxed">\1</span></label>', md_text, flags=re.M)

    # Paragraphs (excluding tags already created)
    blocks = md_text.split('\n\n')
    processed_blocks = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        if block.startswith('<h') or block.startswith('<div') or block.startswith('<ul') or block.startswith('<table') or block.startswith('<block') or block.startswith('<label') or block.startswith('<thead') or block.startswith('<tbody'):
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
        "estrategia": "4_estrategia_y_planificacion.md"
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
            q_text = title_match.group(2).strip()
            # Render body (strip the heading line, parse rest as markdown)
            body_md = block[title_match.end():].strip()
            body_html = parse_markdown_to_html(body_md)
            qna_cards_html += f"""
<div class="qna-card bg-white p-6 rounded-2xl border border-stone-200 shadow-sm space-y-4" data-q="{q_text.lower()}">
    <button onclick="toggleQnA(this)" class="w-full text-left flex items-start justify-between gap-4 group">
        <div class="flex items-center gap-3">
            <span class="bg-reserve-olive/20 text-reserve-olivedark font-title font-black text-sm px-3 py-1.5 rounded-lg shrink-0">#{q_num}</span>
            <h3 class="text-base font-bold text-reserve-forest group-hover:text-reserve-olive transition-colors leading-snug">{q_text}</h3>
        </div>
        <span class="qna-arrow text-reserve-forest text-lg transition-transform shrink-0 mt-0.5">▼</span>
    </button>
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
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;900&family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <!-- TailwindCSS CDN (Premium UI development standard) -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['Outfit', 'sans-serif'],
                        title: ['Montserrat', 'sans-serif'],
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
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(226, 223, 213, 0.5);
        }}
    </style>
</head>
<body class="bg-reserve-light text-reserve-slate min-h-screen flex flex-col font-sans selection:bg-reserve-olive/30 selection:text-reserve-olivedark">

    <!-- Top Premium Brand Header -->
    <header class="glass sticky top-0 z-50 px-6 py-4 shadow-sm flex flex-col md:flex-row justify-between items-center gap-4">
        <div class="flex items-center gap-4">
            <!-- Simulated Premium Botanical Logo Representation -->
            <div class="w-12 h-12 rounded-full bg-gradient-to-tr from-reserve-forest to-reserve-olive flex items-center justify-center text-white font-title font-black text-lg shadow-md select-none">
                SR
            </div>
            <div>
                <h1 class="font-title font-black text-xl tracking-tight text-reserve-forest flex items-center gap-2">
                    Reserva de la Biosfera <span class="text-reserve-olivedark font-medium">Sierra del Rincón</span>
                </h1>
                <p class="text-xs text-stone-500 uppercase tracking-widest font-semibold flex items-center gap-1.5 mt-0.5">
                    🌿 Programa Man & Biosphere (MaB) - UNESCO
                </p>
            </div>
        </div>
        
        <!-- Navigation Menu -->
        <nav class="flex flex-wrap gap-1.5 bg-stone-100/80 p-1 rounded-full border border-stone-200">
            <button onclick="switchTab('esencia')" id="btn-esencia" class="tab-btn px-4 py-2 text-xs md:text-sm font-semibold rounded-full text-reserve-slate hover:bg-stone-200/50 transition-all active-tab bg-reserve-forest text-white shadow-sm">
                🌸 Esencia
            </button>
            <button onclick="switchTab('visual')" id="btn-visual" class="tab-btn px-4 py-2 text-xs md:text-sm font-semibold rounded-full text-reserve-slate hover:bg-stone-200/50 transition-all">
                🎨 Manual Visual
            </button>
            <button onclick="switchTab('plantillas')" id="btn-plantillas" class="tab-btn px-4 py-2 text-xs md:text-sm font-semibold rounded-full text-reserve-slate hover:bg-stone-200/50 transition-all">
                📝 Plantillas
            </button>
            <button onclick="switchTab('estrategia')" id="btn-estrategia" class="tab-btn px-4 py-2 text-xs md:text-sm font-semibold rounded-full text-reserve-slate hover:bg-stone-200/50 transition-all">
                📊 Estrategia
            </button>
            <button onclick="switchTab('generador')" id="btn-generador" class="tab-btn px-4 py-2 text-xs md:text-sm font-semibold rounded-full text-reserve-slate hover:bg-stone-200/50 transition-all bg-reserve-olive/20 text-reserve-olivedark border border-reserve-olive/40 hover:bg-reserve-olive/30 flex items-center gap-1">
                ⚙️ Generador de Post
            </button>
            <button onclick="switchTab('instrucciones')" id="btn-instrucciones" class="tab-btn px-4 py-2 text-xs md:text-sm font-semibold rounded-full text-reserve-slate hover:bg-stone-200/50 transition-all flex items-center gap-1 bg-violet-100/60 text-violet-700 border border-violet-200 hover:bg-violet-100">
                📋 Instrucciones IA
            </button>
            <button onclick="switchTab('qna')" id="btn-qna" class="tab-btn px-4 py-2 text-xs md:text-sm font-semibold rounded-full text-reserve-slate hover:bg-stone-200/50 transition-all flex items-center gap-1 bg-amber-50 text-amber-700 border border-amber-200 hover:bg-amber-100">
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
                <h2 class="text-2xl md:text-3xl font-title font-bold tracking-tight">Portal de Comunicación y Recursos RBSR</h2>
                <p class="text-stone-300 max-w-2xl text-sm leading-relaxed">
                    Esta herramienta interactiva compila las directrices oficiales del plan estratégico para facilitar la redacción y alineación estética de las actividades de la Reserva sin esfuerzo.
                </p>
            </div>
            <div class="relative z-10 bg-white/10 backdrop-blur-md border border-white/20 p-4 rounded-xl text-center flex flex-col items-center gap-1 shadow-sm">
                <span class="text-2xl">🌲</span>
                <span class="text-xs uppercase text-stone-300 font-bold tracking-widest">Estación Activa</span>
                <span id="current-season-badge" class="font-title font-black text-reserve-olive text-sm uppercase">Cargando...</span>
            </div>
        </div>

        <!-- TABS PANELS CONTENT -->
        
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
                <h3 class="text-xl font-bold text-emerald-800 border-b border-stone-100 pb-2 flex items-center gap-2">
                    <span>🎨</span> Paletas de Colores de la Reserva
                </h3>
                
                <div class="space-y-8">
                    <!-- A. Paleta Oficial -->
                    <div>
                        <h4 class="text-xs font-bold uppercase tracking-wider text-stone-500 mb-4 flex items-center gap-1.5">
                            <span class="inline-block w-2.5 h-2.5 rounded-full bg-emerald-600"></span>
                            A. Paleta Oficial de la MARCA (Posters, Infografías y Papelería)
                        </h4>
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                            <!-- Verde Brote -->
                            <div onclick="copyToClipboard('#b8be3f', 'HEX Verde Brote')" class="group cursor-pointer bg-white p-4 rounded-2xl border border-stone-200 hover:border-reserve-olive/60 shadow-sm transition-all hover:-translate-y-1">
                                <div class="w-full h-20 rounded-xl bg-[#b8be3f] shadow-inner mb-3 transition-transform group-hover:scale-98"></div>
                                <div class="flex justify-between items-center">
                                    <div>
                                        <h4 class="font-bold text-stone-800 text-sm">Verde Brote</h4>
                                        <p class="text-[10px] text-stone-500 mt-0.5">Pantone 583C</p>
                                    </div>
                                    <span class="text-xs font-mono bg-stone-100 px-2 py-1 rounded text-stone-600 font-bold">#b8be3f</span>
                                </div>
                            </div>
                            <!-- Olivo Oscuro -->
                            <div onclick="copyToClipboard('#585615', 'HEX Olivo Oscuro')" class="group cursor-pointer bg-white p-4 rounded-2xl border border-stone-200 hover:border-reserve-olive/60 shadow-sm transition-all hover:-translate-y-1">
                                <div class="w-full h-20 rounded-xl bg-[#585615] shadow-inner mb-3 transition-transform group-hover:scale-98"></div>
                                <div class="flex justify-between items-center">
                                    <div>
                                        <h4 class="font-bold text-stone-800 text-sm">Olivo Oscuro</h4>
                                        <p class="text-[10px] text-stone-500 mt-0.5">Pantone 581C</p>
                                    </div>
                                    <span class="text-xs font-mono bg-stone-100 px-2 py-1 rounded text-stone-600 font-bold">#585615</span>
                                </div>
                            </div>
                            <!-- Verde Bosque RERB -->
                            <div onclick="copyToClipboard('#4d7c67', 'HEX Verde Bosque RERB')" class="group cursor-pointer bg-white p-4 rounded-2xl border border-stone-200 hover:border-reserve-olive/60 shadow-sm transition-all hover:-translate-y-1">
                                <div class="w-full h-20 rounded-xl bg-[#4d7c67] shadow-inner mb-3 transition-transform group-hover:scale-98"></div>
                                <div class="flex justify-between items-center">
                                    <div>
                                        <h4 class="font-bold text-stone-800 text-sm">Verde Bosque RERB</h4>
                                        <p class="text-[10px] text-stone-500 mt-0.5">Pantone 624C</p>
                                    </div>
                                    <span class="text-xs font-mono bg-stone-100 px-2 py-1 rounded text-stone-600 font-bold">#4d7c67</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- B. Paletas Canva -->
                    <div>
                        <h4 class="text-xs font-bold uppercase tracking-wider text-stone-500 mb-4 flex items-center gap-1.5">
                            <span class="inline-block w-2.5 h-2.5 rounded-full bg-violet-600"></span>
                            B. Paletas de Canva (Redes Sociales, Creatividades y Plantillas)
                        </h4>
                        
                        <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
                            <!-- Paleta Genérica -->
                            <div class="bg-white p-4 rounded-2xl border border-stone-200 shadow-sm flex flex-col justify-between space-y-4">
                                <div>
                                    <h5 class="font-bold text-stone-800 text-sm flex items-center gap-1">
                                        <span>🔘</span> Paleta Genérica (Principal)
                                    </h5>
                                    <p class="text-[10px] text-stone-500 mt-1">Uso transversal y recordatorios.</p>
                                </div>
                                <div class="grid grid-cols-3 gap-2">
                                    <div onclick="copyToClipboard('#88ab81', 'HEX Verde Musgo Canva')" class="group cursor-pointer text-center">
                                        <div class="w-full h-12 rounded-lg bg-[#88ab81] shadow-inner transition-all hover:scale-105"></div>
                                        <span class="text-[9px] font-mono text-stone-600 block mt-1">#88ab81</span>
                                    </div>
                                    <div onclick="copyToClipboard('#fefaed', 'HEX Crema Hueso Canva')" class="group cursor-pointer text-center">
                                        <div class="w-full h-12 rounded-lg bg-[#fefaed] border border-stone-200 shadow-inner transition-all hover:scale-105"></div>
                                        <span class="text-[9px] font-mono text-stone-600 block mt-1">#fefaed</span>
                                    </div>
                                    <div onclick="copyToClipboard('#92b115', 'HEX Verde Brote Canva')" class="group cursor-pointer text-center">
                                        <div class="w-full h-12 rounded-lg bg-[#92b115] shadow-inner transition-all hover:scale-105"></div>
                                        <span class="text-[9px] font-mono text-stone-600 block mt-1">#92b115</span>
                                    </div>
                                </div>
                            </div>

                            <!-- Paleta Primavera -->
                            <div class="bg-white p-4 rounded-2xl border border-stone-200 shadow-sm flex flex-col justify-between space-y-4">
                                <div>
                                    <h5 class="font-bold text-stone-800 text-sm flex items-center gap-1">
                                        <span>🌸</span> Paleta de Primavera
                                    </h5>
                                    <p class="text-[10px] text-stone-500 mt-1">Floración y renacer de la sierra.</p>
                                </div>
                                <div class="grid grid-cols-4 gap-1">
                                    <div onclick="copyToClipboard('#ff8ac7', 'HEX Rosa Floración')" class="group cursor-pointer text-center">
                                        <div class="w-full h-10 rounded-lg bg-[#ff8ac7] shadow-inner transition-all hover:scale-105"></div>
                                        <span class="text-[8px] font-mono text-stone-500 block mt-1">#ff8ac7</span>
                                    </div>
                                    <div onclick="copyToClipboard('#f1efe2', 'HEX Crema Primavera')" class="group cursor-pointer text-center">
                                        <div class="w-full h-10 rounded-lg bg-[#f1efe2] border border-stone-200 shadow-inner transition-all hover:scale-105"></div>
                                        <span class="text-[8px] font-mono text-stone-500 block mt-1">#f1efe2</span>
                                    </div>
                                    <div onclick="copyToClipboard('#92b115', 'HEX Verde Brote')" class="group cursor-pointer text-center">
                                        <div class="w-full h-10 rounded-lg bg-[#92b115] shadow-inner transition-all hover:scale-105"></div>
                                        <span class="text-[8px] font-mono text-stone-500 block mt-1">#92b115</span>
                                    </div>
                                    <div onclick="copyToClipboard('#103f2b', 'HEX Verde Pino')" class="group cursor-pointer text-center">
                                        <div class="w-full h-10 rounded-lg bg-[#103f2b] shadow-inner transition-all hover:scale-105"></div>
                                        <span class="text-[8px] font-mono text-stone-500 block mt-1">#103f2b</span>
                                    </div>
                                </div>
                            </div>

                            <!-- Paleta Verano -->
                            <div class="bg-white p-4 rounded-2xl border border-stone-200 shadow-sm flex flex-col justify-between space-y-4">
                                <div>
                                    <h5 class="font-bold text-stone-800 text-sm flex items-center gap-1">
                                        <span>☀️</span> Paleta de Verano
                                    </h5>
                                    <p class="text-[10px] text-stone-500 mt-1">Sol, madurez y frescor del agua.</p>
                                </div>
                                <div class="grid grid-cols-4 gap-1">
                                    <div onclick="copyToClipboard('#65b9f0', 'HEX Azul Río')" class="group cursor-pointer text-center">
                                        <div class="w-full h-10 rounded-lg bg-[#65b9f0] shadow-inner transition-all hover:scale-105"></div>
                                        <span class="text-[8px] font-mono text-stone-500 block mt-1">#65b9f0</span>
                                    </div>
                                    <div onclick="copyToClipboard('#e7b43f', 'HEX Amarillo Sol')" class="group cursor-pointer text-center">
                                        <div class="w-full h-10 rounded-lg bg-[#e7b43f] shadow-inner transition-all hover:scale-105"></div>
                                        <span class="text-[8px] font-mono text-stone-500 block mt-1">#e7b43f</span>
                                    </div>
                                    <div onclick="copyToClipboard('#d7bf99', 'HEX Arena')" class="group cursor-pointer text-center">
                                        <div class="w-full h-10 rounded-lg bg-[#d7bf99] shadow-inner transition-all hover:scale-105"></div>
                                        <span class="text-[8px] font-mono text-stone-500 block mt-1">#d7bf99</span>
                                    </div>
                                    <div onclick="copyToClipboard('#103f2b', 'HEX Verde Pino')" class="group cursor-pointer text-center">
                                        <div class="w-full h-10 rounded-lg bg-[#103f2b] shadow-inner transition-all hover:scale-105"></div>
                                        <span class="text-[8px] font-mono text-stone-500 block mt-1">#103f2b</span>
                                    </div>
                                </div>
                            </div>

                            <!-- Paleta Invierno -->
                            <div class="bg-white p-4 rounded-2xl border border-stone-200 shadow-sm flex flex-col justify-between space-y-4">
                                <div>
                                    <h5 class="font-bold text-stone-800 text-sm flex items-center gap-1">
                                        <span>❄️</span> Paleta de Invierno
                                    </h5>
                                    <p class="text-[10px] text-stone-500 mt-1">Silencio y paisaje de nieve blanca.</p>
                                </div>
                                <div class="grid grid-cols-3 gap-2">
                                    <div onclick="copyToClipboard('#006a3e', 'HEX Verde Acebo')" class="group cursor-pointer text-center">
                                        <div class="w-full h-12 rounded-lg bg-[#006a3e] shadow-inner transition-all hover:scale-105"></div>
                                        <span class="text-[9px] font-mono text-stone-600 block mt-1">#006a3e</span>
                                    </div>
                                    <div onclick="copyToClipboard('#9eb3c5', 'HEX Gris Ventisca')" class="group cursor-pointer text-center">
                                        <div class="w-full h-12 rounded-lg bg-[#9eb3c5] shadow-inner transition-all hover:scale-105"></div>
                                        <span class="text-[9px] font-mono text-stone-600 block mt-1">#9eb3c5</span>
                                    </div>
                                    <div onclick="copyToClipboard('#ffffff', 'HEX Blanco Nieve')" class="group cursor-pointer text-center">
                                        <div class="w-full h-12 rounded-lg bg-[#ffffff] border border-stone-200 shadow-inner transition-all hover:scale-105"></div>
                                        <span class="text-[9px] font-mono text-stone-600 block mt-1">#ffffff</span>
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
                    <p class="font-bold text-sm">💡 Consejo para Técnicos</p>
                    <p class="text-xs mt-1">Haz clic en los bloques de texto o plantillas a continuación para copiarlos instantáneamente al portapapeles y editarlos directamente en tus redes o chats.</p>
                </div>

                <!-- Parse plantillas but also add inline interactive widgets to copy -->
                <div class="prose max-w-none text-stone-700">
                    {contents["plantillas"]}
                </div>
            </div>
        </div>

        <!-- Tab 4: Estrategia -->
        <div id="tab-estrategia" class="tab-content space-y-6">
            <div class="glass p-6 md:p-10 rounded-3xl shadow-sm space-y-8">
                {contents["estrategia"]}
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
                        <div class="grid grid-cols-2 gap-4">
                            <div id="input-link-container">
                                <label class="block text-xs font-bold text-stone-600 uppercase tracking-wider mb-1.5">Enlace de Inscripción / Info</label>
                                <input type="text" id="gen-link" placeholder="Ej: www.sierradelrincon.org/agenda.html" class="w-full px-4 py-2.5 rounded-lg border border-stone-300 focus:outline-none focus:ring-2 focus:ring-reserve-forest text-sm">
                            </div>
                            <div>
                                <label class="block text-xs font-bold text-stone-600 uppercase tracking-wider mb-1.5">Estación Estética</label>
                                <select id="gen-season" class="w-full px-4 py-2.5 rounded-lg border border-stone-300 focus:outline-none focus:ring-2 focus:ring-reserve-forest text-sm font-semibold">
                                    <option value="primavera">🌸 Primavera</option>
                                    <option value="verano">☀️ Verano</option>
                                    <option value="otono">🍁 Otoño</option>
                                    <option value="invierno">❄️ Invierno</option>
                                </select>
                            </div>
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
                    <div class="border-t border-stone-200 my-4"></div>
                    <h3 class="text-xl font-bold font-title text-reserve-forest mb-4">Materiales Generados</h3>

                    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                        
                        <!-- Instagram Result Card -->
                        <div class="bg-white p-5 rounded-2xl border border-stone-200 flex flex-col justify-between shadow-sm">
                            <div>
                                <div class="flex justify-between items-center mb-3">
                                    <span class="text-xs font-bold uppercase tracking-widest text-pink-600 bg-pink-50 px-2.5 py-1 rounded">📸 Instagram / FB</span>
                                    <button onclick="copyToClipboard(document.getElementById('out-ig').innerText, 'Instagram Copy')" class="text-xs font-bold text-reserve-forest hover:text-reserve-olive flex items-center gap-1">📋 Copiar</button>
                                </div>
                                <div id="out-ig" class="text-xs text-stone-700 leading-relaxed whitespace-pre-wrap select-all font-sans bg-stone-50 p-4 rounded-xl border border-stone-200/50 max-h-96 overflow-y-auto custom-scrollbar"></div>
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
                        </div>

                    </div>

                    <!-- Visual Prompt & Alt Result Card -->
                    <div class="bg-white p-6 rounded-2xl border border-stone-200 shadow-sm space-y-4">
                        <div class="flex justify-between items-center border-b border-stone-100 pb-2">
                            <h4 class="font-title font-bold text-reserve-forest text-sm flex items-center gap-1.5">🎨 Prompt de Imagen Sugerido & Accesibilidad</h4>
                            <button onclick="copyToClipboard(document.getElementById('out-prompt').innerText, 'Prompt de IA')" class="text-xs font-bold text-reserve-forest hover:text-reserve-olive flex items-center gap-1">📋 Copiar Prompt</button>
                        </div>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <p class="text-xs font-bold text-stone-500 uppercase tracking-widest mb-1">Prompt de Generación con IA (Midjourney/Gemini)</p>
                                <div id="out-prompt" class="text-xs font-mono text-stone-600 bg-stone-50 p-3 rounded-lg border border-stone-100 leading-relaxed select-all"></div>
                            </div>
                            <div>
                                <p class="text-xs font-bold text-stone-500 uppercase tracking-widest mb-1">Texto Alternativo (Accesibilidad ALT)</p>
                                <div id="out-alt" class="text-xs text-stone-700 bg-stone-50 p-3 rounded-lg border border-stone-100 leading-relaxed select-all"></div>
                            </div>
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
    <button id="robot-trigger" onclick="openAdvanced()" title="Modo Avanzado — SKILL Antigravity" class="fixed bottom-6 right-6 z-40 w-12 h-12 rounded-full bg-stone-900/80 backdrop-blur-sm border border-stone-700 text-xl flex items-center justify-center shadow-lg transition-all duration-300 opacity-0 hover:opacity-100 focus:opacity-100 hover:scale-110 hover:bg-stone-800">
        🤖
    </button>

    </main>

    <!-- Footer -->
    <footer class="mt-12 bg-reserve-slate text-stone-400 py-10 border-t border-stone-800">
        <div class="max-w-7xl mx-auto px-6 grid grid-cols-1 md:grid-cols-2 gap-8 text-sm">
            <div class="space-y-3">
                <h4 class="font-title font-bold text-white text-base">Reserva de la Biosfera Sierra del Rincón</h4>
                <p class="text-xs text-stone-500 max-w-sm">
                    Declarada el 26 de junio de 2005. Coordinada por la Dirección General de Biodiversidad y Áreas Protegidas de la Comunidad de Madrid.
                </p>
                <div class="text-xs text-stone-500">
                    Calle Iglesia nº10, Prádena del Rincón (Madrid, España) - 28191.
                </div>
            </div>
            
            <div class="flex flex-col justify-between items-start md:items-end gap-4">
                <span class="px-3 py-1.5 rounded bg-stone-800 text-stone-400 font-mono text-xs select-none">
                    v1.0.0 Stable | MD-to-HTML Compiled
                </span>
                <p class="text-xs text-stone-600 text-left md:text-right">
                    © 2026 RBSR. Todos los derechos reservados. Diseñado para técnicos locales.
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

        // Set default generator season dropdown to current season
        document.getElementById('gen-season').value = activeSeason;

        // Navigation Tabs switching
        function switchTab(tabId) {{
            // Hide all tabs
            const tabs = document.querySelectorAll('.tab-content');
            tabs.forEach(tab => {{
                tab.classList.remove('active');
            }});
            
            // Show selected tab
            const targetTab = document.getElementById(`tab-${{tabId}}`);
            targetTab.classList.add('active');
            
            // Update active button state
            const btns = document.querySelectorAll('.tab-btn');
            btns.forEach(btn => {{
                btn.className = "tab-btn px-4 py-2 text-xs md:text-sm font-semibold rounded-full text-reserve-slate hover:bg-stone-200/50 transition-all";
            }});
            
            const activeBtn = document.getElementById(`btn-${{tabId}}`);
            if (tabId === 'generador') {{
                activeBtn.className = "tab-btn px-4 py-2 text-xs md:text-sm font-semibold rounded-full bg-reserve-forest text-white shadow-sm flex items-center gap-1";
            }} else {{
                activeBtn.className = "tab-btn px-4 py-2 text-xs md:text-sm font-semibold rounded-full bg-reserve-forest text-white shadow-sm";
            }}

            // Smooth scroll to tabs
            window.scrollTo({{ top: 320, behavior: 'smooth' }});
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
                // Create temporary notification bubble
                const bubble = document.createElement('div');
                bubble.innerText = `✔️ ${{message}} con éxito`;
                bubble.className = "fixed bottom-5 right-5 bg-reserve-forest text-white px-5 py-3 rounded-xl shadow-lg border border-reserve-olive/30 text-sm font-semibold z-50 animate-bounce transition-all";
                document.body.appendChild(bubble);
                setTimeout(() => {{
                    bubble.remove();
                }}, 3000);
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
            const season = document.getElementById('gen-season').value;

            // Seasonal sensory details
            const seasonData = {{
                'primavera': {{
                    metaphor: 'Donde la floración despierta los prados y los arroyos cantan con la luz que regresa.',
                    adjective: 'fresco y primaveral',
                    hashtags: '#PrimaveraSerrana #ReservaRincon',
                    promptStyle: 'spring forest morning light, vibrant green colors, fresh blossoms, authentic spanish mountain rural vibe, cinematic high fidelity.'
                }},
                'verano': {{
                    metaphor: 'Sentir el frescor del refugio de las dehesas sombrías bajo los robles centenarios.',
                    adjective: 'cálido y luminoso',
                    hashtags: '#VeranoSerrano #ReservaRincon',
                    promptStyle: 'summer golden hour sunlight filtering through tall oak trees, slate stone houses background, mountain fresh breeze atmosphere.'
                }},
                'otono': {{
                    metaphor: 'Caminar sobre el estallido dorado y ocre de las hojas que anuncian la cosecha del año.',
                    adjective: 'dorado y otoñal',
                    hashtags: '#OtoñoSerrano #Montejo #Ocre',
                    promptStyle: 'autumn warm colors, orange and yellow beech tree canopy, misty mountain morning, cinematic soft focus portrait of spanish villager.'
                }},
                'invierno': {{
                    metaphor: 'Disfrutar de la quietud reconfortante del bosque helado y la calidez tradicional de los hogares.',
                    adjective: 'quieto y acogedor',
                    hashtags: '#InviernoSerrano #SilencioRBSR',
                    promptStyle: 'quiet winter snowy mountain backdrop, rustic stone architecture slate roof, warm orange window lights glowing, foggy woods.'
                }}
            }}[season];

            // Define target copy texts
            let igCopy = '';
            let waCopy = '';
            let liCopy = '';
            let promptText = '';
            let altText = '';

            if (type === 'actividad') {{
                // INTERNAL ACTIVITY COPIES
                igCopy = `🌿 **${{title.toUpperCase()}}**\\n\\n${{seasonData.metaphor}}\\n\\nTe invitamos a vivir una experiencia única en pleno corazón de la Sierra del Rincón. ${{description}}\\n\\nEs un momento idóneo para detener el ritmo apresurado del día a día, respirar aire limpio de montaña y aprender de la mano de personas expertas y apasionadas que cuidan el territorio.\\n\\n📍 **Lugar:** ${{location}}\\n📅 **Fecha:** ${{datetime}}\\n👥 **Dirigido a:** Todos los públicos (plazas limitadas)\\n\\n👉 **Inscripción gratuita:** Reserva tu plaza ya en nuestra web oficial o directamente en el enlace de la bio.\\n\\n---\\n#SierraDelRincon #TurismoSostenible #CEA ${{seasonData.hashtags}}`;
                
                waCopy = `🌿 *${{title}}*\\n📅 ${{datetime}}\\n📍 ${{location}}\\n\\n${{description}}\\n\\n¡Plazas limitadas! Inscríbete gratis ya en el enlace directo 👉 ${{link}}`;
                
                liCopy = `👥 **Fomento de la Educación Ambiental: ${{title}} en la Sierra del Rincón**\\n\\nLa educación y la concienciación sobre el terreno son las herramientas más poderosas de conservación. Dentro de nuestro compromiso bajo el marco del programa Hombre y Biosfera (MaB) de la UNESCO, nos alegra anunciar el taller "${{title}}".\\n\\nEsta sesión interpretativa está diseñada para acercar de forma rigurosa y directa el modelo de sostenibilidad rural a todos los ciudadanos, fomentando dinámicas circulares y el respeto activo hacia nuestro patrimonio natural.\\n\\n📍 Ubicación: ${{location}}\\n📅 Calendario: ${{datetime}}\\n\\nIniciativas locales que tejen futuro y cohesión social en los seis municipios de la Mancomunidad. Descubre los resultados del programa en el siguiente enlace: ${{link}}\\n\\n#SierraDelRincon #DesarrolloSostenible #ProgramaMaB #UNESCO #ComunidadMadrid`;
                
                promptText = `A candid, high-resolution lifestyle photograph showing participants engaged in a "${{title}}" workshop inside a rustic stone hall with slate walls in ${{location}}, Madrid. Natural ${{seasonData.promptStyle}} Shot on 35mm lens, atmospheric depth, documentary photography style, cinematic grading, natural colors. No generic actors.`;
                
                altText = `Fotografía documental de un grupo de personas de distintas edades participando activamente en el taller "${{title}}" en el municipio de ${{location}}, rodeados de elementos naturales y guiados por un formador local en una dehesa de la Sierra.`;
            }} else {{
                // EXTERNAL REVERBERATION COPIES ("Gente del Bosque")
                igCopy = `📢 **HISTORIAS DEL BOSQUE: ${{title.toUpperCase()}}**\\n\\nLa Sierra del Rincón no solo es paisaje; es la gente que la habita, la trabaja y la protege día a día. Hoy queremos compartir el admirable trabajo realizado con la iniciativa "${{title}}" en el municipio de ${{location}}.\\n\\n${{description}}\\n\\nEste tipo de proyectos locales demuestra que la innovación brota de la tradición, logrando que el patrimonio agroalimentario y cultural continúe vivo y con impacto positivo en nuestra comarca.\\n\\nNos enorgullece ser un altavoz de la sabiduría y empuje de nuestros vecinos serranos.\\n\\n👉 Conoce toda la historia de este y otros productores rurales en la sección de relatos de nuestra web o en el enlace: ${{link}}\\n\\n---\\n#GenteDelBosque #SierraDelRincon #DesarrolloRural #Cercania ${{seasonData.hashtags}}`;
                
                waCopy = `📢 *Noticias Serranas: ${{title}}*\\n📍 Municipio: ${{location}}\\n\\nEl admirable proyecto de nuestros vecinos que pone en valor la tradición y economía de cercanía en el territorio.\\n\\nConoce toda la historia completa aquí 👉 ${{link}}`;
                
                liCopy = `📢 **Desarrollo Local y Gobernanza Rural: ${{title}}**\\n\\nEn la Reserva de la Biosfera Sierra del Rincón (RBSR), entendemos la sostenibilidad como un equilibrio tripartito entre conservación ecológica, cohesión social y viabilidad económica rural. El proyecto "${{title}}", desarrollado en el municipio de ${{location}}, es un magnífico ejemplo de este modelo.\\n\\nAl dar soporte y visibilizar estas iniciativas, impulsamos la economía de proximidad, fortalecemos el tejido comunitario local y demostramos que la innovación aplicada a los oficios de raíz es el motor de desarrollo para frenar la despoblación en el norte de Madrid.\\n\\nUn caso de estudio inspirador sobre el impacto de la declaración MaB de la UNESCO.\\n\\nMás información y análisis de impacto en la red: ${{link}}\\n\\n#SierraDelRincon #DesarrolloRural #EconomiaRural #EmpoderamientoComunitario #PymeRural`;
                
                promptText = `A warm, authentic close-up portrait of a local producer representing "${{title}}" in ${{location}}, Madrid. Natural ${{seasonData.promptStyle}} Focus on authentic expressions, rich details, 85mm portrait, highly detailed skin textures, rustic organic grading.`;
                
                altText = `Retrato cercano y sumamente expresivo de un habitante artesano o productor local sonriendo en ${{location}}, que simboliza el esfuerzo comunitario detrás de la iniciativa "${{title}}".`;
            }}

            // Inject to HTML elements
            document.getElementById('out-ig').innerText = igCopy;
            document.getElementById('out-wa').innerText = waCopy;
            document.getElementById('out-li').innerText = liCopy;
            document.getElementById('out-prompt').innerText = promptText;
            document.getElementById('out-alt').innerText = altText;

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
        
    print(f"✔️ Portal web compilado con éxito en: '{output_file}'!")

if __name__ == "__main__":
    compile_portal()
