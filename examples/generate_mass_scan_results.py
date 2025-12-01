"""Generate mass-scan collapse results for Project Singularity tables."""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable, List

from os_gravity_collapse import OSParameters, SuperpositionConfig, os_collapse_rates

OUTPUT_CSV = Path(__file__).resolve().parent.parent / "experiments/analysis/mass_scan_results.csv"

MASSES: Iterable[float] = (10**e for e in range(-24, -5))
SEPARATION_M = 1e-6
LAM = 1.0



def compute_mass_scan() -> List[dict[str, float]]:
    """Compute ΔE_G, Γ_col, and τ_c across a range of masses."""

    params = OSParameters(lam=LAM)
    results: List[dict[str, float]] = []
    for mass in MASSES:
        config = SuperpositionConfig(mass=mass, separation=SEPARATION_M)
        collapse = os_collapse_rates(config, params)
        results.append(
            {
                "mass_kg": mass,
                "separation_m": SEPARATION_M,
                "delta_E_G": collapse.delta_E_G,
                "gamma_col": collapse.gamma_col,
                "tau_c": collapse.tau_c,
            }
        )
    return results


def write_csv(rows: List[dict[str, float]], output_path: Path) -> None:
    """Write mass scan results to CSV with header."""

    fieldnames = ["mass_kg", "separation_m", "delta_E_G", "gamma_col", "tau_c"]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    """Run the mass scan and persist results for paper tables."""

    rows = compute_mass_scan()
    write_csv(rows, OUTPUT_CSV)


if __name__ == "__main__":
    main()
