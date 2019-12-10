import numpy as np
from Water import Pump

# design parameters
FLOW = 100    # gpm
TDH = 111            # ft head

# define pump object and load pump data
pump_1 = Pump()
pump_1.load_pump('Goulds', '3657 1.5x2 -6: 3SS')

# plot curve without affinitized curves and with efficiency curve
pump_1.plot_curve(target_flow=FLOW, tdh=TDH, vfd=False, eff=True, show=True)

new_pump_data = {
            'model' : 'BF 1-1/2 x 2 - 10',
            'mfg' : 'Goulds',
            'flow' : [0, 50, 100, 150, 200, 250],
            'head' : [400, 400, 390, 372, 340, 270],
            'eff' : [0, 0, 0.49, 0.56, 0.60, 0.54],
            'bep' : [200, 340],
            'rpm' : 3500,
            'impeller' : 9.1875
            }

pump_2 = Pump()
pump_2.add_pump(**new_pump_data)

# create system curve
system_flow = np.linspace(1, 220, 20)
system_head = []

for flow in system_flow:
    system_head.append(220 + 20*np.exp(-1/(flow*.005)))


pump_2.plot_curve(system_flow, system_head, show=True)
