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
# %%
total_turns = 50000
step = 500
turn_ranges = [(s, s + step) for s in range(0, total_turns, step)]

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
ax.set_xlim(-0.5, 0.5)
ax.set_ylim(-0.5, 0.5)
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
ax.set_xlim(-0.5, 0.5)
ax.set_ylim(-0.5, 0.5)
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
plt.figure(figsize=(5, 5))
for tracking in tracking_list[0:14]:
    plt.plot(tracking['x'][0:200], tracking['px'][0:200], '.', color='gray', markersize=1)
for tracking in tracking_list[14:15]:
    plt.plot(tracking['x'][0:200], tracking['px'][0:200], '.', color='red', markersize=1)
plt.axis('equal')
plt.gca().set_box_aspect(1)
plt.xlabel(r'$ x\ [\sqrt{\mathrm{m}}]$');           
plt.ylabel(r'$ p_x\ [\sqrt{\mathrm{m}}]$');
plt.xlim(-0.43, 0.43)
plt.ylim(-0.43, 0.43)
# put ticks at 0 0.5, 1
plt.xticks([-0.5, 0, 0.5])
plt.yticks([-0.5, 0, 0.5])
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
# %%
# Harmonic content for all tori: pcolormesh on a common frequency grid
n_tori_plot = 15
freq_bins = np.linspace(0, 0.5, 300)
Z = np.zeros((n_tori_plot, len(freq_bins) - 1))

for i, tracking in enumerate(tracking_list[0:n_tori_plot]):
    Qx = np.abs(tracking['Qx'])
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
ax.set_xlabel('frequency [1/turn]')
ax.set_ylabel(r'$I_x$ [m]')
plt.tight_layout()
plt.savefig('../plots/harmonic_map.pdf', dpi=300, bbox_inches='tight')
# %%
# Reference dimension cell
fig, ax = plt.subplots()

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

# %%
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

# %%
