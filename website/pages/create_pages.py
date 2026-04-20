import os

files = [
    'stochastic_ch1.html', 
    'stochastic_ch1_1.html', 
    'fractal_code.html', 
    'fractal_coherence.html', 
    'fractal_dynamic.html', 
    'fractal_geometric.html', 
    'metaqubit_code.html', 
    'metaqubit_benchmarks.html', 
    'metaqubit_network.html', 
    'metaqubit_dynamics.html'
]

template = """<article class="wp-article">
  <div class="wp-header">
    <div class="wp-eyebrow">
      <span class="wp-tag">Research Page</span>
    </div>
    <h1 class="wp-title">Placeholder Page</h1>
    <p class="wp-subtitle">This content will be populated with technical documentation soon.</p>
  </div>
  <div class="wp-divider"></div>
  <section class="wp-section">
    <div class="wp-section-label">Preview</div>
    <div class="wp-prose">
      <p>Content for this section is currently being processed from the research manuscript.</p>
    </div>
  </section>
</article>"""

base_path = r'c:\Users\nikos\OneDrive\Υπολογιστής\Stochastic-Universe-Framework\website\pages'

if not os.path.exists(base_path):
    os.makedirs(base_path)

for f in files:
    with open(os.path.join(base_path, f), 'w', encoding='utf-8') as file:
        file.write(template)

print("Created 10 placeholder files.")
