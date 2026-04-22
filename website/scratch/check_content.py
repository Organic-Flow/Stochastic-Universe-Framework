import os
import re
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = []
    def handle_data(self, d):
        self.text.append(d)
    def get_data(self):
        return ''.join(self.text)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def clean_md(text):
    text = re.sub(r'[#*_]+', '', text)
    return text

def normalize(text):
    return re.sub(r'\W+', '', text).lower()

def compare(md_path, html_path):
    print(f"Comparing {os.path.basename(md_path)} with {os.path.basename(html_path)}")
    if not os.path.exists(md_path):
        print(f"Missing {md_path}")
        return
    if not os.path.exists(html_path):
        print(f"Missing {html_path}")
        return
        
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()
    with open(html_path, 'r', encoding='utf-8') as f:
        html_text = f.read()
        
    html_plain = strip_tags(html_text)
    sim_h = normalize(html_plain)
    
    md_paras = [p.strip() for p in md_text.split('\n\n') if p.strip()]
    missing = []
    
    for p in md_paras:
        clean_p = clean_md(p)
        clean_words = clean_p.split()
        if len(clean_words) < 5:
            continue
            
        sim_p = normalize(clean_p)
        
        if sim_p not in sim_h:
            missing.append(p[:100] + "...")
            
    if missing:
        print(f"Found {len(missing)} potentially missing paragraphs:")
        for m in missing[:3]:
            print(" -", m)
    else:
        print("All main paragraphs seem to be present in the HTML.")

pairs = [
    ("stochastic_universe/theory/1_from_chaos_to_order.md", "website/pages/stochastic_ch1.html"),
    ("stochastic_universe/theory/1.1_stochasticity_and_stochastic_determinism.md", "website/pages/stochastic_ch1_1.html"),
    ("stochastic_universe/theory/1.2_stochastic_differential_equations_and_dynamical_systems.md", "website/pages/stochastic_ch1_2.html"),
    ("stochastic_universe/theory/1.3_physics_quantum_fluctuations_and_macroscopic_stability.md", "website/pages/stochastic_ch1_3.html"),
    ("stochastic_universe/theory/1.4_stochastic_equations_in_self_organization.md", "website/pages/stochastic_ch1_4.html"),
    ("stochastic_universe/theory/1.5_discussion_and_implications.md", "website/pages/stochastic_ch1_5.html")
]

for md, html in pairs:
    compare(md, html)
    print("-" * 40)
