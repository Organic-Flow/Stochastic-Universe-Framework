import os
import re
import mistune
from mistune.plugins.table import table

# Configuration
FRACTAL_DIR = 'naturalist_fractal/1_Fractal_Structural_Invariance'
METAQUBIT_DIR = 'naturalist_fractal/2_MetaQubit_Dynamic_Homeostasis'
TARGET_DIR = 'website/pages'

FRACTAL_MAPPING = {
    'energy_coherence_analysis.md': 'fractal_coherence.html',
    'First_dynamic_patterns_analysis.md': 'fractal_dynamic.html',
    'geometric_shape_analysis.md': 'fractal_geometric.html'
}

METAQUBIT_MAPPING = {
    '1_Quantum_Benchmarking/BENCHMARK_ANALYSIS.md': 'metaqubit_benchmarks.html',
    '2_Network_Self_Organization/NETWORK_ANALYSIS.md': 'metaqubit_network.html',
    '3_Internal_Dynamics/INTERNAL_DYNAMICS_ANALYSIS.md': 'metaqubit_dynamics.html'
}

def render_content(text):
    if not text: return ""
    # Protect math blocks
    math_blocks = re.findall(r'\$\$(.*?)\$\$', text, flags=re.DOTALL)
    for i, block in enumerate(math_blocks):
        text = text.replace(f"$${block}$$", f"MATHBLOCK{i}MARKER")
    
    inline_math = re.findall(r'\$([^\$]+?)\$', text)
    for i, math in enumerate(inline_math):
        text = text.replace(f"${math}$", f"INLINEMATH{i}MARKER")

    renderer = mistune.HTMLRenderer(escape=False)
    markdown = mistune.Markdown(renderer=renderer, plugins=[table])
    html = markdown(text)
    
    # Restore math
    for i, math in enumerate(inline_math):
        html = html.replace(f"INLINEMATH{i}MARKER", f"${math}$")
    for i, block in enumerate(math_blocks):
        placeholder = f"MATHBLOCK{i}MARKER"
        replacement = f'<div class="math-block">$${block}$$</div>'
        html = html.replace(placeholder, replacement)
    
    # Clean up <p> around math-block
    html = html.replace('<p><div class="math-block">', '<div class="math-block">')
    html = html.replace('</div></p>', '</div>')
    
    # Apply OrganicFlow classes
    html = html.replace('<ul>', '<ul class="wp-list">')
    html = html.replace('<ol>', '<ol class="wp-list">')
    html = html.replace('<blockquote>', '<blockquote class="wp-blockquote">')
    html = html.replace('<table>', '<table class="bench-results-table" style="width:100%; margin: 1.5rem 0;">')
    html = html.replace('<thead>', '<thead class="bench-table-header">')
    html = html.replace('<tbody>', '<tbody>')
    
    return html

def create_collapsible(lang, label, filename, content):
    return f"""
    <div class="bench-collapse" style="margin-top: 0.75rem;">
      <button class="bench-collapse-btn" onclick="toggleBenchCollapse(this)">
        <span class="bench-collapse-icon">▶</span>
        <span class="bench-collapse-lang">{lang}</span>
        <span>{filename}</span>
      </button>
      <div class="bench-collapse-body" style="display:none;">
        <pre class="bench-pre"><code>{content}</code></pre>
      </div>
    </div>"""

def generate_fractal_code_page():
    html_output = f"""<article class="wp-article">
  <header class="wp-header">
    <div class="wp-eyebrow">
      <span class="wp-tag">Naturalist Fractal</span>
      <span class="wp-tag">Structural Invariance</span>
    </div>
    <h1 class="wp-title">Code Analysis<br><em>Structural Invariance Pipeline</em></h1>
    <p class="wp-subtitle">Comprehensive overview of the algorithms used to validate fractal stability across stochastic regimes.</p>
  </header>

  <div class="wp-divider"></div>

  <section class="wp-section">
    <div class="wp-section-label">Pipeline Overview</div>
    <h2 class="wp-section-title">The Analysis Engine</h2>
    <div class="wp-prose">
      <p>The structural invariance of the Naturalist Fractal is validated through a multi-stage pipeline that processes raw experimental frames to extract geometric and information-theoretic signatures. The core logic is distributed across three main tracks:</p>
      <ul class="wp-list">
        <li><strong>Energy Coherence:</strong> Statistical and machine learning models that identify the Information Identity.</li>
        <li><strong>Dynamic Patterns:</strong> Time-series analysis of structural evolution.</li>
        <li><strong>Geometric Shape:</strong> Contour-level analysis of the X-shape invariant.</li>
      </ul>
    </div>
  </section>

  <div class="wp-divider"></div>

  <section class="wp-section">
    <div class="wp-section-label">Core Scripts</div>
    <h2 class="wp-section-title">Implementation Details</h2>
    
    <h3 class="wp-subsection-title">Data Generation — naturalist_by_frame.py</h3>
    <div class="wp-prose">
      <p>The primary experimental driver. It iterates through the stochastic factor range, applying the MetaQubit dynamic to the fractal map and rendering high-resolution frames for analysis.</p>
    </div>
    {create_collapsible("Python", "Source", "naturalist_by_frame.py", "# Placeholder for naturalist_by_frame.py")}

    <h3 class="wp-subsection-title">Visualisation — frames_view.py</h3>
    <div class="wp-prose">
      <p>Utility for generating comparative views and animations of the fractal evolution across different σ values.</p>
    </div>
    {create_collapsible("Python", "Source", "frames_view.py", "# Placeholder for frames_view.py")}
  </section>
</article>"""
    with open(os.path.join(TARGET_DIR, 'fractal_code.html'), 'w', encoding='utf-8') as f:
        f.write(html_output)

def generate_metaqubit_code_page():
    readme_path = os.path.join(METAQUBIT_DIR, 'README.md')
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple conversion for README
    html_content = render_content(content)
    
    # We'll wrap it in a slightly better structure manually to match the theme
    h1_match = re.search(r'^# (.*?)$', content, re.MULTILINE)
    title = h1_match.group(1).strip() if h1_match else "MetaQubit Homeostasis"
    
    # Remove the first H1 from content to avoid duplication
    content_no_h1 = re.sub(r'^# .*?$', '', content, flags=re.MULTILINE).strip()
    
    html_output = f"""<article class="wp-article">
  <header class="wp-header">
    <div class="wp-eyebrow">
      <span class="wp-tag">MetaQubit</span>
      <span class="wp-tag">Dynamic Homeostasis</span>
    </div>
    <h1 class="wp-title">{title}<br><em>Architectural Overview</em></h1>
    <p class="wp-subtitle">A quantum-inspired computational unit designed for noise resilience and self-stabilizing coherence.</p>
  </header>

  <div class="wp-divider"></div>

  <section class="wp-section">
    <div class="wp-prose">
      {render_content(content_no_h1)}
    </div>
  </section>
  
  <div class="wp-divider"></div>
  
  <section class="wp-section">
    <div class="wp-section-label">Implementation</div>
    <h2 class="wp-section-title">Source Code</h2>
    {create_collapsible("Python", "Core Unit", "meta_qubit.py", "# Placeholder for meta_qubit.py")}
  </section>
</article>"""
    with open(os.path.join(TARGET_DIR, 'metaqubit_code.html'), 'w', encoding='utf-8') as f:
        f.write(html_output)

def process_file(source_dir, filename, target_filename, eyebrow_tag):
    source_path = os.path.join(source_dir, filename)
    with open(source_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Extract Title and Subtitle
    h1_match = re.search(r'^# (.*?)(?:\s+—\s+(.*))?$', md_content, re.MULTILINE)
    title = h1_match.group(1).strip() if h1_match else "Analysis"
    subtitle = h1_match.group(2).strip() if h1_match and h1_match.group(2) else ""

    # Metadata extraction
    metadata_match = re.search(r'^# .*?\n\n(.*?)\n\n---', md_content, re.DOTALL | re.MULTILINE)
    metadata_html = ""
    if metadata_match:
        metadata_text = metadata_match.group(1).strip()
        metadata_html = render_content(metadata_text)

    sections = re.split(r'^## (.*?)$', md_content, flags=re.MULTILINE)
    
    html_output = f"""<article class="wp-article">
  <header class="wp-header">
    <div class="wp-eyebrow">
      <span class="wp-tag">{eyebrow_tag}</span>
      <span class="wp-tag">Analysis Report</span>
    </div>
    <h1 class="wp-title">{title}{f"<br><em>{subtitle}</em>" if subtitle else ""}</h1>
    <p class="wp-subtitle">{subtitle if subtitle else "Quantitative analysis of system dynamics."}</p>
  </header>

  <div class="wp-divider"></div>

  <section class="wp-section">
    <div class="wp-prose">
      {metadata_html}
    </div>
  </section>
"""

    for i in range(1, len(sections), 2):
        sec_title = sections[i].strip()
        sec_content = sections[i+1].strip()
        subsections = re.split(r'^### (.*?)$', sec_content, flags=re.MULTILINE)
        
        html_output += f"""
  <div class="wp-divider"></div>
  <section class="wp-section">
    <div class="wp-section-label">{sec_title}</div>
    <h2 class="wp-section-title">{sec_title}</h2>
    <div class="wp-prose">
      {render_content(subsections[0].strip()) if subsections[0].strip() else ""}
    </div>
"""
        for j in range(1, len(subsections), 2):
            sub_title = subsections[j].strip()
            sub_content = subsections[j+1].strip()
            script_name = "script.py"
            script_match = re.search(r'([a-zA-Z0-9_\.]+\.py)', sub_title)
            if script_match:
                script_name = script_match.group(1)
            json_name = script_name.replace('.py', '.json')
            
            html_output += f"""
    <h3 class="wp-subsection-title">{sub_title}</h3>
    <div class="wp-prose">
      {render_content(sub_content)}
    </div>
    
    <div class="wp-section-label" style="margin-top: 2rem;">Experiment Assets</div>
    {create_collapsible("Python", "Source Code", script_name, f"# Placeholder for {script_name}")}
    {create_collapsible("JSON", "Results", json_name, f'{{ "status": "placeholder", "file": "{json_name}" }}')}
"""
        html_output += "  </section>\n"

    html_output += "</article>"

    target_path = os.path.join(TARGET_DIR, target_filename)
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(html_output)
    print(f"Generated {target_path}")

def main():
    generate_fractal_code_page()
    generate_metaqubit_code_page()
    
    for md_file, html_file in FRACTAL_MAPPING.items():
        process_file(FRACTAL_DIR, md_file, html_file, "Naturalist Fractal")
        
    for md_file, html_file in METAQUBIT_MAPPING.items():
        process_file(METAQUBIT_DIR, md_file, html_file, "MetaQubit Homeostasis")

if __name__ == "__main__":
    main()
