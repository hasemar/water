'''
SI Properties:
    Module to assign and access the most common properties of water
    used in fluid mechanics in SI units
'''

# H20 properties in SI units @ 20 deg celcius

density = 1000                  # kg/m^3
specific_weight = 9807          # N/m*3
dynamic_viscosity = 1.002e-3    # N*sec/m^2
kinematic_viscosity = 1.004e-6  # m^2/s
boiling_point = 100             # C 
melting_point = 0               # C
vapor_pressure = 2.338e3        # N/m*2 (absolute)
speed_of_sound = 1481           # m/s

def unit_info():
    info = '''
            density = 1000 kg/m^3
            specific_weight = 9807 N/m*3
            dynamic_viscosity = 1.002e-3 N*sec/m^2
            kinematic_viscosity = 1.004e-6 m^2/s
            boiling_point = 100 C 
            melting_point = 0 C
            vapor_pressure = 2.338e3 Pa (absolute)
            speed_of_sound = 1481 m/s
        '''
    print(info)
    return
    