'''Pumps Module:
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
    'Goulds 25GS50' : '25GS50-GOULDS_3500.csv',
    'Goulds 35GS50' : '35GS50-GOULDS_3500.csv',
    'Goulds 75GS100CB' : '75GS100CB-GOULDS_3500.csv',
    'Grundfos 85S100-9': '85S100-9-Grundfos_3500.csv'
    }
class Pump:
    '''Pump Class:
        object defined to define affinitized pump curve and performance
        attributes:
            - flow_list: list of flows for pump curve (volumetric units) default=empty list
            - head_list: list of head pressure for pump curve (pressure units) default=empty list
            - eff_list: list of efficiencies for pump curve (float 0>eff<1 units) default=None
            - model: pump model as string default=None
            - rpm: pump motor rpm as int default=None
            - imp: pump impeller size as float (distance units) default=None
        properties:
            - vfd_flow: affinitized flow data
            - vfd_head: affinitized head data
            - vfd_eff: affinitized efficiencty data
        methods:
            - load_pump: loads a saved pump curve from /pumps folder
            - affinitize: takes pump curve info and applies affinity laws to the curve
                params: 
                    - pump_data: flow, head or efficiency list
                    - pwr: exponent for operation (1 for flow, 2 for head, 3 for eff)
            - plot_curve: plots pump curve with affinitized data, also plot system curve if entered
                params:
                    - target_flow: system curve flow as list or point
                    - tdh: system curve head as list or point
            - find_head: lookup head condition from flow input.
    '''     
    def __init__(self, flow_list=[], head_list=[], eff_list=[], model='', rpm=None, imp=None):
        self.flow = flow_list
        self.head = head_list
        self.eff = eff_list
        self.model = model
        self.rpm = rpm
        self.impeller = imp

    def load_pump(self, selection):
        '''
        available_pumps = {
        'Goulds 3657' : '3657_1-5X2_GOULDS_3500.csv',
        'Goulds 3642' : '3642_1x1-25_GOULDS_3500.csv'
        'Grunfos CM1' : 'CM1-2-A-GRUNFOS.csv',
        'Goulds 25GS50' : '25GS50-GOULDS_3500.csv',
        'Goulds 35GS50' : '35GS50-GOULDS_3500.csv',
        'Goulds 75GS100CB' : '75GS100CB-GOULDS_3500.csv',
        'Grundfos 85S100-9': '85S100-9-Grundfos_3500.csv'
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
        return self.affinitize(self.flow, 1)

    @property
    def vfd_head(self):
        return self.affinitize(self.head, 2)

    @property
    def vfd_eff(self):
        return self.affinitize(self.eff, 3)

    def affinitize(self, pump_data, pwr):
        '''creates affinitized curves based on motor speed'''
        percent_speed = (np.linspace(60,10,6)/60)**pwr
        affinity_data = []
        for percent in percent_speed:
            affinity_data.append([data * percent for data in pump_data])
        return affinity_data

    def plot_curve(self, target_flow=None, tdh=None, vfd=True, eff=False):
        '''returns a matplotlib plot of the pump curve. 
        default is to plot affinitized curves with full
        speed curve.  User has option to add system curve.
        '''
        title_str = 'Pump: ' + self.model + ' - ' + str(self.rpm) + ' RPM - ' + str(self.impeller) + '" impeller'
        fig = plt.figure()
        if eff:
            ax1 = plt.subplot2grid((3,1), (0,0), rowspan=2)
            ax2 = plt.subplot2grid((3,1), (2,0))

            ax2.plot(self.flow, self.eff, label='efficiency', color='grey')
            ax2.set_ylabel('efficiency')
            ax2.set_xlabel('flow (gpm)')
            ax2.grid(True)
        else:
            ax1 = plt.subplot()
            ax1.set_xlabel('flow (gpm)') 
        if vfd:
            labels = ['60Hz', '50Hz', '40Hz', '30Hz', '20Hz', '10Hz'] 
            for h, l in zip(self.vfd_head, labels):
                ax1.plot(self.flow, h, label=l)
        else:
            ax1.plot(self.flow, self.head, label='60hz')

        if np.any(target_flow) and np.any(tdh):
            ax1.plot(target_flow, tdh, "-.",color="blue", label='system')
        
        ax1.grid(True, alpha=0.5, which='both',)
        ax1.set_title(title_str)
        ax1.set_ylabel('head (ft)')
        ax1.legend()
        fig.tight_layout()
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
            print("Value not found, check you numbers")

        return head

if __name__=="__main__":
    print('test script:')

    pump = Pump()
    #pump2 = Pump()
    pump.load_pump('Goulds 3657')
    #pump2.load_pump('Grunfos CM1')

    for obs in pump.vfd_eff:
        for data in obs:
            print(data)
    system_flow = np.arange(20, 80, 3)
    system_head = np.arange(80, 100)
    design_x = 50
    design_y = 60

    pump.plot_curve(system_flow, system_head, vfd=False, eff=True)
    #pump2.plot_curve(design_x, design_y)

    # TODO  plot method is drawing both pump objects. Also program halts after plt.show. 
    # Need to figure out how to make each plot its own object and to show plots while running program.