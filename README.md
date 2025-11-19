# Introduction


### Confluence link

The confluence is https://confluence.cern.ch/display/IC/Topology+and+Non-linear+Matching%3A+from+KAM+Tori+to+Beam+profiles

### The questions and the quest

This paper aims to address the following main questions, typical of the beam distribution matching between a transfer line and a circular machine (e.g. the injection in the Large Hadron Collider),

1. Given an initial $\rho(x,p)$ at N=0 and the positio s_0 and a KAM topology at the same position $s_0$, find the $lim_N\rho_N$


2. Given a KAM topology and a beam profile (e.g. in 2D the x-profile or in 4D the x-y profile, etc), find the $\rho(x,p)$ that is matched.


3. If the $\rho$ is matched in s_0, is it matched along the full circular machine. Is the $\rho$ constant but for metric factors along the machine? In others words, $\rho|s_1=\rho(a\odot x, b \odot p)|s_0 $? Clearly not. Is the $\rho$_x constant but for metric factors along the machine?


The first problem is a problem on analysis, the second one is a problem of synthesis. The 3 and 4 are corollaries of the 1 and 2.

To address this problem we assume that $\rho(x,p_x,...)$ is zero outside the first compact KAM region around the closed orbit.
Within this working hypothesis, the aforementioned limit exist if the system is non-linear, hence there is a natural.

### Let's answer the question in the case of linear systems

The case of linear system the aforementioned questions are trivial.

In general, the 1 cannot be solved for linear system. In fact the limit does not exist (oscillatory functions). An example is a 2D system, if we start from a $\rho$ not matched to the topology, it will start to oscillate. Nevertheless we can dig much more in the details of this simple example because the same approach can be naturally extended to the non-linear case.
Let us assume that we know in s_0 the topology of the 2D linear phase space. In other words that we know the phasors (2 for the 2D case linear case) that determine the ellipses for each x and px=0, $\Psi(x)$. If $\rho$ is not constant in $\Psi(x)$ for each $x$, then the distribution is mismatched and the profile oscillates $\rho_x$ indefinitely as function of the turn number N.
But we can find the N-average profile by assigning to each  $\Psi(x)$ the average $\rho$ in $\Psi(x)$, in doing so we have the $<\rho>_N$ hence the $<\rho_x>_N$.

In practice, let's assume to have a annular beam, $rho$ is constant with $r_{min}<\sqrt{x^2+p_x^2}<r_{max}$. Let's then assume that the topology can be expresses as $(1+j)x e^(j 2\pi theta)+j x \ e^(-j 2\pi theta)$. For each $x$ we can *numerically* evaluate the $\theta$-average  $\rho$ and this will give the new distribution $<\rho>_N$.

The very same approach hold for a non-linear problem, but this time since the tune will be amplitude dependent, the limit of 1 exists.

And in 4D? Conceptually,the approach is the same as for the 2D  linear and non-linear case. Clearly the numerical averaging is more involved, since for all x, y we should average in $\theta_x$, $\theta_y$ (and similarly for 6D).

As an example we can assume a 4D annular beam, that is $\rho$ constant in $r_{min}<\sqrt{x^2+p_x^2+y^2+y_p^2}<r_{max}$ [TODO EXAMPLE]. In a coupled linear lattice we can compute the average $<\rho>_N$ and compute the x-y projection.

Is this projection ""






