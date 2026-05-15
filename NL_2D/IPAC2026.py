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
x_tori_number = 50
x_start = np.linspace(0.0001,0.5*50/20,x_tori_number)
angular_points_number = 100
# ======================

# ========================
# Henon parameters
num_turns   = int(5e4)
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
    
    tracking_list.append(_tracking)
# %%
for tracking in tracking_list[0:16]:
    plt.plot(tracking['x'][0:500], tracking['px'][0:500], '.', color='k', markersize=1)
for tracking in tracking_list[16:32]:
    plt.plot(tracking['x'][0:500], tracking['px'][0:500], '.', color='r', markersize=1)

for tracking in tracking_list[32:]:
    plt.plot(tracking['x'][0:500], tracking['px'][0:500], '.', color='m', markersize=1)

# for tracking in tracking_list[0:15]:
#     plt.plot(tracking['x'][0], tracking['px'][0], 's', color='k', markersize=3)

# for tracking in tracking_list[15:]:
#     plt.plot(tracking['x'][0], tracking['px'][0], 's', color='r', markersize=3)
plt.axis('equal')
plt.gca().set_box_aspect(1) 
plt.xlabel(r'$ x\ [\sqrt{\mathrm{m}}]$');
plt.ylabel(r'$ p_x\ [\sqrt{\mathrm{m}}]$');
plt.savefig('../plots/henon_map.pdf', dpi=300, bbox_inches='tight')
plt.xlim(-1, 1)
plt.ylim(-1, 1)
# put ticks at 0 0.5, 1
plt.xticks([-1, -0.5, 0, 0.5, 1])
plt.yticks([-1, -0.5, 0, 0.5, 1])
plt.savefig('../plots/henon_map_only_first_500.pdf', dpi=300, bbox_inches='tight')
# %% KAM evolution

# total_turns = 50000
# step = 500
# turn_ranges = [(s, s + step) for s in range(0, total_turns, step)]
turn_ranges = [
    (0, 500),
    (500, 1000),
    (1000, 1500),
    (1500, 2000),
    (2000, 2500),
    (9500, 10000),
    (19500, 20000),
    (29500, 30000),
    (39500, 40000),
    (49500, 50000)
]

for start_turn, end_turn in turn_ranges:
    fig = plt.figure(figsize=(5, 5.5))
    gs = fig.add_gridspec(2, 1, height_ratios=[10, 1], hspace=0.3)
    ax = fig.add_subplot(gs[0])
    ax_bar = fig.add_subplot(gs[1])

    for tracking in tracking_list[0:16]:
        ax.plot(tracking['x'][start_turn:end_turn], tracking['px'][start_turn:end_turn], '.', color='k', markersize=1)
    for tracking in tracking_list[16:32]:
        ax.plot(tracking['x'][start_turn:end_turn], tracking['px'][start_turn:end_turn], '.', color='r', markersize=1)
    for tracking in tracking_list[32:]:
        ax.plot(tracking['x'][start_turn:end_turn], tracking['px'][start_turn:end_turn], '.', color='m', markersize=1)

    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_xticks([-1, -0.5, 0, 0.5, 1])
    ax.set_yticks([-1, -0.5, 0, 0.5, 1])
    ax.set_xlabel(r'$ x\ [\sqrt{\mathrm{m}}]$')
    ax.set_ylabel(r'$ p_x\ [\sqrt{\mathrm{m}}]$')

    # Progress bar
    ax_bar.set_xlim(0, total_turns)
    ax_bar.set_ylim(0, 1)
    # Full background
    ax_bar.barh(0.5, total_turns, left=0, height=1, color='lightgray', align='center', zorder=0)
    # Current segment only (not from 0)
    ax_bar.barh(0.5, step, left=start_turn, height=1, color='green', align='center', zorder=1)
    #ax_bar.text(start_turn + step / 2, 0.5, f'{start_turn}–{end_turn}',
    #            ha='center', va='center', fontsize=8, color='white', fontweight='bold')
    ax_bar.set_xticks(range(0, total_turns + 1, 10000), labels=[f'{t//1000}k' for t in range(0, total_turns + 1, 10000)])
    ax_bar.set_yticks([])
    ax_bar.set_xlabel('Turns')

    plt.savefig(f'../plots/henon_map_only_last_{end_turn}_{start_turn}.pdf', dpi=300, bbox_inches='tight')
    plt.show()
# %%
fig, ax = plt.subplots(figsize=(5, 5))
for tracking in tracking_list[0:16]:
    ax.plot(tracking['x'][0:500], tracking['px'][0:500], '.', color='k', markersize=1)
ax.set_aspect('equal', adjustable='box')
ax.set_xlim(-0.43, 0.43)
ax.set_ylim(-0.43, 0.43)
ax.set_xlabel(r'$ x\ [\sqrt{\mathrm{m}}]$')
ax.set_ylabel(r'$ p_x\ [\sqrt{\mathrm{m}}]$')
plt.savefig('../plots/henon_map_zoom_nonresonant.pdf', dpi=300, bbox_inches='tight')
plt.show()
# %%
r = 0.33
theta = np.linspace(0, 2 * np.pi, 200)
fig, ax = plt.subplots(figsize=(5, 5))
for tracking in tracking_list[0:16]:
    ax.plot(tracking['x'][0:500], tracking['px'][0:500], '.', color='k', markersize=1)
ax.fill(r * np.cos(theta), r * np.sin(theta), color='green', alpha=0.3, zorder=0)
ax.plot(r * np.cos(theta), r * np.sin(theta), '-', color='green', linewidth=1)
ax.set_aspect('equal', adjustable='box')
ax.set_xlim(-0.43, 0.43)
ax.set_ylim(-0.43, 0.43)
ax.set_xlabel(r'$ x\ [\sqrt{\mathrm{m}}]$')
ax.set_ylabel(r'$ p_x\ [\sqrt{\mathrm{m}}]$')
plt.savefig('../plots/henon_map_zoom_nonresonant_circle.pdf', dpi=300, bbox_inches='tight')
plt.show()
# %%
# =======================
# Mesh parameters
x_tori_number = 20
x_start = np.linspace(0.0001,0.5,x_tori_number)
# x_tori_number = 50
# x_start = np.linspace(0.0001,0.5*50/20,x_tori_number)
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
    #Extracting harmonics:
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

    #=====================================
# %%
for tracking in tracking_list[0:15]:
    plt.plot(tracking['x'][0:200], tracking['px'][0:200], '.', color='k', markersize=1)
# for tracking in tracking_list[15:30]:
#     plt.plot(tracking['x'][0:200], tracking['px'][0:200], '.', color='r', markersize=1)

# for tracking in tracking_list[30:]:
#     plt.plot(tracking['x'][0:200], tracking['px'][0:200], '.', color='m', markersize=1)

# for tracking in tracking_list[0:15]:
#     plt.plot(tracking['x'][0], tracking['px'][0], 's', color='k', markersize=3)

# for tracking in tracking_list[15:]:
#     plt.plot(tracking['x'][0], tracking['px'][0], 's', color='r', markersize=3)
plt.axis('equal')
plt.gca().set_box_aspect(1) 
plt.xlabel(r'$ x\ [\sqrt{\mathrm{m}}]$');
plt.ylabel(r'$ p_x\ [\sqrt{\mathrm{m}}]$');
plt.savefig('../plots/henon_map.pdf', dpi=300, bbox_inches='tight')
plt.xlim(-1, 1)
plt.ylim(-1, 1)
# put ticks at 0 0.5, 1
plt.xticks([-1, -0.5, 0, 0.5, 1])
plt.yticks([-1, -0.5, 0, 0.5, 1])

#plot an annulus from 0.1 to 0.3
annulus_inner = 0
annulus_outer = 0.33
theta = np.linspace(0, 2 * np.pi, 50)
# outer circle
x_outer = annulus_outer * np.cos(theta[::-1])
px_outer = annulus_outer * np.sin(theta[::-1])

# inner circle (reverse direction to make a proper closed annulus)
x_inner = annulus_inner * np.cos(theta)
px_inner = annulus_inner * np.sin(theta)
  
plt.plot(x_inner, px_inner, 'g',lw=2,label='Inner Annulus')
plt.plot(x_outer, px_outer, 'g',lw=2,label='Outer Annulus')

x = np.concatenate([x_outer, x_inner])
y = np.concatenate([px_outer, px_inner])

plt.fill(x, y, color='green', alpha=.5)
plt.gca().set_aspect('equal')

# put ticks at 0 0.5, 1
plt.xlabel(r'$ x\ [\sqrt{\mathrm{m}}]$');
plt.ylabel(r'$ p_x\ [\sqrt{\mathrm{m}}]$');
plt.xticks([-0.4, 0, 0.4])
plt.yticks([-0.4, 0, 0.4])
plt.xlim(-0.43, 0.43)
plt.ylim(-0.43, 0.43)

plt.savefig('../plots/henon_map_and_distribution.pdf', dpi=300, bbox_inches='tight')    
# %% same as above but without the annulus
plt.figure(figsize=(5, 5))
for tracking in tracking_list[0:15]:
    plt.plot(tracking['x'][0:200], tracking['px'][0:200], '.', color='k', markersize=1)
plt.axis('equal')
plt.gca().set_box_aspect(1)
plt.xlabel(r'$ x\ [\sqrt{\mathrm{m}}]$');           
plt.ylabel(r'$ p_x\ [\sqrt{\mathrm{m}}]$');
plt.xlim(-0.43, 0.43)
plt.ylim(-0.43, 0.43)
# put ticks at 0 0.5, 1
plt.xticks([-0.5, 0, 0.5])
plt.yticks([-0.5, 0, 0.5])
plt.savefig('../plots/henon_map_zoom.pdf', dpi=300, bbox_inches='tight')

# %% same as above but with the external tori in red and the internal tori in gray
plt.figure(figsize=(3, 3))
plt.rcParams.update({'font.size': 11})

for tracking in tracking_list[0:14]:
    plt.plot(tracking['x'][0:200], tracking['px'][0:200], '.', color='gray', markersize=1, alpha=.1)
for tracking in tracking_list[14:15]:
    plt.plot(tracking['x'][0:200], tracking['px'][0:200], '.', color='red', markersize=1)
plt.axis('equal')
plt.gca().set_box_aspect(1)
plt.xlabel(r'$ x\ [\sqrt{\mathrm{m}}]$');           
plt.ylabel(r'$ p_x\ [\sqrt{\mathrm{m}}]$');
plt.xlim(-0.43, 0.43)
plt.ylim(-0.43, 0.43)
# put ticks at 0 0.5, 1
# plt.xticks([-0.5, 0, 0.5])
# plt.yticks([-0.5, 0, 0.5])
plt.savefig('../plots/henon_map_zoom_red_gray.pdf', dpi=300, bbox_inches='tight')

# %%
# Plotting the harmonic analysis
plt.rcParams.update({'font.size': 11})

bbox_props = dict(boxstyle='round,pad=0.1', facecolor='white', alpha=0.7, edgecolor='none')
max_terms_list = [3, 4, 5, 10, 50]
colors = plt.cm.plasma(np.linspace(0.1, 0.9, len(max_terms_list)))
n_max_values = np.arange(1, 51)

for torus_idx in range(15):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 6),
                                    gridspec_kw={'height_ratios': [4, 3]})

    # ── Top panel: harmonic spectrum ──────────────────────────────────────────
    ax1.semilogy(tracking_list[torus_idx]['Qx'], np.abs(tracking_list[torus_idx]['Ax']), '.', color='k', ms=6, alpha=1)
    ymin = ax1.get_ylim()[0]
    ax1.vlines(tracking_list[torus_idx]['Qx'], ymin, np.abs(tracking_list[torus_idx]['Ax']),
               colors='k', lw=0.5, alpha=0.5)
    for ii in range(50):
        if np.abs(tracking_list[torus_idx]['nx'][ii][0]) < 3:
            ax1.annotate('n=' + str(tracking_list[torus_idx]['nx'][ii][0]),
                         xy=(tracking_list[torus_idx]['Qx'][ii], np.abs(tracking_list[torus_idx]['Ax'][ii])),
                         xytext=(0, 4), textcoords='offset points',
                         ha='center', va='bottom', fontsize=9, bbox=bbox_props)
        else:
            ax1.annotate(str(tracking_list[torus_idx]['nx'][ii][0]),
                         xy=(tracking_list[torus_idx]['Qx'][ii], np.abs(tracking_list[torus_idx]['Ax'][ii])),
                         xytext=(0, 4), textcoords='offset points',
                         ha='center', va='bottom', fontsize=9, bbox=bbox_props)
    ax1.set_xlabel(r'frequency [1/turn]')
    ax1.set_ylabel(r'$ |A_n|$ $[\sqrt{\mathrm{m}}]$')
    ax1.set_title(f'torus {torus_idx}')

    # ── Bottom panel: 1/2 * Sum_{n=1}^{n_max} n |A_n|^2 vs n_max ─────────────
    Ax = tracking_list[torus_idx]['Ax']
    action_sum = np.array([
        0.5 * np.sum([(n + 1) * np.abs(Ax[n])**2 for n in range(n_max)])
        for n_max in n_max_values
    ])
    action_sum_norm = action_sum / action_sum[-1]

    ax2.semilogy(n_max_values, action_sum_norm, '.-', color='k', lw=1, ms=3)
    for idx, n_max in enumerate(max_terms_list):
        ax2.semilogy(n_max, action_sum_norm[n_max - 1], 's', color=colors[idx],
                     ms=7, label=f'$n_{{max}}={n_max}$')

    ax2.set_xlabel(r'$n_\mathrm{max}$')
    ax2.set_ylabel(r'$\frac{1}{2} \sum_{n=1}^{n_\mathrm{max}} n\,|A_n|^2$ [arb. units]')
    ax2.set_yticks([0.9, 1.0])
    ax2.get_yaxis().set_major_formatter(plt.ScalarFormatter())
    ax2.yaxis.set_minor_locator(plt.NullLocator())
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=8, ncol=2, loc='lower right')

    plt.tight_layout()
    plt.savefig(f'../plots/harmonic_analysis_torus{torus_idx:02d}.pdf', dpi=300, bbox_inches='tight')
    plt.close()

# %% Only frequency content for torus 14
fig, ax = plt.subplots(figsize=(3, 3))
Qx = tracking_list[14]['Qx']
Ax = np.abs(tracking_list[14]['Ax'])
ax.semilogy(Qx, Ax, '.', color='k', ms=6, alpha=1)
ymin = ax.get_ylim()[0]
ax.vlines(Qx, ymin, Ax, colors='k', lw=0.5, alpha=0.5)
ax.set_xlabel('frequency [1/turn]')
ax.set_ylabel(r'$|A_n|\ [\sqrt{\mathrm{m}}]$')
plt.tight_layout()
# only xticks at -0.5, 0, 0.5
plt.xticks([-0.5, 0, 0.5])
plt.savefig('../plots/harmonic_spectrum_torus14.pdf', dpi=300, bbox_inches='tight')
plt.show()

# %% Only frequency content for torus 14 + annotation of the main harmonics
fig, ax = plt.subplots(figsize=(3, 3))
Qx = tracking_list[14]['Qx']
Ax = np.abs(tracking_list[14]['Ax'])
nx = tracking_list[14]['nx']
ax.semilogy(Qx, Ax, '.', color='k', ms=6, alpha=1)
ymin = ax.get_ylim()[0]
ax.vlines(Qx, ymin, Ax, colors='k', lw=0.5, alpha=0.5)
bbox_props = dict(boxstyle='round,pad=0.05', facecolor='white', alpha=0.7, edgecolor='none')
for ii in range(len(Qx)):
    n = nx[ii][0]
    if np.abs(n) <= 26:
        label = f'n={n}' if np.abs(n) < 3 else str(n)
        if n not in {-2, -1, 0, 1, 2}:
            x_offset = 0.02 if n > 0 else -0.02
            ax.annotate(label,
                        xy=(Qx[ii], Ax[ii]),
                        xytext=(Qx[ii] + x_offset, Ax[ii]*1.2),
                        textcoords='data',
                        ha='center', va='bottom', fontsize=5.5, color='r', bbox=bbox_props)
        else:
            ax.annotate(label,
                        xy=(Qx[ii], Ax[ii]),
                        xytext=(0, 3), textcoords='offset points',
                        ha='center', va='bottom', fontsize=6, color='r', bbox=bbox_props)
ax.set_xlabel('frequency [1/turn]')
ax.set_ylabel(r'$|A_n|\ [\sqrt{\mathrm{m}}]$')
plt.xticks([-0.5, 0, 0.5])
plt.tight_layout()
plt.savefig('../plots/harmonic_spectrum_torus14_annotated.pdf', dpi=300, bbox_inches='tight')
plt.show()

# %% From the spectrum to the torus
Tx = np.linspace(0, 2 * np.pi, 30, endpoint=False)
torus14 = tori[14]
X  = torus14.X(Tx)
PX = torus14.PX(Tx)

fig = plt.figure(figsize=(3, 3))  # same size as "same as above but with external tori in red"
ax = fig.add_subplot(1, 1, 1)
ax.fill(X, PX, color='C0', alpha=0.3)
# Closed torus curve
ax.plot(np.append(X, X[0]), np.append(PX, PX[0]), color='C0', lw=0.5)

# Spokes from origin to each theta point (closes full 2pi)
for xi, pxi in zip(X, PX):
    ax.plot([0, xi], [0, pxi], color='r', lw=0.4, alpha=0.3)

# Theta points on curve
ax.plot(X, PX, '.', color='r', ms=3)

# theta_x label inside the torus near the first spoke
frac = 0.45
ax.text( 0.1, -0.18, r'$\theta_x$', fontsize=8, ha='center', va='center', color='r')

# Circular arrow spanning 3/2 pi (270 deg) inside torus — inverted direction (arrowhead at start)
r_arr = np.min(np.sqrt(X**2 + PX**2)) * 0.65
theta_arc = np.linspace(Tx[1], Tx[1] + 3 * np.pi / 2, 200)
x_arc = r_arr * np.cos(theta_arc)
px_arc = r_arr * np.sin(theta_arc)
ax.plot(x_arc, px_arc, 'r-', lw=1.0)
ax.annotate('', xy=(x_arc[0], px_arc[0]), xytext=(x_arc[4], px_arc[4]),
            arrowprops=dict(arrowstyle='->', color='r', lw=1.0))

# Ix formula on a single line — same color as area fill (C0)
ax.text(0.05, 0.95,
        r'$I_x = \frac{1}{2}\sum_n n|A_n|^2 = $' + f'${torus14.Ix:.4f}$ m',
        transform=ax.transAxes, fontsize=7, va='top', ha='left', color='C0',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8, edgecolor='none'))

ax.plot(0, 0, 'k+', ms=5)
ax.set_aspect('equal')
ax.set_xlim(-0.43, 0.43)
ax.set_ylim(-0.43, 0.43)
# set xticks and yticks  with -.4, -.2 0 2 .4
plt.xticks([-0.4, -0.2, 0, 0.2, 0.4])
plt.yticks([-0.4, -0.2, 0, 0.2, 0.4])
ax.set_xlabel(r'$x\ [\sqrt{\mathrm{m}}]$')
ax.set_ylabel(r'$p_x\ [\sqrt{\mathrm{m}}]$')
plt.tight_layout()
plt.savefig('../plots/torus14_area.pdf', dpi=300, bbox_inches='tight')
plt.show()

#%% plot the tracking result of the torus14 with the same size and axes limits as the previous plot
fig, ax = plt.subplots(figsize=(3, 3))

tracking = tracking_list[14]
ax.plot(tracking['x'][0:200], tracking['px'][0:200], '.', color='k', markersize=1)
# add in very light gray the tracking of the other tori
for i, tracking in enumerate(tracking_list):
    if i < 14:
        ax.plot(tracking['x'][0:200], tracking['px'][0:200], '.', color='gray', markersize=1, alpha=0.1)
ax.set_aspect('equal')
ax.set_xlim(-0.43, 0.43)
ax.set_ylim(-0.43, 0.43)
ax.set_xlabel(r'$ x\ [\sqrt{\mathrm{m}}]$')
ax.set_ylabel(r'$ p_x\ [\sqrt{\mathrm{m}}]$');
plt.tight_layout()
plt.savefig('../plots/torus14_tracking.pdf', dpi=300, bbox_inches='tight')

# %%
# Harmonic content for all tori: pcolormesh on a common frequency grid
n_tori_plot = 15
freq_bins = np.linspace(-0.5, 0.5, 600)
Z = np.zeros((n_tori_plot, len(freq_bins) - 1))

for i, tracking in enumerate(tracking_list[0:n_tori_plot]):
    Qx = tracking['Qx']
    Ax = np.abs(tracking['Ax'])
    for k in range(len(Qx)):
        bin_idx = np.searchsorted(freq_bins, Qx[k]) - 1
        if 0 <= bin_idx < Z.shape[1]:
            if Ax[k] > Z[i, bin_idx]:
                Z[i, bin_idx] = Ax[k]

Z_log = np.where(Z > 1e-10, np.log10(Z), np.nan)

Ix_values = np.array([tori[i].Ix for i in range(n_tori_plot)])
dIx = np.diff(Ix_values)
Ix_edges = np.concatenate([[Ix_values[0] - dIx[0] / 2],
                            (Ix_values[:-1] + Ix_values[1:]) / 2,
                            [Ix_values[-1] + dIx[-1] / 2]])

cmap = plt.cm.plasma.copy()
cmap.set_bad(alpha=0)

fig, ax = plt.subplots(figsize=(8, 4))
pcm = ax.pcolormesh(freq_bins, Ix_edges, Z_log, cmap=cmap, shading='flat')
plt.colorbar(pcm, ax=ax, label=r'$\log_{10}|A_n|\ [\sqrt{\mathrm{m}}]$')
ax.set_xlim(-0.5, 0.5)
ax.set_xlabel('frequency [1/turn]')
ax.set_ylabel(r'$I_x$ [m]')

# Harmonic number labels at the top (using torus 14 as reference)
ref = tracking_list[14]
for k in range(len(ref['Qx'])):
    n = ref['nx'][k][0]
    f = ref['Qx'][k]
    if np.abs(n) <= 15 and -0.5 <= f <= 0.5:
        ax.text(f, 1.01, str(n), transform=ax.get_xaxis_transform(),
                fontsize=5, ha='center', va='bottom', color='k')

plt.tight_layout()
plt.savefig('../plots/harmonic_map.pdf', dpi=300, bbox_inches='tight')
plt.show()


# %%
# Reference dimension cell
fig, ax = plt.subplots()
torus= tori[14]
max_terms_list = [3, 4, 5, 10, 50]

colors = plt.cm.plasma(np.linspace(0.1, 0.9, len(max_terms_list)))
lw_values = np.linspace(1, 1, len(max_terms_list))

for idx, max_terms in enumerate(max_terms_list):
    new = torus.copy(max_terms=max_terms)
    ptplt.xloop(new, num_points=200, edgecolor=colors[idx], alpha=0.85,
                lw=lw_values[idx], label=f'n$_{{\\rm{{max}}}}$={max_terms}')

ax.set_xlim(-0.43, 0.43)
ax.set_ylim(-0.43, 0.43)
ax.set_aspect('equal')
ax.set_box_aspect(1)
ax.set_xlabel(r'$ x\ [\sqrt{\mathrm{m}}]$')
ax.set_ylabel(r'$ p_x\ [\sqrt{\mathrm{m}}]$')
ax.legend(fontsize=8, loc='lower right')

# Zoomed inset centred in the axes
x_c, y_c, dx, dy = 0.19, 0.3, 0.04, 0.04
ins_w, ins_h = 0.45, 0.45
axins = ax.inset_axes([(1 - ins_w) / 2, (1 - ins_h) / 2, ins_w, ins_h])

Tx_ins = np.linspace(0, 2*np.pi, 2000)
for idx, max_terms in enumerate(max_terms_list):
    new = torus.copy(max_terms=max_terms)
    axins.plot(new.X(Tx_ins), new.PX(Tx_ins), color=colors[idx], alpha=0.85, lw=1)

axins.set_xlim(x_c - dx/2, x_c + dx/2)
axins.set_ylim(y_c - dy/2, y_c + dy/2)
axins.set_xticks([x_c - dx/2, x_c, x_c + dx/2])
axins.set_yticks([y_c - dy/2, y_c, y_c + dy/2])
axins.xaxis.set_major_formatter(plt.FormatStrFormatter('%.3f'))
axins.yaxis.set_major_formatter(plt.FormatStrFormatter('%.3f'))
axins.tick_params(labelsize=6)
ax.indicate_inset_zoom(axins, edgecolor='black', lw=1.2)

plt.tight_layout()
plt.savefig('../plots/tori_approximation.pdf', dpi=600, bbox_inches='tight')
# %%
# Plotting the tori mesh NL
#--------------------------------------------------
from matplotlib.colors import LinearSegmentedColormap

n_angles = 201
Tx = np.linspace(0, 2*np.pi, n_angles, endpoint=False)

# Peace flag colormap (smooth gradient over the rings)
peace_colors = ['#E40303', '#FF8C00', '#FFED00', '#008026', '#004DFF', '#750787']
peace_cmap = LinearSegmentedColormap.from_list('peace', peace_colors)

tori_plot = tori[0:15]
Ix_list = [torus.Ix for torus in tori_plot]
n_rings = len(tori_plot) - 1

# Collect mesh node coordinates: shape (n_tori, n_angles)
X_mesh  = np.array([torus.X(Tx)  for torus in tori_plot])
PX_mesh = np.array([torus.PX(Tx) for torus in tori_plot])

fig, ax = plt.subplots()

# Fill each quadrilateral cell, color mapped by ring index
for i in range(n_rings):
    color = peace_cmap(i / (n_rings - 1))
    for j in range(n_angles):
        j1 = (j + 1) % n_angles
        quad_x  = [X_mesh[i, j],  X_mesh[i, j1],  X_mesh[i+1, j1],  X_mesh[i+1, j]]
        quad_px = [PX_mesh[i, j], PX_mesh[i, j1], PX_mesh[i+1, j1], PX_mesh[i+1, j]]
        ax.fill(quad_x, quad_px, color=color, alpha=0.7, linewidth=0)

# White dot at the center of each outermost ring cell
i_outer = n_rings - 1
for j in range(n_angles):
    j1 = (j + 1) % n_angles
    cx = 0.25 * (X_mesh[i_outer, j] + X_mesh[i_outer, j1] + X_mesh[i_outer+1, j1] + X_mesh[i_outer+1, j])
    cy = 0.25 * (PX_mesh[i_outer, j] + PX_mesh[i_outer, j1] + PX_mesh[i_outer+1, j1] + PX_mesh[i_outer+1, j])
    ax.plot(cx, cy, '.', color='white', ms=1, zorder=5)

# Rings on top
for torus in tori_plot:
    ptplt.xloop(torus, num_points=200, edgecolor='k', alpha=0.6, lw=0.8)

# Spokes on top
for j in range(n_angles):
    ax.plot(X_mesh[:, j], PX_mesh[:, j], color='k', lw=0.5, alpha=0.4)

ax.set_xlim(-0.43, 0.43)
ax.set_ylim(-0.43, 0.43)
ax.set_aspect('equal')
ax.set_box_aspect(1)
ax.set_xlabel(r'$ x\ [\sqrt{\mathrm{m}}]$')
ax.set_ylabel(r'$ p_x\ [\sqrt{\mathrm{m}}]$')
plt.tight_layout()
plt.savefig('../plots/tori_mesh.pdf', dpi=600, bbox_inches='tight')


# %%
# Tori mesh with highlighted ring between tori 12 and 13
fig, ax = plt.subplots()

highlight_ring = 12
for i in range(n_rings):
    color = peace_cmap(i / (n_rings - 1))
    alpha = 0.7 if i == highlight_ring else 0.12
    for j in range(n_angles):
        j1 = (j + 1) % n_angles
        quad_x  = [X_mesh[i, j],  X_mesh[i, j1],  X_mesh[i+1, j1],  X_mesh[i+1, j]]
        quad_px = [PX_mesh[i, j], PX_mesh[i, j1], PX_mesh[i+1, j1], PX_mesh[i+1, j]]
        ax.fill(quad_x, quad_px, color=color, alpha=alpha, linewidth=0)

# Rings on top
for torus in tori_plot:
    ptplt.xloop(torus, num_points=200, edgecolor='k', alpha=0.3, lw=0.8)

# Spokes on top
for j in range(n_angles):
    ax.plot(X_mesh[:, j], PX_mesh[:, j], color='k', lw=0.5, alpha=0.15)

ax.set_xlim(-0.43, 0.43)
ax.set_ylim(-0.43, 0.43)
ax.set_aspect('equal')
ax.set_box_aspect(1)
ax.set_xlabel(r'$ x\ [\sqrt{\mathrm{m}}]$')
ax.set_ylabel(r'$ p_x\ [\sqrt{\mathrm{m}}]$')
plt.tight_layout()
plt.savefig('../plots/tori_mesh_highlight_ring12.pdf', dpi=600, bbox_inches='tight')

# %% Tori mesh: sweep all sectors for highlight_ring=12
# # Tori mesh: sweep all sectors for highlight_ring=12
# highlight_ring = 12

# for j_highlight in range(n_angles):
#     fig, ax = plt.subplots()

#     for i in range(n_rings):
#         color = peace_cmap(i / (n_rings - 1))
#         for j in range(n_angles):
#             j1 = (j + 1) % n_angles
#             alpha = 0.7 if (i == highlight_ring and j == j_highlight) else 0.12
#             quad_x  = [X_mesh[i, j],  X_mesh[i, j1],  X_mesh[i+1, j1],  X_mesh[i+1, j]]
#             quad_px = [PX_mesh[i, j], PX_mesh[i, j1], PX_mesh[i+1, j1], PX_mesh[i+1, j]]
#             ax.fill(quad_x, quad_px, color=color, alpha=alpha, linewidth=0)

#     # Rings on top
#     for torus in tori_plot:
#         ptplt.xloop(torus, num_points=200, edgecolor='k', alpha=0.3, lw=0.8)

#     # Spokes on top
#     for j in range(n_angles):
#         ax.plot(X_mesh[:, j], PX_mesh[:, j], color='k', lw=0.5, alpha=0.15)

#     ax.set_xlim(-0.43, 0.43)
#     ax.set_ylim(-0.43, 0.43)
#     ax.set_aspect('equal')
#     ax.set_box_aspect(1)
#     ax.set_xlabel(r'$ x\ [\sqrt{\mathrm{m}}]$')
#     ax.set_ylabel(r'$ p_x\ [\sqrt{\mathrm{m}}]$')
#     plt.tight_layout()
#     plt.savefig(f'../plots/tori_mesh_ring{highlight_ring}_sector{j_highlight:03d}.pdf', dpi=600, bbox_inches='tight')
#     plt.close()

# %% Tori mesh: all slabs highlighted for sector theta=0
j_highlight = 0
fig, ax = plt.subplots()

for i in range(n_rings):
    color = peace_cmap(i / (n_rings - 1))
    for j in range(n_angles):
        j1 = (j + 1) % n_angles
        alpha = 0.7 if j == j_highlight else 0.12
        quad_x  = [X_mesh[i, j],  X_mesh[i, j1],  X_mesh[i+1, j1],  X_mesh[i+1, j]]
        quad_px = [PX_mesh[i, j], PX_mesh[i, j1], PX_mesh[i+1, j1], PX_mesh[i+1, j]]
        ax.fill(quad_x, quad_px, color=color, alpha=alpha, linewidth=0)

# Rings on top
for torus in tori_plot:
    ptplt.xloop(torus, num_points=200, edgecolor='k', alpha=0.3, lw=0.8)

# Spokes on top
for j in range(n_angles):
    ax.plot(X_mesh[:, j], PX_mesh[:, j], color='k', lw=0.5, alpha=0.15)

ax.set_xlim(-0.43, 0.43)
ax.set_ylim(-0.43, 0.43)
ax.set_aspect('equal')
ax.set_box_aspect(1)
ax.set_xlabel(r'$ x\ [\sqrt{\mathrm{m}}]$')
ax.set_ylabel(r'$ p_x\ [\sqrt{\mathrm{m}}]$')
plt.tight_layout()
plt.savefig(f'../plots/tori_mesh_all_rings_sector{j_highlight:03d}.pdf', dpi=600, bbox_inches='tight')
plt.show()


# %% Full mesh plot of tori foliation
import numpy as np
import matplotlib.pyplot as plt

import nafflib
import pytori as pt
import pytori.plotting as ptplt

# =======================
# Mesh parameters
#x_tori_number_ext = 200
#x_tori_number_int = 50
#x_tori_number = x_tori_number_ext + x_tori_number_int

x_tori_number = 199
x_start = np.linspace(0.00001,0.39,x_tori_number)
# I_x_range = ((0.1*(1+1/x_tori_number_int))**2/2, 0.39**2/2) # Corresponding to x_start range via I = x^2/2
# I_x_start = np.linspace(I_x_range[0], I_x_range[1], x_tori_number_ext)
# x_start_int = np.linspace(0.0001, 0.1, x_tori_number_int)
# x_start = np.concatenate([ x_start_int, np.sqrt(2 * I_x_start)])

angular_points_number = 500
# ======================

# ========================
# Henon parameters
num_turns   = int(0.5e4)
Q0          = 0.2071
# ========================


# Generating tori
# px_start   = 0.37 * x_start
px_start   = 0 * x_start
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
    #============================================================================

    _tracking['Ax'] = Ax
    _tracking['Qx'] = Qx
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


# Plotting
#--------------------------------------------------

# %%

plt.figure()
for torus in tori:
    # Full loop around 0-2pi    
    ptplt.xloop(torus,num_points=200,edgecolor='C0',alpha=0.7,lw=1)

    # torus = torus.copy(max_terms=1)
    # ptplt.xloop(torus,num_points=200,edgecolor='C0',alpha=0.7,lw=1)

    # Free hand plot of the torus
    Tx = np.linspace(0-np.pi/8,2*np.pi-np.pi/8,50) # Theta_x values
    #plt.plot(torus.X(Tx), torus.PX(Tx),'-',color='C3',lw=1)
    #plt.plot(torus.X(Tx[0]), torus.PX(Tx[0]),'o',color='C3',ms=3)
    #plt.plot(torus.X(Tx[:-1]), torus.PX(Tx[:-1]),'-',color='C3',ms=3.5,alpha=0.2)




plt.axis('equal')
plt.gca().set_box_aspect(1) 
plt.xlabel(r'$x\ [\sqrt{\mathrm{m}}]$');
plt.ylabel(r'$p_x\ [\sqrt{\mathrm{m}}]$');

# # plot an annulus from 0.1 to 0.3
# annulus_inner = 0
# annulus_outer = 0.33
# theta = np.linspace(0, 2 * np.pi, angular_points_number)
# # outer circle
# x_outer = annulus_outer * np.cos(theta[::-1])
# px_outer = annulus_outer * np.sin(theta[::-1])

# # inner circle (reverse direction to make a proper closed annulus)
# x_inner = annulus_inner * np.cos(theta)
# px_inner = annulus_inner * np.sin(theta)
  
# plt.plot(x_inner, px_inner, 'g',lw=2,label='Inner Annulus')
# plt.plot(x_outer, px_outer, 'g',lw=2,label='Outer Annulus')

# x = np.concatenate([x_outer, x_inner])
# y = np.concatenate([px_outer, px_inner])

# plt.fill(x, y, color='orange', alpha=.1)
plt.gca().set_aspect('equal')
plt.savefig('../plots/tori_foliation_denser.pdf', dpi=300, bbox_inches='tight')
# %%
# %%
# Harmonic content for all tori: pcolormesh on a common frequency grid
plt.figure(figsize=(6, 6))
n_tori_plot = x_tori_number
freq_bins = np.linspace(-0.5, 0.5, 400)
Z = np.zeros((n_tori_plot, len(freq_bins) - 1))

for i, tracking in enumerate(tracking_list[0:n_tori_plot]):
    Qx = tracking['Qx']
    Ax = np.abs(tracking['Ax'])
    for k in range(len(Qx)):
        bin_idx = np.searchsorted(freq_bins, Qx[k]) - 1
        if 0 <= bin_idx < Z.shape[1]:
            if Ax[k] > Z[i, bin_idx]:
                Z[i, bin_idx] = Ax[k]

Z_log = np.where(Z > 1e-13, np.log10(Z), np.nan)

Ix_values = np.array([tori[i].Ix for i in range(n_tori_plot)])
dIx = np.diff(Ix_values)
Ix_edges = np.concatenate([[Ix_values[0] - dIx[0] / 2],
                            (Ix_values[:-1] + Ix_values[1:]) / 2,
                            [Ix_values[-1] + dIx[-1] / 2]])

cmap = plt.cm.plasma.copy()
cmap.set_bad(alpha=0)

fig, ax = plt.subplots(figsize=(6, 4))
pcm = ax.pcolormesh(freq_bins, Ix_edges, Z_log, cmap=cmap, shading='flat')
plt.colorbar(pcm, ax=ax, label=r'$\log_{10}|A_n|\ [\sqrt{\mathrm{m}}]$',
             location='bottom', pad=0.15)
ax.set_xlim(-0.5, 0.5)
ax.set_xlabel('frequency [1/turn]')
ax.set_ylabel(r'$I_x$ [m]')
# Harmonic number labels at the top (using torus 14 as reference)
# ref = tracking_list[14]
# for k in range(len(ref['Qx'])):
#     n = ref['nx'][k][0]
#     f = ref['Qx'][k]
#     if np.abs(n) <= 15 and -0.5 <= f <= 0.5:
#         ax.text(f, 1.01, str(n), transform=ax.get_xaxis_transform(),
#                 fontsize=5, ha='center', va='bottom', color='k')

plt.tight_layout()
plt.savefig('../plots/harmonic_map.pdf', dpi=300, bbox_inches='tight')
plt.show()
# %%

plt.figure()
for torus in tori:
    # Full loop around 0-2pi    
    ptplt.xloop(torus,num_points=200,edgecolor='C0',alpha=0.7,lw=1)

    # torus = torus.copy(max_terms=1)
    # ptplt.xloop(torus,num_points=200,edgecolor='C0',alpha=0.7,lw=1)

    # Free hand plot of the torus
    Tx = np.linspace(0-np.pi/8,2*np.pi-np.pi/8,50) # Theta_x values
    #plt.plot(torus.X(Tx), torus.PX(Tx),'-',color='C3',lw=1)
    #plt.plot(torus.X(Tx[0]), torus.PX(Tx[0]),'o',color='C3',ms=3)
    #plt.plot(torus.X(Tx[:-1]), torus.PX(Tx[:-1]),'-',color='C3',ms=3.5,alpha=0.2)




plt.axis('equal')
plt.gca().set_box_aspect(1) 
plt.xlabel(r'$x\ [\sqrt{\mathrm{m}}]$');
plt.ylabel(r'$p_x\ [\sqrt{\mathrm{m}}]$');

# plot an annulus from 0.1 to 0.3
annulus_inner = 0
annulus_outer = 0.33
theta = np.linspace(0, 2 * np.pi, angular_points_number)
# outer circle
x_outer = annulus_outer * np.cos(theta[::-1])
px_outer = annulus_outer * np.sin(theta[::-1])

# inner circle (reverse direction to make a proper closed annulus)
x_inner = annulus_inner * np.cos(theta)
px_inner = annulus_inner * np.sin(theta)
  
plt.plot(x_inner, px_inner, 'g',lw=2,label='Inner Annulus')
plt.plot(x_outer, px_outer, 'g',lw=2,label='Outer Annulus')

x = np.concatenate([x_outer, x_inner])
y = np.concatenate([px_outer, px_inner])

plt.fill(x, y, color='orange', alpha=.1)
plt.gca().set_aspect('equal')
plt.savefig('../plots/tori_foliation_denser_and_distribution.pdf', dpi=300, bbox_inches='tight')
plt.show()

# %%

import numpy as np

def annulus(x, y, annulus_inner, annulus_outer):
    # Convert to numpy arrays (no effect if they are already arrays)
    x = np.asarray(x)
    y = np.asarray(y)

    r2 = x**2 + y**2
    return np.where((annulus_inner**2 <= r2) & (r2 <= annulus_outer**2), 1, 0)

def area_quadrilateral(x1, px1, x2, px2, x3, px3, x4, px4):
    # split into two triangles
    area1 = 0.5 * np.abs(x1*(px2 - px3) + x2*(px3 - px1) + x3*(px1 - px2))
    area2 = 0.5 * np.abs(x1*(px3 - px4) + x3*(px4 - px1) + x4*(px1 - px3))
    return area1 + area2 

def annulus_weighted(Q, P, annulus_inner, annulus_outer):
    """
    Evaluate annulus membership and weight by distance between consecutive points.
    
    Parameters:
    -----------
    Q : np.array
        Array of Q coordinates (shape: N)
    P : np.array  
        Array of P coordinates (shape: N)
    annulus_inner : float
        Inner radius of annulus
    annulus_outer : float
        Outer radius of annulus
        
    Returns:
    --------
    weights : np.array
        Array of weights for each point. Points outside annulus get weight 0.
        Points inside annulus get weight proportional to distance from previous point.
    """
    Q = np.asarray(Q)
    P = np.asarray(P)
    
   
    
    # Binary mask for points in annulus
    value = annulus(Q, P, annulus_inner, annulus_outer)
    
    
    
    # Calculate distances between consecutive points
    area = 1
    for ii in range(1,x_tori_number):
        for jj in range(angular_points_number-1):
            area = 1
    #        area = 1 #area_quadrilateral(x[ii-1,jj-1], px[ii-1,jj-1],
                        #   x[ii-1,jj], px[ii-1,jj],
                        #   x[ii,jj], px[ii,jj],
                        #   x[ii,jj-1], px[ii,jj-1]))
    # Weight by distance, but only for points in annulus
    weights = value * area
    
    return weights

def gaussian_2d(x, y, sigma, truncation_sigma=3.0):
    """
    Isotropic 2D Gaussian evaluated at (x, y), truncated to 0 beyond
    truncation_sigma * sigma.  Analogous to annulus() but returns a
    continuous density value instead of a binary mask.

    Parameters
    ----------
    x, y            : coordinates (scalar or array)
    sigma           : Gaussian sigma [same units as x, y]
    truncation_sigma: hard cut-off radius in units of sigma (default 3)
    """
    x = np.asarray(x)
    y = np.asarray(y)
    r2     = x**2 + y**2
    r2_max = (truncation_sigma * sigma)**2
    value  = np.exp(-r2 / (2.0 * sigma**2))
    return np.where(r2 <= r2_max, value, 0.0)


def gaussian_2d_weighted(Q, P, sigma, truncation_sigma=3.0):
    """
    Weight each mesh cell by the truncated 2D Gaussian density times the
    cell area.  Analogous to the annulus inline loop, but for a Gaussian
    distribution.

    Parameters
    ----------
    Q, P             : mesh coordinate arrays, shape (x_tori_number, n_ang)
    sigma            : Gaussian sigma
    truncation_sigma : hard cut-off radius in units of sigma (default 3)

    Returns
    -------
    weights_g : array of shape (x_tori_number, n_ang)
    """
    Q = np.asarray(Q)
    P = np.asarray(P)
    n_tori, n_ang = Q.shape
    weights_g = np.zeros_like(Q)
    for ii in range(1, n_tori):
        for jj in range(n_ang):
            value = gaussian_2d(Q[ii, jj], P[ii, jj], sigma, truncation_sigma)
            area  = area_quadrilateral(
                Q[ii-1, jj-1], P[ii-1, jj-1],
                Q[ii-1, jj],   P[ii-1, jj],
                Q[ii,   jj],   P[ii,   jj],
                Q[ii,   jj-1], P[ii,   jj-1])
            weights_g[ii, jj] = value * area
    return weights_g


my_Q = []
my_P = []
my_density = []
my_average_density = []

for torus in tori: 
    looping = 'x'
    Tx = np.linspace(0,2*np.pi,angular_points_number) 
    Q = torus.X(Tx)
    P = torus.PX(Tx)

    my_Q.append(Q[:-1])
    my_P.append(P[:-1])  
    density = annulus_weighted(Q[:-1], P[:-1], annulus_inner, annulus_outer)
    my_density.append(density)
    average_density = np.mean(density)
    my_average_density.append(average_density*np.ones_like(Q[:-1]))
    
# ── Mesh construction ──────────────────────────────────────────────────────
my_Q = []
my_P = []
my_Q_p = []
my_P_p = []
my_Ix = []

for torus in tori:
    Tx = np.linspace(0, 2*np.pi, angular_points_number)
    Q_t = torus.X(Tx)
    P_t = torus.PX(Tx)
    my_Q.append(Q_t[:-1])
    my_P.append(P_t[:-1])
    my_Q_p.append(Q_t[1:])
    my_P_p.append(P_t[1:])
    my_Ix.append(torus.Ix)

Q = np.reshape(my_Q, (x_tori_number, angular_points_number-1))
P = np.reshape(my_P, (x_tori_number, angular_points_number-1))
Q_p = np.reshape(my_Q_p, (x_tori_number, angular_points_number-1))
P_p = np.reshape(my_P_p, (x_tori_number, angular_points_number-1))
# ── Annulus weights (binary mask × cell area) ──────────────────────────────
weights = np.zeros_like(Q)
values  = np.zeros_like(Q)

for ii in range(1, x_tori_number):
    for jj in range(angular_points_number-1):
        #value = annulus(Q[ii, jj], P[ii, jj], annulus_inner, annulus_outer)
        
        value1 = annulus(Q[ii-1, jj-1], P[ii-1, jj-1], annulus_inner, annulus_outer)
        value2 = annulus(Q[ii-1, jj], P[ii-1, jj], annulus_inner, annulus_outer)
        value3 = annulus(Q[ii, jj], P[ii, jj], annulus_inner, annulus_outer)
        value4 = annulus(Q[ii, jj-1], P[ii, jj-1], annulus_inner, annulus_outer)
        value = (value1 + value2 + value3 + value4)/4

        # area  = area_quadrilateral(Q[ii-1, jj-1], P[ii-1, jj-1],
        #                            Q[ii-1, jj],   P[ii-1, jj],
        #                            Q[ii,   jj],   P[ii,   jj],
        #                            Q[ii,   jj-1], P[ii,   jj-1])
        
        area = (my_Ix[ii]-my_Ix[ii-1])*2*np.pi/angular_points_number
        values[ii, jj]  = value
        weights[ii, jj] = value * area

# ── Plot ───────────────────────────────────────────────────────────────────
from mpl_toolkits.axes_grid1 import make_axes_locatable

fig, ax = plt.subplots(figsize=(6.4, 5.6))
# sc = ax.scatter(Q, P, c=weights, cmap='viridis', marker='o', s=.1,
#                 vmin=weights.min(), vmax=weights.max())
sc = ax.scatter((Q+Q_p)/2, (P+P_p)/2, c=weights, cmap='viridis', marker='o', s=.1,
                vmin=weights.min(), vmax=weights.max())
ax.set_xlim(-0.43, 0.43)
ax.set_ylim(-0.43, 0.43)
ax.set_aspect('equal')
ax.set_box_aspect(1)
ax.set_xlabel(r'$ x\ [\sqrt{\mathrm{m}}]$')
ax.set_ylabel(r'$ p_x\ [\sqrt{\mathrm{m}}]$')

average_weights = np.mean(weights, axis=1)
average_weights = np.repeat(average_weights[:, np.newaxis], angular_points_number-1, axis=1)

divider = make_axes_locatable(ax)
cax = divider.append_axes('bottom', size='5%', pad=0.5)
cbar = fig.colorbar(sc, cax=cax, orientation='horizontal',
                    label='weighted density [arb. units]',
                    location='bottom', pad=0.15)
cbar.set_ticks([weights.min(), weights.max()])
cbar.set_ticklabels(['0', '1'])
plt.tight_layout()
plt.savefig('../plots/average_density.pdf', dpi=300, bbox_inches='tight')
# %%
fig, ax = plt.subplots(figsize=(6.4, 5.6))
ax.scatter(my_Q, my_P, c=average_weights, cmap='viridis',  marker='o',vmin=weights.min(), vmax=weights.max(), s=.1)
# plt.title('After filamentation')
plt.xlabel(r'$x\ [\sqrt{\mathrm{m}}]$');
plt.ylabel(r'$p_x\  [\sqrt{\mathrm{m}}]$')
ax = plt.gca()
ax.set_xlim(-0.43, 0.43)
ax.set_ylim(-0.43, 0.43)
ax.set_aspect('equal')
ax.set_box_aspect(1)
divider = make_axes_locatable(ax)
cax = divider.append_axes('bottom', size='5%', pad=0.5)
cbar = fig.colorbar(sc, cax=cax, orientation='horizontal',
                    label='weighted density [arb. units]',
                    location='bottom', pad=0.15)
cbar.set_ticks([weights.min(), weights.max()])
cbar.set_ticklabels(['0', '1'])
plt.savefig('../plots/average_density_filamented.pdf', dpi=300, bbox_inches='tight')

# %%

import numpy as np
import matplotlib.pyplot as plt

# Example arrays
# X, Y, W are 1D arrays of the same length
# X = ...
# Y = ...
# W = ...

# Bin definitions
my_Q_aux = np.concatenate(Q)
my_P_aux = np.concatenate(P)
my_average_density_aux = np.concatenate(average_weights)

steps = 150
xbins = np.linspace(min(my_Q_aux), max(my_Q_aux), steps)
ybins = np.linspace(min(my_P_aux), max(my_P_aux), steps)

# Build 2D weighted histogram
H, xedges, yedges = np.histogram2d(my_Q_aux, my_P_aux, bins=[xbins, ybins], weights=my_average_density_aux)

# Projection on X: sum over Y bins
projXX = H.sum(axis=1)

# Projection on Y: sum over X bins
projYY = H.sum(axis=0)

# Plot projections

#plt.step(xedges[:-1], projXX, where='mid')


my_Q_aux = np.concatenate(Q)
my_P_aux = np.concatenate(P)
my_density_aux = np.concatenate(weights)
xbins = np.linspace(-0.45, 0.45, steps)
ybins = np.linspace(-0.45, 0.45, steps)

# Build 2D weighted histogram
H, xedges, yedges = np.histogram2d(my_Q_aux, my_P_aux, bins=[xbins, ybins], weights=my_density_aux)

# Projection on X: sum over Y bins
projX = H.sum(axis=1)

# Projection on Y: sum over X bins
projY = H.sum(axis=0)

rotations = [
    (0,           r'$f_\infty$ at $s_0$'),
    (np.pi/4,     r'$f_\infty$ at $s_0$ and $\mu_x=\pi/4$ '),
    (np.pi/2,     r'$f_\infty$ at $s_0$ and $\mu_x=\pi/2$ '),
    (3*np.pi/4,   r'$f_\infty$ at $s_0$ and $\mu_x=3\pi/4$ '),
]
proj_list = []
for theta, label in rotations:
    QQ = Q*np.cos(theta) - P*np.sin(theta)
    PP = Q*np.sin(theta) + P*np.cos(theta)
    H, xedges, _ = np.histogram2d(np.concatenate(QQ), np.concatenate(PP),
                                   bins=[xbins, ybins], weights=my_average_density_aux, density=True)
    proj_list.append((H.sum(axis=1), label))


# Plot projections
x_centers = xedges[1:]

    
# Abel transform of a uniform disk of radius annulus_outer
R = annulus_outer
x_abel = np.linspace(-0.5, 0.5, 1000)
p_abel = 2 * np.sqrt(np.maximum(R**2 - x_abel**2, 0))
# Normalise to the same integral as the filamented projection
norm = np.trapezoid(proj_list[0][0], x_centers) / np.trapezoid(p_abel, x_abel)
plt.plot(x_abel, p_abel * norm, 'k--', lw=1.5, label=r'$f_0$ (analytical)')

for proj, label in proj_list[0:1]:
    plt.step(x_centers, proj, where='mid', label='$f_\infty$ at $s_0$')

plt.title("Projection on $x$-axis")
plt.xlabel(r'$x\ [\sqrt{\mathrm{m}}]$')
plt.ylabel("Weighted counts")

plt.tight_layout()
plt.grid()
plt.legend()

plt.xlabel(r'$x\ [\sqrt{\mathrm{m}}]$')
plt.ylabel("Counts")
plt.tight_layout()
plt.grid()
plt.legend()
plt.xlim(-0.45, 0.45)
plt.ylim(0, 350)

ax = plt.gca()
ax.set_box_aspect(1)
plt.savefig('../plots/projection_x_final.pdf', dpi=300, bbox_inches='tight')
# %% Repeate above just considering proj_list[0:2]
plt.plot(x_abel, p_abel * norm, 'k--', lw=1.5, label=r'$f_0$ (analytical)')
for proj, label in proj_list[0:2]:
    plt.step(x_centers, proj, where='mid', label=label) 
plt.title("Projection on $x$-axis")
plt.xlabel(r'$x\ [\sqrt{\mathrm{m}}]$')
plt.ylabel("Counts")
plt.tight_layout()
#plt.grid()
plt.legend()
plt.xlim(-0.45, 0.45)
plt.ylim(0, 350)

ax = plt.gca()
ax.set_box_aspect(1)
plt.savefig('../plots/projection_x_final_rotation.pdf', dpi=300, bbox_inches='tight')

# %% plot weights as a scatter plot in (Ix, theta) space
Ix_values = np.array([tori[i].Ix for i in range(x_tori_number)])

Ix_grid    = np.repeat(Ix_values[:, np.newaxis], angular_points_number-1, axis=1)
theta_grid = np.tile(np.linspace(0, 2*np.pi, angular_points_number-1), (x_tori_number, 1))

log_w = np.log(weights.flatten())
finite_mask = np.isfinite(log_w)
vmin, vmax = log_w[finite_mask].min(), log_w[finite_mask].max()

fig, ax = plt.subplots()
sc = ax.scatter(Ix_grid.flatten(), theta_grid.flatten(), c=log_w, vmin=vmin, vmax=vmax, s=1)
ax.set_xlabel(r'$I_x$ [m]')
ax.set_ylabel(r'$\theta_x$')
ax.set_xlim(Ix_values[0], Ix_values[-2])
ax.set_ylim(0, 2*np.pi)
ax.set_yticks([0, np.pi, 2*np.pi], [r'$0$', r'$\pi$', r'$2\pi$'])
cbar = fig.colorbar(sc, ax=ax, location='bottom', pad=0.15, label='log10(weighted density) [arb. units]')
cbar.set_ticks([vmin, vmax])
cbar.set_ticklabels(['-1', '0'])
plt.tight_layout()
plt.savefig('../plots/weights_Ix_theta.pdf', dpi=300, bbox_inches='tight')
# %%
# Density as a function of action
Ix_values = np.array([tori[i].Ix for i in range(x_tori_number)])

density_action = weights.sum(axis=1)

dI_1 = np.diff(np.concatenate([[0], Ix_values[:-1]], axis=0))
dI_2 = np.diff(Ix_values)
dI   = (dI_1 + dI_2) / 2
Ix_mid = 0.5 * (Ix_values[:-1] + Ix_values[1:])
density_per_dI = 0.5 * (density_action[:-1] + density_action[1:]) / dI

# Normalise to a PDF (integral over I = 1)
norm = np.trapezoid(density_per_dI, Ix_mid)
density_per_dI = density_per_dI / norm
I_max = annulus_outer**2/2
# plot also a pdf constant in 0<Ix<I_max for reference
uniform_pdf = np.where((Ix_mid >= 0) & (Ix_mid <= I_max), 1/I_max, 0)   
fig, ax = plt.subplots()

plt.plot(Ix_mid, uniform_pdf, 'g--', label='linear lattice')

ax.plot(Ix_mid, density_per_dI, 'r.-', label='non-linear lattice')

ax.set_xlabel(r' $I_x$  [m]')
ax.set_ylabel(r'pdf$(I_x)$  [m$^{-1}$]')
ax.grid(True, alpha=0.3)
plt.xlim(0, Ix_values[-2])
plt.legend()
plt.tight_layout()
plt.savefig('../plots/density_per_dI.pdf', dpi=300, bbox_inches='tight')
# %%
# ── Mesh construction ──────────────────────────────────────────────────────
my_Q = []
my_P = []

for torus in tori:
    Tx = np.linspace(0, 2*np.pi, angular_points_number)
    Q_t = torus.X(Tx)
    P_t = torus.PX(Tx)
    my_Q.append(Q_t[:-1])
    my_P.append(P_t[:-1])

Q = np.reshape(my_Q, (x_tori_number, angular_points_number-1))
P = np.reshape(my_P, (x_tori_number, angular_points_number-1))

# ── Gaussian weights (density × cell area) ────────────────────────────────
weights = np.zeros_like(Q)
values  = np.zeros_like(Q)

alpha =0.5
for ii in range(1, x_tori_number):
    for jj in range(angular_points_number-1):
        #value = gaussian_2d(Q[ii, jj], P[ii, jj], sigma=0.11*alpha, truncation_sigma=3.0/alpha)
        value = gaussian_2d(Q[ii, jj], P[ii, jj], sigma=0.055, truncation_sigma=6)
        area  = area_quadrilateral(Q[ii-1, jj-1], P[ii-1, jj-1],
                                   Q[ii-1, jj],   P[ii-1, jj],
                                   Q[ii,   jj],   P[ii,   jj],
                                   Q[ii,   jj-1], P[ii,   jj-1])
        values[ii, jj]  = value
        weights[ii, jj] = value * area

# ── Plot ───────────────────────────────────────────────────────────────────
from mpl_toolkits.axes_grid1 import make_axes_locatable

fig, ax = plt.subplots(figsize=(6.4, 5.6))
sc = ax.scatter(Q, P, c=weights, cmap='viridis', marker='o', s=.1,
                vmin=weights.min(), vmax=weights.max())
ax.set_xlim(-0.43, 0.43)
ax.set_ylim(-0.43, 0.43)
ax.set_aspect('equal')
ax.set_box_aspect(1)
ax.set_xlabel(r'$ x\ [\sqrt{\mathrm{m}}]$')
ax.set_ylabel(r'$ p_x\ [\sqrt{\mathrm{m}}]$')

average_weights = np.mean(weights, axis=1)
average_weights = np.repeat(average_weights[:, np.newaxis], angular_points_number-1, axis=1)

divider = make_axes_locatable(ax)
cax = divider.append_axes('bottom', size='5%', pad=0.5)
cbar = fig.colorbar(sc, cax=cax, orientation='horizontal',
                    label='weighted density [arb.units]')
cbar.set_ticks([weights.min(), weights.max()])
cbar.set_ticklabels(['0', '1'])
plt.tight_layout()
plt.savefig('../plots/average_density_gaussian.pdf', dpi=300, bbox_inches='tight')
# %%
fig, ax = plt.subplots(figsize=(6.4, 5.6))
ax.scatter(my_Q, my_P, c=average_weights, cmap='viridis',  marker='o',vmin=weights.min(), vmax=weights.max(), s=.1)
# plt.title('After filamentation')
plt.xlabel(r'$x\ [\sqrt{\mathrm{m}}]$');
plt.ylabel(r'$p_x\  [\sqrt{\mathrm{m}}]$')
ax = plt.gca()
ax.set_xlim(-0.43, 0.43)
ax.set_ylim(-0.43, 0.43)
ax.set_aspect('equal')
ax.set_box_aspect(1)
divider = make_axes_locatable(ax)
cax = divider.append_axes('bottom', size='5%', pad=0.5)
cbar = fig.colorbar(sc, cax=cax, orientation='horizontal',
                    label='weighted density [arb. units]')
cbar.set_ticks([weights.min(), weights.max()])
cbar.set_ticklabels(['0', '1'])
plt.savefig('../plots/average_density_gaussian_filamented.pdf', dpi=300, bbox_inches='tight')
# %%
import numpy as np
import matplotlib.pyplot as plt

# Example arrays
# X, Y, W are 1D arrays of the same length
# X = ...
# Y = ...
# W = ...

# Bin definitions
my_Q_aux = np.concatenate(Q)
my_P_aux = np.concatenate(P)
my_average_density_aux = np.concatenate(average_weights)

steps = 150
xbins = np.linspace(min(my_Q_aux), max(my_Q_aux), steps)
ybins = np.linspace(min(my_P_aux), max(my_P_aux), steps)

# Build 2D weighted histogram
H, xedges, yedges = np.histogram2d(my_Q_aux, my_P_aux, bins=[xbins, ybins], weights=my_average_density_aux)

# Projection on X: sum over Y bins
projXX = H.sum(axis=1)

# Projection on Y: sum over X bins
projYY = H.sum(axis=0)

# Plot projections

#plt.step(xedges[:-1], projXX, where='mid')


my_Q_aux = np.concatenate(Q)
my_P_aux = np.concatenate(P)
my_density_aux = np.concatenate(weights)
xbins = np.linspace(-0.45, 0.45, steps)
ybins = np.linspace(-0.45, 0.45, steps)

# Build 2D weighted histogram
H, xedges, yedges = np.histogram2d(my_Q_aux, my_P_aux, bins=[xbins, ybins], weights=my_density_aux)

# Projection on X: sum over Y bins
projX = H.sum(axis=1)

# Projection on Y: sum over X bins
projY = H.sum(axis=0)

rotations = [
    (0,           r'$f_\infty$ at $s_0$'),
    (np.pi/4,     r'$f_\infty$ at $s_0$ and $\mu_x=\pi/4$ '),
    (np.pi/2,     r'$f_\infty$ at $s_0$ and $\mu_x=\pi/2$ '),
    (3*np.pi/4,   r'$f_\infty$ at $s_0$ and $\mu_x=3\pi/4$ '),
]
proj_list = []
for theta, label in rotations:
    QQ = Q*np.cos(theta) - P*np.sin(theta)
    PP = Q*np.sin(theta) + P*np.cos(theta)
    H, xedges, _ = np.histogram2d(np.concatenate(QQ), np.concatenate(PP),
                                   bins=[xbins, ybins], weights=my_average_density_aux, density=True)
    proj_list.append((H.sum(axis=1), label))


# Plot projections
x_centers = xedges[1:]
# for proj, label in [proj_list[0], proj_list[3]]:
#     plt.step(x_centers, np.log10(proj), where='mid', label=label)
    
# Abel transform of a uniform disk of radius annulus_outer
R = annulus_outer
x_abel = np.linspace(-R, R, 1000)
p_abel = 2 * np.sqrt(np.maximum(R**2 - x_abel**2, 0))
# Normalise to the same integral as the filamented projection
norm = np.trapezoid(proj_list[0][0], x_centers) / np.trapezoid(p_abel, x_abel)
#plt.plot(x_abel, p_abel * norm, 'k--', lw=1.5, label=r'Analytical $x$-projection (Abel transform)')

# plt.title("Projection on X")
# plt.xlabel(r'$x\ [\sqrt{\mathrm{m}}]$')
# plt.ylabel("Weighted counts")

# plt.tight_layout()
# plt.grid()
# plt.legend()

# my_Q_aux = np.concatenate(Q)
# my_P_aux = np.concatenate(P)
my_density_aux = np.concatenate(weights)

# steps = 150
# xbins = np.linspace(min(my_Q_aux), max(my_Q_aux), steps)
# ybins = np.linspace(min(my_P_aux), max(my_P_aux), steps)

rotations = [
    (0,           r'$f_\infty$ at $s_0$'),
    (np.pi/4,     r'$f_\infty$ at $s_0$ and $\mu_x=\pi/4$ '),
    (np.pi/2,     r'$f_\infty$ at $s_0$ and $\mu_x=\pi/2$ '),
    (3*np.pi/4,   r'$f_\infty$ at $s_0$ and $\mu_x=3\pi/4$ '),
]

proj_list = []
for theta, label in rotations:
    QQ = Q*np.cos(theta) - P*np.sin(theta)
    PP = Q*np.sin(theta) + P*np.cos(theta)
    H, xedges, _ = np.histogram2d(np.concatenate(QQ), np.concatenate(PP),
                                   bins=[xbins, ybins], weights=my_density_aux, density=True)
    proj_list.append((H.sum(axis=1), label))

x_centers = xedges[1:]
for proj, label in proj_list[0:1]:
    plt.step(x_centers, np.log10(proj), where='mid', label='$f_0$', color='k')

proj_list = []
for theta, label in rotations:
    QQ = Q*np.cos(theta) - P*np.sin(theta)
    PP = Q*np.sin(theta) + P*np.cos(theta)
    H, xedges, _ = np.histogram2d(np.concatenate(QQ), np.concatenate(PP),
                                   bins=[xbins, ybins], weights=my_average_density_aux, density=True)
    proj_list.append((H.sum(axis=1), label))


# Plot projections
x_centers = xedges[1:]
for proj, label in [proj_list[0], proj_list[3]]:
    plt.step(x_centers, np.log10(proj), where='mid', label=label)

plt.xlabel(r'$x\ [\sqrt{\mathrm{m}}]$')
plt.ylabel("log10(Counts)")
plt.title("Projection on $x$-axis")
plt.tight_layout()
# plt.grid()
plt.legend()
plt.xlim(-0.45, 0.45)
ax = plt.gca()
ax.set_box_aspect(1)
plt.savefig('../plots/projection_x_final_gaussian.pdf', dpi=300, bbox_inches='tight')
# %%
# plot weights as a scatter plot in (Ix, theta) space
Ix_values = np.array([tori[i].Ix for i in range(x_tori_number)])

Ix_grid    = np.repeat(Ix_values[:, np.newaxis], angular_points_number-1, axis=1)
theta_grid = np.tile(np.linspace(0, 2*np.pi, angular_points_number-1), (x_tori_number, 1))

log_w = np.log(weights.flatten())
finite_mask = np.isfinite(log_w)
vmin, vmax = log_w[finite_mask].min(), log_w[finite_mask].max()

sc = plt.scatter(Ix_grid.flatten(), theta_grid.flatten(), c=log_w, vmin=vmin, vmax=vmax, s=1)
plt.xlabel(r'$I_x$ [m]')
plt.ylabel(r'$\theta_x$')
plt.xlim(Ix_values[0], Ix_values[-2])
plt.ylim(0, 2*np.pi)
plt.yticks([0, np.pi, 2*np.pi], [r'$0$', r'$\pi$', r'$2\pi$'])
cbar = plt.colorbar(sc, label='log10(weighted density) [arb. units]',
                    location='bottom', pad=0.15)
cbar.set_ticks([vmin, vmax])
cbar.set_ticklabels(['-1', '0'])
plt.tight_layout()
plt.savefig('../plots/weights_Ix_theta_gaussian.pdf', dpi=300, bbox_inches='tight')
# %%
# Density as a function of action
Ix_values = np.array([tori[i].Ix for i in range(x_tori_number)])

density_action = weights.sum(axis=1)

dI_1 = np.diff(np.concatenate([[0], Ix_values[:-1]], axis=0))
dI_2 = np.diff(Ix_values)
dI   = (dI_1 + dI_2) / 2
Ix_mid = 0.5 * (Ix_values[:-1] + Ix_values[1:])
density_per_dI = 0.5 * (density_action[:-1] + density_action[1:]) / dI

# Normalise to a PDF (integral over I = 1)
norm = np.trapezoid(density_per_dI, Ix_mid)
density_per_dI = density_per_dI / norm
I_max = annulus_outer**2/2
# plot also a pdf constant in 0<Ix<I_max for reference
uniform_pdf = np.where((Ix_mid >= 0) & (Ix_mid <= I_max), 1/I_max, 0)   
fig, ax = plt.subplots()

#plt.plot(Ix_mid, uniform_pdf, 'g--', label='In the $I_x$ of the linear lattice')


ax.set_xlabel(r' $I_x$  [m]')
ax.set_ylabel(r'pdf$(I_x)$  [m$^{-1}$]')
ax.grid(True, alpha=0.3)
plt.xlim(0, Ix_values[-2])
plt.legend()
plt.tight_layout()
# Plot a exp(-I/I0) for reference
sigma = 0.055
I0 = sigma**2
sigma_max = 6*sigma
I_max = sigma_max**2/2

pdf_exp = (1/I0) * np.exp(-Ix_mid/I0)
# put pdf_exp = 0 for Ix_mid > 0.01 to avoid plotting the tail
pdf_exp = np.where(Ix_mid <= I_max, pdf_exp, 0)
# Normalize pdf_exp to the same area as density_per_dI for Ix_mid < 0.01
norm_exp = np.trapezoid(pdf_exp, Ix_mid)
norm_density = np.trapezoid(density_per_dI, Ix_mid)
pdf_exp = pdf_exp * (norm_density / norm_exp)
plt.semilogy(Ix_mid, pdf_exp, 'g--', label=r'linear lattice')
plt.semilogy(Ix_mid, density_per_dI, 'r.-', label='non-linear lattice')

plt.legend()
plt.savefig('../plots/density_per_dI_gaussian.pdf', dpi=300, bbox_inches='tight')
# %%
