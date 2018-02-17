'''
Raft Island Initial Storage Calcs
2-3-18 - Ryan Haseman
'''
import numpy as np
from Water import *

# define functions
def ft2psi(feetH20):
    psi = feetH20 * 0.4335
    return psi

### SYSTEM INFO ###
system = 'Raft Island - Booster Pump Station'
MDD = 635.0     # gpd/ERU
N = 232         # ERU's
F = 75          # from table 5.1 in DOH man
C = 2           # from table 5.1 in DOH man
Q_fire = 750    # gpm
t_fire = 45     # minutes


### SUPPLY ###

# wells #
well_1 = 93     # gpm
well_2 = 82    # gpm

Qs = well_1 + well_2    # total flow supply
time_mdd = (N*MDD)/(Qs*60)  

# existing tanks #
'''
3 tanks on-site using list format [tank1,tank2,tank3]
'''
dims = {      #[tank1, tank2, tank3]
        'name' : ['Tank 1', 'Tank 2', 'Tank 3'],
        'diameter' : [9, 13, 20],
        'height' : [22, 20, 20],
        'freeboard' : [1, 1, 1],
        'deadstorage' : [2 ,2 ,2],
        'elevation' : [157, 157, 157]
        }
tanks = []
total_vol = 0.0

# creating 3 tank objects with above stated dimensions
for n, d, h, fb, ds, el in zip(
                               dims['name'],
                               dims['diameter'],
                               dims['height'],
                               dims['freeboard'],
                               dims['deadstorage'],
                               dims['elevation']
                               ):
    tanks.append(Tank(name=n, diameter=d, height=h, freeboard=fb, deadstorage=ds, elevation=el))

for tank in tanks:
    total_vol += tank.useable
    
### DEMAND ###

PHD = (MDD/1440)*(C*N + F) + 18     # gpm  peak
AHD = PHD/1.74                      # gpm  average
LHD = AHD * 0.22                    # gpm  lowest

### Capacity ###

# equalizing storage
ES = (PHD-Qs)*150                 # gal 

# standby storage
SB_doh = 200*N                    # gal  DOH min recommended standby storage
SB_initial = N*MDD                # gal  initial required standby storage
SB_theo = SB_initial - min([well_1, well_2])*1440    # minimum theoretical standby storage

SB = max([SB_theo, SB_doh])       # use greater value of DOH and theoretical

# fire flow
FFS = Q_fire * t_fire             # gal  (per Pierce County rule)

if FFS < SB:   # if true nest fire flow storage
    FFS = 0

OS = total_vol - (ES + SB + FFS)

###### Storage Head Pressure ######

suction_head = 0




#### PRINT INFO #####
print "System Info: " + system
print "Peak Hour Demand is: {0:.2f} gmp".format(PHD)
print "Time to max production is achieved: {0:.1f} hrs".format(time_mdd)

if time_mdd < 18:
    print "Source production is adequate for {} ERU's".format(N)
else:
    print "WARNING: SOURCE PRODUCTION IS NOT ADEQUATE FOR THIS NUMBER OF ERU'S"

print "Equalizing Storage is: {0:.2f} gal".format(ES)
print "\n\r"

for tank in tanks:
    tank.getInfo(SB, ES, OS, total_vol, details=True)

