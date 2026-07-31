"""
Grid Convergence Index (GCI) — ribbed channel, Stage 1
======================================================

Closes the last link of the attribution chain: is the over-long
reattachment bubble a discretisation artefact, or intrinsic to the model?

Procedure: Celik et al. (2008), J. Fluids Eng. 130(7), 078001.

Consumes three bottom-wall ASCII exports (same format as
ribbed_bottomwall.csv: node, x, y, temperature, x-wall-shear):

    data/cfd/ribbed_bottomwall_coarse.csv    ~13 500 elements
    data/cfd/ribbed_bottomwall.csv           ~27 100 elements  (medium, exists)
    data/cfd/ribbed_bottomwall_fine.csv      ~53 800 elements

For each mesh it evaluates two validation metrics:
    * Xr/e            — reattachment length (tau_x sign change downstream of tau_min)
    * Nu/Nu0 (avg)    — pitch-averaged normalised Nusselt number

and reports the apparent order p, the Richardson-extrapolated value, and
GCI_fine for each. Element counts are read from ELEMENTS below (edit if the
generated meshes differ from the nominal targets).

Usage
-----
    python mesh_independence.py
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
CFD = ROOT / "data" / "cfd"

# nominal element counts (fine, medium, coarse) — edit to the generated values
ELEMENTS = dict(fine=53800, medium=27100, coarse=13500)

FILES = dict(
    fine=CFD / "ribbed_bottomwall_fine.csv",
    medium=CFD / "ribbed_bottomwall.csv",
    coarse=CFD / "ribbed_bottomwall_coarse.csv",
)

# geometry / properties (identical to postprocess_ribbed.py)
E_RIB, PITCH, X_RIB_BACK, D_H = 5.0e-3, 45.0e-3, 17.5e-3, 0.05
Q_FLUX, K_FLUID, T_BULK = 1000.0, 0.0242, 300.00116
RE_DH, PR = 30010.0, 0.744


def to_xe(x):
    return ((x - X_RIB_BACK) % PITCH) / E_RIB


def find_col(df, *kw):
    for c in df.columns:
        n = c.strip().strip('"').lower().replace("-", " ").replace("_", " ")
        if all(k in n for k in kw):
            return c
    raise KeyError(kw)


def metrics(path):
    """Return (Xr/e, pitch-averaged Nu/Nu0) for one mesh export."""
    df = pd.read_csv(path, sep=None, engine="python", skipinitialspace=True)
    df.columns = [c.strip().strip('"') for c in df.columns]
    x = df[find_col(df, "x", "coordinate")].astype(float).to_numpy()
    T = df[find_col(df, "temperature")].astype(float).to_numpy()
    tau = df[find_col(df, "x", "wall", "shear")].astype(float).to_numpy()
    xe = to_xe(x)
    o = np.argsort(xe)
    xe, T, tau = xe[o], T[o], tau[o]

    # reattachment: first -> + crossing downstream of the tau minimum
    xe_min = xe[tau.argmin()]
    xr = None
    for i in range(len(tau) - 1):
        if tau[i] < 0 <= tau[i + 1] and xe[i] > xe_min:
            f = -tau[i] / (tau[i + 1] - tau[i])
            xr = xe[i] + f * (xe[i + 1] - xe[i])
            break

    nu0 = 0.023 * RE_DH ** 0.8 * PR ** 0.4
    ratio = (Q_FLUX * D_H / ((T - T_BULK) * K_FLUID)) / nu0
    nu_avg = np.trapezoid(ratio, xe) / (xe[-1] - xe[0])
    return xr, nu_avg


def gci(phi1, phi2, phi3, r21, r32, name):
    """Celik 2008 GCI. phi1=fine, phi2=medium, phi3=coarse."""
    e21, e32 = phi2 - phi1, phi3 - phi2
    s = np.sign(e32 / e21) if e21 != 0 else 1.0
    # fixed-point iteration for apparent order p
    p = 2.0
    for _ in range(100):
        q = np.log((r21 ** p - s) / (r32 ** p - s))
        p_new = abs(np.log(abs(e32 / e21)) + q) / np.log(r21)
        if abs(p_new - p) < 1e-10:
            break
        p = p_new
    phi_ext = (r21 ** p * phi1 - phi2) / (r21 ** p - 1)
    e_a = abs((phi1 - phi2) / phi1)
    e_ext = abs((phi_ext - phi1) / phi_ext)
    gci_fine = 1.25 * e_a / (r21 ** p - 1)
    print(f"\n  {name}")
    print(f"    coarse / medium / fine : {phi3:.4f} / {phi2:.4f} / {phi1:.4f}")
    print(f"    apparent order p       : {p:.3f}")
    print(f"    Richardson extrapolated: {phi_ext:.4f}")
    print(f"    approx. rel. error e_a : {e_a*100:.3f} %")
    print(f"    extrap. rel. error     : {e_ext*100:.3f} %")
    print(f"    GCI_fine (95% band)    : {gci_fine*100:.3f} %")
    return dict(p=p, phi_ext=phi_ext, gci=gci_fine)


def main():
    print("=" * 68)
    print("Grid Convergence Index — ribbed channel Stage 1 (Celik 2008)")
    print("=" * 68)

    missing = [k for k, f in FILES.items() if not f.exists()]
    if missing:
        print("\n  Waiting for mesh exports:")
        for k in missing:
            print(f"    [{k:6s}] {FILES[k]}  ({ELEMENTS[k]} elements, nominal)")
        print("\n  Export each from Fluent exactly as the medium mesh was:")
        print("    File > Export > Solution Data > ASCII")
        print("    Surface   : bottom-wall")
        print("    Quantities: X-Coordinate, Static Temperature, X-Wall Shear Stress")
        print("    Delimiter : comma")
        print("\n  The medium mesh (ribbed_bottomwall.csv) is already present.")
        return

    N = ELEMENTS
    r21 = (N["fine"] / N["medium"]) ** 0.5     # 2D: h ~ N^(-1/2)
    r32 = (N["medium"] / N["coarse"]) ** 0.5
    print(f"\n  refinement ratios: r21={r21:.3f} (fine/med), "
          f"r32={r32:.3f} (med/coarse)   [need > 1.3]")

    m = {k: metrics(f) for k, f in FILES.items()}
    xr = {k: m[k][0] for k in m}
    nu = {k: m[k][1] for k in m}

    gci(xr["fine"], xr["medium"], xr["coarse"], r21, r32, "Xr/e")
    gci(nu["fine"], nu["medium"], nu["coarse"], r21, r32, "Nu/Nu0 (pitch avg)")

    print("\n" + "-" * 68)
    print("  Interpretation:")
    print("   * small GCI  + Xr/e still ~8  -> mesh is innocent; deviation is")
    print("     intrinsic to the 2D model (the remaining open cause).")
    print("   * Xr/e drops toward 4-5 on the fine mesh -> the cause was the grid.")
    print("=" * 68)


if __name__ == "__main__":
    main()
