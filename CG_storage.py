'''
Cedar Grove Initial Storage Calcs
2-15-18 - Ryan Haseman
'''
import numpy as np
from Water import *

# define functions
def ft2psi(feetH20):
    psi = feetH20 * 0.4335
    return psi

### SYSTEM INFO ###
MDD = 430.0     # gpd/ERU
N = 95         # ERU's
F = 25          # from table 5.1 in DOH man
C = 2.5           # from table 5.1 in DOH man
Q_fire = 0    # gpm
t_fire = 0     # minutes

### SUPPLY ###

# wells #
well_1 = 50     # gpm


Qs = well_1
time_mdd = (N*MDD)/(Qs*60)  

# existing tanks #
'''
2 tanks on-site using list format [tank1,tank2]
'''
dims = {      #[tank1, tank2, tank3]
        'name' : ['Tank 1', 'Tank 2'],
        'diameter' : [7.83, 8],
        'height' : [7.83, 10],
        'freeboard' : [1, 1],
        'deadstorage' : [.1 ,0],
        'elevation' : [115, 245]
        'shape' : : ['horizontal', 'vertical']
        }
tanks = []
total_vol = 0.0

# creating 3 tank objects with above stated dimensions
for n, d, h, fb, ds, el, s in zip(
                               dims['name'],
                               dims['diameter'],
                               dims['height'],
                               dims['freeboard'],
                               dims['deadstorage'],
                               dims['elevation'],
                               dims['shape']
                               ):
    tanks.append(Tank(name=n, diameter=d, height=h, freeboard=fb, deadstorage=ds, elevation=el, shape=s))

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
SB_theo = SB_initial - min([well_1])*1440    # minimum theoretical standby storage

SB = max([SB_theo, SB_doh])       # use greater value of DOH and theoretical

# fire flow
FFS = Q_fire * t_fire             # gal  (per Pierce County rule)

if FFS < SB:   # if true nest fire flow storage
    FFS = 0

OS = total_vol - (ES + SB + FFS)

###### Storage Head Pressure ######

suction_head = 0




#### PRINT INFO #####
print "System Info:"
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
