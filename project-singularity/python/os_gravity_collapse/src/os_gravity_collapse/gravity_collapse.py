"""
Core formulas and data structures for a gravity-weighted collapse model (ΔE_G, Γ_col, τ_c).

This module implements a simple Observer–Singularity (OS) collapse model using a
Diósi–Penrose-style point-mass gravitational self-energy estimate. It is intended as
an extensible, readable starting point for more detailed models (e.g., extended mass
profiles, environmental decoherence, or alternative collapse mechanisms).
"""
from __future__ import annotations

import math
from dataclasses import dataclass

# Physical constants (SI units)
G: float = 6.67430e-11  # m^3 kg^-1 s^-2
HBAR: float = 1.054571817e-34  # J·s


@dataclass
class OSParameters:
    """Model parameters for the Observer–Singularity gravity-weighted collapse model.

    Attributes
    ----------
    lam:
        Dimensionless coupling λ (order unity). Must be strictly positive.
    """

    lam: float = 1.0

    def __post_init__(self) -> None:
        if self.lam <= 0:
            raise ValueError("Parameter 'lam' must be positive for a physical collapse rate.")


@dataclass
class SuperpositionConfig:
    """Configuration for a simple two-branch spatial superposition with point masses.

    Attributes
    ----------
    mass:
        Effective mass of the superposed object in kilograms. Must be positive.
    separation:
        Spatial separation between the branches in meters. Must be positive.
    """

    mass: float
    separation: float

    def __post_init__(self) -> None:
        if self.mass <= 0:
            raise ValueError("Mass must be positive for a physical superposition configuration.")
        if self.separation <= 0:
            raise ValueError("Separation must be positive for a physical superposition configuration.")


@dataclass
class CollapseResult:
    """Container for collapse-related quantities.

    Attributes
    ----------
    delta_E_G:
        Gravitational self-energy gap ΔE_G in joules.
    gamma_col:
        Collapse rate Γ_col in s^-1.
    tau_c:
        Collapse timescale τ_c in seconds. Uses math.inf if γ is zero or negative.
    """

    delta_E_G: float
    gamma_col: float
    tau_c: float


def delta_E_G_point_mass(mass: float, separation: float, g_geom: float = 1.0) -> float:
    """Estimate gravitational self-energy for two point-mass branches.

    Parameters
    ----------
    mass:
        Mass of the object in kilograms. Must be positive.
    separation:
        Distance between the branch centroids in meters. Must be positive.
    g_geom:
        Dimensionless geometry factor to rescale the point-mass estimate
        (default 1.0). Must be positive.

    Returns
    -------
    float
        Approximate ΔE_G ≈ G * m^2 / d (joules) following the Diósi–Penrose point-mass
        estimate for a sharply localized superposition.

    Raises
    ------
    ValueError
        If mass or separation are non-physical (<= 0).
    """

    if mass <= 0:
        raise ValueError("Mass must be positive to compute ΔE_G.")
    if separation <= 0:
        raise ValueError("Separation must be positive to compute ΔE_G.")
    if g_geom <= 0:
        raise ValueError("Geometry factor g_geom must be positive to compute ΔE_G.")
    return g_geom * G * mass**2 / separation


def os_collapse_rates(
    config: SuperpositionConfig,
    params: OSParameters | None = None,
    g_geom: float = 1.0,
) -> CollapseResult:
    """Compute OS collapse quantities for a two-branch point-mass superposition.

    The OS law for collapse rate is Γ_col = λ * ΔE_G / ℏ. The corresponding collapse
    time is τ_c = 1 / Γ_col. If Γ_col is non-positive, τ_c is reported as ``math.inf``.

    Parameters
    ----------
    config:
        Superposition configuration (mass, separation).
    params:
        Observer–Singularity parameters. If omitted, defaults to ``OSParameters()``.
    g_geom:
        Dimensionless geometry factor applied to the point-mass ΔE_G estimate. Defaults
        to 1.0 (pure point mass). Must be positive.

    Returns
    -------
    CollapseResult
        Dataclass containing ΔE_G, Γ_col, and τ_c.
    """

    _params = params or OSParameters()
    delta_e_g = delta_E_G_point_mass(config.mass, config.separation, g_geom=g_geom)
    gamma_col = _params.lam * delta_e_g / HBAR
    tau_c = math.inf if gamma_col <= 0 else 1.0 / gamma_col
    return CollapseResult(delta_E_G=delta_e_g, gamma_col=gamma_col, tau_c=tau_c)


def visibility_os(t: float, gamma_col: float) -> float:
    """Compute OS visibility V_OS(t) = exp(-Γ_col * t).

    Parameters
    ----------
    t:
        Time in seconds. Must satisfy ``t >= 0``.
    gamma_col:
        Collapse rate Γ_col in s^-1.

    Returns
    -------
    float
        Interference visibility at time ``t`` under OS collapse dynamics.

    Raises
    ------
    ValueError
        If ``t`` is negative.
    """

    if t < 0:
        raise ValueError("Time must be non-negative when evaluating visibility.")
    return math.exp(-gamma_col * t)


def visibility_qm_no_collapse(t: float) -> float:
    """Baseline quantum visibility with no intrinsic collapse (V_QM = 1)."""

    return 1.0


def visibility_env(t: float, gamma_env: float) -> float:
    """Visibility under a pure environment decoherence model V_env(t) = exp(-Γ_env * t).

    Parameters
    ----------
    t:
        Time in seconds. Must satisfy ``t >= 0``.
    gamma_env:
        Environment decoherence rate Γ_env in s^-1. Must be non-negative.

    Returns
    -------
    float
        Interference visibility at time ``t`` under environment-only decoherence.

    Raises
    ------
    ValueError
        If ``t`` is negative or ``gamma_env`` is negative.
    """

    if t < 0:
        raise ValueError("Time must be non-negative when evaluating environment visibility.")
    if gamma_env < 0:
        raise ValueError("Environment decoherence rate gamma_env must be non-negative.")
    return math.exp(-gamma_env * t)


def visibility_os_plus_env(t: float, gamma_col: float, gamma_env: float) -> float:
    """Combined OS collapse and environment decoherence V_OS+env(t) = exp(-(Γ_col+Γ_env) * t).

    Parameters
    ----------
    t:
        Time in seconds. Must satisfy ``t >= 0``.
    gamma_col:
        OS collapse rate Γ_col in s^-1.
    gamma_env:
        Environment decoherence rate Γ_env in s^-1. Must be non-negative.

    Returns
    -------
    float
        Interference visibility at time ``t`` under the combined model.

    Raises
    ------
    ValueError
        If ``t`` is negative or ``gamma_env`` is negative.
    """

    if t < 0:
        raise ValueError("Time must be non-negative when evaluating combined visibility.")
    if gamma_env < 0:
        raise ValueError("Environment decoherence rate gamma_env must be non-negative.")
    return math.exp(-(gamma_col + gamma_env) * t)


def visibility_curve_os(
    times: list[float] | tuple[float, ...],
    gamma_col: float,
) -> list[float]:
    """Evaluate OS visibility over a sequence of times.

    Parameters
    ----------
    times:
        Iterable of times in seconds. All values must be non-negative.
    gamma_col:
        Collapse rate Γ_col in s^-1.

    Returns
    -------
    list[float]
        Visibility values corresponding to the input time grid.

    Raises
    ------
    ValueError
        If any time value is negative.
    """

    for t in times:
        if t < 0:
            raise ValueError("All time values must be non-negative for visibility curves.")
    return [visibility_os(t, gamma_col) for t in times]


def visibility_curve_env(
    times: list[float] | tuple[float, ...],
    gamma_env: float,
) -> list[float]:
    """Evaluate environment-only visibility over a sequence of times."""

    for t in times:
        if t < 0:
            raise ValueError("All time values must be non-negative for visibility curves.")
    if gamma_env < 0:
        raise ValueError("Environment decoherence rate gamma_env must be non-negative.")
    return [visibility_env(t, gamma_env) for t in times]


def visibility_curve_os_plus_env(
    times: list[float] | tuple[float, ...],
    gamma_col: float,
    gamma_env: float,
) -> list[float]:
    """Evaluate combined OS + environment visibility over a sequence of times."""

    for t in times:
        if t < 0:
            raise ValueError("All time values must be non-negative for visibility curves.")
    if gamma_env < 0:
        raise ValueError("Environment decoherence rate gamma_env must be non-negative.")
    return [visibility_os_plus_env(t, gamma_col, gamma_env) for t in times]


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
    "visibility_env",
    "visibility_os_plus_env",
    "visibility_curve_env",
    "visibility_curve_os_plus_env",
]
