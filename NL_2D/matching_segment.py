# %%
# /mnt/hdd1/sterbini/IPAC2026_NL_matching/miniconda/bin/python
import numpy as np
import pandas as pd
import xtrack as xt

import matplotlib.pyplot as plt

# %%

import numpy as np
import matplotlib.pyplot as plt

import nafflib
import pytori as pt
import pytori.plotting as ptplt

# =======================
# Mesh parameters
x_tori_number = 20
x_start = np.linspace(0.0001,0.5,x_tori_number)
angular_points_number = 100
# ======================

# ========================
# Henon parameters
num_turns   = int(5e3)
Q0          = 0.2071
# ========================


# Generating tori
px_start   = 0. * x_start

tori    = []
tracking_list = []
for x0, px0 in zip(x_start, px_start):
    # Iterating Henon map
    x, px   = nafflib.henon_map(x0, px0, Q0, num_turns)
    _tracking = {}
    _tracking['x'] = x
    _tracking['px'] = px
    # Extracting harmonics:
    #============================================================================
    n_harm  = 50
    w_order = 4
    Ax,Qx   = nafflib.harmonics(x,px,num_harmonics = n_harm,window_order=w_order)
    _tracking['Ax'] = Ax
    _tracking['Qx'] = Qx
    #============================================================================

    # Indexing harmonics
    #============================================================================
    max_n       = 90 #(high numbers needed in 2D..)
    max_alias   = 50
    warning_tol = np.inf #Disable warnings
    Qvec    = [Qx[0]]
    nx      = nafflib.linear_combinations(Qx,Qvec = Qvec,max_n=max_n,max_alias=max_alias,warning_tol=warning_tol)
    _tracking['nx'] = nx
    #============================================================================

    # Building torus (2D-torus)
    #============================================================================
    _torus = pt.Torus.from_naff(n=[nx],A=[Ax])
    tori.append(_torus)
    tracking_list.append(_tracking)

    #============================================================================

for tracking in tracking_list[0:15]:
    plt.plot(tracking['x'][0:200], tracking['px'][0:200], '.', color='k', markersize=1)
for tracking in tracking_list[15:]:
    plt.plot(tracking['x'][0:200], tracking['px'][0:200], '.', color='r', markersize=1)

for tracking in tracking_list[0:15]:
    plt.plot(tracking['x'][0], tracking['px'][0], 's', color='k', markersize=3)

for tracking in tracking_list[15:]:
    plt.plot(tracking['x'][0], tracking['px'][0], 's', color='r', markersize=3)
plt.axis('equal')
plt.gca().set_box_aspect(1) 
plt.xlabel(r'$ x\ [\sqrt{\mathrm{m}}]$');
plt.ylabel(r'$ p_x\ [\sqrt{\mathrm{m}}]$');

# %% ---- Build the line ----
N, Lq, Ld = 12, 0.2, 1.0  # 12 quads, 0.2 m each, 1 m drifts between

twiss_init  = {'betx':1 ,'alfx': 0}
#------------------------------------------
gemitt_x = 1 
h1  = -1j/4  # non-linear strength parameter, Henon definition
k2l = -1j*8*h1/twiss_init['betx']**(3/2)/gemitt_x**(1/2) # sextupole strength
assert np.imag(k2l) == 0, "k2l should be real"
k2l = np.real(k2l)

line = xt.Line(elements={
    'tr.start'  : xt.Marker(),
    'sext'      : xt.Multipole(knl=[0,0,k2l], ksl=[0,0,0],length=0),
    # ==========================
    'd0'        : xt.Drift(length=Ld),
    'q1'        : xt.Quadrupole(length=Lq, k1=0.0),
    # --------------------------
    'd1'        : xt.Drift(length=Ld),
    'q2'        : xt.Quadrupole(length=Lq, k1=0.0),
    # --------------------------
    'd2'        : xt.Drift(length=Ld),
    'q3'        : xt.Quadrupole(length=Lq, k1=0.0),
    # --------------------------
    'd3'        : xt.Drift(length=Ld),
    'q4'        : xt.Quadrupole(length=Lq, k1=0.0),
    # --------------------------
    'd4'        : xt.Drift(length=Ld),
    'q5'        : xt.Quadrupole(length=Lq, k1=0.0),
    # --------------------------
    'd5'        : xt.Drift(length=Ld),
    'q6'        : xt.Quadrupole(length=Lq, k1=0.0),
    # --------------------------
    'd6'        : xt.Drift(length=Ld),
    'q7'        : xt.Quadrupole(length=Lq, k1=0.0),
    # --------------------------
    'd7'        : xt.Drift(length=Ld),
    'q8'        : xt.Quadrupole(length=Lq, k1=0.0),
    # --------------------------
    'd8'        : xt.Drift(length=Ld),
    'q9'        : xt.Quadrupole(length=Lq, k1=0.0),
    # --------------------------
    'd9'        : xt.Drift(length=Ld),
    'q10'       : xt.Quadrupole(length=Lq, k1=0.0),
    # --------------------------
    'd10'       : xt.Drift(length=Ld),
    'q11'       : xt.Quadrupole(length=Lq, k1=0.0),
    # --------------------------
    'd11'       : xt.Drift(length=Ld),
    'q12'       : xt.Quadrupole(length=Lq, k1=0.0),
    # ==========================
    'd_end'     : xt.Drift(length=Ld),
    'tr.end'    : xt.Marker(),
})
line.particle_ref = xt.Particles(p0c=7e12, mass0=xt.PROTON_MASS_EV, q0=1)

# %% Expose quad strengths as knobs
for i in range(N):
    line.vars[f'k{i+1}'] = 0.0
    line.element_refs[f'q{i+1}'].k1 = line.vars[f'k{i+1}']

# %% Reasonable FODO-like seed (alternating signs)
seed = [5.033571436491605,
-4.320388955493479,
4.3661443771168695,
-4.155299019583114,
4.229837411481433,
-1.510083731703031,
-1.520774771579453,
4.209451369946942,
-4.207158224932284,
4.471753297307329,
-4.3479587631873855,
4.70666622112177,
]

for i, k in enumerate(seed):
    line.vars[f'k{i+1}'] = k

# # %% ---- Boundary conditions ----
# init = xt.TwissInit(betx=1.0, alfx=0.0, bety=1.0, alfy=0.0,
#                     element_name='tr.start', line=line)

# %% ---- Step 1: find a reference solution at some (μx0, μy0) ----
mux0, muy0 = (1+.2071), 0.8  # cycles, not radians
line.match(
    betx=1, bety=1, alfx=0, alfy=0,
    vary=[xt.VaryList([f'k{i+1}' for i in range(N)], step=1e-5)],
    targets=[
        xt.Target('betx', 1.0, at='tr.end'),
        xt.Target('alfx', 0.0, at='tr.end'),
        xt.Target('bety', 1.0, at='tr.end'),
        xt.Target('alfy', 0.0, at='tr.end'),
        xt.Target('mux',  mux0, at='tr.end'),
        # xt.Target('muy',  muy0, at='tr.end'),
    ],
)
#plot twiss4d
init = xt.TwissInit(betx=1.0, alfx=0.0, bety=1.0, alfy=0.0,
                    element_name='tr.start', line=line)
tw = line.twiss(method = '4d',init=init, start='tr.start', end='tr.end')
plt.plot(tw['s'], tw['betx'])
plt.plot(tw['s'], tw['bety'])

plt.figure()
plt.plot(tw['s'], tw['mux'])
plt.plot(tw['s'], tw['muy'])
for i, k in enumerate(seed):
    print(line.vars[f'k{i+1}']._value)
    
print(tw.mux[-1], tw.muy[-1])
# %%
import xobjects as xo

#=========================================================================================
nrj             = 7000e9
nemitt_x        = None
nemitt_y        = None
#-----------------------------------------------------------------------------------------
context         = xo.ContextCpu(omp_num_threads='auto')
particle_ref    = xt.Particles(p0c=nrj, q0=1, mass0=xt.PROTON_MASS_EV)
gemitt_x        = 1 if nemitt_x is None else ( nemitt_x / particle_ref.beta0[0] / particle_ref.gamma0[0])
gemitt_y        = 1 if nemitt_x is None else ( nemitt_y / particle_ref.beta0[0] / particle_ref.gamma0[0])
line.particle_ref   = particle_ref
#line.build_tracker(_context=context)
line.freeze_longitudinal(True)
twiss   = line.twiss4d()


# %%
num_turns = int(5e3)

x_start = np.linspace(0.0001,0.5,x_tori_number)

# Initialize particles in CS-normalized phase space
#=======================================================================
particles = line.build_particles(   x_norm   = x_start,
                                    method   = '4d',
                                    nemitt_x = nemitt_x,
                                    nemitt_y = nemitt_y,
                                    nemitt_zeta     = None,
                                    W_matrix        = twiss.W_matrix[0],
                                    particle_on_co  = twiss.particle_on_co.copy(),
                                    _context        = context)
line.config.XTRACK_GLOBAL_XY_LIMIT = 3

line.track(particles, num_turns= num_turns,turn_by_turn_monitor=True,with_progress=True)
# %%
mon = line.record_last_track
n = 200

plt.figure(figsize=(5, 5))
for tracking in tracking_list[0:15]:
    plt.plot(tracking['x'][0:n], tracking['px'][0:n], 'x', color='k', markersize=3)
for tracking in tracking_list[15:]:
    plt.plot(tracking['x'][0:n], tracking['px'][0:n], 'x', color='r', markersize=3)



for ii in range(x_tori_number):
    plt.plot(mon.x[ii, :n], mon.px[ii, :n], ".b", markersize=2)

for tracking in tracking_list[0:15]:
    plt.plot(tracking['x'][0], tracking['px'][0], 's', color='k', markersize=3)

for tracking in tracking_list[15:]:
    plt.plot(tracking['x'][0], tracking['px'][0], 's', color='r', markersize=3)

plt.xlabel("x [m]")
plt.ylabel("px")
plt.title("Particle 0 — first 200 turns")
#plt.axis("equal")
plt.tight_layout()
# %%
# %%
strengths = line.get_strengths()

from xtrack import rdt_first_order_perturbation

my_dict = {}

# corresponding the the n=-2 line
my_dict[-2] = [
    'f3000',
]

# corresponding the the n=0 line
my_dict[0] = [
    'f2100',
]

# corresponding the the n=1 line
# my_dict[1] = [
#     "f1100",
#     "f2200",
#     "f3300",
# ]


# corresponding the the n=2 line
my_dict[2] = [
    "f0100",
    "f1200",
    "f2300",
]

# corresponding the the n=3 line
# my_dict[3] = [
#     "f0200",
#     "f1300",
#     "f2400",
# ]

# corresponding the the n=4 line
# my_dict[4] = [
#     "f0300",
#     "f1400",
# ]

# corresponding the the n=5 line
# my_dict[5] = [
#     "f0400",
#     ]






# Compute RDT results once (independent of Ix)
rdt_results = {}
for nn in my_dict.keys():
    rdt_results[nn] = rdt_first_order_perturbation(
        rdt=my_dict[nn],
        twiss=twiss,
        strengths=strengths,
        feed_down=True,
    )

# %% Build the torus
phi = np.linspace(0, 2 * np.pi, 1000)

plt.figure(figsize=(5, 5))
for Ix in np.linspace(0, np.sqrt(0.05), 20)[1:]**2:
    phasors = {}
    for nn in my_dict.keys():
        my_result = 0
        for rdt in my_dict[nn]:
            p = int(rdt[1:2])
            q = int(rdt[2:3])
            my_result += -2*1j*p*(2*Ix)**((p+q-1)/2)*p*rdt_results[nn][rdt][0]
        phasors[nn] = my_result
    phasors[1] = np.sqrt(2*Ix)

    # X - 1j*Px = sum_n  phasors[n] * exp(1j * n * phi)
    z = sum(phasors[nn] * np.exp(1j * nn * phi) for nn in phasors)
    plt.plot(np.real(z), -np.imag(z))

plt.xlabel('x')
plt.ylabel('px')
plt.axis('equal')
plt.tight_layout()

for ii in range(15):
    plt.plot(mon.x[ii, :n], mon.px[ii, :n], ".b", markersize=1)

# %%
