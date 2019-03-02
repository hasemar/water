'''
Genset:
    This module helps size auxiliary power for a pumping system based on 
    electrical loads.
'''
from __future__ import print_function
import Water.tools as tools

load_kinds = {'3ph inductive': 0.89, '1ph inductive': 0.85, 'resistive': 1}

class Genset:
    def __init__(self):
        self.load_list = []
        self.total_load = 0

    def add_load(self, power, kind):
        load_list = list(load_kinds.keys())
        if kind in load_list[:-1]:
            kVA = (power * 746 * .001/load_kinds[kind])
            self.load_list.append(kVA)
            self.total_load += kVA
        else:
            kw = power/1000
            self.load_list.append(kw)
            self.total_load += kw
    
    def delete_load(self, index):
        self.total_load -= self.load_list[index]
        print(self.load_list.pop(index), 'has been removed')
        

               