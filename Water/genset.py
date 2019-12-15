'''
Genset:

    This module helps size auxiliary power for a pumping system based on 
    electrical loads.
'''
from __future__ import print_function, division

class Genset:
    '''Defines a Genset object to calculate generator loads. 

    :param voltage:  generator output voltage (v)
    :param phase: generator phase (ph)
    :param capacity: generator load capaicty (kW), *default None*
    :param model: generator model, *default None*
    :param  mfg: generator manufacturer,  *default None*
    :type voltage: int
    :type phase: int
    :type capacity: int
    :type model: string
    :type mfg: string
    :return: Genset object
    :rtype: object

    :Example:  

    >>> from Water import Genset
    >>> gen = Genset(voltage=480, phase=3, capacity=120, model='AB120', mfg='Acme')
    
    '''
    def __init__(self, voltage, phase, capacity=None, model=None, mfg=None):
        self.load_dict = {'domestic':[], 'fire':[], 'resistive':[]}
        self.voltage = voltage
        self.phase = phase
        self.capacity = capacity
        self.model = model
        self._power_factors = {3 : 0.89, 1 : 0.85}
        self.consumption = []

    @property
    def fire_load(self):
        '''returns sum of all fire pump motor loads'''
        return sum(self.load_dict['fire'])
    @property
    def dom_load(self):
        '''returns sum of all domestic pump motor loads'''
        return sum(self.load_dict['domestic'])
    @property
    def res_load(self):
        '''returns sum of all resistive loads'''
        return sum(self.load_dict['resistive'])
    @property
    def total_load(self):
        '''returns sum total of domestic, fire and resistive loads'''
        return sum(sum(self.load_dict.values(),[]))
    @property
    def power_factors(self):
        '''returns power factors for apparent power'''
        return self._power_factors
    @property
    def full_load(self):
        '''returns percent genset is loaded under fire flow conditions (fully loaded)'''
        return int((self.total_load/self.capacity)*100)
    @property
    def normal_load(self):
        '''returns percent genset is loaded under normal conditions (domestic and resistive only)'''
        norm = self.total_load - self.fire_load
        return int((norm/self.capacity)*100)

    def add_motor_load(self, power, units='hp', fire=False):
        '''adds motor load to self.load_dict uses kVA calculation
        based on default power factors. All loads are saved in self.load_dict 
        in kilovolt-amps

            * 3-Phase motor power factor:  0.89
            * 1-Phase motor power factor: 0.85 

        :param power: motor power
        :param units: units of power ('hp' or 'kw'), *default hp*
        :param fire: enable fire-flow load, *default False*
        :type power: int/float
        :type units: string
        :type fire: boolean

        :Example:

        >>> gen.add_motor_load(power=5)   # adding domestic pump motor load
        >>> gen.add_motor_load(power=25, fire=True)   # adding fire-pump motor load
         
        '''

        units = units.lower()
        assert (units == 'hp' or units == 'kw'), "units must be either 'kw' or 'hp'"

        if units == 'kw':
            kVA = power/self.power_factors[self.phase]
        elif units == 'hp':
            kVA = (power * 745.7 * .001/self.power_factors[self.phase])

        if fire:
            self.load_dict['fire'].append(kVA)
        else:
            self.load_dict['domestic'].append(kVA)
    
    def add_resistive_load(self, power, units='kw'):
        '''adds resistive load to self.load_dict 

            *for example heaters, lights, controls...*
            
        :param power: resistive load power
        :param units: power units ('kw' or 'watts'), *default 'kw'*
        :type power: int/float
        :type units: string
        
        :Example:

        >>> gen.add_resistive_load(power=0.5)   
        >>> gen.add_resistive_load(power=500, units='watts')

        '''
        units = units.lower()
        assert (units == 'watts' or units == 'kw'), "units must be either 'kw' or 'watts'"

        if units == 'watts':
            self.load_dict['resistive'].append(power * 0.001)
        elif units == 'kw':
            self.load_dict['resistive'].append(power)

    def delete_load(self, load_type, index=-1):
        '''deletes specific load from self.load_dict
            Prints verification when removed.

        :param load_type: load type keyword ('fire', 'domestic', 'resistive')
        :param index: index number (use python index conventions), *default -1*
        :type load_type: string
        :type index: int

        :Example:

        >>> gen.show_loads()
            {'domestic': [4.189325842696629], 'fire': [20.94662921348315], 'resistive': [0.5, 0.5]}
        >>> gen.delete_load('resistive') 
            0.5 has been removed
        >>> gen.show_loads()
            {'domestic': [4.189325842696629], 'fire': [20.94662921348315], 'resistive': [0.5]}

        '''
        print(self.load_dict[load_type].pop(index), ' has been removed')

    def add_consumption(self, consumption_list):
        '''Sets consumption rate for Genset object
        
        Consumtion rates are entered as a 4 item list.
        Consumption values are in scfm and represent fuel consumed 
        at 25%, 50%, 75% and 100% capacity.

        :param consumption_list: fuel consumption at different capacities, in scfm
        :type consumption_list: list

        :Example: 

        >>> consumption_list=[100, 200, 300 400]  # scfm 
    
        '''
        self.consumption = consumption_list

    def change_power_factor(self, factor):
        '''Change the default power factor for the object.

        default power factors:   
            * 3-Phase motor power factor:  0.89
            * 1-Phase motor power factor: 0.85 

        :param factor: power factor
        :type factor: float
        
        '''
        self._power_factors[self.phase] = factor

    def show_loads(self):
        '''see loads in self.load_dict()
        
        :return: loads from the genset object
        :rtype: dictionary

        '''
        return self.load_dict

# test script
if __name__ == "__main__":
    gen = Genset(480, 3, 100)   # instantiate 480 volt 3 phase, 100 kw genset
    gen.add_motor_load(10)      # add 10 hp domestic pump motor
    gen.add_motor_load(power=7.5, units='hp', fire=False)  # add 7.5 hp domestic pump motor
    gen.add_resistive_load(500, units='watts') # add resistive load
    gen.add_motor_load(25, fire=True) # add 25 hp fire pump motor
    gen.add_motor_load(30, fire=True) # add 30 hp fire pump motor

    # example of printing out loads that have been entered
    load_report = '''
    fire-flow load = {0:.2f} kVA
    domestic load = {1:.2f} kVA
    resistive load = {3:.2f} kVA
    total load = {2:.2f} kVA
    '''.format(gen.fire_load, gen.dom_load, gen.total_load, gen.res_load)
    print(load_report)

    # deleting a load
    gen.delete_load('fire', index=1)
    gen.delete_load('resistive')
    load_report = '''
    fire-flow load = {0:.2f} kVA
    domestic load = {1:.2f} kVA
    resistive load = {3:.2f} kVA
    total load = {2:.2f} kVA
    '''.format(gen.fire_load, gen.dom_load, gen.total_load, gen.res_load)
    print(load_report)

    # add the fuel consumption rates of the genset
    gen.add_consumption([100, 150, 200, 250])
    print(gen.full_load, gen.normal_load)

    print(gen.power_factors)
