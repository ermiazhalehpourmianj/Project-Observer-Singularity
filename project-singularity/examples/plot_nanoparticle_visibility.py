"""Plot a nanoparticle OS visibility curve for quick figure generation."""
from __future__ import annotations

import matplotlib.pyplot as plt

from os_gravity_collapse import OSParameters, SuperpositionConfig, os_collapse_rates
from os_gravity_collapse.plotting import plot_visibility_vs_time


def main() -> None:
    """Generate and display a visibility curve for a sample nanoparticle scenario."""

    config = SuperpositionConfig(1e-17, 1e-6)
    params = OSParameters(lam=1.0)
    collapse = os_collapse_rates(config, params)

    print(f"mass = {config.mass:.3e} kg")
    print(f"separation = {config.separation:.3e} m")
    print(f"tau_c = {collapse.tau_c:.3e} s")

    plot_visibility_vs_time(config, params, t_max=1.0)
    plt.show()


if __name__ == "__main__":
    main()
