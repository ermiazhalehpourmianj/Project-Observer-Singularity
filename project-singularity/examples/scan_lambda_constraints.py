"""Scan λ constraints against experimental visibility data."""

from __future__ import annotations

import csv
from pathlib import Path

from os_gravity_collapse import ExperimentData, find_lambda_constraint


def main() -> None:
    data_path = Path("experiments/analysis/experimental_visibility_data.csv")
    output_path = Path("experiments/analysis/lambda_constraints.csv")
    data_path.parent.mkdir(parents=True, exist_ok=True)

    if not data_path.exists():
        template_rows = [
            [
                "mock_interferometer",
                "1e-17",
                "1e-7",
                "0.1",
                "0.95",
                "0.01",
                "0.0",
            ],
            [
                "macro_device",
                "1e-9",
                "1e-5",
                "1.0",
                "0.8",
                "0.05",
                "0.0",
            ],
        ]
        with data_path.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "name",
                    "mass_kg",
                    "separation_m",
                    "t_s",
                    "visibility_observed",
                    "visibility_error",
                    "gamma_env",
                ]
            )
            writer.writerows(template_rows)
        print(f"Template created at {data_path}. Please populate it with experimental data and re-run.")
        return

    experiments: list[tuple[ExperimentData, float]] = []
    with data_path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            gamma_env = float(row.get("gamma_env", 0.0) or 0.0)
            experiment = ExperimentData(
                name=row["name"],
                mass_kg=float(row["mass_kg"]),
                separation_m=float(row["separation_m"]),
                t_s=float(row["t_s"]),
                visibility_observed=float(row["visibility_observed"]),
                visibility_error=float(row["visibility_error"]),
            )
            experiments.append((experiment, gamma_env))

    lambda_grid = [10**e for e in range(-4, 3)]

    constraints = [
        find_lambda_constraint(exp, lambda_grid, gamma_env=gamma_env)
        for exp, gamma_env in experiments
    ]

    print("Lambda constraints:")
    print(
        f"{'Name':20s} {'lambda_max_allowed':>18s} {'visibility_obs':>16s} {'visibility_err':>15s}"
    )
    for constraint, (_, gamma_env) in zip(constraints, experiments):
        exp = constraint.experiment
        max_allowed = constraint.lambda_max_allowed
        max_display = f"{max_allowed:.2e}" if max_allowed is not None else "None"
        print(
            f"{exp.name:20s} {max_display:>18s} {exp.visibility_observed:16.3f} {exp.visibility_error:15.3f}"
        )

    with output_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "name",
                "mass_kg",
                "separation_m",
                "t_s",
                "visibility_observed",
                "visibility_error",
                "gamma_env",
                "lambda_max_allowed",
            ]
        )
        for constraint, (_, gamma_env) in zip(constraints, experiments):
            exp = constraint.experiment
            writer.writerow(
                [
                    exp.name,
                    exp.mass_kg,
                    exp.separation_m,
                    exp.t_s,
                    exp.visibility_observed,
                    exp.visibility_error,
                    gamma_env,
                    constraint.lambda_max_allowed if constraint.lambda_max_allowed is not None else "",
                ]
            )
    print(f"Saved constraints to {output_path}")


if __name__ == "__main__":
    main()
