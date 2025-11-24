# %%
import xtrack as xt
import matplotlib.pyplot as plt

line = xt.load('lhc_injection.json')

# %%
tw = line.twiss(method='4d')

# %%
plt.plot(tw.s, tw.betx, label='betx')

# %%
line.twiss(method='4d', at_s=30)
line['on_x1_v']=111
# %%
collider = xt.Environment()

collider.import_line(line=line,
                             line_name='lhcb1')

# %%
collider['on_x1_v']
# %%
