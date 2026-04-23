import os
import re
import mistune

# Configuration
MD_DIR = 'stochastic_universe/theory'
HTML_DIR = 'website/pages'
TEMPLATE_FILE = 'website/pages/stochastic_ch7.html' # We use ch7 as a loose reference for structure

def pre_process_naked_code(md_content):
    lines = md_content.split('\n')
    new_lines = []
    in_naked_code = False
    
    start_keywords = ['import ', 'def ', 'class ', 'from ', 'x = ', 'plt.']
    code_keywords = ['plt.', 'np.', 'tf.', 'random.', 'plt.show', 'print(', 'plt.figure', 'plt.plot', 'plt.xlabel', 'plt.ylabel', 'plt.legend', 'plt.title', ' = ', 'np.']
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Check if line starts at index 0 (no leading space)
        starts_at_zero = not line.startswith(' ') and len(line) > 0
        
        is_start_of_code = any(stripped.startswith(kw) for kw in start_keywords)
        is_code_like = any(kw in line for kw in code_keywords)
        
        # If we see triple backticks, handle the block and skip
        if stripped.startswith('```'):
            if in_naked_code:
                new_lines.append('```')
                in_naked_code = False
            new_lines.append(line)
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                new_lines.append(lines[i])
                i += 1
            if i < len(lines):
                new_lines.append(lines[i])
                i += 1
            continue

        # Logic to START code block
        if not in_naked_code:
            if is_start_of_code or (line.startswith(' ') and is_code_like):
                new_lines.append('```python')
                in_naked_code = True
        
        # Logic to CONTINUE or EXIT code block
        if in_naked_code:
            should_close = False
            # If a line starts with a Capital and ends with a period, it's prose
            # even if it has a leading space.
            if re.match(r'^\s*[A-Z].*[\.!\?]$', line):
                # But wait, comments in Python can also look like this.
                # However, Python comments start with #. 
                # If it doesn't start with # and looks like a sentence, it's prose.
                if not stripped.startswith('#'):
                    should_close = True
            
            if starts_at_zero:
                if stripped.startswith('#') and not any(kw in stripped for kw in code_keywords):
                    should_close = True
                elif stripped.startswith('---') or stripped.startswith('##'):
                    should_close = True
                elif stripped.startswith('- ') or stripped.startswith('* '):
                    should_close = True
            
            if should_close:
                new_lines.append('```')
                in_naked_code = False
        
        new_lines.append(line)
        i += 1
        
    if in_naked_code:
        new_lines.append('```')
        
    return '\n'.join(new_lines)

def parse_md_to_wp_html(md_content, base_label):
    # Pre-process to fix the source MD's missing code blocks
    md_content = pre_process_naked_code(md_content)
    
    # Extract Title and Subtitle from H1
    h1_match = re.search(r'^# (.*?)(?:\s+—\s+(.*))?$', md_content, re.MULTILINE)
    
    if h1_match:
        full_title = h1_match.group(1).strip()
        subtitle = h1_match.group(2).strip() if h1_match.group(2) else ""
        
        # If title starts with "Chapter N:", split it
        ch_regex = re.match(r'^(Chapter\s+[\d\.]+):\s*(.*)$', full_title)
        if ch_regex:
            ch_label = ch_regex.group(1)
            title = ch_regex.group(2)
        else:
            ch_label = f"Chapter {base_label}"
            title = full_title
    else:
        ch_label = f"Chapter {base_label}"
        title = "Untitled"
        subtitle = ""

    # Remove H1 and any horizontal rules
    content = re.sub(r'^# .*?$', '', md_content, flags=re.MULTILINE)
    content = re.sub(r'^---+$', '', content, flags=re.MULTILINE)

    # Split by H2
    sections = re.split(r'^## (.*?)$', content, flags=re.MULTILINE)
    
    html_output = f"""<article class="wp-article">
  <header class="wp-header">
    <div class="wp-eyebrow">
      <span class="wp-tag">Stochastic Universe</span>
      <span class="wp-tag">{ch_label}</span>
    </div>
    <h1 class="wp-title">{title}{f"<br><em>{subtitle}</em>" if subtitle else ""}</h1>
    <p class="wp-subtitle">{subtitle if subtitle else "Exploring the foundations of stochastic determinism."}</p>
  </header>
"""

    # We use a custom renderer to preserve LaTeX backslashes
    class MathRenderer(mistune.HTMLRenderer):
        def text(self, text):
            return text # Don't escape backslashes too aggressively if possible
            
    # Custom markdown processing to handle math
    # First, protect math blocks
    math_blocks = re.findall(r'\$\$(.*?)\$\$', content, flags=re.DOTALL)
    for i, block in enumerate(math_blocks):
        content = content.replace(f"$${block}$$", f"MATHBLOCK{i}MARKER")
    
    inline_math = re.findall(r'\$([^\$]+?)\$', content)
    for i, math in enumerate(inline_math):
        content = content.replace(f"${math}$", f"INLINEMATH{i}MARKER")

    # Render Markdown
    # We use escape=False because we want to preserve LaTeX backslashes 
    # and we trust our source MD files.
    renderer = mistune.HTMLRenderer(escape=False)
    markdown = mistune.Markdown(renderer=renderer)
    
    def render_content(text):
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
        return html

    # Preamble
    preamble = sections[0].strip()
    if preamble:
        html_output += f"""
  <div class="wp-divider"></div>
  <section class="wp-section">
    <div class="wp-prose">
      {render_content(preamble)}
    </div>
  </section>
"""

    for i in range(1, len(sections), 2):
        sec_title = sections[i]
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
            sub_title = subsections[j]
            sub_content = subsections[j+1].strip()
            html_output += f"""
    <h3 class="wp-subsection-title">{sub_title}</h3>
    <div class="wp-prose">
      {render_content(sub_content)}
    </div>
"""
        html_output += "  </section>\n"

    html_output += "</article>"
    
    html_output = html_output.replace('<ul>', '<ul class="wp-list">')
    html_output = html_output.replace('<blockquote>', '<blockquote class="wp-blockquote">')

    return html_output

def main():
    files = [f for f in os.listdir(MD_DIR) if f.endswith('.md')]
    for filename in files:
        if filename == '7_naturalist_fractal.md': # Skip 7 as it is our reference
            continue
            
        md_path = os.path.join(MD_DIR, filename)
        with open(md_path, 'r') as f:
            content = f.read()
            
        # Determine output filename
        # 1_from_chaos_to_order.md -> stochastic_ch1.html
        # 1.1_stochasticity...md -> stochastic_ch1_1.html
        base = filename.split('_')[0]
        if '.' in base:
            out_name = f"stochastic_ch{base.replace('.', '_')}.html"
        else:
            out_name = f"stochastic_ch{base}.html"
            
        html_path = os.path.join(HTML_DIR, out_name)
        print(f"Generating {html_path} from {md_path}...")
        
        html_content = parse_md_to_wp_html(content, base)
        
        # Wrap in minimal layout if needed, or just the article tag as requested
        # We also need to add the link to shared.css
        final_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Stochastic Universe - {base}</title>
    <link rel="stylesheet" href="shared.css">
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body style="background: #fcf9f0; padding: 4rem 6rem;">
    {html_content}
</body>
</html>"""
        
        with open(html_path, 'w') as f:
            f.write(final_html)

if __name__ == "__main__":
    main()
