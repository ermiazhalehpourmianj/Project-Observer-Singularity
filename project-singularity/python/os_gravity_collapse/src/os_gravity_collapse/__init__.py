"""
Toy toolkit for modeling gravity-weighted collapse (Observer–Singularity / Diósi–Penrose-style) and comparing it to standard quantum mechanics.

This package currently provides stubs and placeholders for formulas, scenarios, and plotting utilities. Real physics implementations will be added in future iterations.
"""

from .gravity_collapse import (
    OSParameters,
    SuperpositionConfig,
    CollapseResult,
    delta_E_G_point_mass,
    os_collapse_rates,
    visibility_os,
    visibility_qm_no_collapse,
)
from .experiments import ScenarioResult, run_scenario, benchmark_scenarios
from .plotting import plot_visibility_vs_time

__all__ = [
    "OSParameters",
    "SuperpositionConfig",
    "CollapseResult",
    "delta_E_G_point_mass",
    "os_collapse_rates",
    "visibility_os",
    "visibility_qm_no_collapse",
    "ScenarioResult",
    "run_scenario",
    "benchmark_scenarios",
    "plot_visibility_vs_time",
]
