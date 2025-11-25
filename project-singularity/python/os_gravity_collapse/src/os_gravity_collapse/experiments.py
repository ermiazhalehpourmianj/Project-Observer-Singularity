"""
Predefined scenarios and helpers to run OS vs QM comparisons.

This module will hold convenience wrappers for defining mass/separation/time tuples,
running collapse calculations, and comparing to baseline quantum visibility.
"""

from dataclasses import dataclass

from .gravity_collapse import OSParameters, SuperpositionConfig, os_collapse_rates, visibility_os


@dataclass
class ScenarioResult:
    """Container for scenario-level outputs."""

    name: str
    config: SuperpositionConfig
    params: OSParameters
    tau_c: float
    visibility_at_t: float


def run_scenario(name: str, mass_kg: float, separation_m: float, t_s: float, lam: float = 1.0) -> ScenarioResult:
    """Run a single scenario with placeholder OS collapse calculations."""

    config = SuperpositionConfig(mass=mass_kg, separation=separation_m)
    params = OSParameters(lam=lam)
    # TODO: call os_collapse_rates and compute visibility
    collapse = os_collapse_rates(config, params)
    visibility = visibility_os(t_s, collapse.gamma_col)
    return ScenarioResult(
        name=name,
        config=config,
        params=params,
        tau_c=collapse.tau_c,
        visibility_at_t=visibility,
    )


def benchmark_scenarios() -> list[tuple[str, float, float, float]]:
    """Provide a set of reference scenarios (name, mass_kg, separation_m, t_s)."""

    # TODO: extend with realistic parameter sweeps
    return [
        ("microsphere-baseline", 1e-15, 1e-6, 1.0),
        ("mesoscopic-separated", 1e-12, 1e-5, 0.1),
    ]
