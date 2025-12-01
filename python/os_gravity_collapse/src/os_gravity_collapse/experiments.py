"""
Predefined scenarios and helpers to run OS vs QM comparisons.

This module provides convenience wrappers for assembling common mass/separation/time
configurations, computing OS collapse rates, and reporting visibility values.
"""
from __future__ import annotations

from dataclasses import dataclass

from .gravity_collapse import (
    OSParameters,
    SuperpositionConfig,
    os_collapse_rates,
    visibility_os,
)


@dataclass
class ScenarioResult:
    """Container for scenario-level outputs."""

    name: str
    config: SuperpositionConfig
    params: OSParameters
    tau_c: float
    visibility_at_t: float


def run_scenario(
    name: str,
    mass_kg: float,
    separation_m: float,
    t_s: float,
    lam: float = 1.0,
) -> ScenarioResult:
    """Run a single scenario for the OS collapse model.

    Parameters
    ----------
    name:
        Label for the scenario.
    mass_kg:
        Mass of the object in kilograms.
    separation_m:
        Branch separation in meters.
    t_s:
        Time at which to sample the visibility.
    lam:
        OS coupling λ (dimensionless), defaults to 1.0.

    Returns
    -------
    ScenarioResult
        Summary of collapse properties and the visibility at time ``t_s``.
    """

    config = SuperpositionConfig(mass=mass_kg, separation=separation_m)
    params = OSParameters(lam=lam)
    collapse = os_collapse_rates(config, params)
    visibility = visibility_os(t_s, collapse.gamma_col)
    return ScenarioResult(
        name=name,
        config=config,
        params=params,
        tau_c=collapse.tau_c,
        visibility_at_t=visibility,
    )


def benchmark_scenarios() -> list[ScenarioResult]:
    """Return a collection of illustrative OS scenarios for quick exploration."""

    scenarios = [
        ("molecule", 1e-23, 1e-8, 1.0),
        ("nanoparticle", 1e-17, 1e-6, 1.0),
        ("mesoscopic", 1e-12, 1e-6, 0.1),
        ("macroscopic", 1e-6, 1e-3, 1e-3),
    ]
    return [run_scenario(name, mass, sep, t, lam=1.0) for name, mass, sep, t in scenarios]


def scenario_summary(result: ScenarioResult) -> str:
    """Generate a concise human-readable summary for a scenario result."""

    return (
        f"{result.name}: mass={result.config.mass:.2e} kg, "
        f"separation={result.config.separation:.2e} m, "
        f"tau_c={result.tau_c:.2e} s, visibility(t)={result.visibility_at_t:.3e}"
    )


__all__ = [
    "ScenarioResult",
    "run_scenario",
    "benchmark_scenarios",
    "scenario_summary",
]
