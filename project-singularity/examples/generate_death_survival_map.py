"""Generate death/survival and testability maps for the OS model."""

from __future__ import annotations

import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from os_gravity_collapse import assess_regime, assess_testability


def main() -> None:
    masses = [10**e for e in range(-24, -9)]
    separations = [10**e for e in range(-9, -3)]
    t_s = 0.1
    lam = 1.0
    gamma_env = 0.0

    output_dir = Path("experiments/analysis")
    output_dir.mkdir(parents=True, exist_ok=True)

    t_over_tau_grid = np.zeros((len(masses), len(separations)))
    testable_mask = np.zeros((len(masses), len(separations)), dtype=bool)

    rows: list[list[str | float | bool]] = []

    for i, mass in enumerate(masses):
        for j, separation in enumerate(separations):
            regime_assessment = assess_regime(
                mass_kg=mass,
                separation_m=separation,
                t_s=t_s,
                lam=lam,
                gamma_env=gamma_env,
            )
            testability = assess_testability(
                mass_kg=mass,
                separation_m=separation,
                t_s=t_s,
                lam=lam,
                gamma_env=gamma_env,
            )

            t_over_tau_grid[i, j] = regime_assessment.t_over_tau
            testable_mask[i, j] = testability.os_testable

            rows.append(
                [
                    mass,
                    separation,
                    t_s,
                    lam,
                    regime_assessment.t_over_tau,
                    regime_assessment.regime,
                    regime_assessment.strong_deviation,
                    testability.os_testable,
                ]
            )

    csv_path = output_dir / "death_survival_map_mass_separation.csv"
    with csv_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "mass_kg",
                "separation_m",
                "t_s",
                "lam",
                "t_over_tau",
                "regime",
                "strong_deviation",
                "os_testable",
            ]
        )
        writer.writerows(rows)

    log_t_over_tau = np.log10(np.maximum(t_over_tau_grid, 1e-300))

    extent = [
        math.log10(min(separations)),
        math.log10(max(separations)),
        math.log10(min(masses)),
        math.log10(max(masses)),
    ]

    plt.figure(figsize=(8, 6))
    im = plt.imshow(log_t_over_tau, origin="lower", aspect="auto", extent=extent, cmap="viridis")
    plt.colorbar(im, label="log10(t / tau_c)")
    plt.xlabel("log10(separation [m])")
    plt.ylabel("log10(mass [kg])")
    plt.title("OS death/survival map (t_over_tau)")
    plt.xticks([math.log10(s) for s in separations], [f"{s:.0e}" for s in separations], rotation=45)
    plt.yticks([math.log10(m) for m in masses], [f"{m:.0e}" for m in masses])
    death_map_path = output_dir / "death_map_mass_separation.png"
    plt.tight_layout()
    plt.savefig(death_map_path)
    plt.close()

    plt.figure(figsize=(8, 6))
    im_mask = plt.imshow(testable_mask, origin="lower", aspect="auto", extent=extent, cmap="gray_r")
    plt.colorbar(im_mask, label="OS strongly testable")
    plt.xlabel("log10(separation [m])")
    plt.ylabel("log10(mass [kg])")
    plt.title("Testable OS region")
    plt.xticks([math.log10(s) for s in separations], [f"{s:.0e}" for s in separations], rotation=45)
    plt.yticks([math.log10(m) for m in masses], [f"{m:.0e}" for m in masses])
    testable_map_path = output_dir / "testable_region_mass_separation.png"
    plt.tight_layout()
    plt.savefig(testable_map_path)
    plt.close()

    print(f"Saved map CSV to {csv_path}")
    print(f"Saved heatmap to {death_map_path}")
    print(f"Saved testable-region map to {testable_map_path}")


if __name__ == "__main__":
    main()
