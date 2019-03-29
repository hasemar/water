'''
Fuel bottle sizing
Test Script for propane bottle size
'''
from __future__ import division, print_function
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress
import csv
from os import path
from Water import Genset

# csv fieldnames header
header_list = [
                'water_system',
                'eng_file',
                'project_name',
                'project_number',
                'gen_model',
                'flow_25',
                'flow_50',
                'flow_75',
                'flow_100',
                'full_load',
                'norm_load',
                'v_bottle',
                'v_effective',
                'full_flow',
                'norm_flow',
                'v_fire',
                'q_fire',
                'q_dom',
                't_empty_hr',
                't_empty_day',
                'vap_rate',
                'vap_rate_gal',
                'total_btu',
                'num_bottles',
                'safety_factor',
                'q_total']

# PROJECT INFORMATION                
water_system = 'Test System'
project_name = 'Wellsite Propane Tank Sizing'
eng_file = '2373'
project_number = '00118233'
gen_model = 'GGHG-5709325'

# Generator Loads
dom_pumps = {
        'S01': 3,
        'S02': 2,
        'bp1': 7.5,
        'bp2': 15
        }
highQ_pumps = {
        'bp3': 25,
        'bp4': 25
}
resistive = {
            'lights': 200,
            'heater and controls': 13000
            }

gen = Genset(voltage=480, phase=3, capacity=100)

for pump in dom_pumps.values():
    gen.add_motor_load(pump)

for pump in highQ_pumps.values():
    gen.add_motor_load(pump, fire=True)

for res in resistive.values():
    gen.add_resistive_load(res, units='watts')

full_load = int((gen.total_load/gen.capacity)*100)   # percent of generator capacity
norm_load =  int(((gen.dom_load+gen.res_load)/gen.capacity)*100)   # percent of generator capacity
fire_flow_time = 2  # hrs
safety_factor = 4

# PROPANE PROPERTIES
v_prop = 36.39      # cu. ft
btu_per_gal = 91547 # btu/gal
v_bottle = 500      # gal : start with 500 gal, program will increase if needed
num_bottles = 1     # start with 1 bottle, program will define more if needed

# GENERATOR LOADS AND FLOWS
loads = [25, 50, 75, 100]               # % gen capacity
flows = [104, 147, 202, 246]            # scfh model dependent

# LINEAR REGRESSION TO FIND FLOW FOR SPECIFIC LOAD
slope, intercept, r_value, p_value, std_errt = linregress(loads, flows)

# CREATE LOAD-FLOW GRAPH LINE
load_arr = np.linspace(0,100,101)
f_arr = []
for load in load_arr:
    f_arr.append(slope * load + intercept)

# DEFINE FLOWS BASED ON FULL AND NORMAL LOAD
full_flow = f_arr[full_load+1]  # scfh
norm_flow = f_arr[norm_load+1]  # scfh

# VAPORIZATION RATE OF PROPANE (rule of thumb)
tank_d = [37, 41]      # inches
tank_l = [119, 192]    # inches
temp_factor = 2
fill_factor = 60

vap = []
for d, l in zip(tank_d, tank_l):
    vr = d*l*temp_factor*fill_factor
    vap.append((vr, vr/btu_per_gal))

# DEFINE PROPANE FLOWS    
q_fire = full_flow/v_prop   # gph
q_dom = norm_flow/v_prop    # gph
q_total = flows[-1]/v_prop  # gph
total_btu = btu_per_gal * q_total   # btu/hr

# PROPANE VOLUMES
v_effective = num_bottles * v_bottle * 0.6          # gal
v_fire = q_fire * fire_flow_time * safety_factor    # gal

# TIME TO EMPTY
t_empty_hr = (v_effective - v_fire)/q_dom           # hrs
t_empty_day = t_empty_hr / 24                       # days

# IF 500 GAL IS NOT SUFFICIENT BUMP TO 1000 GAL BOTTLE
if t_empty_day < 4:
    v_bottle = 1000
    v_effective = num_bottles * v_bottle * 0.6
    t_empty_hr = (v_effective - v_fire)/q_dom
    t_empty_day = t_empty_hr / 24

# IF 1 1000 GAL BOTTLE IS NOT SUFFICIENT INCREASE UNTIL IT IS    
while t_empty_day < 4:
    num_bottles += 1
    v_effective = num_bottles * v_bottle * 0.6
    t_empty_hr = (v_effective - v_fire)/q_dom
    t_empty_day = t_empty_hr / 24

# DEFINE VAPORIZATION RATE FOR BOTTLE VOLUME
if v_bottle == 500:
    vap_rate = vap[0][0]
    vap_rate_gal = vap[0][1]
else:
     vap_rate = num_bottles * vap[1][0]
     vap_rate_gal = num_bottles * vap[1][1]

# WARN IF VAPORIZATION RATE IS LESS THAN FULL FLOW
if vap_rate_gal < q_fire:
    print('WARNING: The Vaporation Rate is less than Full Capacity Flow. Increase tank size or quanitity')
else:
    print('Generating csv file now...')

# VALUES FOR CSV FILE
value_list = [
              water_system,
              eng_file,
              project_name,
              project_number,
              gen_model,
              flows[0],
              flows[1],
              flows[2],
              flows[3],
              full_load,
              norm_load,
              v_bottle,
              v_effective,
              round(full_flow,2),
              round(norm_flow,2),
              round(v_fire,2),
              round(q_fire,2),
              round(q_dom,2),
              round(t_empty_hr,2),
              round(t_empty_day,2),
              round(vap_rate,1),
              round(vap_rate_gal,1),
              round(total_btu,1),
              num_bottles,
              safety_factor,
              round(q_total,2)
              ]
# FILE NAMES
filename = eng_file + ' ' + water_system + ' ' + gen_model + '.csv'
figure_name = eng_file + ' ' + water_system + ' ' + gen_model + '.png'

# WRITE CSV
with open(path.join(path.dirname(__file__), filename), 'w') as csvfile:
    cwriter = csv.writer(csvfile, delimiter=',',
                         quotechar='|', quoting=csv.QUOTE_MINIMAL)
    cwriter.writerow(header_list)
    cwriter.writerow(value_list)

# CREATE FLOW VS LOAD GRAPHIC FOR DOCUMENT
p1_text = 'All pumps running \n ({0:}, {1:.2f})'.format(full_load, full_flow)
p0_text = 'Domestic pumps running \n ({0:}, {1:.2f})'.format(norm_load, norm_flow)
plt.plot(loads, flows, 'o')
plt.plot(load_arr, f_arr)
plt.plot([norm_load, full_load], [norm_flow, full_flow], '*', ms=15)
plt.title('Propane Vapor Flow vs. Load %')
plt.xlabel('% Load')
plt.ylabel('Flow (scfh)')
#plt.text(full_load - 22, full_flow - 5, p1_text)
#plt.text(norm_load + 7, norm_flow - 5, p0_text)
plt.grid()
plt.savefig(path.join(path.dirname(__file__), figure_name))
print('days until empty: ', t_empty_day, '\nnumber of bottles:', num_bottles, '\nbottle size: ', v_bottle)
print('total load: ', gen.total_load)
print(gen.load_dict)
print('All done!')
