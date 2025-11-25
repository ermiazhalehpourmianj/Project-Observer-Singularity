"""Compare Observer–Singularity (OS) collapse predictions to baseline QM.

This script evaluates a set of predefined spatial superposition scenarios
using the OS collapse model and contrasts the predicted visibility decay
with a collapse-free quantum mechanical baseline.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Iterable, List, Sequence

from os_gravity_collapse import (
    OSParameters,
    SuperpositionConfig,
    os_collapse_rates,
    visibility_os,
    visibility_qm_no_collapse,
)


SCENARIOS: Sequence[tuple[str, float, float, float, float]] = [
    ("molecule", 1e-23, 1e-8, 1.0, 1.0),
    ("nanoparticle", 1e-17, 1e-6, 1.0, 1.0),
    ("mesoscopic", 1e-12, 1e-6, 0.1, 1.0),
    ("macroscopic", 1e-6, 1e-3, 1e-3, 1.0),
]

OUTPUT_CSV = Path("experiments/analysis/os_vs_qm_comparison.csv")


def format_sci(value: float) -> str:
    """Return a scientific-notation string, using ``inf`` for infinite values."""
    return "inf" if math.isinf(value) else f"{value:.3e}"


def compute_results(
    scenarios: Iterable[tuple[str, float, float, float, float]]
) -> List[dict[str, float | str]]:
    """Compute OS and QM visibilities for a collection of scenarios."""
    results: List[dict[str, float | str]] = []
    for name, mass_kg, separation_m, time_s, lam in scenarios:
        config = SuperpositionConfig(mass=mass_kg, separation=separation_m)
        params = OSParameters(lam=lam)
        collapse = os_collapse_rates(config, params)

        v_os = visibility_os(time_s, collapse.gamma_col)
        v_qm = visibility_qm_no_collapse(time_s)

        results.append(
            {
                "name": name,
                "mass_kg": mass_kg,
                "separation_m": separation_m,
                "time_s": time_s,
                "tau_c": collapse.tau_c,
                "V_os": v_os,
                "V_qm": v_qm,
                "delta_visibility": v_qm - v_os,
            }
        )
    return results


def print_table(results: Sequence[dict[str, float | str]]) -> None:
    """Print a formatted comparison table to stdout."""
    header = (
        "name", "mass_kg", "separation_m", "time_s", "tau_c", "V_os", "V_qm", "delta_visibility"
    )
    row_fmt = (
        "{name:<12s} {mass_kg:>12.3e} {separation_m:>12.3e} {time_s:>10.3e} "
        "{tau_c:>12s} {V_os:>10.3e} {V_qm:>10.3e} {delta_visibility:>16.3e}"
    )

    print(" ".join(f"{h:>12s}" if i else f"{h:<12s}" for i, h in enumerate(header)))
    for result in results:
        print(
            row_fmt.format(
                name=str(result["name"]),
                mass_kg=float(result["mass_kg"]),
                separation_m=float(result["separation_m"]),
                time_s=float(result["time_s"]),
                tau_c=format_sci(float(result["tau_c"])),
                V_os=float(result["V_os"]),
                V_qm=float(result["V_qm"]),
                delta_visibility=float(result["delta_visibility"]),
            )
        )


def write_csv(results: Sequence[dict[str, float | str]], output_path: Path) -> None:
    """Write scenario comparison results to a CSV file with a header row."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "name",
        "mass_kg",
        "separation_m",
        "time_s",
        "tau_c",
        "V_os",
        "V_qm",
        "delta_visibility",
    ]
    with output_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow({key: row[key] for key in fieldnames})


def main() -> None:
    """Run OS vs QM comparisons for predefined scenarios and save results."""
    results = compute_results(SCENARIOS)
    print_table(results)
    write_csv(results, OUTPUT_CSV)


if __name__ == "__main__":
    main()
