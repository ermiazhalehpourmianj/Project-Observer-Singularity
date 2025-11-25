"""
Toy toolkit for modeling gravity-weighted collapse (Observer–Singularity / Diósi–Penrose-style) and comparing it to standard quantum mechanics.

This package implements a minimal Observer–Singularity (OS) collapse model using a
point-mass gravitational self-energy approximation, along with helper utilities for
benchmark scenarios and plotting. It is designed to be extended with richer physics
in future iterations.
"""
from .gravity_collapse import (
    G,
    HBAR,
    OSParameters,
    SuperpositionConfig,
    CollapseResult,
    delta_E_G_point_mass,
    os_collapse_rates,
    visibility_os,
    visibility_qm_no_collapse,
    visibility_curve_os,
)
from .experiments import (
    ScenarioResult,
    run_scenario,
    benchmark_scenarios,
    scenario_summary,
)
from .plotting import plot_visibility_vs_time, quick_plot_nanoparticle_demo

__all__ = [
    "G",
    "HBAR",
    "OSParameters",
    "SuperpositionConfig",
    "CollapseResult",
    "delta_E_G_point_mass",
    "os_collapse_rates",
    "visibility_os",
    "visibility_qm_no_collapse",
    "visibility_curve_os",
    "ScenarioResult",
    "run_scenario",
    "benchmark_scenarios",
    "scenario_summary",
    "plot_visibility_vs_time",
    "quick_plot_nanoparticle_demo",
]
