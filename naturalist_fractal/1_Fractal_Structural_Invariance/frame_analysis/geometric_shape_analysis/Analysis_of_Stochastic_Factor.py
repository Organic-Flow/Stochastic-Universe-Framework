import os
import numpy as np
import matplotlib.pyplot as plt
import json

os.makedirs("csv", exist_ok=True)
os.makedirs("plot_reports", exist_ok=True)
os.makedirs("json_reports", exist_ok=True)


def analyze_stochastic_effect(curvature_results):
    # Group data by stochastic factor
    grouped_curvatures = {}
    for res in curvature_results:
        factor = res["stochastic_factor"]
        curvature = res["curvature"]
        if factor not in grouped_curvatures:
            grouped_curvatures[factor] = []
        grouped_curvatures[factor].append(curvature)

    # Compute means and variances per factor
    factor_means = []
    factor_vars = []
    factors = sorted(grouped_curvatures.keys())
    for factor in factors:
        curvatures = grouped_curvatures[factor]
        mean_curvature = np.mean(curvatures)
        var_curvature = np.var(curvatures)
        factor_means.append(mean_curvature)
        factor_vars.append(var_curvature)

    # Visualize results
    plt.figure(figsize=(10, 6))
    plt.plot(factors, factor_means, label="Mean Curvature", color="blue")
    plt.fill_between(factors,
                     np.array(factor_means) - np.array(factor_vars),
                     np.array(factor_means) + np.array(factor_vars),
                     color="blue", alpha=0.2, label="Variance")
    plt.xlabel("Stochastic Factor")
    plt.ylabel("Curvature")
    plt.title("Effect of Stochastic Factor on Curvature")
    plt.legend()
    plt.savefig("plot_reports/stochastic_factor_curvature_effect.png", dpi=150, bbox_inches="tight")
    plt.show()

    # Save to JSON
    json_report_data = {
        "name": "Stochastic Factor Effect Analysis",
        "factors": [float(f) for f in factors],
        "means": [float(m) for m in factor_means],
        "variances": [float(v) for v in factor_vars]
    }
    json_report_file = "json_reports/stochastic_factor_curvature_effect.json"
    with open(json_report_file, "w", encoding="utf-8") as f:
        json.dump(json_report_data, f, indent=2, ensure_ascii=False)
    print(f"JSON report saved to {json_report_file}")
