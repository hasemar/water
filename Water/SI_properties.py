'''
SI Properties:
    Module to assign and access the most common properties of water
    used in fluid mechanics in SI units
'''

# H20 properties in SI units @ 10 deg celcius

density = 999.7                  # kg/m^3
specific_weight = 9807          # N/m*3
dynamic_viscosity = 1.31e-3    # N*sec/m^2
kinematic_viscosity = 1.31e-6  # m^2/s
boiling_point = 100             # C 
freezing_point = 0               # C
vapor_pressure = 1.23e3        # N/m*2 (absolute)
speed_of_sound = 1481           # m/s
g = 9.81                        # m/s^2

def unit_info():
    '''Displays default unit information

    - density = 999.7 kg/m^3
    - specific_weight = 9807 N/m*3
    - dynamic_viscosity = 1.31e-3  N*sec/m^2
    - kinematic_viscosity = 1.31e-6  m^2/s
    - boiling_point = 100 C 
    - freezing_point = 0 C
    - vapor_pressure = 1.23e3 N/m*2 (absolute)
    - speed_of_sound = 1481 m/s
    - g = 9.81 m/s^2

    '''
    info = '''
            density = 999.7 kg/m^3
            specific_weight = 9807 N/m*3
            dynamic_viscosity = 1.31e-3 N*sec/m^2
            kinematic_viscosity = 1.31e-6 m^2/s
            boiling_point = 100 C 
            melting_point = 0 C
            vapor_pressure = 1.23e3 Pa (absolute)
            speed_of_sound = 1481 m/s
            g = 9.81 m/s^2
        '''
    print(info)
    return
    