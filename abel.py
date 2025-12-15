# %%
# plot the projection in x of the phase space x-px where x-px is a circular torus
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm  

j_x =40
# new seed
np.random.seed()
N = 10000000
theta_x = np.random.uniform(0, 2*np.pi, N)
r_x = np.sqrt(2*j_x)
x = r_x * np.cos(theta_x)
px = r_x * np.sin(theta_x)

N_range = 101
x_range= np.linspace(-10, 10, N_range)


a = np.max(r_x)
def my_fun(x, a):
    if np.abs(x) >= a:
        return 0
    else:
        return 2* a /(np.sqrt(a**2 - x**2))

plt.hist(x, bins=x_range, weights=np.ones_like(x) * (N_range/4*np.sqrt(np.pi*j_x)  / len(x)))

plt.plot(x_range, [my_fun(xi, a) for xi in x_range], label='theory')
plt.ylim(0, 5)
# %% in 4D
j_x =.025
j_y =.025

j_x =50
j_y =50 
N = int(100000*np.sqrt(j_x)*np.sqrt(j_y))
theta_x = np.random.uniform(0, 2*np.pi, N)
theta_y = np.random.uniform(0, 2*np.pi, N)

r_x = np.sqrt(2*j_x)
r_y = np.sqrt(2*j_y)
x = r_x * np.cos(theta_x)
px = r_x * np.sin(theta_x)
y = r_y * np.cos(theta_y)
py = r_y * np.sin(theta_y)

# hist2d with logscale
N_range = 51
x_bins = np.linspace(-10, 10, N_range)  # 100 bins covering the x range
y_bins = np.linspace(-10, 10, N_range)  # 100 bins covering the y range

plt.figure()
plt.hist2d(x, y, bins=[x_bins, y_bins], density=True, )#norm=LogNorm())
plt.colorbar(label='Density')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Phase Space Distribution (x-y)')

# 3D plot with density as z-axis
# Define custom mesh

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
hist, xedges, yedges = np.histogram2d(x, y, bins=[x_bins, y_bins], density=True)
xpos, ypos = np.meshgrid(xedges[:-1], yedges[:-1], indexing='ij')
ax.plot_surface(xpos, ypos, hist, cmap='viridis')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('Density')
ax.set_title('Phase Space Distribution (x-y) - 3D')

# %%
# then https://chatgpt.com/s/t_6939929fff3c81919ecdfd3554b59449