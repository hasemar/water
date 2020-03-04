from Water import Tank, tools
import matplotlib.pyplot as plt

# create a dictionary for the tank parameters
tank_data = {
            'name' : 'Horizontal Tank',
            'diameter' : 10,
            'length' : 20,
            'freeboard' : 1,
            'deadstorage' : 0,
            'elevation' : 100,
            'shape' : 'horizontal'
            }

#instantiate object
horiz_tank = Tank(**tank_data)

vols = []
for level in range(0, horiz_tank.diameter+1):
    vols.append(horiz_tank.horizontal_vol(level))

# plot a graph of the volume change while the tank is filling
plt.plot(vols)
plt.title('Volume While Tank is Filling')
plt.xlabel('Water Level (ft)')
plt.ylabel('Volume of Water (cu. ft.)')
#plt.show()

# create a dictionary for the tank parameters
data = {
    'name' : 'Tank 1',
    'diameter' : 60,
    'height' : 45,
    'freeboard' : 3,
    'deadstorage' : 2,
    'elevation' : 230
    }

# instantiate object
tank_1 = Tank(**data)

print(tank_1.vol, 'gallons')

print(tank_1.getInfo())