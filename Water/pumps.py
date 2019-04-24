'''
Pumps Module:
    This module calculates and produces pump curves based on mfg's data points
'''
from __future__ import print_function, division
import csv
import matplotlib.pyplot as plt
import numpy as np
from os import path

pumps_dir = path.join(path.dirname(__file__), 'pumps')

available_pumps = {
    'Goulds 3657' : '3657_1-5x2_GOULDS_3500.csv',
    'Goulds 3642' : '3642_1x1-25_GOULDS_3500.csv',
    'Grunfos CM1' : 'CM1-2-A-GRUNFOS.csv',
    'Goulds 25GS50' : '25GS50-GOULDS_3500.csv'
    }

def affinitize(pump_data, pwr):
    ''' takes pump data and creates affinitized curves
        based on motor speed
    '''
    percent_speed = (np.linspace(60,10,6)/60)**pwr
    affinity_data = []
    for percent in percent_speed:
        affinity_data.append([data * percent for data in pump_data])
    return affinity_data

class Pump:
    def __init__(self):
        self.flow = []
        self.head = []
        self.eff = []
        self.model = ''
        self.rmp = 0
        self.impeller = 0.0

    def load_pump(self, selection):
        '''
        available_pumps = {
        'Goulds 3657' : '3657_1-5X2_GOULDS_3500.csv',
        'Goulds 3642' : '3642_1x1-25_GOULDS_3500.csv'
        'Grunfos CM1' : 'CM1-2-A-GRUNFOS.csv',
        'Goulds 25GS50' : '25GS50-GOULDS_3500.csv'
        }
        '''
        file_path = pumps_dir + '/' + available_pumps[selection]
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
    
            for line in csv_reader:
                if line[0]:
                    self.model = line[0]
                    self.rpm = int(line[1])
                    self.impeller = line[2]
                self.flow.append(int(line[3]))
                self.head.append(int(line[4]))
                self.eff.append(float(line[5]))

    @property
    def vfd_flow(self):
        return affinitize(self.flow, 1)

    @property
    def vfd_head(self):
        return affinitize(self.head, 2)

    @property
    def vfd_eff(self):
        return affinitize(self.eff, 3)

    def plot_curve(self, target_flow=None, tdh=None):
        title_str = 'Pump: ' + self.model + ' - ' + str(self.rpm) + ' RPM - ' + str(self.impeller) + '" impeller'
        for h in self.vfd_head:
            plt.plot(self.flow, h)
        if np.any(target_flow) and np.any(tdh):
            plt.plot(target_flow, tdh, "o")
        plt.grid(True)
        plt.title(title_str)
        plt.xlabel('flow (gpm)')
        plt.ylabel('head (ft)')
        plt.legend(['60Hz', '50Hz', '40Hz', '30Hz', '20Hz', '10Hz'])
        plt.show()

    def find_head(self, flow):
        ''' Returns head value from pump curve based on flow input.
            if flow is not a known value it will interprolate between the
            two closest points on the curve.
        '''
        try:
            if flow in self.flow:
                head = self.head[self.flow.index(flow)]
            else:
                head = np.interp(flow, self.flow, self.head)
        except ValueError:
            print(" Value not found, check you numbers")

        return head

if __name__=="__main__":
    print('test script:')

    pump = Pump()
    pump2 = Pump()
    pump.load_pump('Goulds 3657')
    pump2.load_pump('Grunfos CM1')

    for obs in pump.vfd_eff:
        for data in obs:
            print(data)
    
    
    pump.plot_curve(60, 50)
