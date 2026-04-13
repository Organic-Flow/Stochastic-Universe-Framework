# MetaQubit Dynamic Homeostasis

This directory documents the experimental research program around the **MetaQubit** — a quantum-inspired computational unit designed for noise resilience, self-stabilizing coherence, and emergent self-organization. The research is organized into three progressive investigations: quantum benchmarking, large-scale network coordination, and internal dynamics analysis.

---

## What is the MetaQubit?

The MetaQubit is a quantum circuit unit implemented in PennyLane that goes beyond standard qubit simulation. Rather than performing exact quantum computation, it acts as a **self-stabilizing quantum processor** — maintaining coherence, resisting noise, and producing stable, information-rich outputs across a wide range of conditions.

### Architecture

The MetaQubit circuit runs four sequential stages:

```
Input parameters
      ↓
1. Superposition     — Hadamard gates applied to all qubits
      ↓
2. Entanglement      — CNOT chains connecting adjacent qubits
      ↓
3. Coherence         — RX / RY / RZ rotation gates on each qubit
      ↓
4. Quantum Tunneling — Stochastic CY gates between non-adjacent qubits
      ↓
Output: PauliZ expectation values per qubit
```

**Key properties:**
- Configurable qubit count (4 to 22+ qubits tested)
- Trainable parameters via Gradient Descent optimization
- Stochastic tunneling layer introduces controlled non-linearity
- Output is a vector of expectation values, not a probability distribution

**Source code:** [`../meta_qubit.py`](../meta_qubit.py)

### Why "Meta"?

The prefix "meta" refers to the qubit's capacity to act at a higher level than a standard qubit. Where a default qubit collapses under noise, deep circuits, or repeated operations, the MetaQubit maintains coherence through its multi-layer architecture. It doesn't compute *exactly* — it computes *robustly*, trading precision for resilience.

This makes it well-suited for:
- NISQ (Noisy Intermediate-Scale Quantum) environments
- Quantum-classical hybrid algorithms
- Large-scale network coordination with minimal quantum resources
- Situations where output stability matters more than exact fidelity

---

## Dynamic Homeostasis

The subtitle of this research program — **Dynamic Homeostasis** — captures the defining behavioral property observed across all experiments:

> The MetaQubit maintains stable, structured output in the presence of noise, depth, and perturbation — not by suppressing change, but by actively balancing competing forces within its quantum dynamics.

Homeostasis here is not static equilibrium but dynamic balance: cost functions oscillating around zero without diverging, variance increasing monotonically without exploding, and output quality persisting where standard systems collapse. The MetaQubit is a system that stabilizes through motion, not rigidity.

---

## Directory Structure

```
2_MetaQubit_Dynamic_Homeostasis/
├── README.md                          ← This file
│
├── 1_Quantum_Benchmarking/
│   ├── BENCHMARK_ANALYSIS.md          ← Comprehensive benchmark results & discoveries
│   └── tests/                         ← 13 individual experiment documents
│       ├── circuit_depth_test.md
│       ├── decoherence_resilience_capacity_stability.md
│       ├── error_tolerance_test.md
│       ├── fourier_transform.md
│       ├── gate_robustness_test.md
│       ├── phase_estimation.md
│       ├── quantum_error_correction.md
│       ├── repeated_operations_test.md
│       ├── search_space_test.md
│       ├── speed_test.md
│       ├── stability_test.md
│       ├── volume_test.md
│       └── VQE_QAOA_HHL_Benchmark.md
│
├── 2_Network_Self_Organization/
│   ├── NETWORK_ANALYSIS.md            ← Merged analysis & results document
│   ├── chaos_environment.py           ← Simulation code (100-node network, 12 MetaQubits)
│   └── images/                        ← Simulation plots organized by steps
│       ├── STEPS=300/
│       ├── STEPS=600/
│       └── STEPS=1000/
│
└── 3_Internal_Dynamics/
    ├── INTERNAL_DYNAMICS_ANALYSIS.md  ← Internal property analysis & results
    ├── HeatmapAnalysis.py             ← Coherence/entanglement/noise heatmaps
    ├── NoiseAnalysis.py               ← 3D noise impact analysis
    ├── Tunneling3DAnalysis.py         ← Tunneling/coherence/entanglement geometry
    ├── performance.py                 ← Information capacity vs. standard circuits
    ├── visualize_metaqubit.py         ← Network dynamics animation generator
    ├── analysis_plots/                ← Generated analysis plots (PNG)
    └── visualize/                     ← Animated simulations (MP4)
        ├── meta_qubit(8)_simulation.mp4
        ├── meta_qubit(14)_simulation.mp4
        ├── meta_qubit(18)_simulation.mp4
        └── meta_qubit(22)_simulation.mp4
```

---

## Research Threads

### 1 — Quantum Benchmarking

**Question:** How does MetaQubit compare to a standard quantum simulator across fundamental quantum capabilities?

**Result:** MetaQubit outperforms `default.qubit` in 12 of 13 benchmarks. Key margins:
- Circuit depth stability: 0.992 vs. 0.001 (992× better signal)
- Measurement stability: std 0.0002 vs. 1.000 (5,000× lower variance)
- QAOA MaxCut: 1.437 vs. 0.703 (2× higher)
- Implicit error correction: 39–74% recovery vs. 0%

The only metric where the standard qubit wins is raw execution speed.

**Full analysis:** [1_Quantum_Benchmarking/BENCHMARK_ANALYSIS.md](1_Quantum_Benchmarking/BENCHMARK_ANALYSIS.md)

---

### 2 — Network Self-Organization

**Question:** Can a small MetaQubit system drive meaningful self-organization in a large classical network?

**Result:** 12 MetaQubits successfully coordinate 4,950 edge weights in a 100-node network across 1,000 steps. The network develops:
- A bimodal weight distribution (sparse coding structure)
- Slowly increasing variance without explosive divergence
- Persistent cost oscillation around zero (balanced exploration)

The compression ratio — 12 qubits coordinating 4,950 edges — is approximately **412:1**.

**Full analysis:** [2_Network_Self_Organization/NETWORK_ANALYSIS.md](2_Network_Self_Organization/NETWORK_ANALYSIS.md)

---

### 3 — Internal Dynamics

**Question:** What are the internal quantum properties that explain MetaQubit's external behavior?

**Result:** Four analyses probe the MetaQubit's internals:
- Coherence, entanglement, and noise scale gracefully with MetaQubit count (heatmaps)
- Quantum properties degrade smoothly under noise, not sharply (noise analysis)
- The parameter space is geometrically structured, with correlated tunneling/coherence regions (3D analysis)
- Information capacity is 18–36 bits per evaluation vs. 0 for the standard baseline (performance analysis)

**Full analysis:** [3_Internal_Dynamics/INTERNAL_DYNAMICS_ANALYSIS.md](3_Internal_Dynamics/INTERNAL_DYNAMICS_ANALYSIS.md)

---

## Key Numbers at a Glance

| Property | Value |
|----------|-------|
| Benchmarks won | 12/13 |
| Circuit depth stability | 0.992 ± 0.042 (vs. 0.001 ± 0.229) |
| Measurement std | 0.000222 (vs. 0.999998) |
| Implicit error recovery | 39–74% (vs. 0%) |
| Network coordination ratio | 412:1 (edges per qubit) |
| Information capacity range | 18–36 bits |
| Noise degradation | Smooth (no sharp threshold) |
| QAOA advantage | 2× MaxCut score |

---

## Running the Experiments

All scripts require PennyLane and should be run from the `naturalist_fractal/` root directory:

```bash
# Internal dynamics (from naturalist_fractal/)
PYTHONPATH=. python 2_MetaQubit_Dynamic_Homeostasis/3_Internal_Dynamics/HeatmapAnalysis.py
PYTHONPATH=. python 2_MetaQubit_Dynamic_Homeostasis/3_Internal_Dynamics/NoiseAnalysis.py
PYTHONPATH=. python 2_MetaQubit_Dynamic_Homeostasis/3_Internal_Dynamics/Tunneling3DAnalysis.py
PYTHONPATH=. python 2_MetaQubit_Dynamic_Homeostasis/3_Internal_Dynamics/performance.py

# Network simulation (from naturalist_fractal/)
PYTHONPATH=. python 2_MetaQubit_Dynamic_Homeostasis/2_Network_Self_Organization/chaos_environment.py
```

Generated plots are saved to `3_Internal_Dynamics/analysis_plots/`.
