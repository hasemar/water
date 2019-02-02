'''
This script calculates the FTW recycle injection control valve 
position based on head conditions between high and low demand modes.
Major and minor losses are taken into account from the FTW storage tank
to the high water level at the DAF.

Uses Water package developed by Ryan Haseman
'''
from __future__ import division, print_function
import numpy as np
import matplotlib.pyplot as plt
from Water import *

# water system info
system_name = "Rosario"
station_name = "Water Treatment Plant"
tank_data = {          
    'name' : 'ftw_storage',
    'diameter' : 11.75,
    'height' : 13.08,
    'freeboard' : 1.5,
    'deadstorage' : 1.5,
    'elevation' : 340
}
# create storage tank 
storage = Tank(**tank_data)   # FTW storage tank

# flow parameters
Q_hi = 23      # gpm
Q_low = 14     # gpm
Q_vec = np.linspace(Q_low, Q_hi, num=((Q_hi - Q_low)+1))

# Final pumping height
outlet_height = 12      # ft  DAF water level 

'''
################ SUCTION SIDE LOSSES ################
consists of: 
- storage tank to pump
'''
# pipe parameters 
s2p_size = 2
s2p_len = 6
s2p = Pipe(s2p_len, s2p_size, 'PVC', sch=80)

# fittings for suction pipe section
# listed as fitting object(type, params, etc..), and number of fittings
s2p.fitting('elbow_90', 'standard_glued', 3)
s2p.fitting('valve', 'ball',2)

'''
################# DISCHARGE SIDE LOSSES ####################
consists of: 
- pump to reducer
- reducer to injection point
- injection point to DAF
- 2" bypass
'''
### pump to reducer ###
# pipe parameters
p2r_size = 1
p2r_len = 2
p2r = Pipe(p2r_len, p2r_size, 'PVC',sch=80)

# fittings for pump to reducer section
p2r.fitting('elbow_90', 'standard_glued', 1)
p2r.fitting('tee_through', 'standard_glued', 1)
p2r.fitting('reducer', 'standard_glued', 1, 0.8)

### reducer to injection point ###
# pipe parameters
r2ip_size = 1.25
r2ip_length = 50
r2ip = Pipe(r2ip_length, r2ip_size, 'PVC', sch=40)

# fittings for reducer to injection point section
# (assuming control valve wide open)
r2ip.fitting('elbow_90', 'standard_glued', 2)
r2ip.fitting('tee_branch', 'standard_glued')
r2ip.fitting('valve', 'ball', 2)
r2ip.fitting('valve', 'swing_check')

### injection point to DAF ###
# pipe paramters
ip2DAF_size = 8
ip2DAF_length = 180
ip2DAF = Pipe(ip2DAF_length, ip2DAF_size, 'PVC', sch=80)

# fittings for injection point to DAF
ip2DAF.fitting('elbow_90', 'standard_glued', 20)
ip2DAF.fitting('tee_branch', 'standard_glued',2)
ip2DAF.fitting('valve', 'butterfly', 2)
ip2DAF.fitting('valve', 'swing_check')
ip2DAF.fitting('static_mixer', 'standard_threaded', 1, 2)
ip2DAF.fitting('flow_meter', 'standard_threaded', 1, 4)

#### 2 inch bypass in feed line ###
# pipe parameters
bypass_size = 2
bypass_length = 5
bypass = Pipe(bypass_length, bypass_size, kind='PVC', sch=80)

# fittings in bypass
bypass.fitting('valve', 'gate')
bypass.fitting('tee_branch', 'standard_glued', 2)

# Calculating losses with flow vector
pipes = [s2p, p2r, r2ip, ip2DAF, bypass] 

losses = []

# calculating losses for all pipes sections for each flow
for each_pipe in pipes:
    q_list = []
    for each_flow in Q_vec:
        q_list.append(each_pipe.get_losses(each_flow))
    losses.append(q_list)

# define suction side losses
suc_losses = losses[0]
# define discharge side losses
dis_losses = sum(np.array(losses[1:]))

############ Pumping Head Calculations #############

# suction head
suc_head = [x - storage.deadstorage for x in suc_losses]
# discharge head
dis_head = [x + outlet_height for x in dis_losses] 
# total dynamic head condition for each flow in Q_vec
tdh = [sum(x) for x in zip(dis_head, suc_head)]

print(tools.report_losses(suc_losses, Q_vec, 'suction losses'))
print(tools.report_losses(dis_losses, Q_vec, 'discharge losses'))

########## Pump Specification ############

# create injection pump
inj_pump = Pump()
# load pump data for Goulds 3642
inj_pump.load_pump('Goulds 3642')

########## Find Required Cv Value for Control Valve #########

# find head on pump curve for desired flows
head = [inj_pump.find_head(x) for x in Q_vec]
# find difference between pump curve head and system curve
delta_p = [x-y for x,y in zip(head, tdh)]

# calculate Cv value required to meet pump curve
Cv = [q / np.sqrt(dp) for q, dp in zip(Q_vec, delta_p)]
# new system curve
tdh_with_valve = [sum(x) for x in zip(tdh, delta_p)]

# data from selected V8 series valve with 30 degree port mfg chart
Cv_valve = [0.0, 0.2, 0.4, 1.1, 2.0, 3.7, 5.5, 8.0, 10.0, 13.0, 15.0]
valve_pos = [0, 15, 20, 30, 40, 50, 60, 70, 80, 90, 100]   # percent open

# Find valve position for Cv
control_pos = [np.interp(x, Cv_valve, valve_pos) for x in Cv]
pos_str = ["{:.1f}".format(x) + " %" for x in control_pos]  # string output for graphing

# create sub-plots for system curve, pump curve, Cv value, adjusted system curve
# (the rest of this code is just for plotting a graph of the results)
plt.figure(1)
# system curve and pump curve (no valve)
plt.subplot(221)
# pump curve
plt.plot(inj_pump.flow, inj_pump.head)
# system curve
plt.plot(Q_vec, tdh)
# chart elements
plt.title("Goulds Model: " + inj_pump.model + " Pump and System Curve")
plt.xlabel("Flow (gpm)")
plt.ylabel("Head (ft)")
#plt.text(Q_vec[-1]-1, tdh[-1] - 3, "   System Curve \n(No Control Valve)")
#plt.text(Q_vec[-1]-1, tdh[-1] + 8, "Pump Curve")
plt.legend(['pump curve', 'system curve'])
plt.grid()

# valve curve
plt.subplot(222)
plt.plot(valve_pos, Cv_valve)
# chart elements
plt.title("V-Series Control Ball Valve w/ 30deg port")
plt.xlabel("% Open")
plt.ylabel("Cv value")
plt.grid()

plt.subplot(313)
# pump curve
plt.plot(inj_pump.flow, inj_pump.head)
# system curve (no valve)
plt.plot(Q_vec, tdh)
# adujsted system curve (with valve)
plt.plot(Q_vec, tdh_with_valve, lw=3, color='red')
# chart elements
plt.fill_between(Q_vec, tdh_with_valve, tdh, facecolor="palegreen")
for i, txt in enumerate(pos_str):
    plt.annotate(txt, xy=(Q_vec[i], tdh_with_valve[i]), fontsize=10)
plt.title("Pump Curve and System Curve using Control Valve")
plt.xlabel("Flow (gpm)")
plt.ylabel("Head (ft)")
plt.xlim((12,25))
plt.text(Q_vec[-1], tdh_with_valve[0], "(% Open)")
plt.grid()
plt.legend(['pump curve','sys curve (no valve)', 'sys curve (with valve)'])

plt.show()
