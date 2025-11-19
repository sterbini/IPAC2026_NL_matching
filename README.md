# Introduction


### Links

- Confluence [link](https://confluence.cern.ch/display/IC/Topology+and+Non-linear+Matching%3A+from+KAM+Tori+to+Beam+profiles).

- Overleaf [link]()

### The questions and the quest

This paper aims to study the beam distribution matching and its generalization to non-linear (NL) periodic lattices. For this aims we will use the topological approach as presented in P. Bélanger PhD.

The  logic flow of the paper has as skeleton the following questions:

1. Given an initial $\rho(\vec{x},\vec{p})$ (at the turn N=0 and position $s_0$) and a KAM topology of the phase space {$\vec{x},\vec{p}$} at the same position $s_0$, find the $lim_N\rho$.

2. Given a KAM topology of the phase space {$\vec{x},\vec{p}$} and a beam $\vec{x}$-profile $\rho_{\vec{x}}=\int\rho(\vec{x},\vec{p})d\vec{p}$, find the corresponding $\rho(\vec{x},\vec{p})$ profile.

3. If the $\rho$ is matched in $s_0$, it is matched along the full NL circular machine.  Let's assume linear machines. Is the $\rho$ constant but for metric factors along the machine? In others words, is $\rho|s_1=\rho(a\odot x, b \odot p)|s_0 $? Clearly not (example: Gaussian beam with $\alpha_{CS}=0$ and $\alpha_{CS}\ne 0$). Is $\rho_{\vec{x}}$ constant but for metric factors along the machine?


The first problem is a problem on analysis, the second one is a problem of synthesis. The 3 is a corollary of 1 and 2.

To address this problem we assume that $\rho$ is zero outside the KAM region around the closed orbit.

### Linear systems

In the case of linear systems, the aforementioned questions are trivial.

In general, the 1 cannot be answered. In fact the limit does not exist (oscillatory functions). A 2D example: if we start from a $\rho$ not matched to the topology, it will start to oscillate. Nevertheless we can dig more in the details of this  example because the approach can be naturally extended to the NL case.
Let us assume to know in $s_0$ the topology of the 2D linear phase space. In other words that we know the two phasors that determine the ellipses $\Psi(J, \theta)$. If $\rho$ is not $\theta$-constant in $\Psi$ for each $J$, then the distribution is mismatched and the x-profile, $\rho_x$, oscillates indefinitely as function of the turn number $N$.

Let's assume to have a 2D annular beam, i.e.~$\rho$ is constant with $r_{min}<\sqrt{x^2+p_x^2}<r_{max}$. Let's then assume that the topology can be expressed with the tori $\Psi(J, \theta)$=$(1+j) \sqrt{J} e^(j 2\pi \theta)+ j \sqrt{J}  \ e^(-j 2\pi \theta)$.

::: TODO
Is it correct the J dependence?
:::

 For each $x$ we can *numerically* evaluate the $\theta$-averaged $\rho$ and this will give the new distribution $<\rho>_N$, that is

\begin{equation}
<\rho>_N (J)= 
\end{equation}

The very same approach hold for a non-linear problem, but this time since the tune will be amplitude dependent, the limit of 1 exists.

And in 4D? Conceptually,the approach is the same as for the 2D  linear and non-linear case. Clearly the numerical averaging is more involved, since for all x, y we should average in $\theta_x$, $\theta_y$ (and similarly for 6D).

As an example we can assume a 4D annular beam, that is $\rho$ constant in $r_{min}<\sqrt{x^2+p_x^2+y^2+y_p^2}<r_{max}$ [TODO EXAMPLE]. In a coupled linear lattice we can compute the average $<\rho>_N$ and compute the x-y projection.

Is this projection ""






