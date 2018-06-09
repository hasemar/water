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
    'Grunfos CM1' : 'CM1-2-A-GRUNFOS.csv'
    }

def affinitize(pump_data, pwr):
    percent_speed = (np.linspace(10,60,6)/60)**pwr
    affinity_data = []
    for percent in percent_speed:
        affinity_data.append(data * percent for data in pump_data)
    return affinity_data

class Pump:
    def __init__(self):
        self.flow = []
        self.head = []
        self.eff = []
        self.model = ''
        self.rmp = 0
        impeller = 0.0

    def load_pump(self, selection):
        '''
        available_pumps = {
        'Goulds 3657' : '3657_1-5X2_GOULDS_3500.csv',
        'Grunfos CM1' : 'CM1-2-A-GRUNFOS.csv'
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
                    self.impeller = float(line[2])
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

    def plot_curve(self):
        title_str = 'Pump: ' + self.model + ' - ' + str(self.rpm) + ' RPM - ' + str(self.impeller) + '" impeller'
        c = np.polyfit(self.flow, self.head, 3)
        p = np.poly1d(c)
        f = np.linspace(min(self.flow), max(self.flow), 100)
        plt.plot(f, p(f))
        plt.grid(True)
        plt.title(title_str)
        plt.xlabel('flow (gpm)')
        plt.ylabel('head (ft)')
        plt.legend('60Hz')
        plt.show()


if __name__=="__main__":
    print('test script:')

    pump = Pump()
    pump.load_pump('Goulds 3657')
    for obs in pump.vfd_flow:
        for data in obs:
            print(data)
    
    
    #pump.plot_curve()
