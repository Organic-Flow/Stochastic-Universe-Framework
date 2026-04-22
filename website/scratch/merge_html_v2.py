import os
import re
from bs4 import BeautifulSoup
import markdown

def md_to_html(text):
    # Preprocess math blocks
    math_blocks = []
    def math_repl(m):
        math_blocks.append(m.group(1))
        return f"MATHBLOCKPLACEHOLDER{len(math_blocks)-1}"
    
    text = re.sub(r'\$\$(.*?)\$\$', math_repl, text, flags=re.DOTALL)
    
    # Preprocess code blocks
    code_blocks = []
    def code_repl(m):
        code = m.group(1).replace('<', '&lt;').replace('>', '&gt;')
        code_blocks.append(code)
        return f"CODEBLOCKPLACEHOLDER{len(code_blocks)-1}"
    
    text = re.sub(r'```python\r?\n(.*?)(?:\r?\n)?```', code_repl, text, flags=re.DOTALL)
    
    # Convert markdown
    html = markdown.markdown(text)
    
    # Restore code blocks
    for i, block in enumerate(code_blocks):
        replacement = f'<pre class="wp-code-block"><code>{block}</code></pre>'
        html = html.replace(f"<p>CODEBLOCKPLACEHOLDER{i}</p>", replacement)
        html = html.replace(f"CODEBLOCKPLACEHOLDER{i}", replacement)
    
    # Restore math blocks
    for i, block in enumerate(math_blocks):
        replacement = f'<div class="math-block">\n$${block}$$\n</div>'
        html = html.replace(f"<p>MATHBLOCKPLACEHOLDER{i}</p>", replacement)
        html = html.replace(f"MATHBLOCKPLACEHOLDER{i}", replacement)

    return html

def process_file(md_path, html_path):
    print(f"Processing {os.path.basename(md_path)} ...")
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()
    
    # Remove the very first # Title line from md_text
    md_text = re.sub(r'^# .*?\n+', '', md_text)
    
    md_sections = re.split(r'\n##\s+', md_text)
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html_text = f.read()
        
    soup = BeautifulSoup(html_text, 'html.parser')
    html_sections = soup.find_all('section', class_='wp-section')
    
    # Simple mapping: HTML sections -> MD sections
    md_to_html_mapping = {i: [i] for i in range(len(html_sections))}
    if len(md_sections) > len(html_sections):
        # map all remaining md sections to the last html section
        md_to_html_mapping[len(html_sections)-1] = list(range(len(html_sections)-1, len(md_sections)))

    for html_idx, html_sec in enumerate(html_sections):
        # 1. Remove direct child wp-prose and wp-blockquote divs to keep only UI boxes
        for child in html_sec.find_all(['div', 'blockquote'], recursive=False):
            if child.get('class') and ('wp-prose' in child.get('class') or 'wp-blockquote' in child.get('class')):
                child.decompose()
                continue
            # Also remove dividers if they are direct children
            if child.get('class') and 'wp-divider' in child.get('class'):
                child.decompose()
            
        # 2. Get corresponding md sections
        md_indices = md_to_html_mapping.get(html_idx, [])
        combined_md = ""
        for i in md_indices:
            if i < len(md_sections):
                # if it's not the very first part of the document, add the heading back
                # Actually, the first part is index 0. If it's > 0, it means it originally had a ##
                if i > 0:
                    combined_md += "\n\n## " + md_sections[i]
                else:
                    combined_md += md_sections[i]
                    
        # 3. Convert to HTML
        if combined_md.strip():
            prose_html = md_to_html(combined_md)
            
            # 4. Create new elements
            divider = soup.new_tag('div', attrs={"class": "wp-divider", "style": "margin: 2.5rem 0; border-top: 1px dashed rgba(195, 200, 190, 0.5);"})
            prose_div = soup.new_tag('div', attrs={"class": "wp-prose"})
            
            # Parse the prose_html into bs4 elements and append
            prose_soup = BeautifulSoup(prose_html, 'html.parser')
            for el in prose_soup.contents:
                prose_div.append(el)
                
            html_sec.append(divider)
            html_sec.append(prose_div)
            
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Successfully updated {html_path}")

pairs = [
    ("stochastic_universe/theory/1.2_stochastic_differential_equations_and_dynamical_systems.md", "website/pages/stochastic_ch1_2.html"),
    ("stochastic_universe/theory/1.3_physics_quantum_fluctuations_and_macroscopic_stability.md", "website/pages/stochastic_ch1_3.html"),
    ("stochastic_universe/theory/1.4_stochastic_equations_in_self_organization.md", "website/pages/stochastic_ch1_4.html"),
    ("stochastic_universe/theory/1.5_discussion_and_implications.md", "website/pages/stochastic_ch1_5.html")
]

for md_path, html_path in pairs:
    process_file(md_path, html_path)
