# %%
import xtrack as xt
import matplotlib.pyplot as plt

line = xt.load('lhc_injection.json')
# %%
tw = line.twiss(method='4d')

# %%
plt.plot(tw.s, tw.betx, label='betx')

# %%
