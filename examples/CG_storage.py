'''
Cedar Grove Initial Storage Calcs
2-15-18 - Ryan Haseman
'''
from Water import *

# define functions
def ft2psi(feetH20):
    psi = feetH20 * 0.4335
    return psi

### SYSTEM INFO ###
system_name = 'Cedar Grove'
MDD = 430.0     # gpd/ERU
N = 95         # ERU's
F = 25          # from table 5.1 in DOH man
C = 2.5           # from table 5.1 in DOH man
Q_fire = 0    # gpm
t_fire = 0     # minutes
genset = True

### SUPPLY ###

# wells #
# Cedar Grove wells operate on an OR basis
well_1a = 50     # gpm
well_1b = 50     # gpm


Qs = well_1a
time_mdd = (N*MDD)/(Qs*60)  

# existing tanks #
'''
2 tanks on-site using list format [tank1,tank2]
'''
dims = {      #[tank1, tank2]
        'name' : ['wellsite #1', 'Sunny Jim'],
        'diameter' : [7.83, 8],
        'height' : [0, 10],
        'length' : [22, 0],
        'freeboard' : [1, 1],
        'deadstorage' : [.1 ,.1],
        'elevation' : [115, 245],
        'shape' : ['horizontal', 'vertical']
        }
tanks = []
total_vol = 0.0

# creating 2 tank objects with above stated dimensions
for n, d, h, l, fb, ds, el, s in zip(
                               dims['name'],
                               dims['diameter'],
                               dims['height'],
                               dims['length'],
                               dims['freeboard'],
                               dims['deadstorage'],
                               dims['elevation'],
                               dims['shape']
                               ):
    tanks.append(Tank(name=n, diameter=d, height=h, length=l, freeboard=fb, deadstorage=ds, elevation=el, shape=s))

for tank in tanks:
    total_vol += tank.useable
    
### DEMAND ###
PHD, ADH, LHD = tools.PHD(MDD, N)

### Capacity ###
# equalizing storage
ES = tools.equalizing_storage(PHD, Qs)              # gal 

# standby storage
SB_doh = 200*N                    # gal  DOH min recommended standby storage
SB_initial = N*MDD                # gal  initial required standby storage
SB_theo = SB_initial - min([well_1a, well_1b])*1440    # minimum theoretical standby storage

SB = max([SB_theo, SB_doh])       # use greater value of DOH and theoretical
if genset:
    SB_credit = min([well_1a, well_1b]) * 60 * 24
    SB -= SB_credit
if SB < 0:
    SB = 0

# fire flow
FFS = Q_fire * t_fire             # gal  (per Pierce County rule)

if FFS < SB:   # if true nest fire flow storage
    FFS = 0

OS = total_vol - (ES + SB + FFS)

#### PRINT INFO #####
info ='''
    System Info: \r\n
    Water System: {0} \r\n
    Peak Hour Demand: {1:.2f} GPM \r\n
    Time to max production is achieved in {2:.1f} hrs \r\n
    '''.format(system_name, PHD, time_mdd)

if time_mdd < 18:
    info += "Source production is adequate for {} ERU's \r\n".format(N)
else:
    info += "WARNING: SOURCE PRODUCTION IS NOT ADEQUATE FOR THIS NUMBER OF ERU'S \r\n"

print(info)
[print(tank.getInfo(SB, ES, OS, FFS, total_vol, details=True)) for tank in tanks]

