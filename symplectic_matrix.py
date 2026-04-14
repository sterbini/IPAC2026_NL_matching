# %%
"""
Lie Transform: Symmetric Matrix → Symplectic Matrix
====================================================
Given a symmetric matrix S (2n × 2n), the matrix JS belongs to the
symplectic Lie algebra sp(2n), and its matrix exponential M = exp(JS)
is a symplectic matrix in Sp(2n).

Background
----------
- Standard symplectic form J = [[0, I], [-I, 0]]
- Symplectic group:   Sp(2n) = { M : M^T J M = J }
- Symplectic algebra: sp(2n) = { X : X^T J + J X = 0 }
- Claim: S symmetric  ⟹  JS ∈ sp(2n)  ⟹  exp(JS) ∈ Sp(2n)

Physical meaning: S encodes a quadratic Hamiltonian H(z) = ½ zᵀ S z,
and M = exp(t JS) is the phase-space flow at time t=1.
"""

import numpy as np
from scipy.linalg import expm
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import TwoSlopeNorm

# ── Helpers ──────────────────────────────────────────────────────────────────

def symplectic_form(n: int) -> np.ndarray:
    """Standard 2n×2n symplectic form J = [[0, I], [-I, 0]]."""
    I = np.eye(n)
    return np.block([[np.zeros((n, n)), I], [-I, np.zeros((n, n))]])


def random_symmetric(size: int, rng: np.random.Generator, scale: float = 1.0) -> np.ndarray:
    """Generate a random symmetric matrix."""
    A = rng.standard_normal((size, size)) * scale
    return (A + A.T) / 2


def lie_transform(S: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute the Lie transform of a symmetric matrix S.

    Parameters
    ----------
    S : symmetric (2n, 2n) array

    Returns
    -------
    X : generator  JS  ∈ sp(2n)
    M : symplectic map  exp(JS) ∈ Sp(2n)
    """
    assert S.shape[0] == S.shape[1], "S must be square"
    assert S.shape[0] % 2 == 0,      "Size must be even (2n)"
    assert np.allclose(S, S.T, atol=1e-10), "S must be symmetric"

    n = S.shape[0] // 2
    J = symplectic_form(n)
    X = J @ S          # generator in sp(2n)
    M = expm(X)        # symplectic map in Sp(2n)
    return X, M


# ── Verification ─────────────────────────────────────────────────────────────

def verify_symplectic(M: np.ndarray, J: np.ndarray, tol: float = 1e-9) -> dict:
    """Check M^T J M = J and |det M| = 1."""
    residual = M.T @ J @ M - J
    error    = np.linalg.norm(residual, ord='fro')
    det      = np.linalg.det(M)
    return {
        "symplectic_error":  error,
        "is_symplectic":     error < tol,
        "det(M)":            det.real,
        "det_error":         abs(abs(det) - 1.0),
    }


def verify_algebra(X: np.ndarray, J: np.ndarray, tol: float = 1e-9) -> dict:
    """Check X^T J + J X = 0 (X lies in sp(2n))."""
    residual = X.T @ J + J @ X
    error    = np.linalg.norm(residual, ord='fro')
    return {
        "algebra_error": error,
        "in_sp2n":       error < tol,
    }


# ── Visualization ─────────────────────────────────────────────────────────────

def plot_results(S: np.ndarray, X: np.ndarray, M: np.ndarray, J: np.ndarray, n: int):
    fig = plt.figure(figsize=(14, 10), facecolor="#0f0f14")
    fig.suptitle(
        f"Lie Transform  ·  n = {n}  (matrices are {2*n}×{2*n})",
        fontsize=16, fontweight="bold", color="white", y=0.97,
        fontfamily="monospace",
    )

    gs = gridspec.GridSpec(
        2, 4, figure=fig,
        hspace=0.45, wspace=0.35,
        left=0.06, right=0.97, top=0.90, bottom=0.08,
    )

    axes_info = [
        (gs[0, 0], S,          r"$S$ — symmetric input",              "Input"),
        (gs[0, 1], X,          r"$X = JS$ — generator in $\mathfrak{sp}(2n)$", "Algebra"),
        (gs[0, 2], M,          r"$M = e^{X}$ — symplectic map",       "Group"),
        (gs[0, 3], M.T@J@M-J,  r"$M^\top J M - J$ — symplectic residual", "Check"),
        (gs[1, 0], S@S.T,      r"$SS^\top$ — symmetric (sanity)",     None),
        (gs[1, 1], X.T@J+J@X,  r"$X^\top J + JX$ — algebra residual", None),
        (gs[1, 2], M.T@M,      r"$M^\top M$ — (not identity in general)", None),
        (gs[1, 3], J,          r"$J$ — symplectic form",              None),
    ]

    for spec, mat, title, badge in axes_info:
        ax = fig.add_subplot(spec)
        vmax = max(abs(mat).max(), 1e-14)
        norm = TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)
        im = ax.imshow(mat, cmap="RdBu_r", norm=norm, interpolation="nearest", aspect="equal")
        ax.set_title(title, fontsize=8.5, color="#c8c8d8", pad=4, fontfamily="monospace")
        ax.tick_params(colors="#666", labelsize=6)
        for spine in ax.spines.values():
            spine.set_edgecolor("#333")
        cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cb.ax.tick_params(labelsize=6, colors="#888")

        if badge:
            ax.text(
                0.97, 0.97, badge,
                transform=ax.transAxes, ha="right", va="top",
                fontsize=7, color="white", fontfamily="monospace",
                bbox=dict(boxstyle="round,pad=0.25", fc="#1e3a5f", ec="#4477aa", lw=0.8),
            )

    # ── Phase-space orbit panel ──────────────────────────────────────────────
    ax_orbit = fig.add_subplot(gs[1, :2])  # reuse bottom-left two slots... but gs is 2×4
    # Actually let me put it differently — add a wide axis at the bottom
    # The gs[1,0] and gs[1,1] are already used; let me overlay a new subplot
    # I'll add a dedicated text box instead
    ax_info = fig.add_axes([0.06, 0.01, 0.88, 0.065], facecolor="#13131a")
    ax_info.axis("off")

    info_lines = (
        r"$S$ symmetric $\;\Rightarrow\;$"
        r"$X = JS \in \mathfrak{sp}(2n)$"
        r"$\;\Rightarrow\;$"
        r"$M = e^{X} \in \mathrm{Sp}(2n)$"
        r"$\quad[\,M^\top J M = J\,]$"
    )
    ax_info.text(
        0.5, 0.55, info_lines,
        ha="center", va="center", fontsize=11, color="#a8d8ff",
        transform=ax_info.transAxes,
    )

    plt.savefig("/mnt/user-data/outputs/lie_transform.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("Figure saved → lie_transform.png")


# ── Phase-space demo: propagate an ellipse ────────────────────────────────────

def plot_phase_space(S: np.ndarray, steps: int = 200):
    """
    Show how the symplectic flow M(t) = exp(t JS) acts on a circle
    of initial conditions in 2D phase space (n=1).
    """
    assert S.shape == (2, 2), "Phase-space demo requires n=1 (2×2 matrices)"
    J = symplectic_form(1)
    X = J @ S

    theta = np.linspace(0, 2 * np.pi, 200)
    circle = np.stack([np.cos(theta), np.sin(theta)], axis=0)  # (2, 200)

    ts = np.linspace(0, 2 * np.pi, steps)
    trajectories = []
    for t in ts:
        Mt = expm(t * X)
        trajectories.append(Mt @ circle)  # (2, 200)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5), facecolor="#0f0f14")
    fig.suptitle("Phase-space flow (n=1):  circle under  $M(t) = e^{tJS}$",
                 color="white", fontsize=13, fontfamily="monospace")

    # Left: snapshots at several times
    ax = axes[0]
    ax.set_facecolor("#0f0f14")
    cmap = plt.cm.plasma
    snapshot_times = np.linspace(0, 2 * np.pi, 8, endpoint=False)
    for t in snapshot_times:
        Mt = expm(t * X)
        pts = Mt @ circle
        color = cmap(t / (2 * np.pi))
        ax.plot(pts[0], pts[1], lw=1.5, color=color, alpha=0.85)
    ax.plot(*circle, lw=2, color="white", ls="--", alpha=0.4, label="t = 0")
    ax.set_title("Snapshots at $t = 0, \\frac{\\pi}{4}, \\ldots, 2\\pi$",
                 color="#c8c8d8", fontfamily="monospace")
    ax.set_aspect("equal")
    ax.tick_params(colors="#666")
    for sp in ax.spines.values():
        sp.set_edgecolor("#333")
    ax.legend(fontsize=8, labelcolor="white", facecolor="#1a1a25", edgecolor="#333")

    # Right: trace of a single point
    ax2 = axes[1]
    ax2.set_facecolor("#0f0f14")
    point = np.array([1.0, 0.0])
    orbit = np.array([expm(t * X) @ point for t in ts])
    sc = ax2.scatter(orbit[:, 0], orbit[:, 1], c=ts, cmap="plasma", s=8, zorder=3)
    ax2.set_title("Orbit of $(1, 0)$ over $t \\in [0, 2\\pi]$",
                  color="#c8c8d8", fontfamily="monospace")
    ax2.set_aspect("equal")
    ax2.tick_params(colors="#666")
    for sp in ax2.spines.values():
        sp.set_edgecolor("#333")
    cb = fig.colorbar(sc, ax=ax2, fraction=0.046, pad=0.04)
    cb.set_label("$t$", color="white", fontsize=10)
    cb.ax.tick_params(colors="#888", labelsize=7)

    plt.tight_layout()
    plt.savefig("/mnt/user-data/outputs/lie_transform_phase_space.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("Figure saved → lie_transform_phase_space.png")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    rng = np.random.default_rng(42)

    # ── General case: n = 3 (6×6 matrices) ──────────────────────────────────
    n = 3
    N = 2 * n
    S = random_symmetric(N, rng, scale=0.8)
    J = symplectic_form(n)

    X, M = lie_transform(S)

    alg_check  = verify_algebra(X, J)
    symp_check = verify_symplectic(M, J)

    print("=" * 55)
    print(f"  Lie Transform Demo  (n={n}, matrices {N}×{N})")
    print("=" * 55)
    print(f"\n  S symmetric?        {np.allclose(S, S.T)}")
    print(f"\n  X = JS  ∈ sp(2n)?")
    print(f"    ‖X^T J + J X‖_F  = {alg_check['algebra_error']:.2e}   ✓" if alg_check["in_sp2n"]
          else f"    ‖X^T J + J X‖_F  = {alg_check['algebra_error']:.2e}   ✗")
    print(f"\n  M = exp(X) ∈ Sp(2n)?")
    print(f"    ‖M^T J M - J‖_F  = {symp_check['symplectic_error']:.2e}   ✓" if symp_check["is_symplectic"]
          else f"    ‖M^T J M - J‖_F  = {symp_check['symplectic_error']:.2e}   ✗")
    print(f"    det(M)           = {symp_check['det(M)']:.10f}  (should be 1)")
    print(f"    |det(M)| - 1     = {symp_check['det_error']:.2e}")
    print("=" * 55)

    plot_results(S, X, M, J, n)

    # ── Phase-space demo: n = 1 ──────────────────────────────────────────────
    print("\nPhase-space demo (n=1) ...")
    S1 = random_symmetric(2, rng, scale=1.0)
    plot_phase_space(S1)

# %%

if __name__ == "__main__":
    main()