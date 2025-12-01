"""
Lightweight analysis helpers for classifying OS regimes and experiment testability.

This module builds on the core gravity-collapse formulas to provide a few
convenience data classes and predicates for reasoning about the quantum-like,
transitional, or collapse-dominated character of a configuration, along with
basic visibility-based testability checks.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from .gravity_collapse import (
    HBAR,
    OSParameters,
    SuperpositionConfig,
    os_collapse_rates,
    visibility_env,
    visibility_os,
    visibility_os_plus_env,
    visibility_qm_no_collapse,
)


@dataclass
class RegimeAssessment:
    """Summary of where a configuration sits relative to collapse dynamics.

    Attributes
    ----------
    t_over_tau:
        Dimensionless ratio of experiment time to the OS collapse time.
    regime:
        Text label for the identified regime ("qm-dominated", "intermediate",
        or "collapse-dominated").
    visibility_qm:
        Ideal quantum-mechanical visibility (no collapse, no decoherence).
    visibility_os:
        Visibility predicted by the bare OS collapse channel.
    visibility_env:
        Visibility predicted by environment-only decoherence.
    visibility_os_plus_env:
        Visibility predicted by combined OS + environment processes.
    deviates_from_qm:
        Whether the combined model differs from the QM baseline by at least the
        configured deviation fraction.
    deviates_from_env:
        Whether the combined model differs from the environment-only model by at
        least the configured deviation fraction.
    """

    t_over_tau: float
    regime: str
    visibility_qm: float
    visibility_os: float
    visibility_env: float
    visibility_os_plus_env: float
    deviates_from_qm: bool
    deviates_from_env: bool


@dataclass
class ExperimentData:
    """Container describing a single experimental probe of OS collapse."""

    config: SuperpositionConfig
    t_s: float
    gamma_env: float = 0.0
    params: OSParameters = field(default_factory=OSParameters)


@dataclass
class TestabilityAssessment:
    """Flags summarizing whether an experiment can probe OS collapse."""

    experiment: ExperimentData
    regime: RegimeAssessment
    os_safely_alive: bool
    os_strongly_testable: bool
    os_deviation_detectable: bool


@dataclass
class LambdaConstraint:
    """Constraint on the OS coupling λ based on a target visibility level."""

    lam_limit: float
    gamma_col_limit: float
    visibility_at_limit: float
    is_excluded: bool


def assess_regime(
    experiment: ExperimentData,
    *,
    quiet_threshold: float = 0.1,
    collapse_threshold: float = 10.0,
    deviation_fraction: float = 0.01,
) -> RegimeAssessment:
    """Classify the OS regime for a given experiment configuration.

    The classification is based on the ratio ``t/τ_c`` (experiment time relative
    to the predicted collapse time). A small ratio implies the OS effect is
    effectively dormant (``"qm-dominated"``), a large ratio implies an OS-driven
    collapse is essentially guaranteed (``"collapse-dominated"``), and values in
    between are marked as ``"intermediate"``.

    Parameters
    ----------
    experiment:
        Experimental configuration and OS parameters.
    quiet_threshold:
        Upper bound on ``t/τ_c`` for a configuration to be considered safely
        quantum-like. Defaults to ``0.1``.
    collapse_threshold:
        Lower bound on ``t/τ_c`` for being considered collapse-dominated.
        Defaults to ``10.0``.
    deviation_fraction:
        Minimum fractional change in visibility used to flag a deviation between
        models. Defaults to ``0.01`` (1%).
    """

    collapse = os_collapse_rates(experiment.config, experiment.params)
    t_over_tau = math.inf if collapse.tau_c == math.inf else experiment.t_s / collapse.tau_c

    visibility_qm = visibility_qm_no_collapse(experiment.t_s)
    visibility_os_only = visibility_os(experiment.t_s, collapse.gamma_col)
    visibility_env_only = visibility_env(experiment.t_s, experiment.gamma_env)
    visibility_os_env = visibility_os_plus_env(experiment.t_s, collapse.gamma_col, experiment.gamma_env)

    if t_over_tau < quiet_threshold:
        regime = "qm-dominated"
    elif t_over_tau > collapse_threshold:
        regime = "collapse-dominated"
    else:
        regime = "intermediate"

    deviates_from_qm = abs(visibility_os_env - visibility_qm) >= deviation_fraction
    deviates_from_env = abs(visibility_os_env - visibility_env_only) >= deviation_fraction

    return RegimeAssessment(
        t_over_tau=t_over_tau,
        regime=regime,
        visibility_qm=visibility_qm,
        visibility_os=visibility_os_only,
        visibility_env=visibility_env_only,
        visibility_os_plus_env=visibility_os_env,
        deviates_from_qm=deviates_from_qm,
        deviates_from_env=deviates_from_env,
    )


def is_os_safely_alive(regime: RegimeAssessment, threshold: float = 0.1) -> bool:
    """Return ``True`` if the OS hypothesis remains effectively untested.

    This is operationalized as ``t/τ_c < threshold``, with a default threshold of
    ``0.1`` corresponding to an experiment time more than an order of magnitude
    shorter than the expected collapse time.
    """

    return regime.t_over_tau < threshold


def is_os_strongly_testable(
    regime: RegimeAssessment,
    *,
    threshold: float = 10.0,
    deviation_fraction: float = 0.01,
) -> bool:
    """Return ``True`` if the OS effect should be unambiguously testable.

    A configuration is considered strongly testable when ``t/τ_c`` comfortably
    exceeds the ``threshold`` (default ``10.0``) **and** the combined visibility
    differs from either the QM or pure-environment prediction by at least
    ``deviation_fraction``.
    """

    above_threshold = regime.t_over_tau >= threshold
    deviates = regime.deviates_from_qm or regime.deviates_from_env
    return above_threshold and deviates


def assess_testability(
    experiment: ExperimentData,
    *,
    quiet_threshold: float = 0.1,
    collapse_threshold: float = 10.0,
    deviation_fraction: float = 0.01,
) -> TestabilityAssessment:
    """Evaluate whether an experiment probes the OS collapse hypothesis."""

    regime = assess_regime(
        experiment,
        quiet_threshold=quiet_threshold,
        collapse_threshold=collapse_threshold,
        deviation_fraction=deviation_fraction,
    )
    os_alive = is_os_safely_alive(regime, threshold=quiet_threshold)
    os_testable = is_os_strongly_testable(
        regime, threshold=collapse_threshold, deviation_fraction=deviation_fraction
    )
    os_deviation_detectable = regime.deviates_from_env or regime.deviates_from_qm

    return TestabilityAssessment(
        experiment=experiment,
        regime=regime,
        os_safely_alive=os_alive,
        os_strongly_testable=os_testable,
        os_deviation_detectable=os_deviation_detectable,
    )


def find_lambda_constraint(
    experiment: ExperimentData,
    target_visibility: float,
    *,
    clamp_to_zero: bool = True,
) -> LambdaConstraint:
    """Compute the λ value that would saturate a target visibility measurement.

    The calculation assumes a measured visibility of ``target_visibility`` and
    returns the maximum collapse rate (and corresponding λ) that would not push
    the OS + environment prediction below that measurement. Values of λ larger
    than ``lam_limit`` would be excluded under this interpretation.
    """

    if target_visibility <= 0 or target_visibility > 1:
        raise ValueError("target_visibility must lie in the interval (0, 1].")

    collapse = os_collapse_rates(experiment.config, experiment.params)
    delta_e_g = collapse.delta_E_G

    gamma_col_needed = -math.log(target_visibility) / experiment.t_s - experiment.gamma_env
    if clamp_to_zero and gamma_col_needed < 0:
        gamma_col_needed = 0.0

    lam_limit = 0.0 if delta_e_g == 0 else gamma_col_needed * HBAR / delta_e_g
    visibility_at_limit = visibility_os_plus_env(
        experiment.t_s, gamma_col_needed, experiment.gamma_env
    )
    current_visibility = visibility_os_plus_env(
        experiment.t_s, collapse.gamma_col, experiment.gamma_env
    )
    is_excluded = collapse.gamma_col > gamma_col_needed if gamma_col_needed > 0 else False

    return LambdaConstraint(
        lam_limit=lam_limit,
        gamma_col_limit=gamma_col_needed,
        visibility_at_limit=visibility_at_limit,
        is_excluded=is_excluded or current_visibility < target_visibility,
    )


__all__ = [
    "RegimeAssessment",
    "ExperimentData",
    "TestabilityAssessment",
    "LambdaConstraint",
    "assess_regime",
    "is_os_safely_alive",
    "is_os_strongly_testable",
    "assess_testability",
    "find_lambda_constraint",
]
