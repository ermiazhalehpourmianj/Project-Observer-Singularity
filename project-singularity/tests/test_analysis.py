import math

from os_gravity_collapse import (
    ExperimentData,
    assess_regime,
    assess_testability,
    find_lambda_constraint,
)


def test_assess_regime_micro_safe():
    assessment = assess_regime(mass_kg=1e-24, separation_m=1e-6, t_s=1.0)
    assert assessment.regime == "micro_safe"
    assert assessment.strong_deviation is False
    assert assessment.t_over_tau < 1e-3


def test_assess_regime_meso_collapse():
    assessment = assess_regime(mass_kg=1e-12, separation_m=1e-9, t_s=1.0)
    assert assessment.regime == "meso_collapse"
    assert assessment.strong_deviation is True
    assert assessment.t_over_tau > 1e2


def test_assess_testability_os_testable():
    testability = assess_testability(
        mass_kg=1e-15,
        separation_m=1e-7,
        t_s=0.1,
        lam=1.0,
        gamma_env=0.01,
        deviation_threshold=0.1,
        env_loss_max=0.01,
    )
    assert testability.os_deviation_large is True
    assert testability.env_loss_small is True
    assert testability.os_testable is True


def test_find_lambda_constraint():
    experiment = ExperimentData(
        name="mock",
        mass_kg=1e-15,
        separation_m=1e-7,
        t_s=0.1,
        visibility_observed=0.9,
        visibility_error=0.05,
    )
    lambda_grid = [0.001, 0.01, 0.1, 1.0]
    constraint = find_lambda_constraint(experiment, lambda_grid)
    assert constraint.lambda_max_allowed is not None
    assert math.isclose(constraint.lambda_max_allowed, 0.1)
