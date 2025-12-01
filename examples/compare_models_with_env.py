"""Compare OS collapse, environment decoherence, and QM baselines for sample scenarios."""
from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Iterable, List, Sequence

from os_gravity_collapse import (
    OSParameters,
    SuperpositionConfig,
    os_collapse_rates,
    visibility_env,
    visibility_os,
    visibility_os_plus_env,
    visibility_qm_no_collapse,
)

SCENARIOS: Sequence[tuple[str, float, float, float, float, float]] = [
    ("molecule_low_env", 1e-23, 1e-8, 1.0, 1.0, 1e-3),
    ("nanoparticle_mid_env", 1e-17, 1e-6, 1.0, 1.0, 1e0),
    ("mesoscopic_high_env", 1e-12, 1e-6, 0.1, 1.0, 1e3),
]

OUTPUT_CSV = (
    Path(__file__).resolve().parent.parent
    / "experiments/analysis/os_vs_env_vs_qm_comparison.csv"
)

FIELDNAMES = (
    "name",
    "mass_kg",
    "separation_m",
    "time_s",
    "lam",
    "gamma_env",
    "tau_c_os",
    "V_os",
    "V_env",
    "V_os_plus_env",
    "V_qm",
)


def format_sci(value: float) -> str:
    """Return a scientific-notation string, using ``inf`` for infinite values."""

    return "inf" if math.isinf(value) else f"{value:.3e}"


def compute_results(
    scenarios: Iterable[tuple[str, float, float, float, float, float]]
) -> List[dict[str, float | str]]:
    """Compute OS, environment, combined, and QM visibilities for scenarios."""

    results: List[dict[str, float | str]] = []
    for name, mass_kg, separation_m, time_s, lam, gamma_env in scenarios:
        config = SuperpositionConfig(mass=mass_kg, separation=separation_m)
        params = OSParameters(lam=lam)
        collapse = os_collapse_rates(config, params)

        v_os = visibility_os(time_s, collapse.gamma_col)
        v_env = visibility_env(time_s, gamma_env)
        v_os_env = visibility_os_plus_env(time_s, collapse.gamma_col, gamma_env)
        v_qm = visibility_qm_no_collapse(time_s)

        results.append(
            {
                "name": name,
                "mass_kg": mass_kg,
                "separation_m": separation_m,
                "time_s": time_s,
                "lam": lam,
                "gamma_env": gamma_env,
                "tau_c_os": collapse.tau_c,
                "V_os": v_os,
                "V_env": v_env,
                "V_os_plus_env": v_os_env,
                "V_qm": v_qm,
            }
        )
    return results


def print_table(results: Sequence[dict[str, float | str]]) -> None:
    """Print a CSV-style comparison table to stdout."""

    print(",".join(FIELDNAMES))
    for result in results:
        print(
            ",".join(
                [
                    str(result["name"]),
                    f"{float(result['mass_kg']):.6e}",
                    f"{float(result['separation_m']):.6e}",
                    f"{float(result['time_s']):.6e}",
                    f"{float(result['lam']):.6e}",
                    f"{float(result['gamma_env']):.6e}",
                    format_sci(float(result["tau_c_os"])),
                    f"{float(result['V_os']):.6e}",
                    f"{float(result['V_env']):.6e}",
                    f"{float(result['V_os_plus_env']):.6e}",
                    f"{float(result['V_qm']):.6e}",
                ]
            )
        )


def write_csv(results: Sequence[dict[str, float | str]], output_path: Path) -> None:
    """Write comparison results to a CSV file with a header row."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
        writer.writeheader()
        for row in results:
            writer.writerow({key: row[key] for key in FIELDNAMES})


def main() -> None:
    """Run OS vs environment vs QM comparisons and persist results."""

    results = compute_results(SCENARIOS)
    print_table(results)
    write_csv(results, OUTPUT_CSV)


if __name__ == "__main__":
    main()
