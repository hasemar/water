'''
Genset:
    This module helps size auxiliary power for a pumping system based on 
    electrical loads.
'''
from __future__ import print_function
import Water.tools as tools

load_kinds = {'3ph inductive': 0.89, '1ph inductive': 0.85, 'resistive': 1}

class Genset:
    '''Genset Class:
        object defined to define generator loads
        attributes:
            - voltage: generator voltage (V)
            - phase: generator phase
            - capacity: the power capacity of the generator (kW) defaults to None
        methods:
            - add_load: appends load to self.load_list and sums list to 
                calculate self.total_load
            - delete_load: deletes load fro self.load_list and decreases 
                self.total_load
    '''
    def __init__(self, voltage, phase, capacity=None):
        self.load_list = []
        self.voltage = voltage
        self.phase = phase
        self.capacity = capacity
        self.pf = {3 : 0.89, 1 : 0.85}

    @property
    def total_load(self):
        return sum(self.load_list)

    def add_motor_load(self, power, units='hp'):
        '''adds motor load to self.load_list uses kVA calculation
            based on power factors.
            
            attributes: 
                power: motor power
                units: power units(default hp)
                    unit options-> 'hp', 'kw'
        '''
        units = units.lower()
        if units == 'kw':
            kVA = power/self.pf[self.phase]
        elif units == 'hp':
            kVA = (power * 745.7 * .001/self.pf[self.phase])
        else:
            print('units not recognized: use "hp" or "kw"')
        self.load_list.append(kVA)
    
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
            self.load_list.append(power * 0.001)
        elif units == 'kw':
            self.load_list.append(power)
        else:
            print('units not recognized: use "kw" or "watts"')

    def delete_load(self, index):
        '''deletes specific load from self.load_list
            enter list index. prints verification when removed
        '''
        print(self.load_list.pop(index), 'has been removed')

    def set_pf(self, phase, power_factor):
        self.pf[phase] = power_factor
        print("power factor set to", self.pf[phase])
   