import math

import pytest

from os_gravity_collapse import (
    CollapseResult,
    OSParameters,
    SuperpositionConfig,
    benchmark_scenarios,
    delta_E_G_point_mass,
    os_collapse_rates,
    scenario_summary,
    visibility_os,
)


def test_delta_e_g_monotonicity():
    small_mass = delta_E_G_point_mass(1.0, 1.0)
    large_mass = delta_E_G_point_mass(2.0, 1.0)
    closer_sep = delta_E_G_point_mass(1.0, 0.5)
    assert large_mass > small_mass
    assert closer_sep > small_mass


def test_os_collapse_rates_positive():
    config = SuperpositionConfig(mass=1.0, separation=1.0)
    result = os_collapse_rates(config, OSParameters(lam=1.0))
    assert isinstance(result, CollapseResult)
    assert result.delta_E_G > 0
    assert result.gamma_col > 0
    assert math.isfinite(result.tau_c)


def test_visibility_behavior():
    gamma = 1.0
    assert visibility_os(0.0, gamma) == pytest.approx(1.0)
    assert visibility_os(1.0, gamma) < visibility_os(0.5, gamma)
    with pytest.raises(ValueError):
        visibility_os(-1.0, gamma)


def test_benchmark_scenarios_uniqueness():
    scenarios = benchmark_scenarios()
    assert len(scenarios) >= 3
    names = {s.name for s in scenarios}
    assert len(names) == len(scenarios)
    # Ensure scenario_summary is callable and returns a string
    assert all(isinstance(scenario_summary(s), str) for s in scenarios)
