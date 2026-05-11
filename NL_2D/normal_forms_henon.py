# %%
# Imports
import matplotlib.pyplot as plt
import numpy as np
import xpart as xp
import xtrack as xt

from xnlbd.analyse.normal_forms import *
from xnlbd.track import Henonmap
from xnlbd.visualise.orbits import get_orbit_points

# %%
# Lattice and beam parameters
alpha_x = 0.0
beta_x = 1.0
alpha_y = 0.0
beta_y = 1.0

Qx1 = 0.2071   # horizontal tune
Qy1 = 0.2071   # vertical tune

K2 = 1.0       # sextupole strength
K3 = 0.0       # octupole strength

nemitt_x = 1           # horizontal normalised emittance
nemitt_y = 0.0000001   # vertical normalised emittance (quasi-1D)

# %%
# Build Henon map element and xtrack line
henon1 = Henonmap(
    omega_x=2 * np.pi * Qx1,
    omega_y=2 * np.pi * Qy1,
    twiss_params=[alpha_x, beta_x, alpha_y, beta_y],
    dqx=0.0,
    dqy=0.0,
    dx=0.0,
    ddx=0.0,
    multipole_coeffs=[K2, K3],
    norm=False,
)

drift1 = xt.Drift(length=0.0)  # zero-length drift required for aperture check

line1 = xt.Line(
    elements=[drift1, henon1],
    element_names=["zero_len_drift", "henon"],
)
line1.particle_ref = xt.Particles(mass0=xp.PROTON_MASS_EV)
line1.twiss_default["method"] = "4d"
line1.config.XTRACK_GLOBAL_XY_LIMIT = 0.9
line1.build_tracker()

# %%
# Compute phase-space portrait in the horizontal plane (physical coords)
orbits1 = get_orbit_points(line1, element="henon", planes="H", num_pts=50)

# %%
# Plot portrait in physical (x, px) coordinates
plt.figure()
plt.plot(
    orbits1["H_orbit_points"]["x"],
    orbits1["H_orbit_points"]["px"],
    color="black",
    marker=".",
    markersize=0.1,
    linestyle="None",
)
plt.xlabel("x [m]")
plt.ylabel("px [rad]")
plt.title("Horizontal phase-space portrait (physical coords)")
plt.axis("equal")

# %%
# Plot portrait in normalised (x_norm, px_norm) coordinates
plt.figure()
plt.plot(
    orbits1["H_orbit_points_norm"]["x_norm"],
    orbits1["H_orbit_points_norm"]["px_norm"],
    color="black",
    marker=".",
    markersize=0.1,
    linestyle="None",
)
plt.xlabel(r"$\hat{x}$ [normalised]")
plt.ylabel(r"$\hat{p}_x$ [normalised]")
plt.title("Horizontal phase-space portrait (normalised coords)")
plt.axis("equal")

# %%
# Compute the one-turn map and normal form via PolyLine4D
poly_line1 = PolyLine4D(
    line1,
    line1.particle_ref,
    max_ele_order=2,
    max_map_order=3,
    nemitt_x=nemitt_x,
    nemitt_y=nemitt_y,
)
poly_line1.calculate_one_turn_map()
poly_line1.calculate_normal_form(
    max_nf_order=8,
    res_space_dim=0,
    res_case=0,
)
# %%
H = poly_line1.normal_form.H
import pandas as pd

records = []
for t in H.terms:
    records.append({
        "j": t.x_exp, "k": t.px_exp, "l": t.y_exp, "m": t.py_exp,
        "order": t.x_exp + t.px_exp + t.y_exp + t.py_exp,
        "coeff": t.coeff,
        "abs": abs(t.coeff),
        "phase": np.angle(t.coeff),
    })
df = pd.DataFrame(records).sort_values("abs", ascending=False)
# %%
# Overlay normal-form invariant curves on top of tracked orbits
plt.figure()
for Ix in np.linspace(0, 0.25, 2):
    theta_x = np.linspace(0, 2 * np.pi, 200)
    # Complex normal-form coordinates for a circle of action Ix
    zeta_1 = np.sqrt(2 * Ix) * np.exp(1j * theta_x)
    zeta_1_conj = np.conjugate(zeta_1)
    zeta_2 = np.zeros_like(zeta_1)
    zeta_2_conj = np.zeros_like(zeta_1)
    # Map from normal-form to physical normalised coordinates
    aux = poly_line1.normal_form.nf_to_norm(zeta_1, zeta_1_conj, zeta_2, zeta_2_conj)
    plt.plot(
        np.real(aux[0]),
        np.real(aux[1]),
        color="black",
        linestyle="-",
        label="Normal form" if Ix == 0 else None,
    )

plt.plot(
    orbits1["H_orbit_points"]["x"],
    orbits1["H_orbit_points"]["px"],
    color="red",
    marker=".",
    markersize=0.1,
    linestyle="None",
    label="Tracked orbits",
)
plt.xlabel("x [m]")
plt.ylabel("px [rad]")
plt.title("Normal-form invariant curves vs tracked orbits")
plt.axis("equal")

# %%
"""
Plot the amplitude spectrum predicted by Phi at given (Jx, Jy).
No tracking, no NAFF.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

# ===== INPUTS =====
Jx = 0.06   # [m·rad]
Jy = 0.0  # [m·rad]
n_label = 8     # how many top lines to annotate

# ===== TUNE WITH AMPLITUDE DETUNING (from diagonal H) =====
def amplitude_tunes(H, Qx0_frac, Qy0_frac, Jx, Jy):
    rows = [(t.x_exp, t.y_exp, complex(t.coeff)) for t in H.terms
            if t.x_exp == t.px_exp and t.y_exp == t.py_exp]
    df = (pd.DataFrame(rows, columns=["j", "l", "c"])
            .groupby(["j", "l"], as_index=False).sum())
    c10 = df.query("j==1 and l==0")["c"].iloc[0].imag
    c01 = df.query("j==0 and l==1")["c"].iloc[0].imag
    kx, ky = Qx0_frac / c10, Qy0_frac / c01
    Qx = kx * sum(r.c.imag * r.j * Jx**(r.j-1) * Jy**r.l
                  for r in df.itertuples() if r.j >= 1)
    Qy = ky * sum(r.c.imag * r.l * Jx**r.j * Jy**(r.l-1)
                  for r in df.itertuples() if r.l >= 1)
    return Qx, Qy

# ===== SPECTRUM FROM A LINEAR COMBO OF POLYNOMS =====
def combine_polys(*polys_factors):
    """Sum  factor_i * poly_i  aligned by monomial -> dict (j,k,l,m): coeff."""
    out = defaultdict(lambda: 0 + 0j)
    for poly, factor in polys_factors:
        for t in poly.terms:
            out[(t.x_exp, t.px_exp, t.y_exp, t.py_exp)] += factor * complex(t.coeff)
    return out

def spectrum(poly_dict, Jx, Jy, atol=1e-30):
    """Group by (nx, ny) = (j-k, l-m) and sum complex amplitudes."""
    spec = defaultdict(lambda: 0 + 0j)
    for (j, k, l, m), c in poly_dict.items():
        spec[(j - k, l - m)] += c * Jx**((j + k) / 2) * Jy**((l + m) / 2)
    df = pd.DataFrame([{"nx": nx, "ny": ny, "A": A, "abs_A": abs(A)}
                       for (nx, ny), A in spec.items()])
    return (df[df["abs_A"] > atol]
              .sort_values("abs_A", ascending=False)
              .reset_index(drop=True))

# ===== COMPUTE =====
nf, tw = poly_line1.normal_form, poly_line1.tw
Qx0, Qy0 = tw.qx % 1, tw.qy % 1
Qx, Qy   = amplitude_tunes(nf.H, Qx0, Qy0, Jx, Jy)

# Complex one-sided signals: h+_x = x_norm - i px_norm,  h+_y = y_norm - i py_norm
hxp = combine_polys((nf.Phi.x_poly, 1.0), (nf.Phi.px_poly, -1j))
hyp = combine_polys((nf.Phi.y_poly, 1.0), (nf.Phi.py_poly, -1j))

spec_x = spectrum(hxp, Jx, Jy)
spec_y = spectrum(hyp, Jx, Jy)
# wrap to [-0.5, 0.5)  instead of [0, 1)
for s in (spec_x, spec_y):
    s["freq"] = ((s["nx"] * Qx + s["ny"] * Qy + 0.5) % 1) - 0.5



# ===== PLOT =====
fig, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=True)
for ax, spec, label in zip(
        axes, [spec_x, spec_y],
        [r"$h_x^+ = x_n - i\,p_{x,n}$", r"$h_y^+ = y_n - i\,p_{y,n}$"]):
    ml, sl, bl = ax.stem(spec["freq"], spec["abs_A"], basefmt=" ")
    plt.setp(ml, markersize=4)
    for r in spec.head(n_label).itertuples():
        ax.annotate(f"({r.nx},{r.ny})", (r.freq, r.abs_A),
                    fontsize=8, ha="center", va="bottom",
                    xytext=(0, 3), textcoords="offset points")
    ax.set_yscale("log")
    ax.set_ylabel(f"|A|  on  {label}")
    ax.grid(alpha=0.3)

axes[0].set_title(rf"Spectrum from $\Phi$    "
                  rf"$J_x={Jx:.2e},\ J_y={Jy:.2e}$    "
                  rf"$Q_x={Qx:.5f},\ Q_y={Qy:.5f}$")
axes[1].set_xlabel("fractional tune")
axes[1].set_xlim(-0.5, 0.5)
plt.tight_layout()
plt.show()
# %%
