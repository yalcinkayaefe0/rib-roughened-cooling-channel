"""
Ribbed cooling channel — Stage 1 post-processing
=================================================

Reads the Fluent ASCII export of the heated floor (`bottom-wall`) and produces:

  1. The reattachment length Xr/e, from the sign change of the streamwise
     wall shear stress (linear interpolation between adjacent nodes).
  2. The local Nusselt number distribution Nu/Nu0 versus X/e.
  3. Publication figures written directly into report/figures/.

Usage
-----
    python postprocess_ribbed.py

Edit the CONFIG block below before running. The only values that must come
from outside this script are:

  * T_BULK        — mass-weighted mean temperature on periodic-1
  * DT_SMOOTH     — (T_w - T_b) from the Stage 0 smooth-channel run
  * K_FLUID       — thermal conductivity used in BOTH runs

Column detection is by fuzzy name matching, so the exact header Fluent
writes does not matter as long as the four quantities are present.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# =====================================================================
# CONFIG
# =====================================================================

ROOT = Path(__file__).resolve().parent.parent

CFD_CSV = ROOT / "data" / "cfd" / "ribbed_bottomwall.csv"
EXP_CSV = ROOT / "data" / "experimental" / "rau_fig15_pe9_1s.csv"
FIGDIR = ROOT / "report" / "figures"

# --- geometry --------------------------------------------------------
E_RIB = 5.0e-3       # rib height                              [m]
PITCH = 45.0e-3      # periodic segment length                 [m]
X_RIB_BACK = 17.5e-3  # x of the rib trailing face             [m]
D_H = 0.05           # hydraulic diameter (Rau definition)     [m]

# --- boundary condition / properties ---------------------------------
Q_FLUX = 1000.0      # imposed floor heat flux                 [W/m^2]
K_FLUID = 0.0242     # thermal conductivity                    [W/m/K]

# --- from the solution -----------------------------------------------
T_BULK = 300.00116   # mass-weighted mean T on periodic-1      [K]

# --- normalisation ----------------------------------------------------
# Rau et al. (1996), Eq. 1, normalise by the Dittus-Boelter smooth-tube
# correlation, NOT by their own smooth-channel measurement. To compare
# like for like we must do the same. DT_SMOOTH is therefore left unused
# for the validation figure; it is kept only to allow the alternative
# normalisation against our own Stage 0 run to be reported separately.
DT_SMOOTH = None     # [K]  (T_w - T_b) from the Stage 0 smooth-channel run

RE_DH = 30010.0
PR = 0.744

# --- friction factor --------------------------------------------------
# Rau et al., Eq. 3 (Fanning) and Eq. 4 (Blasius reference):
#   f  = dp/dx * D_h / (2 rho U^2)
#   f0 = 0.046 * Re^-0.2
DPDX = 37.4          # [Pa/m]  solver-reported periodic pressure gradient
RHO = 1.18           # [kg/m3]
U_BULK = 9.10        # [m/s]
DPDX_SMOOTH_CFD = 10.22   # [Pa/m]  Stage 0 run, for the secondary comparison

# --- experimental reattachment band (Rau et al., p/e = 9) -------------
# Measured as the interval over which U < 0 at Y/e = 0.05 in the symmetry
# plane -- NOT from the wall shear stress. See RIB_PROBE_HEIGHT below.
XR_EXP = (4.00, 4.25)
RIB_PROBE_HEIGHT = 0.05 * E_RIB   # [m] = 0.25 mm, Rau's LDV traverse height


# =====================================================================
# HELPERS
# =====================================================================

def find_column(df, *keywords):
    """Return the first column whose normalised name contains all keywords."""
    for col in df.columns:
        name = col.strip().strip('"').lower().replace("-", " ").replace("_", " ")
        if all(kw in name for kw in keywords):
            return col
    raise KeyError(
        f"No column matching {keywords!r}. Available columns: {list(df.columns)}"
    )


def to_xe(x_m):
    """Map physical x [m] onto Rau's periodic X/e axis."""
    return ((x_m - X_RIB_BACK) % PITCH) / E_RIB


def zero_crossings(xe, tau):
    """
    Locate sign changes of tau along the (sorted) X/e axis.

    Returns a list of (xe_cross, direction) where direction is
    '-> +' for reattachment and '-> -' for separation onset.
    """
    out = []
    for i in range(len(tau) - 1):
        t0, t1 = tau[i], tau[i + 1]
        if t0 == 0.0:
            out.append((xe[i], "-> +" if t1 > 0 else "-> -"))
        elif t0 * t1 < 0.0:
            # linear interpolation of the zero
            frac = -t0 / (t1 - t0)
            xc = xe[i] + frac * (xe[i + 1] - xe[i])
            out.append((xc, "-> +" if t1 > 0 else "-> -"))
    return out


def dittus_boelter(re, pr):
    return 0.023 * re ** 0.8 * pr ** 0.4


# =====================================================================
# LOAD
# =====================================================================

def load_cfd(path):
    if not path.exists():
        raise SystemExit(
            f"CFD export not found:\n  {path}\n\n"
            "Export it from Fluent:\n"
            "  File > Export > Solution Data > ASCII\n"
            "  Surface   : bottom-wall\n"
            "  Quantities: X-Coordinate, Static Temperature, X-Wall Shear Stress\n"
            "  Delimiter : comma"
        )

    df = pd.read_csv(path, sep=None, engine="python", skipinitialspace=True)
    df.columns = [c.strip().strip('"') for c in df.columns]

    col_x = find_column(df, "x", "coordinate")
    col_t = find_column(df, "temperature")
    try:
        col_tau = find_column(df, "x", "wall", "shear")
    except KeyError:
        col_tau = find_column(df, "shear")
        print(f"  ! Using '{col_tau}' as wall shear stress. If this is the "
              "MAGNITUDE rather than the x-component, the reattachment point "
              "cannot be found — re-export with 'X-Wall Shear Stress'.")

    out = pd.DataFrame({
        "x": df[col_x].astype(float),
        "Tw": df[col_t].astype(float),
        "tau_x": df[col_tau].astype(float),
    })
    out["Xe"] = to_xe(out["x"].to_numpy())
    out = out.sort_values("Xe").reset_index(drop=True)
    return out


# =====================================================================
# MAIN
# =====================================================================

def main():
    FIGDIR.mkdir(parents=True, exist_ok=True)

    print("=" * 68)
    print("Ribbed channel — Stage 1 post-processing")
    print("=" * 68)

    df = load_cfd(CFD_CSV)
    print(f"\nLoaded {len(df)} points from {CFD_CSV.name}")
    print(f"  x range   : {df['x'].min()*1e3:.2f} .. {df['x'].max()*1e3:.2f} mm")
    print(f"  X/e range : {df['Xe'].min():.3f} .. {df['Xe'].max():.3f}")

    # -----------------------------------------------------------------
    # Reattachment
    # -----------------------------------------------------------------
    xe = df["Xe"].to_numpy()
    tau = df["tau_x"].to_numpy()
    crossings = zero_crossings(xe, tau)

    print("\n--- Wall shear stress sign changes ---")
    if not crossings:
        print("  none found — check that X-Wall Shear Stress (signed) was exported")
    for xc, direction in crossings:
        label = "reattachment" if direction == "-> +" else "separation onset"
        print(f"  X/e = {xc:6.3f}   {direction}   ({label})")

    # The primary recirculation bubble is the one containing the global
    # minimum of tau_x. Its reattachment point is the first negative->positive
    # crossing DOWNSTREAM of that minimum. Selecting the first crossing overall
    # would instead pick up the small corner eddy at the rib base, which also
    # produces a sign change but is not reattachment.
    xe_taumin = xe[tau.argmin()]
    reatt = [xc for xc, d in crossings if d == "-> +" and xc > xe_taumin]
    xr = None
    if reatt:
        xr = min(reatt)
        print(f"\n  (tau_x minimum at X/e = {xe_taumin:.2f}; "
              "reattachment taken as the first sign change downstream of it)")
        lo, hi = XR_EXP
        status = "within" if lo <= xr <= hi else "outside"
        err_lo = (xr - lo) / lo * 100.0
        err_hi = (xr - hi) / hi * 100.0
        print(f"\n  Xr/e (CFD)        = {xr:.3f}")
        print(f"  Xr/e (experiment) = {lo:.2f} .. {hi:.2f}   [{status} band]")
        print(f"  deviation         = {err_lo:+.1f}% / {err_hi:+.1f}% "
              "(vs lower / upper bound)")

    # -----------------------------------------------------------------
    # Nusselt number
    # -----------------------------------------------------------------
    dT = df["Tw"].to_numpy() - T_BULK
    nu = Q_FLUX * D_H / (dT * K_FLUID)

    if DT_SMOOTH is not None:
        nu0 = Q_FLUX * D_H / (DT_SMOOTH * K_FLUID)
        nu0_src = f"Stage 0 run, (Tw-Tb)0 = {DT_SMOOTH:.3f} K"
    else:
        nu0 = dittus_boelter(RE_DH, PR)
        nu0_src = f"Dittus-Boelter, Re = {RE_DH:.0f}, Pr = {PR:.3f}"
        print("\n  ! DT_SMOOTH is not set — falling back to the Dittus-Boelter")
        print("    correlation. Set it from the Stage 0 run for a like-for-like")
        print("    comparison, since q'', D_h and k then cancel exactly.")

    ratio = nu / nu0

    print(f"\n--- Nusselt number ---")
    print(f"  Nu0 source        : {nu0_src}")
    print(f"  Nu0               = {nu0:.2f}")
    print(f"  Nu/Nu0  min       = {ratio.min():.3f}  at X/e = {xe[ratio.argmin()]:.2f}")
    print(f"  Nu/Nu0  max       = {ratio.max():.3f}  at X/e = {xe[ratio.argmax()]:.2f}")
    print(f"  Nu/Nu0  pitch avg = {np.trapezoid(ratio, xe) / (xe[-1] - xe[0]):.3f}")

    # -----------------------------------------------------------------
    # Friction factor
    # -----------------------------------------------------------------
    f_ribbed = DPDX * D_H / (2.0 * RHO * U_BULK ** 2)
    f_smooth_cfd = DPDX_SMOOTH_CFD * D_H / (2.0 * RHO * U_BULK ** 2)
    f0_blasius = 0.046 * RE_DH ** -0.2

    print("\n--- Friction factor (Fanning) ---")
    print(f"  f  (ribbed, CFD)             = {f_ribbed:.5f}")
    print(f"  f0 (Blasius, Rau Eq. 4)      = {f0_blasius:.5f}   <- use this one")
    print(f"  f0 (smooth channel, Stage 0) = {f_smooth_cfd:.5f}")
    print(f"\n  f/f0  vs Blasius   = {f_ribbed / f0_blasius:.3f}   "
          "[comparable with Rau et al.]")
    print(f"  f/f0  vs Stage 0   = {f_ribbed / f_smooth_cfd:.3f}   "
          "[internal reference, NOT comparable]")
    print(f"\n  Stage 0 / Blasius  = {f_smooth_cfd / f0_blasius:.3f}")
    print("    The 2D channel has D_h = 2H = 0.1 m, but D_h = 0.05 m (Rau's")
    print("    square duct) is used in the normalisation. The smooth 2D channel")
    print("    therefore does not reproduce the Blasius smooth-tube value, and")
    print("    the Stage 0 run cannot serve as the reference for comparison.")

    # -----------------------------------------------------------------
    # Experimental overlay
    # -----------------------------------------------------------------
    exp = None
    if EXP_CSV.exists():
        exp = pd.read_csv(EXP_CSV, header=None, names=["Xe", "ratio"])
        exp = exp.sort_values("Xe")
        print(f"\n  Experimental data loaded: {len(exp)} points")
    else:
        print(f"\n  ! Experimental data not found at {EXP_CSV}")
        print("    Digitise Rau et al. Fig. 15 (p/e = 9, ONE-SIDE curve).")

    # -----------------------------------------------------------------
    # Figure 1 — Nu/Nu0
    # -----------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.plot(xe, ratio, "-", lw=1.8, color="#1f4e79", label="CFD, $k$-$\\omega$ SST")
    if exp is not None:
        ax.plot(exp["Xe"], exp["ratio"], "o", ms=4.5, mfc="none",
                mec="#c00000", mew=1.2, label="Rau et al. (1996)")
    if xr is not None:
        ax.axvline(xr, color="gray", ls="--", lw=1.0)
        ax.annotate(f"$X_r/e = {xr:.2f}$", xy=(xr, ax.get_ylim()[1]),
                    xytext=(4, -12), textcoords="offset points",
                    fontsize=9, color="gray", va="top")
    ax.axvspan(*XR_EXP, color="#c00000", alpha=0.10, lw=0)
    ax.set_xlabel("$X/e$")
    ax.set_ylabel("$Nu/Nu_0$")
    ax.set_xlim(0, 8)
    ax.grid(alpha=0.25, lw=0.6)
    ax.legend(frameon=False)
    fig.tight_layout()
    out1 = FIGDIR / "fig_nusselt.pdf"
    fig.savefig(out1)
    print(f"\n  wrote {out1}")

    # -----------------------------------------------------------------
    # Figure 2 — wall shear stress
    # -----------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(7.0, 3.4))
    ax.plot(xe, tau, "-", lw=1.8, color="#1f4e79")
    ax.axhline(0.0, color="black", lw=0.8)
    for xc, direction in crossings:
        ax.plot(xc, 0.0, "o", ms=5,
                color="#c00000" if direction == "-> +" else "#7f7f7f")
    ax.axvspan(*XR_EXP, color="#c00000", alpha=0.10, lw=0,
               label="experimental $X_r/e$ band")
    ax.set_xlabel("$X/e$")
    ax.set_ylabel(r"$\tau_{w,x}$  [Pa]")
    ax.set_xlim(0, 8)
    ax.grid(alpha=0.25, lw=0.6)
    ax.legend(frameon=False)
    fig.tight_layout()
    out2 = FIGDIR / "fig_wallshear.pdf"
    fig.savefig(out2)
    print(f"  wrote {out2}")

    # -----------------------------------------------------------------
    # Tidy CSV for the record
    # -----------------------------------------------------------------
    df_out = pd.DataFrame({
        "Xe": xe,
        "x_mm": df["x"] * 1e3,
        "Tw_K": df["Tw"],
        "tau_x_Pa": tau,
        "Nu": nu,
        "Nu_over_Nu0": ratio,
    })
    out3 = ROOT / "data" / "cfd" / "ribbed_bottomwall_processed.csv"
    df_out.to_csv(out3, index=False, float_format="%.6g")
    print(f"  wrote {out3}")

    print("\n" + "=" * 68)


if __name__ == "__main__":
    main()
