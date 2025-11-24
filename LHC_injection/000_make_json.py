# %%
import xtrack as xt
from cpymad.madx import Madx
import matplotlib.pyplot as plt

# %%

mad = Madx()

# Load mad model and apply element shifts
# after having git clone https://gitlab.cern.ch/acc-models/acc-models-lhc.git 
# in the local folder
mad.input('''
call, file='acc-models-lhc/scenarios/cycle/pp/ramp/0/model.madx';
''')

# %%
line = xt.Line.from_madx_sequence(
    sequence=mad.sequence.lhcb1,
    allow_thick=True,
    deferred_expressions=True,
)

# %%

line.set_particle_ref('proton', p0c=0.450e12)

# you can inspect the knobs with
# line.vars.get_table().show()
# then
# line.vars('kof.b1')._info()


# flat machine
line['on_sep1_h'] = 0
line['on_sep2h'] = 0
line['on_sep5_v'] = 0
line['on_sep8v'] = 0
line['on_x1_v'] = 0
line['on_x2v'] = 0
line['on_x5_h'] = 0
line['on_x8h'] = 0
line['on_a2'] = 0
line['on_a8'] = 0

# on disp
line['on_disp'] = 0

# tune
line['dqx.b1'] = 0
line['dqy.b1'] = 0

# linear coupling
line['cmrs.b1'] = 0
line['cmis.b1'] = 0

# set chromaticity
line['dqpx.b1_op'] = 5
line['dqpy.b1_op'] = 5

# set octupoles
line['kof.b1'] = 0
line['kod.b1'] = 0

tw = line.twiss(method='4d')


# %%
plt.plot(tw.s, tw.betx, label='betx')
# %%
line.to_json('lhc_injection.json')
# %%
