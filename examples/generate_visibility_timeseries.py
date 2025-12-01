"""Generate visibility time series for representative scenarios."""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable, List, Sequence

from os_gravity_collapse import (
    OSParameters,
    SuperpositionConfig,
    os_collapse_rates,
    visibility_os,
    visibility_qm_no_collapse,
)

OUTPUT_CSV = (
    Path(__file__).resolve().parent.parent
    / "experiments/analysis/visibility_timeseries.csv"
)

SCENARIOS: Sequence[tuple[str, float, float, float]] = (
    ("nanoparticle", 1e-17, 1e-6, 1.0),
    ("mesoscopic", 1e-12, 1e-6, 0.1),
)
LAM = 1.0
N_POINTS = 200


def generate_time_grid(t_max: float, n_points: int) -> List[float]:
    """Generate a uniform time grid from 0 to t_max inclusive."""

    if n_points < 2:
        raise ValueError("n_points must be at least 2 to form a time grid.")
    step = t_max / (n_points - 1)
    return [i * step for i in range(n_points)]


def compute_timeseries(
    scenarios: Iterable[tuple[str, float, float, float]],
    lam: float,
    n_points: int,
) -> List[dict[str, float | str]]:
    """Compute OS and QM visibilities over time for each scenario."""

    params = OSParameters(lam=lam)
    rows: List[dict[str, float | str]] = []
    for name, mass_kg, separation_m, t_max in scenarios:
        config = SuperpositionConfig(mass=mass_kg, separation=separation_m)
        collapse = os_collapse_rates(config, params)
        times = generate_time_grid(t_max, n_points)
        for t in times:
            rows.append(
                {
                    "scenario_name": name,
                    "t": t,
                    "V_os": visibility_os(t, collapse.gamma_col),
                    "V_qm": visibility_qm_no_collapse(t),
                }
            )
    return rows


def write_csv(rows: List[dict[str, float | str]], output_path: Path) -> None:
    """Write visibility time-series results to CSV with header."""

    fieldnames = ["scenario_name", "t", "V_os", "V_qm"]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    """Run visibility time-series generation for predefined scenarios."""

    rows = compute_timeseries(SCENARIOS, lam=LAM, n_points=N_POINTS)
    write_csv(rows, OUTPUT_CSV)


if __name__ == "__main__":
    main()
