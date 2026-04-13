#!/usr/bin/env python3
"""
Combine all theory/ chapter files into one unified markdown document.
Order: for each chapter N → main file, then N.1, N.2... then N.K (conclusion)
Output: stochastic_universe_complete.md in the repo root.
Original files are NOT modified.
"""

from pathlib import Path

THEORY_DIR = Path(__file__).parent / "theory"
OUTPUT = Path(__file__).parent / "stochastic_universe_complete.md"

TITLE = """\
# Stochastic Universe: How Randomness Creates Reality

**Author:** Nikos Demopoulos

---

"""

# Explicit ordered file list: main → chapters → conclusion, for each of 6 papers
ORDER = [
    # Chapter 1
    "1_from_chaos_to_order.md",
    "1.1_stochasticity_and_stochastic_determinism.md",
    "1.2_stochastic_differential_equations_and_dynamical_systems.md",
    "1.3_physics_quantum_fluctuations_and_macroscopic_stability.md",
    "1.4_stochastic_equations_in_self_organization.md",
    "1.5_discussion_and_implications.md",
    # Chapter 2
    "2_stochastic_determinism_physical_systems.md",
    "2.1_stochastic_processes_in_physics.md",
    "2.2_stochastic_differential_equations_in_physical_systems.md",
    "2.3_chaos_nonlinearity_and_stochastic_stability.md",
    "2.4_case_studies_in_stochastic_physics.md",
    "2.5_discussion_and_future_research.md",
    "2.6_conclusions.md",
    # Chapter 3
    "3_emergence_order_biological_systems.md",
    "3.1_stochasticity_in_evolutionary_biology.md",
    "3.2_stochasticity_in_genetic_regulation_and_development.md",
    "3.3_molecular_stochasticity_and_cellular_functions.md",
    "3.4_emergence_of_order_in_biological_networks.md",
    "3.5_discussion_and_future_research.md",
    "3.6_conclusions.md",
    # Chapter 4
    "4_randomness_structure_socio_economic_systems.md",
    "4.1_stochastic_processes_in_financial_markets.md",
    "4.2_macroeconomic_stability_and_stochastic_models.md",
    "4.3_social_networks_and_random_interactions.md",
    "4.4_economic_resilience_and_policy_making.md",
    "4.5_discussion_and_future_research.md",
    "4.6_conclusions.md",
    # Chapter 5
    "5_stochastic_paradoxical_logic.md",
    "5.1_theoretical_foundations.md",
    "5.2_mathematical_framework.md",
    "5.3_philosophical_implications.md",
    "5.4_applications_and_examples.md",
    "5.5_computational_implementation.md",
    "5.6_experimental_validation.md",
    "5.7_implications_for_scientific_method.md",
    "5.8_limitations_and_future_research.md",
    "5.9_conclusion.md",
    # Chapter 6
    "6_unified_stochastic_framework.md",
    "6.1_stochasticity_as_the_unifying_principle_in_physics_biol.md",
    "6.2_mathematical_foundations_of_stochastic_unification.md",
    "6.3_entropy_self_organization_and_stochastic_dynamics.md",
    "6.4_stochastic_networks_and_the_emergence_of_structure.md",
    "6.5_grand_unified_stochastic_equations_and_proofs.md",
    "6.6_applications_of_the_unified_stochastic_theory.md",
    "6.7_future_research_and_open_questions.md",
    "6.8_conclusions.md",
    # Chapter 7
    "7_naturalist_fractal.md",
]

sections = [TITLE]
missing = []

for filename in ORDER:
    path = THEORY_DIR / filename
    if not path.exists():
        missing.append(filename)
        continue
    content = path.read_text(encoding="utf-8").strip()
    sections.append(content)
    sections.append("\n\n---\n\n")  # separator between sections

if missing:
    print(f"WARNING: {len(missing)} file(s) not found:")
    for f in missing:
        print(f"  - {f}")

# Remove trailing separator
if sections and sections[-1] == "\n\n---\n\n":
    sections.pop()

unified = "\n\n".join(sections)
OUTPUT.write_text(unified, encoding="utf-8")

word_count = len(unified.split())
print(f"Output: {OUTPUT.name}")
print(f"Sections: {len(ORDER) - len(missing)}/{len(ORDER)}")
print(f"Approx. words: {word_count:,}")
print(f"File size: {OUTPUT.stat().st_size / 1024:.1f} KB")
