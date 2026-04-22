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
    
    text = re.sub(r'\$\\$\$', math_repl, text, flags=re.DOTALL)
    
    # Convert markdown
    html = markdown.markdown(text)
    
    # Restore math blocks
    for i, block in enumerate(math_blocks):
        placeholder = f"<p>MATHBLOCKPLACEHOLDER{i}</p>"
        replacement = f'<div class="math-block">\n{block}\n</div>'
        html = html.replace(placeholder, replacement)
        
        # Sometimes markdown doesn't wrap it in <p> if there are empty lines
        placeholder_raw = f"MATHBLOCKPLACEHOLDER{i}"
        html = html.replace(placeholder_raw, replacement)

    return html

def process_file(md_path, html_path, md_to_html_mapping=None):
    print(f"Processing {os.path.basename(md_path)} ...")
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()
    
    # Remove the very first # Title line from md_text to avoid duplicating the main title
    md_text = re.sub(r'^# .*?\n+', '', md_text)
    
    md_sections = re.split(r'\n##\s+', md_text)
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html_text = f.read()
        
    soup = BeautifulSoup(html_text, 'html.parser')
    html_sections = soup.find_all('section', class_='wp-section')
    
    if md_to_html_mapping is None:
        md_to_html_mapping = {i: [i] for i in range(len(html_sections))}
        if len(md_sections) > len(html_sections):
            # map all remaining md sections to the last html section
            md_to_html_mapping[len(html_sections)-1] = list(range(len(html_sections)-1, len(md_sections)))

    for html_idx, html_sec in enumerate(html_sections):
        # 1. Remove direct child wp-prose divs
        for child in html_sec.find_all('div', class_='wp-prose', recursive=False):
            child.decompose()
            
        # Also remove blockquotes if they are direct children (to avoid duplicating old summaries)
        for child in html_sec.find_all('blockquote', class_='wp-blockquote', recursive=False):
            child.decompose()
            
        # 2. Get corresponding md sections
        md_indices = md_to_html_mapping.get(html_idx, [])
        combined_md = ""
        for i in md_indices:
            if i < len(md_sections):
                # if it's not the first one, add the heading back (since we split by \n## )
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
