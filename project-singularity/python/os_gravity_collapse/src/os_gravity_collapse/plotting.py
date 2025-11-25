"""
Matplotlib-based plotting utilities for visibility vs time comparisons.

These functions visualize OS collapse trajectories alongside baseline quantum
predictions to support exploratory analysis and documentation figures.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .gravity_collapse import (
    OSParameters,
    SuperpositionConfig,
    os_collapse_rates,
    visibility_curve_os,
    visibility_qm_no_collapse,
)

if TYPE_CHECKING:  # pragma: no cover - import for type checking only
    from matplotlib.axes import Axes
else:  # pragma: no cover - at runtime we type alias to avoid hard dependency on import time
    Axes = Any


def plot_visibility_vs_time(
    config: SuperpositionConfig,
    params: OSParameters,
    t_max: float,
    n_points: int = 200,
    show_qm_baseline: bool = True,
) -> Axes:
    """Plot visibility vs time for OS collapse and optionally a QM baseline.

    Parameters
    ----------
    config:
        Superposition configuration describing mass and separation.
    params:
        OS collapse model parameters (λ).
    t_max:
        Maximum time (seconds) for the plotted trajectory.
    n_points:
        Number of samples in the time grid (minimum 2).
    show_qm_baseline:
        If True, overlay a flat V_QM = 1 line for comparison.

    Returns
    -------
    matplotlib.axes.Axes
        The axes containing the plotted curves.
    """

    import matplotlib.pyplot as plt

    collapse = os_collapse_rates(config, params)
    if n_points < 2:
        raise ValueError("n_points must be at least 2 to plot a time series.")
    step = t_max / (n_points - 1)
    times = [i * step for i in range(n_points)]
    visibility_os_values = visibility_curve_os(times, collapse.gamma_col)

    fig, ax = plt.subplots()
    ax.plot(times, visibility_os_values, label="OS collapse", color="tab:blue")

    if show_qm_baseline:
        ax.plot(
            times,
            [visibility_qm_no_collapse(t) for t in times],
            linestyle="--",
            label="QM baseline",
            color="tab:orange",
        )

    ax.set_xlabel("time [s]")
    ax.set_ylabel("visibility")
    ax.set_title(
        f"OS visibility: m={config.mass:.2e} kg, d={config.separation:.2e} m, λ={params.lam:.2e}"
    )
    ax.legend()
    return ax


def quick_plot_nanoparticle_demo():
    """Create a quick demo plot for a nanoparticle scenario."""

    import matplotlib.pyplot as plt

    config = SuperpositionConfig(mass=1e-17, separation=1e-6)
    params = OSParameters(lam=1.0)
    ax = plot_visibility_vs_time(config, params, t_max=1.0, n_points=200, show_qm_baseline=True)
    plt.show()
    return ax


__all__ = [
    "plot_visibility_vs_time",
    "quick_plot_nanoparticle_demo",
]
