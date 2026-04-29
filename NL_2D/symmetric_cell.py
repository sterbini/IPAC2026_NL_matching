# %% Imports

# %%
import numpy as np
import matplotlib.pyplot as plt
import xtrack as xt

# %% Lattice definition
# ──────────────────────────────────────────────────────────────────────────────
# Symmetric cell with 6 independent quadrupole families.
#
# Layout (→ right):
#   QF1/2 – D – QD1 – D/2 – QF3 – D/2 – QF2 – D/4 – QD3 – D/4 – [QD2] – D/4 – QD3 – D/4 – QF2 – D/2 – QF3 – D/2 – QD1 – D – QF1/2
#
# By construction qf1.l / qf1.r share k1f1, and so on for the other families.
# Mirror symmetry (palindrome) gives M₁₁=M₂₂. This alone does NOT guarantee
# alfx=alfy=0 at exit. However, once betx=bety=1 is also matched at exit,
# symplecticity forces M₂₁=−M₁₂ and alfx=alfy=0 follows automatically.
# Free variables k1f1, k1d1, k1f2, k1d2, k1f3, k1d3 → match betx=bety=1, alfx=alfy=0, mux, muy.
# ──────────────────────────────────────────────────────────────────────────────

Lq = 0.3   # quadrupole length [m]
Ld = 1.5   # inter-quadrupole drift [m]

env = xt.Environment()
env.vars({
    'k1f1':  1.0,   # QF1: outer focusing quads (half-length at each end)
    'k1d1': -0.8,   # QD1: outer defocusing quads
    'k1f3':  0.4,   # QF3: mid focusing quads (in d2 drift)
    'k1f2':  0.5,   # QF2: inner focusing quads
    'k1d3': -0.2,   # QD3: inner defocusing quads (in d3 drift)
    'k1d2': -0.3,   # QD2: central defocusing quad (full, at symmetry point)
})

line = env.new_line(components=[
    # ── left half ─────────────────────────────────────────────────────────
    env.new('qf1.l',  xt.Quadrupole, k1='k1f1', length=Lq / 2),
    env.new('d1.l',   xt.Drift,                 length=Ld),
    env.new('qd1.l',  xt.Quadrupole, k1='k1d1', length=Lq),
    env.new('d2a.l',  xt.Drift,                 length=Ld / 2),
    env.new('qf3.l',  xt.Quadrupole, k1='k1f3', length=Lq),
    env.new('d2b.l',  xt.Drift,                 length=Ld / 2),
    env.new('qf2.l',  xt.Quadrupole, k1='k1f2', length=Lq),
    env.new('d3a.l',  xt.Drift,                 length=Ld / 4),
    env.new('qd3.l',  xt.Quadrupole, k1='k1d3', length=Lq),
    env.new('d3b.l',  xt.Drift,                 length=Ld / 4),
    # ── centre (symmetry point) ───────────────────────────────────────────
    env.new('qd2',    xt.Quadrupole, k1='k1d2', length=Lq),
    # ── right half (mirror) ───────────────────────────────────────────────
    env.new('d3b.r',  xt.Drift,                 length=Ld / 4),
    env.new('qd3.r',  xt.Quadrupole, k1='k1d3', length=Lq),
    env.new('d3a.r',  xt.Drift,                 length=Ld / 4),
    env.new('qf2.r',  xt.Quadrupole, k1='k1f2', length=Lq),
    env.new('d2b.r',  xt.Drift,                 length=Ld / 2),
    env.new('qf3.r',  xt.Quadrupole, k1='k1f3', length=Lq),
    env.new('d2a.r',  xt.Drift,                 length=Ld / 2),
    env.new('qd1.r',  xt.Quadrupole, k1='k1d1', length=Lq),
    env.new('d1.r',   xt.Drift,                 length=Ld),
    env.new('qf1.r',  xt.Quadrupole, k1='k1f1', length=Lq / 2),
])

line.particle_ref = xt.Particles(mass0=0.511e-3, q0=-1, p0c=1.0)  # electron with 1 GeV/c

# %% Initial Twiss (before matching)
tw0 = line.twiss(
    method='4d',
    init=xt.TwissInit(betx=1.0, alfx=0.0, bety=1.0, alfy=0.0),
)

print('Before matching – Twiss at exit:')
print(f'  betx = {tw0.betx[-1]:.4f}   alfx = {tw0.alfx[-1]:.4f}')
print(f'  bety = {tw0.bety[-1]:.4f}   alfy = {tw0.alfy[-1]:.4f}')
print(f'  mux  = {tw0.mux[-1]:.4f}    muy  = {tw0.muy[-1]:.4f}   [2π]')

# %% Matching
# ──────────────────────────────────────────────────────────────────────────────
# Set the desired phase advances here.
# alfx = alfy = 0 at exit follows automatically once betx=bety=1 is matched (palindrome symmetry).
# 6 targets (betx, bety, alfx, alfy, mux, muy) for 6 free variables.
# ──────────────────────────────────────────────────────────────────────────────

mux_target = 1.25   # [2π]
muy_target  = 0.20  # [2π]

opt = line.match(
    method='4d',
    init=xt.TwissInit(betx=1.0, alfx=0.0, bety=1.0, alfy=0.0),
    vary=[
        xt.Vary('k1f1', step=1e-12),
        xt.Vary('k1d1', step=1e-12),
        xt.Vary('k1f3', step=1e-12),
        xt.Vary('k1f2', step=1e-12),
        xt.Vary('k1d3', step=1e-12),
        xt.Vary('k1d2', step=1e-12),
    ],
    targets=[
        xt.Target('betx', 1.0,        at=xt.END, tol=1e-6),
        xt.Target('bety', 1.0,        at=xt.END, tol=1e-6),
        xt.Target('alfx', 0.0,        at=xt.END, tol=1e-6),
        xt.Target('alfy', 0.0,        at=xt.END, tol=1e-6),
        xt.Target('mux',  0.6, at=xt.END, tol=1e-1),
        #xt.Target('muy',  0.20, at=xt.END, tol=1e-6),
    ],
)

# %% Verification and plot
tw = line.twiss(
    method='4d',
    init=xt.TwissInit(betx=1.0, alfx=0.0, bety=1.0, alfy=0.0),
)

print('\nAfter matching – Twiss at exit:')
print(f'  betx = {tw.betx[-1]:.6f}   alfx = {tw.alfx[-1]:.2e}')
print(f'  bety = {tw.bety[-1]:.6f}   alfy = {tw.alfy[-1]:.2e}')
print(f'  mux  = {tw.mux[-1]:.6f}    muy  = {tw.muy[-1]:.6f}   [2π]')

print('\nMatched quad strengths [m⁻²]:')
for var in ['k1f1', 'k1d1', 'k1f3', 'k1f2', 'k1d3', 'k1d2']:
    print(f'  {var} = {line.vars[var]._value:+.6f}')

fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

axes[0].plot(tw.s, tw.betx, label=r'$\beta_x$')
axes[0].plot(tw.s, tw.bety, label=r'$\beta_y$', ls='--')
axes[0].set_ylabel(r'$\beta\;[\mathrm{m}]$')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].plot(tw.s, tw.mux, label=r'$\mu_x\;[2\pi]$')
axes[1].plot(tw.s, tw.muy, label=r'$\mu_y\;[2\pi]$', ls='--')
axes[1].set_xlabel('s [m]')
axes[1].set_ylabel(r'$\mu\;[2\pi]$')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.suptitle(
    rf'Symmetric cell  –  '
    rf'$\mu_x = {mux_target}\times2\pi$,  $\mu_y = {muy_target}\times2\pi$'
    '\n'
    rf'Exit: $\beta_x={tw.betx[-1]:.4f}$ m, $\alpha_x={tw.alfx[-1]:.1e}$, '
    rf'$\beta_y={tw.bety[-1]:.4f}$ m, $\alpha_y={tw.alfy[-1]:.1e}$'
)
plt.tight_layout()
plt.savefig('../plots/symmetric_cell_twiss.pdf', dpi=150, bbox_inches='tight')
plt.show()

# %%
