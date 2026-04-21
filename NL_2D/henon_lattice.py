# %% Imports

import numpy as np
import matplotlib.pyplot as plt
import xtrack as xt
import nafflib

# %% Parameters
Q0        = 0.2071        # fractional tune
num_turns = int(5e3)

# Initial conditions
x0_list  = np.linspace(0.0001, 0.5, 20)
px0_list = 0.0 * x0_list

# %% Build xsuite Hénon lattice
# Hénon map: Δpx = +x²  →  xt.Multipole with k2l = -2 (since Δpx = -k2l/2 * x²)
henon_kick = xt.Multipole(knl=[0, 0, -2.0])

# Linear rotation in Floquet (normalized) coords: beta=1, alpha=0
linear_map = xt.LineSegmentMap(
    qx=Q0,
    betx=1.0, alfx=0.0,
    qy=0.31,                        # decoupled dummy y-plane
    bety=1.0, alfy=0.0,
)

n_part = len(x0_list)
p = xt.Particles(
    x=x0_list.copy(), px=px0_list.copy(),
    y=np.zeros(n_part), py=np.zeros(n_part),
    zeta=np.zeros(n_part), delta=np.zeros(n_part),
)

line = xt.Line(
    elements=[henon_kick, linear_map],
    element_names=['henon_kick', 'linear_map'],
)

# %%
line.build_tracker()
particle_ref = line.build_particles(p)
strengths = line.get_strengths()

# %%
# All 4th-order RDTs (n = p+q+r+t = 4)
rdts_4th = [
    "f4000",
    "f3100", 
    "f2200",
    "f2020",  
    "f2002",  
    "f1120", 
    "f1102", 
    "f0040", 
    "f0031", 
]

result = rdt_first_order_perturbation(
    rdt=rdts_4th,
    twiss=tw,
    strengths=strengths,
    feed_down=True,
)

# %% Track with xsuite
n_part = len(x0_list)
p = xt.Particles(
    x=x0_list.copy(), px=px0_list.copy(),
    y=np.zeros(n_part), py=np.zeros(n_part),
    zeta=np.zeros(n_part), delta=np.zeros(n_part),
)
line.track(p, num_turns=num_turns, turn_by_turn_monitor=True)
mon = line.record_last_track   # mon.x shape: (n_part, num_turns)

# %% Track with nafflib for comparison
x_naff_list  = []
px_naff_list = []
for x0, px0 in zip(x0_list, px0_list):
    x_n, px_n = nafflib.henon_map(x0, px0, Q0, num_turns)
    x_naff_list.append(x_n)
    px_naff_list.append(px_n)

# %% Compare phase-space portraits (first particle)
fig, axes = plt.subplots(1, 2, figsize=(10, 5))

n_show = 500   # turns to display

ax = axes[0]
ax.set_title('nafflib')
for x_n, px_n in zip(x_naff_list, px_naff_list):
    ax.plot(x_n[:n_show], px_n[:n_show], '.k', ms=1, alpha=0.5)
ax.set_aspect('equal')
ax.set_xlabel(r'$x$')
ax.set_ylabel(r'$p_x$')

ax = axes[1]
ax.set_title('xsuite')
for i in range(n_part):
    ax.plot(mon.x[i, :n_show], mon.px[i, :n_show], '.r', ms=1, alpha=0.5)
ax.set_aspect('equal')
ax.set_xlabel(r'$x$')
ax.set_ylabel(r'$p_x$')

plt.tight_layout()
plt.savefig('../plots/henon_comparison.pdf', dpi=300, bbox_inches='tight')
plt.show()

# %% Residual check (single particle, first trajectory)
x_xs  = mon.x[0]
px_xs = mon.px[0]
x_nf, px_nf = x_naff_list[0], px_naff_list[0]

residual_x  = np.max(np.abs(x_xs  - x_nf))
residual_px = np.max(np.abs(px_xs - px_nf))
print(f'Max |Δx|  = {residual_x:.2e}')
print(f'Max |Δpx| = {residual_px:.2e}')

# %% Analytical RDT f_{h000}
import math

def f_h000_analytical(h, knl, beta=1.0, Q=Q0, phase=0.0):
    """
    First-order RDT f_{h000} from a single thin-multipole element.
    Only the h-pole (knl[h-1]) contributes at first order.
    h_{h000} = knl[h-1] * beta^{h/2} * exp(i*h*phase) / (h! * 2^h)
    f_{h000} = h_{h000} / (1 - exp(2*pi*i*h*Q))
    |f_{h000}| = |knl[h-1]| * beta^{h/2} / (h! * 2^h * 2*|sin(h*pi*Q)|)
    """
    if h < 1 or h - 1 >= len(knl) or knl[h - 1] == 0:
        return 0.0 + 0j
    k_hL = knl[h - 1]
    h_coeff = k_hL * beta ** (h / 2) * np.exp(1j * h * phase) / (math.factorial(h) * 2 ** h)
    denom = 1 - np.exp(2j * np.pi * h * Q)
    return h_coeff / denom


def f_h000_magnitude(h, knl, beta=1.0, Q=Q0):
    """Magnitude of f_{h000} (no phase needed)."""
    if h < 1 or h - 1 >= len(knl) or knl[h - 1] == 0:
        return 0.0
    return abs(knl[h - 1]) * beta ** (h / 2) / (math.factorial(h) * 2 ** h * 2 * abs(np.sin(h * np.pi * Q)))


# Test for Hénon sextupole: knl = [0, 0, -2]  → only h=3 is non-zero
knl_henon = [0, 0, -2.0]
print("Analytical RDTs for Hénon map (beta=1, Q=Q0):")
for h in [1, 2, 3, 4]:
    f   = f_h000_analytical(h, knl_henon)
    mag = f_h000_magnitude(h, knl_henon)
    print(f"  |f_{{{h}000}}| = {abs(f):.6e}   (formula: {mag:.6e})")

# %%
