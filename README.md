# Topology and Non-linear Matching: from KAM Tori to Beam profiles

In modern circular accelerators, beam mismatch at injection into non-linear lattices can play a crucial role for beam quality degradation. In this work, we explore the process of non-linear matching within the Kolmogorov–Arnold–Moser (KAM) quasi-periodic regime, focusing on how the intrinsic phase-space structure influences the evolution of initial beam distributions. Using a topological approach, we quantify how mismatched Gaussian beams can develop non-Gaussian tails when propagated through non-linear focusing elements, as a consequence of the underlying invariant tori. These results are relevant for the design and operation of high-intensity storage rings and colliders where beam-halo control is critical.

### Links

- Confluence [link](https://confluence.cern.ch/display/IC/Topology+and+Non-linear+Matching%3A+from+KAM+Tori+to+Beam+profiles).

- We will use the [PhD thesis](https://cernbox.cern.ch/files/spaces/eos/user/s/sterbini/2025/Philippe%20Belanger/Philippe_Belanger_PhD_not_final.pdf) of Philippe and its [`pytori`](https://github.com/pbelange/pytori/tree/main) package.


### The questions and the quest

This paper aims to study the beam distribution matching and its generalization to non-linear (NL) periodic lattices. For this aims we will use the topological approach as presented in P. Bélanger's PhD.

The  logic flow of the paper has as skeleton the following questions:

1. Given an initial $\rho(\vec{x},\vec{p})$ (at the turn N=0 and position $s_0$) and a KAM topology of the phase space $\{\vec{x},\vec{p}\}$ at the same position $s_0$, find the $lim_N\rho$.

2. Given a KAM topology of the phase space $\{\vec{x},\vec{p}\}$ and a beam $\vec{x}$-profile $\rho_{\vec{x}}=\int\rho(\vec{x},\vec{p})d\vec{p}$, find the corresponding $\rho(\vec{x},\vec{p})$ profile.

3. If the $\rho$ is matched in $s_0$, it is matched along the full NL circular machine.  Let's assume linear machines. Is the $\rho$ constant but for metric factors along the machine? In others words, is $\rho|s_1=\rho(a\odot x, b \odot p)|s_0 $? Clearly not (example: Gaussian beam with $\alpha_{CS}=0$ and $\alpha_{CS}\ne 0$). Is $\rho_{\vec{x}}$ constant but for metric factors along the machine?


The first problem is a problem on analysis, the second one is a problem of synthesis. The third problem is a corollary of 1 and 2.

To address these questions we assume that $\rho$ is zero outside the KAM region around the closed orbit.

### Linear systems

In the case of linear systems, the aforementioned questions are trivial.

In general, the 1 cannot be answered. In fact the limit does not exist (oscillatory functions). A 2D example: if we start from a $\rho$ not matched to the topology, it will start to oscillate. Nevertheless we can dig more in the details of this  example because the approach can be naturally extended to the NL case.
Let us assume to know in $s_0$ the topology of the 2D linear phase space. In other words that we know the two phasors that determine the ellipses $\Psi(J, \theta)$. If $\rho$ is not $\theta$-constant in $\Psi$ for each $J$, then the distribution is mismatched and the x-profile, $\rho_x$, oscillates indefinitely as function of the turn number $N$.

Let's assume to have a 2D annular beam, i.e. $\rho$ is constant with $r_{min}<\sqrt{x^2+p_x^2}<r_{max}$. Let's then assume that the topology can be expressed with the tori, from  Eq. 4.14 of Philippe's thesis (PBT),  

$$
\Psi(I_x, \theta_x)=\sqrt{2 I_x}(\lambda_x^+ e^{i \Theta_x}+    \lambda_x^- \ e^{-i \Theta_x})
$$

where $\lambda_x^{\pm}$ are defined following Eq. 4.43 of PBT.


```diff
- is OK to express in action? Numerically I think is not a problem and probably is not confusin the reader.
```

 For each $x$ we can *numerically* evaluate the $\Theta_x$-averaged $\rho$ and this will give the new distribution

$$
\begin{equation}
<\rho>_N (I_x)= \frac{1}{2\pi}\int_0^{2\pi} \rho(\Psi(I_x, \Theta_x))d\Theta_x.
\end{equation}
$$

To do this integral we just need to track a simple ensemble of particle ($x_i$,$p_x$=0).  We can associate a torus to each $x_i$, that is a set of ($x, p_x$) coordinates corresponding to a regular $\Theta_x$-mesh in the interval [0, 2$\pi$). Then we map the density $\rho$ on this set and compute its average.
We associate to the the torus (the set of ($x, p_x$) coordinates) the new average value. In doing so, for our $i$-tori, we build the  $<\rho>_N (I_x)$.


The very same approach hold for a non-linear problem, but this time since the tune will be amplitude dependent, the limit exists.

```diff
- Example of a 2D Hénon map.
```

And in 4D? Conceptually, the approach is the same as for the 2D case. Clearly the numerical averaging is more involved, since for all {($x_i,p_x=0,y_i,p_y=0$)} we should mesh and average in $\theta_x$, $\theta_y$ (and similarly for 6D).

As an example we can assume a 4D annular beam, that is $\rho$ constant in $r_{min}<\sqrt{x^2+p_x^2+y^2+y_p^2}<r_{max}$. In a linear and coupled lattice we can compute the average $<\rho>_N$ and compute the x-y projection.

```diff
- Example of a FODO a skew-quad bump. Show how the $\rho_{\vec{x}}$ varies along the machine. Discussion on the "emittance exchange"?

- Show a lattice 4D e.g. injection of the LHC with strong octupoles. Try to play with tune and octupoles current to moderately deform the KAM up 4-5 sigma. Inject a 4D gaussian beam linearly matched. Compute the limit of 1. Compare with tracking.
```

We can now move to the second question: we have the projected profile $\rho_{\vec{x}}$ and we would like to obtain the matched  $\rho$ given the NL topology (KAM hypothesis). In the linear case, we can address this question by the inverse Abel transform. For the non-linear case we can get inspired by longitudinal tomography, LT (with all the differences between the two cases: LT solve the 2D phase space distribution from initial distribution from longitudinal time-varying profile. Here we want to focuse on steady state projection in >2D case). The 2D NL case can be dealt with the scraping method ``à la Kostas''. 

Here I think the key is the projection of the tori on the $x-y$ plane. A single point in $x-y$ belongs to infinite tori and a single torus projects in infinite $x-y$ points with different ``multiplicity (crossing)''. The solutions is to define a list of tori; for each torus define its domain of projection with multiplicity.

Starting from a mesh in x-y we can compute the ``layers'' of each single torus on this mesh. The xy projection is the linear combination of all layers. The coefficient of this linear combination are the unknown to find (e.g., via least squares minimization). 

```diff
- The second question can be a good way to open the problem of non factorization, and more importantly, that to solve unambiguously the $\rho$ problem,  one needs to have the x-y projection and not the x and y projections separately. 
```

## A possible plan

- Take a lattice, e.g. the LHC lattice at the injection and make it linear and uncoupled, track it 4D (since uncoupled is a 2D) using `xsuite`. Use `pytori` to find numerically a *dense* set of tori. Solve the annular distribution problem in 2D.

- Linearly couple the lattice (4D) and repeat.

- Switch ON sextupole and octupole to repeat the linera 4D with the annular distribution and or with a Guaussian.

- Address the question 2 by matching the annular distribution to the 4D NL problems. Show that the distribution is matched, e.g. by applying the method of question 1 as sanity check. 

```diff
- Clearly the paper can be very long (or longer than the canonical 3 pages). Once can consider in a later stage to drop question 2.
```

### Weighted macro-particle representation

The first step is to represente $\rho$ using a grid of weighted macroparticle. In 2D, the grid has to be chosen on the tori $J_x$ at regular $\theta_x$ intervals. It is to be noted that in gerneal the grid is not regular [TODO: improve the concept ot regularity]. Each macro-particle has to be the value in rho and weighted by the area of the corresponding mesh. We assume a non resonant KAM region around a single fixed point of multiplicity 1 (the closed orbit). In other words the mesh is homothetic to a polar grid (via a normal form) assuming same $J_x$ at $\theta_x$ intervals.



