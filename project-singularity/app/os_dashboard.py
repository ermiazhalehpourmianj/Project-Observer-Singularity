"""Interactive Streamlit dashboard for exploring the OS collapse model."""

from __future__ import annotations

import matplotlib.pyplot as plt
import streamlit as st

from os_gravity_collapse import (
    OSParameters,
    SuperpositionConfig,
    os_collapse_rates,
    visibility_os,
    visibility_qm_no_collapse,
)


st.set_page_config(page_title="OS Collapse Dashboard", layout="wide")
st.title("Observer–Singularity Collapse Dashboard")
st.markdown(
    "Explore collapse times and visibilities for two-branch point-mass superpositions."
)

with st.sidebar:
    st.header("Configuration")
    mass = st.number_input(
        "Mass (kg)",
        min_value=1e-24,
        max_value=1e-6,
        value=1e-17,
        step=1e-18,
        format="%e",
    )
    separation = st.number_input(
        "Separation (m)", min_value=1e-9, max_value=1e-3, value=1e-6, step=1e-9, format="%e"
    )
    lam = st.number_input("lambda (λ)", min_value=1e-3, max_value=10.0, value=1.0, step=0.1)
    t_max = st.number_input("Max time (s)", min_value=1e-6, max_value=10.0, value=1.0, step=0.1)
    n_points = st.slider("Time samples", min_value=10, max_value=500, value=200, step=10)

config = SuperpositionConfig(mass=mass, separation=separation)
params = OSParameters(lam=lam)
collapse = os_collapse_rates(config, params)

st.subheader("Collapse parameters")
st.write(
    f"ΔE_G = {collapse.delta_E_G:.3e} J, Γ_col = {collapse.gamma_col:.3e} s⁻¹, τ_c = {collapse.tau_c:.3e} s"
)

step = t_max / (n_points - 1)
times = [i * step for i in range(n_points)]
visibility_os_values = [visibility_os(t, collapse.gamma_col) for t in times]
visibility_qm_values = [visibility_qm_no_collapse(t) for t in times]

fig, ax = plt.subplots()
ax.plot(times, visibility_os_values, label="V_OS(t)", color="tab:blue")
ax.plot(times, visibility_qm_values, label="V_QM(t)", linestyle="--", color="tab:orange")
ax.set_xlabel("time [s]")
ax.set_ylabel("visibility")
ax.set_title(
    f"OS visibility: m={config.mass:.2e} kg, d={config.separation:.2e} m, λ={params.lam:.2e}"
)
ax.legend()
ax.grid(True, linestyle=":", alpha=0.5)

st.pyplot(fig)
