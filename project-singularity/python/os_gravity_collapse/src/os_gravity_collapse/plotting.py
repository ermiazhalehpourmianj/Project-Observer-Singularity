"""
Matplotlib-based plotting utilities for visibility vs time comparisons.

These functions will visualize OS collapse trajectories alongside baseline quantum
predictions. At this stage they are placeholders to be expanded with real plotting
logic.
"""

from typing import Iterable

import matplotlib.pyplot as plt

from .gravity_collapse import OSParameters, SuperpositionConfig, os_collapse_rates, visibility_os, visibility_qm_no_collapse


def plot_visibility_vs_time(
    config: SuperpositionConfig,
    params: OSParameters,
    t_max: float,
    n_points: int = 200,
    show_qm_baseline: bool = True,
):
    """Plot visibility vs time for OS collapse and optionally a QM baseline."""

    # TODO: replace with proper time grid and model outputs
    times: Iterable[float] = [0.0, t_max]
    collapse = os_collapse_rates(config, params)
    visibility_os_values = [visibility_os(t, collapse.gamma_col) for t in times]

    plt.figure()
    plt.plot(times, visibility_os_values, label="OS collapse (stub)")

    if show_qm_baseline:
        visibility_qm_values = [visibility_qm_no_collapse(t) for t in times]
        plt.plot(times, visibility_qm_values, label="QM baseline (stub)", linestyle="--")

    plt.xlabel("Time (s)")
    plt.ylabel("Visibility")
    plt.title("Visibility vs Time (Placeholder)")
    plt.legend()
    # TODO: customize axes, add annotations, and expose file-saving options
    plt.close()
    return plt.gcf()
