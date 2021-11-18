"""
Imperial Properties:
    Module to assign and access the most common properties of water
    used in fluid mechanics in english units
"""

# H20 properties in imperial units @ 50 deg celcius

density = 1.94                  # slugs/ft^3
specific_weight = 62.4         # lbf/ft^3
dynamic_viscosity = 2.73e-5     # lb*s/ft^2
kinematic_viscosity = 1.407e-5  # ft^2/s
boiling_point = 212             # F 
freezing_point = 32              # F
vapor_pressure = 1.781e-1       # psi (absolute)
speed_of_sound = 4748           # ft/s
g = 32.2                        # ft/s^2

def unit_info():
    """Displays default unit information.\n
    - density = 1.94 slugs/ft^3
    - specific_weight = 62.4 lb/ft^3
    - dynamic_viscosity = 2.73e-5 lb*s/ft^2
    - kinematic_viscosity = 1.407e-5 ft^2/s
    - boiling_point = 212 F 
    - freezing_point = 32 F
    - vapor_pressure = 1.781e-1 psia
    - speed_of_sound = 4748 ft/s
    - g = 32.2 ft/s^2

    """
    
    info = f"""
            density = {density} slugs/ft^3
            specific_weight = {specific_weight} lb/ft^3
            dynamic_viscosity = {dynamic_viscosity} lb*s/ft^2
            kinematic_viscosity = {kinematic_viscosity} ft^2/s
            boiling_point = {boiling_point} F 
            freezing_point = {freezing_point} F
            vapor_pressure = {vapor_pressure} psia
            speed_of_sound = {speed_of_sound} ft/s
            g = {g} ft/s^2
        """
    print(info)
    return
    