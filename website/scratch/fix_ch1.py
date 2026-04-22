import re

def process_file(md_path, html_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        md = f.read()
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Split md by sections
    sections_md = re.split(r'\n##\s+', md)
    
    # We will just manually reconstruct the HTML to be safe and perfect.
    pass

