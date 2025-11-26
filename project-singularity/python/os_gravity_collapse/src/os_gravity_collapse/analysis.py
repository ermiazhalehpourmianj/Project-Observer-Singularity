from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

from .gravity_collapse import (
    OSParameters,
    SuperpositionConfig,
    os_collapse_rates,
    visibility_env,
    visibility_os,
    visibility_os_plus_env,
    visibility_qm_no_collapse,
)

RegimeLabel = Literal["micro_safe", "nano_edge", "meso_collapse", "macro_classical"]


@dataclass
class RegimeAssessment:
    mass_kg: float
    separation_m: float
    t_s: float
    lam: float
    gamma_env: float | None
    tau_c_os: float
    v_os: float
    v_qm: float
    v_env: float | None
    v_os_plus_env: float | None
    t_over_tau: float
    regime: RegimeLabel
    strong_deviation: bool


def assess_regime(
    mass_kg: float,
    separation_m: float,
    t_s: float,
    lam: float = 1.0,
    gamma_env: float | None = None,
    deviation_threshold: float = 0.1,
) -> RegimeAssessment:
    """
    Use the existing OS collapse engine and environment helpers to:
    - compute τ_c_OS, V_OS(t), V_QM(t), and optionally V_env(t), V_OS+env(t)
    - compute t_over_tau = t_s / τ_c_OS
    - classify into micro_safe / nano_edge / meso_collapse / macro_classical
      based on t_over_tau and mass_kg (document thresholds)
    - set strong_deviation if |V_OS - V_QM| >= deviation_threshold
    """

    params = OSParameters(lam=lam)
    config = SuperpositionConfig(mass=mass_kg, separation=separation_m)
    collapse = os_collapse_rates(config, params)

    tau_c_os = collapse.tau_c
    v_os = visibility_os(t_s, collapse.gamma_col)
    v_qm = visibility_qm_no_collapse(t_s)

    v_env = visibility_env(t_s, gamma_env) if gamma_env is not None else None
    v_os_plus_env = (
        visibility_os_plus_env(t_s, collapse.gamma_col, gamma_env)
        if gamma_env is not None
        else None
    )

    if math.isfinite(tau_c_os) and tau_c_os > 0:
        t_over_tau = t_s / tau_c_os
    else:
        t_over_tau = 0.0

    if mass_kg >= 1e-6 or (math.isfinite(tau_c_os) and tau_c_os < 1e-9):
        regime: RegimeLabel = "macro_classical"
    elif t_over_tau < 1e-3:
        regime = "micro_safe"
    elif t_over_tau <= 1e2:
        regime = "nano_edge"
    elif t_over_tau > 1e2 and mass_kg < 1e-6:
        regime = "meso_collapse"
    else:
        regime = "macro_classical"

    strong_deviation = abs(v_os - v_qm) >= deviation_threshold

    return RegimeAssessment(
        mass_kg=mass_kg,
        separation_m=separation_m,
        t_s=t_s,
        lam=lam,
        gamma_env=gamma_env,
        tau_c_os=tau_c_os,
        v_os=v_os,
        v_qm=v_qm,
        v_env=v_env,
        v_os_plus_env=v_os_plus_env,
        t_over_tau=t_over_tau,
        regime=regime,
        strong_deviation=strong_deviation,
    )


def is_os_safely_alive(assessment: RegimeAssessment) -> bool:
    """True if OS is effectively indistinguishable from QM (micro_safe and not strong_deviation)."""

    return assessment.regime == "micro_safe" and not assessment.strong_deviation


def is_os_strongly_testable(assessment: RegimeAssessment) -> bool:
    """True if OS strongly deviates from QM in nano_edge or meso_collapse regimes."""

    return assessment.strong_deviation and assessment.regime in {"nano_edge", "meso_collapse"}


@dataclass
class TestabilityAssessment:
    mass_kg: float
    separation_m: float
    t_s: float
    lam: float
    gamma_env: float
    v_os: float
    v_qm: float
    v_env: float
    v_os_plus_env: float
    delta_os_qm: float
    env_loss: float
    os_deviation_large: bool
    env_loss_small: bool
    os_testable: bool


def assess_testability(
    mass_kg: float,
    separation_m: float,
    t_s: float,
    lam: float = 1.0,
    gamma_env: float = 0.0,
    deviation_threshold: float = 0.1,
    env_loss_max: float = 0.01,
) -> TestabilityAssessment:
    """
    Evaluate whether OS is testable against QM in the presence of environment decoherence:
    - delta_os_qm = |V_OS - V_QM|
    - env_loss = 1 - V_env
    - os_deviation_large if delta_os_qm >= deviation_threshold
    - env_loss_small if env_loss <= env_loss_max
    - os_testable = os_deviation_large and env_loss_small
    """

    params = OSParameters(lam=lam)
    config = SuperpositionConfig(mass=mass_kg, separation=separation_m)
    collapse = os_collapse_rates(config, params)

    v_os = visibility_os(t_s, collapse.gamma_col)
    v_qm = visibility_qm_no_collapse(t_s)
    v_env = visibility_env(t_s, gamma_env)
    v_os_plus_env = visibility_os_plus_env(t_s, collapse.gamma_col, gamma_env)

    delta_os_qm = abs(v_os - v_qm)
    env_loss = 1 - v_env
    os_deviation_large = delta_os_qm >= deviation_threshold
    env_loss_small = env_loss <= env_loss_max
    os_testable = os_deviation_large and env_loss_small

    return TestabilityAssessment(
        mass_kg=mass_kg,
        separation_m=separation_m,
        t_s=t_s,
        lam=lam,
        gamma_env=gamma_env,
        v_os=v_os,
        v_qm=v_qm,
        v_env=v_env,
        v_os_plus_env=v_os_plus_env,
        delta_os_qm=delta_os_qm,
        env_loss=env_loss,
        os_deviation_large=os_deviation_large,
        env_loss_small=env_loss_small,
        os_testable=os_testable,
    )


@dataclass
class ExperimentData:
    name: str
    mass_kg: float
    separation_m: float
    t_s: float
    visibility_observed: float
    visibility_error: float


@dataclass
class LambdaConstraint:
    experiment: ExperimentData
    lambda_grid: list[float]
    lambda_max_allowed: float | None


def find_lambda_constraint(
    experiment: ExperimentData,
    lambda_grid: list[float],
    gamma_env: float | None = None,
    sigma_factor: float = 2.0,
) -> LambdaConstraint:
    """
    For each λ in lambda_grid, compute V_OS(t) (and optionally V_OS+env).
    OS is 'allowed' if:
        V_OS >= visibility_observed - sigma_factor * visibility_error
    Return the largest λ that is still allowed (lambda_max_allowed),
    or None if all λ are ruled out.
    """

    allowed_max: float | None = None
    threshold = experiment.visibility_observed - sigma_factor * experiment.visibility_error

    for lam in lambda_grid:
        params = OSParameters(lam=lam)
        config = SuperpositionConfig(mass=experiment.mass_kg, separation=experiment.separation_m)
        collapse = os_collapse_rates(config, params)

        if gamma_env is None:
            visibility = visibility_os(experiment.t_s, collapse.gamma_col)
        else:
            visibility = visibility_os_plus_env(experiment.t_s, collapse.gamma_col, gamma_env)

        if visibility >= threshold:
            if allowed_max is None or lam > allowed_max:
                allowed_max = lam

    return LambdaConstraint(
        experiment=experiment,
        lambda_grid=lambda_grid,
        lambda_max_allowed=allowed_max,
    )
