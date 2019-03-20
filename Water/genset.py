'''
Genset:
    This module helps size auxiliary power for a pumping system based on 
    electrical loads.
'''
from __future__ import print_function, division

class Genset:
    '''Genset Class:
        object defined to define generator loads
        attributes:
            - voltage: generator voltage (V)
            - phase: generator phase
            - capacity: the power capacity of the generator (kW) defaults to None
            - fire_list: list of fire flow motor loads
            - dom_list : list of domestic flow motor loads
            - pf: dict of power factors for 3ph and 1ph motor
        methods:
            - add_load: appends load to self.load_list and sums list to 
                calculate self.total_load
            - delete_load: deletes load fro self.load_list and decreases 
                self.total_load
    '''
    def __init__(self, voltage, phase, capacity=None, model=None):
        self.load_dict = {'domestic':[], 'fire':[], 'resistive':[]}
        self.voltage = voltage
        self.phase = phase
        self.capacity = capacity
        self.model = model
        self._power_factors = {3 : 0.89, 1 : 0.85}

    @property
    def fire_load(self):
        return sum(self.load_dict['fire'])
    @property
    def dom_load(self):
        return sum(self.load_dict['domestic'])
    @property
    def res_load(self):
        return sum(self.load_dict['resistive'])
    @property
    def total_load(self):
        return sum(sum(self.load_dict.values(),[]))
    @property
    def power_factors(self):
        return self._power_factors
    @power_factors.setter
    def power_factors(self, pwr_factor):
        self._power_factors[self.phase] = pwr_factor

    def add_motor_load(self, power, units='hp', fire=False):
        '''adds motor load to self.load_list uses kVA calculation
            based on power factors.
            
            attributes: 
                power: motor power
                units: power units(default hp)
                    unit options-> 'hp', 'kw'
        '''
        units = units.lower()
        if units == 'kw':
            kVA = power/self.power_factors[self.phase]
        elif units == 'hp':
            kVA = (power * 745.7 * .001/self.power_factors[self.phase])
        else:
            print('units not recognized: use "hp" or "kw"')
        if fire:
            self.load_dict['fire'].append(kVA)
        else:
            self.load_dict['domestic'].append(kVA)
    
    def add_resistive_load(self, power, units='kw'):
        '''adds resistive load to self.load_list
            E.G. heaters, lights, controls...
            
            attributes: 
                power: power
                units: power units(default kw)
                    unit options-> 'kw', 'watts'
        '''
        units = units.lower()
        if units == 'watts':
            self.load_dict['resistive'].append(power * 0.001)
        elif units == 'kw':
            self.load_dict['resistive'].append(power)
        else:
            print('units not recognized: use "kw" or "watts"')

    def delete_load(self, load_type, index=-1):
        '''deletes specific load from self.load_dict
            enter load_type, list index. 
            prints verification when removed
            default index is last item in list (-1)
            load_types = 'fire', 'domestic', 'resistive'
        '''
        print(self.load_dict[load_type].pop(index), ' has been removed')

if __name__ == "__main__":
    gen = Genset(480, 3, 100)
    gen.add_motor_load(10)
    gen.add_motor_load(7.5)
    gen.add_resistive_load(500, units='watts')
    gen.add_motor_load(25, fire=True)
    gen.add_motor_load(30, fire=True)

    load_report = '''
    fire-flow load = {0:.2f} kVA
    domestic load = {1:.2f} kVA
    resistive load = {3:.2f} kVA
    total load = {2:.2f} kVA
    '''.format(gen.fire_load, gen.dom_load, gen.total_load, gen.res_load)
    print(load_report)

    gen.delete_load('fire', index=1)
    gen.delete_load('resistive')
    load_report = '''
    fire-flow load = {0:.2f} kVA
    domestic load = {1:.2f} kVA
    resistive load = {3:.2f} kVA
    total load = {2:.2f} kVA
    '''.format(gen.fire_load, gen.dom_load, gen.total_load, gen.res_load)
    print(load_report)

    print(gen.power_factors)