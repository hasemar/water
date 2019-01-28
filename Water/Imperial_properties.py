'''
Imperial Properties:
    Module to assign and access the most common properties of water
    used in fluid mechanics in english units
'''

# H20 properties in imperial units @ 50 deg celcius

density = 1.94                  # slugs/ft^3
specific_weight = 62.41         # lb/ft^3
dynamic_viscosity = 2.73e-5     # lb*s/ft^2
kinematic_viscosity = 1.407e-5  # ft^2/s
boiling_point = 212             # F 
melting_point = 32              # F
vapor_pressure = 1.781e-1       # psi (absolute)
speed_of_sound = 4748           # ft/s

def unit_info():
    info = '''
            density = 1.94 slugs/ft^3
            specific_weight = 62.41 lb/ft^3
            dynamic_viscosity = 2.73e-5 lb*s/ft^2
            kinematic_viscosity = 1.407e-5 ft^2/s
            boiling_point = 212 F 
            melting_point = 32 F
            vapor_pressure = 1.781e-1 psia
            speed_of_sound = 4748 ft/s
        '''
    print(info)
    return
    