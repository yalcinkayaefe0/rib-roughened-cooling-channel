"""
Ribbed cooling channel — Stage 1, URANS perturbation test
=========================================================

Builds the figure documenting the finite-amplitude perturbation test of
Section 5.4 (steady-state assumption, elimination chain).

Two runs are read:

  * unperturbed  — 500 steps advanced from the converged steady field with
                   no forcing.  Fluent closes each step in 2-3 inner
                   iterations and every monitor is bit-for-bit constant.
                   Files at the project root.
  * perturbed    — the same 500 steps, restarted from the same field after
                   a region patch of v = 2 m/s over
                   x = 18..28 mm, y = 4..8 mm (X/e = 0.1..2.1, Y/e = 0.8..1.6).
                   Files in Fluent/.

Monitors (identical in both runs):
    y-vel-probe   y-velocity at (x, y) = (0.024, 0.006) m  ->  X/e = 1.3, Y/e = 1.2
    force         total streamwise force on all walls      [N]
    tw-bottom     area-weighted mean T on bottom-wall      [K]
    tw-rib        area-weighted mean T on rib-wall         [K]

Outputs: 03_Report/figures/fig_urans_steady.pdf     (unperturbed run)
         03_Report/figures/fig_urans_perturbed.pdf  (perturbation test)

Usage:   python urans_perturbation.py
"""

from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# =====================================================================
# CONFIG
# =====================================================================

ROOT = Path(__file__).resolve().parent.parent
FIGDIR = ROOT / "03_Report" / "figures"

UNPERT_DIR = ROOT              # 500 steps, no forcing
PERT_DIR = ROOT / "Fluent"     # 500 steps, restarted after the patch

DT = 2.0e-5                    # time step                      [s]
U_BULK = 9.10                  # bulk velocity                  [m/s]
PITCH = 45.0e-3                # periodic segment length        [m]
T_FLOW = PITCH / U_BULK        # flow-through time              [s]

MONITORS = [
    ("y-vel-probe-rfile.out", r"probe $v$ at $X/e=1.3$", "#1f4e79"),
    ("force-rfile.out",       r"total wall force $F_x$",  "#c00000"),
    ("tw-bottom-rfile.out",   r"$\overline{T}_w$ floor",  "#2e7d32"),
    ("tw-rib-rfile.out",      r"$\overline{T}_w$ rib",    "#8e6c00"),
]


RMS_WINDOW = 25                # 25 steps = 0.5 ms, for the envelope in (b)


def load_rfile(path):
    """Read a Fluent monitor .out file -> (flow_time [s], value)."""
    rows = []
    with open(path) as fh:
        for line in fh:
            try:
                r = [float(x) for x in line.split()]
            except ValueError:
                continue          # header lines
            if len(r) == 3:
                rows.append(r)
    a = np.array(rows)
    return a[:, 2], a[:, 1]


def running_rms(x, n=RMS_WINDOW):
    """Centred running r.m.s. of x over n samples (edges shortened)."""
    out = np.empty_like(x, dtype=float)
    h = n // 2
    for i in range(len(x)):
        lo, hi = max(0, i - h), min(len(x), i + h + 1)
        out[i] = np.sqrt((x[lo:hi] ** 2).mean())
    return out


def figure_unforced():
    """Relative drift of the four monitors in the unforced run (Figure 7)."""
    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    for name, label, colour in MONITORS:
        t, v = load_rfile(UNPERT_DIR / name)
        ax.plot(t * 1e3, (v - v[0]) / abs(v[0]), "-", lw=1.5,
                color=colour, label=label)
        print(f"  {name:24s} unforced |rel. drift|_max = "
              f"{np.abs((v - v[0]) / v[0]).max():.2e}")

    ax.axhline(0.0, color="black", lw=0.8, ls=":")
    ax.set_xlabel("flow time  [ms]")
    ax.set_ylabel(r"$(\phi - \phi_{0}) / |\phi_{0}|$")
    ax.set_xlim(0, 10)
    ax.grid(alpha=0.25, lw=0.6)
    ax.legend(frameon=False, fontsize=8, ncol=2, loc="lower left")
    fig.tight_layout()
    out = FIGDIR / "fig_urans_steady.pdf"
    fig.savefig(out)
    print(f"  wrote {out}\n")


def main():
    FIGDIR.mkdir(parents=True, exist_ok=True)

    print("=" * 68)
    print("URANS perturbation test")
    print("=" * 68)

    figure_unforced()

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(7.0, 5.6), sharex=True,
        gridspec_kw=dict(height_ratios=[1.0, 1.0], hspace=0.13))

    # -----------------------------------------------------------------
    # Panel (a) — the probe signal itself, both runs on one axis
    # -----------------------------------------------------------------
    name, _, _ = MONITORS[0]
    t_u, v_u = load_rfile(UNPERT_DIR / name)
    t_p, v_p = load_rfile(PERT_DIR / name)

    v_steady = v_u.mean()
    t_patch = t_p[0] - DT           # the patch is applied at the end of the
                                    # unperturbed run, i.e. at t = 10 ms
    print(f"  steady probe value      : {v_steady:+.5f} m/s")
    print(f"  perturbation applied at : t = {t_patch*1e3:.2f} ms")
    print(f"  first peak              : {v_p.max():+.4f} m/s "
          f"at t = {t_p[v_p.argmax()]*1e3:.2f} ms")
    print(f"  first trough            : {v_p.min():+.4f} m/s "
          f"at t = {t_p[v_p.argmin()]*1e3:.2f} ms")
    print(f"  final 50 steps          : {v_p[-50:].mean():+.5f} "
          f"+/- {v_p[-50:].std():.5f} m/s")

    ax1.plot(t_u * 1e3, v_u, "-", lw=1.6, color="#9e9e9e",
             label="unperturbed (steady restart)")
    ax1.plot(t_p * 1e3, v_p, "-", lw=1.6, color="#1f4e79",
             label="perturbed")
    ax1.axhline(v_steady, color="black", lw=0.8, ls=":")
    ax1.annotate(f"steady value $v = {v_steady:.3f}$ m/s",
                 xy=(1.0, v_steady), xytext=(4, 5), textcoords="offset points",
                 fontsize=8, color="black")
    ax1.axvline(t_patch * 1e3, color="#c00000", lw=1.0, ls="--")
    ax1.annotate("patch:\n$v = 2$ m/s", xy=(t_patch * 1e3, 0.30),
                 xytext=(-6, 0), textcoords="offset points",
                 fontsize=8, color="#c00000", ha="right", va="center")

    # mark the successive excursions
    for lbl, idx in [("1st peak", v_p.argmax()), ("1st trough", v_p.argmin())]:
        ax1.plot(t_p[idx] * 1e3, v_p[idx], "o", ms=4, color="#1f4e79")
        ax1.annotate(f"{lbl}  {v_p[idx]:+.2f}", xy=(t_p[idx] * 1e3, v_p[idx]),
                     xytext=(8, 4 if v_p[idx] > 0 else -4),
                     textcoords="offset points", fontsize=8, color="#1f4e79",
                     va="bottom" if v_p[idx] < 0 else "top")

    ax1.set_ylabel(r"$v$ at $(X/e,\,Y/e) = (1.3,\,1.2)$  [m/s]")
    ax1.set_ylim(-0.47, 0.44)
    ax1.grid(alpha=0.25, lw=0.6)
    ax1.legend(frameon=False, fontsize=9, loc="lower left")

    # -----------------------------------------------------------------
    # Panel (b) — decay envelope of every monitor, log scale
    # -----------------------------------------------------------------
    floor = 1e-12
    for name, label, colour in MONITORS:
        t_u, v_u = load_rfile(UNPERT_DIR / name)
        t_p, v_p = load_rfile(PERT_DIR / name)
        ref = v_u.mean()
        env_u = running_rms((v_u - ref) / ref)
        env_p = running_rms((v_p - ref) / ref)
        ax2.semilogy(t_u * 1e3, np.maximum(env_u, floor), "-", lw=1.0,
                     color=colour, alpha=0.45)
        ax2.semilogy(t_p * 1e3, np.maximum(env_p, floor), "-", lw=1.3,
                     color=colour, label=label)

        # windowed rms, for the record
        rms = [np.sqrt((((v_p[(t_p >= lo) & (t_p < lo + 2e-3)] - ref) / ref)
                        ** 2).mean())
               for lo in np.arange(t_p[0] - DT, t_p[-1], 2e-3)]
        print(f"  {name:24s} rms rel. dev. per 2 ms window: "
              + "  ".join(f"{x:.3g}" for x in rms))

    ax2.axvline(t_patch * 1e3, color="#c00000", lw=1.0, ls="--")
    ax2.set_xlabel("flow time  [ms]")
    ax2.set_ylabel("r.m.s. " + r"$|\phi - \phi_{\rm steady}| / |\phi_{\rm steady}|$"
                   + "\n(0.5 ms window)", fontsize=9)
    ax2.set_ylim(1e-11, 3e1)
    ax2.set_xlim(0, t_p[-1] * 1e3)
    ax2.grid(alpha=0.25, lw=0.6, which="major")
    ax2.legend(frameon=False, fontsize=8, ncol=2, loc="upper left")

    # secondary axis in flow-through times
    axt = ax1.secondary_xaxis(
        "top", functions=(lambda x: x * 1e-3 / T_FLOW,
                          lambda x: x * T_FLOW * 1e3))
    axt.set_xlabel("flow-through times", fontsize=9)

    fig.tight_layout()
    out = FIGDIR / "fig_urans_perturbed.pdf"
    fig.savefig(out)
    print(f"\n  wrote {out}")
    print("=" * 68)


if __name__ == "__main__":
    main()
