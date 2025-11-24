# %%
import xtrack as xt

line = xt.load('lhc_injection.json')
# %%

tw = line.twiss(method='4d')

# %%
import matplotlib.pyplot as plt
plt.plot(tw.s, tw.betx, label='betx')
# %%
