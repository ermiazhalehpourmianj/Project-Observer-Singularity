# Project Singularity – Observer–Singularity Research Stack

**Project Singularity** is an open research stack that explores how a single classical reality might emerge from quantum superpositions when you combine:

1. A **gravity-weighted collapse model** (Observer–Singularity, “OS model”) that proposes a concrete, testable law for wavefunction collapse; and  
2. An **Observer Geometry framework** that treats the observer’s state as a geometric, feedback-driven structure shaping what becomes “the present.”

This repository contains:

- A **Python OS collapse calculator** (`os_collapse`) for estimating ΔE_G, Γ_col, τ_c, and visibility curves in simple toy scenarios.  
- **Reproducible simulation and analysis tools** (examples, tests) for labs and theorists exploring gravity-based collapse.  
- **Two companion papers** (Observer–Singularity & Observer Geometry) that define the theory and its experiential / geometric extension.

> ⚠️ This is research code. It is intended for exploration, not for safety-critical or production use.

---

## Table of Contents

- [Motivation](#motivation)
- [What’s in this repo](#whats-in-this-repo)
- [Repository structure](#repository-structure)
- [Installation](#installation)
- [Quickstart](#quickstart)
  - [Python API](#python-api)
  - [Example script](#example-script)
- [Conceptual overview](#conceptual-overview)
  - [1. Gravity-weighted collapse (OS model)](#1-gravity-weighted-collapse-os-model)
  - [2. Observer Geometry (feedback & pattern)](#2-observer-geometry-feedback--pattern)
- [Reproducibility & testing](#reproducibility--testing)
- [Using this in your own work](#using-this-in-your-own-work)
- [Roadmap](#roadmap)
- [Citing](#citing)
- [License](#license)

---

## Motivation

Standard quantum mechanics evolves states smoothly and linearly, yet our experience is of **one definite outcome** at a time. Decoherence explains why certain “pointer states” are stable, but not *why one branch actually becomes real*.

**Project Singularity** explores one specific, testable answer:

- Use a **final-state / observer–singularity constraint** to select a single classical branch,  
- Weight the collapse by the **gravitational self-energy gap** ΔE_G between branches, and  
- Treat the observer’s internal state as a **geometric feedback system** (Observer Geometry) that shapes how information is integrated into the present.

This repo is the **working environment** for that program: code, experiments, and papers in one place.

---

## What’s in this repo

- **`os_collapse` (Python library)**  
  - Compute **ΔE_G ≈ G m² / d** for simple point-mass superpositions.  
  - Compute **collapse rate** Γ_col = λ ΔE_G / ħ and **collapse time** τ_c = 1 / Γ_col.  
  - Model **visibility loss** V_OS(t) ≈ exp(−Γ_col t) compared to a no-collapse baseline V_QM(t) = 1.

- **Examples & tools**  
  - Ready-to-run scripts that show how to plug the OS model into simple parameter scans and visibility plots.  
  - A starting point for labs to adapt OS-style estimates to their own interferometer / optomechanical setups.

- **Papers**  
  - **Paper 1 – Observer–Singularity:** formalizes the gravity-weighted collapse model, compares it to GRW/CSL/Many-Worlds, and lays out an experimental decision tree.  
  - **Paper 2 – Observer Geometry:** proposes a geometric / feedback-loop model of the observer (frequency, patterns, loops) that connects the OS collapse rule to lived, experiential structure.

---
