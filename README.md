# Rib-Roughened Cooling Channel — CFD Validation

2D periodic RANS validation of turbulent flow and heat transfer in a
single-wall rib-roughened cooling channel, against the experimental data of
**Rau et al. (1996), ASME 96-GT-541**. This is the kind of internal cooling
passage geometry used for gas-turbine blade cooling: transverse ribs
(turbulators) trip the boundary layer to enhance heat transfer at the cost of
extra pressure loss.

## Case setup

| Parameter | Value |
|---|---|
| Rib pitch-to-height ratio, $p/e$ | 9 |
| Blockage ratio, $e/D_h$ | 0.1 |
| Reynolds number, $Re_{D_h}$ | 30,000 |
| Domain | 2D, streamwise-periodic single segment |
| Turbulence model | $k$–$\omega$ SST, resolved to $y^+ < 1$ (no wall functions) |
| Rib thermal condition | Adiabatic (non-conducting, matches the plexiglass ribs in the reference experiment) |
| Solver | ANSYS Fluent (via ANSYS Workbench and standalone Fluent sessions) |

## Result: an open, actively-diagnosed discrepancy

This is not a "clean match" validation — it documents a real, unresolved
deviation and the elimination process used to isolate its cause.

The model reproduces the reference flow topology (all three vortex
structures reported by Rau) and the qualitative pressure/heat-transfer
trends, but:

- **over-predicts the reattachment length by ~2x**: $X_r/e \approx 7.95$
  (CFD) vs. $4.00$–$4.25$ (experiment)
- **under-predicts peak Nusselt enhancement by ~40%**
- **under-predicts friction enhancement by ~53%**

The cause was isolated by systematic elimination:

| Candidate cause | Status | Evidence |
|---|---|---|
| Measurement-definition mismatch | ruled out | Matching Rau's exact LDV probe location, the reverse flow persists to the end of the floor |
| Unsteadiness (steady-state assumption) | ruled out | Finite-amplitude perturbation test (URANS): the disturbance decays, monitors return to the same steady state |
| Mesh resolution | ruled out | GCI (Celik et al. 2008) on 3 grids: $\mathrm{GCI}_{fine} \approx 0.001\%$ ($X_r/e$), $0.7\%$ ($Nu/Nu_0$) |
| **Turbulence closure ($k$–$\omega$ SST shear-stress limiter)** | **governing cause** | Realizable $k$–$\varepsilon$ agrees with SST within 0.5% and a Stress-Omega RSM also fails to reattach, but Keshmiri et al. (2016) solved the identical 2D case and found that $v^2$–$f$ and $\varphi$–$f$ recover reattachment while SST alone does not, attributing this to the SST shear-stress limiter suppressing $\mu_t$ in the inter-rib cavity |
| 2D idealization | secondary contribution | Cannot represent the turbulence-driven secondary flows; but since 2D computations with other closures reproduce the data, it is not the governing cause (see also Keshmiri 2012) |

Full derivation, the correlation-normalization pitfalls found along the way,
and the next steps (a direct test of the SST limiter coefficient and a 3D
re-run to quantify the secondary-flow contribution) are in [`docs/project_notes.md`](docs/project_notes.md)
(Turkish) and in the report itself.

## Repository structure

```
report/                 LaTeX source, compiled PDF, and figures for the validation report
  drafts/                Overleaf export history of the manuscript
scripts/                Post-processing (Python): reattachment/Nusselt extraction, GCI, URANS perturbation test
data/
  cfd/                   Fluent ASCII exports of the bottom-wall solution (raw + processed)
  experimental/           Digitized Rau et al. Figure 15 data
docs/
  project_notes.md        Detailed results/decision log (Turkish)
  geometry_and_mesh.md    Geometry and mesh generation rationale (Turkish)
  screenshots/            Raw ANSYS/Fluent screenshots
simulation/
  ansys_workbench/         The two ANSYS Workbench projects (.wbpj + companion _files/) used to build geometry, mesh, and run Fluent
  fluent_standalone/       A standalone Fluent session (URANS perturbation test, RSM re-run) run outside Workbench
  results/                 Final Fluent case/data snapshots and monitor histories referenced by the report and scripts
references/              (not tracked) local copies of third-party papers cited below — see Copyright note
```

## Reproducing the post-processing

Requires Python with `numpy`, `pandas`, `matplotlib`:

```bash
python scripts/postprocess_ribbed.py       # reattachment length, Nusselt/friction, figures
python scripts/mesh_independence.py        # grid convergence index (GCI)
python scripts/urans_perturbation.py       # steady-state assumption check
```

Rebuilding the report:

```bash
cd report && pdflatex ribchannel_validation.tex && pdflatex ribchannel_validation.tex
```

Opening/re-running the CFD itself requires a licensed ANSYS Workbench/Fluent
installation; the `.wbpj` files in `simulation/ansys_workbench/` must stay
next to their matching `_files/` folder.

## References

- G. Rau, M. Çakan, D. Moeller, T. Arts, *The Effect of Periodic Ribs on the
  Local Aerodynamic and Heat Transfer Performance of a Straight Cooling
  Channel*, ASME Paper 96-GT-541, 1996.
- A. Keshmiri, K. Osman, S. Benhamadouche, N. Shokri, *Assessment of
  Advanced RANS Models against Large Eddy Simulation and Experimental Data in
  the Investigation of Ribbed Passages with Passive Heat Transfer*, Numerical
  Heat Transfer, Part B, 69(2), 96–110, 2016.
- A. Keshmiri, *Numerical sensitivity analysis of 3- and 2-dimensional
  rib-roughened channels*, Heat and Mass Transfer, 2012.
  [doi:10.1007/s00231-012-0968-z](https://doi.org/10.1007/s00231-012-0968-z)
- I. B. Celik, U. Ghia, P. J. Roache, C. J. Freitas, H. Coleman, P. E. Raad,
  *Procedure for Estimation and Reporting of Uncertainty Due to
  Discretization in CFD Applications*, J. Fluids Eng. 130(7), 2008.
- F. R. Menter, *Two-Equation Eddy-Viscosity Turbulence Models for
  Engineering Applications*, AIAA Journal 32(8), 1994.

The reference papers themselves are copyrighted and are not redistributed in
this repository.

## Author

Efe Yalçınkaya, Department of Mechanical Engineering, Eskişehir Osmangazi
University.
