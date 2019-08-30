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
    'Goulds 3657' : '3657_1-5X2_GOULDS_3500.csv',
    'Goulds 3642' : '3642_1x1-25_GOULDS_3500.csv',
    'Grunfos CM1' : 'CM1-2-A-GRUNFOS.csv',
    'Goulds 25GS50' : '25GS50-GOULDS_3500.csv',
    'Goulds 35GS50' : '35GS50-GOULDS_3500.csv',
    'Goulds 75GS100CB' : '75GS100CB-GOULDS_3500.csv',
    'Goulds 85GS100' : '85GS100-GOULDS_3500.csv',
    'Grundfos CMBE 5-62' : 'CMBE_5-62-GRUNFOS.csv',
    'Goulds 85GS75' : '85GS75-GOULDS_3500.csv',
    'Grundfos 85S100-9': '85S100-9-Grundfos_3500.csv'
    }
class Pump:
    '''Defines Tank object to plot and/or affinitized pump curve and performance\n

    attributes:\n
    - flow_list: list of flows for pump curve (volumetric units) default=empty list
    - head_list: list of head pressure for pump curve (pressure units) default=empty list
    - eff_list: list of efficiencies for pump curve (float 0>eff<1 units) default=None
    - model: pump model as string default=None
    - rpm: pump motor rpm as int default=None
    - imp: pump impeller size as float (distance units) default=None

    properties:\n
    - vfd_flow: affinitized flow data
    - vfd_head: affinitized head data
    - vfd_eff: affinitized efficiencty data

    methods:\n
    - load_pump: loads a saved pump curve from /pumps folder
    - affinitize: takes pump curve info and applies affinity laws to the curve
        params:\n 
        - pump_data: flow, head or efficiency list
        - pwr: exponent for operation (1 for flow, 2 for head, 3 for eff)

    - plot_curve: plots pump curve with affinitized data, also plot system curve if entered
        params:\n
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
        self.fig = None
        self.affinity_data = []
        self.ax1 = None
        self.ax2 = None


    def load_pump(self, selection):
        '''loads pump data from /pump folder included in package directory. Pump data
        is in .csv format and loaded from a dictionary in class (not ideal).\n

        available_pumps = {\n
        'Goulds 3657' : '3657_1-5X2_GOULDS_3500.csv',\n
        'Goulds 3642' : '3642_1x1-25_GOULDS_3500.csv'\n
        'Grunfos CM1' : 'CM1-2-A-GRUNFOS.csv',\n
        'Goulds 25GS50' : '25GS50-GOULDS_3500.csv',\n
        'Goulds 35GS50' : '35GS50-GOULDS_3500.csv',\n
        'Goulds 75GS100CB' : '75GS100CB-GOULDS_3500.csv',\n
        'Grundfos 85S100-9': '85S100-9-Grundfos_3500.csv'\n
        }0
        

        #TODO make this more user friendly so the class source code does not have to be changed every
        time a pump is added to /pump folder.

        '''
        f = []
        h = []
        ef = []
        available_pumps = {
        'Goulds 3657' : '3657_1-5X2_GOULDS_3500.csv',
        'Goulds 3642' : '3642_1x1-25_GOULDS_3500.csv',
        'Grunfos CM1' : 'CM1-2-A-GRUNFOS.csv',
        'Goulds 25GS50' : '25GS50-GOULDS_3500.csv',
        'Goulds 35GS50' : '35GS50-GOULDS_3500.csv',
        'Goulds 75GS100CB' : '75GS100CB-GOULDS_3500.csv',
        'Goulds 85GS100' : '85GS100-GOULDS_3500.csv',
        'Grundfos CMBE 5-62' : 'CMBE_5-62-GRUNFOS.csv',
        'Goulds 85GS75' : '85GS75-GOULDS_3500.csv',
        'Grundfos 85S100-9': '85S100-9-Grundfos_3500.csv'
        }
        
        
        file_path = pumps_dir + '/' + available_pumps[selection]
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
    
            for line in csv_reader:
                if line[0]:
                    self.model = line[0]
                    self.rpm = int(line[1])
                    self.impeller = line[2]
                f.append(int(line[3]))
                h.append(int(line[4]))
                ef.append(float(line[5]))
            self.flow = f
            self.head = h
            self.eff = ef

    @property
    def vfd_flow(self):
        ''' returns a numpy array of affinitized flows'''
        return self.affinitize(self.flow, 1)

    @property
    def vfd_head(self):
        ''' returns a numpy array of affinitized heads'''
        return self.affinitize(self.head, 2)

    @property
    def vfd_eff(self):
        ''' returns a numpy array of affinitized efficiencies'''
        return self.affinitize(self.eff, 3)

    def affinitize(self, pump_data, pwr):
        '''creates affinitized curves for flow, head and efficiency for motor speeds at:\n
        Frequency =\n
        - 60 hz
        - 50 hz
        - 40 hz
        - 30 hz
        - 20 hz
        - 10 hz

        '''
        percent_speed = (np.linspace(60,10,6)/60)**pwr
        
        for percent in percent_speed:
            self.affinity_data.append([data * percent for data in pump_data])
        return self.affinity_data

    def plot_curve(self, target_flow=None, tdh=None, vfd=True, eff=False):
        '''returns a matplotlib plot of the pump curve.\n
        Default is to plot affinitized curves with full speed curve. 
        User has option to add system curve and efficiency curve
        '''
        title_str = 'Pump: ' + self.model + ' - ' + str(self.rpm) + ' RPM - ' + str(self.impeller) + '" impeller'
        self.fig, self.ax = plt.subplots(2,1)

        if eff:
            self.ax[0] = plt.subplot2grid((3,1), (0,0), rowspan=2)
            self.ax[1] = plt.subplot2grid((3,1), (2,0))

            self.ax[1].plot(self.flow, self.eff, label='efficiency', color='grey')
            self.ax[1].set_ylabel('efficiency')
            self.ax[1].set_xlabel('flow (gpm)')
            self.ax[1].grid(True, alpha=0.5, which='both')
        else:
            self.ax[0] = plt.subplot2grid((2,1), (0,0), rowspan=2)
            self.ax[0].set_xlabel('flow (gpm)')

        if vfd:
            labels = ['60Hz', '50Hz', '40Hz', '30Hz', '20Hz', '10Hz'] 
            for h, l in zip(self.vfd_head, labels):
                self.ax[0].plot(self.flow, h, label=l)
        else:
            self.ax[0].plot(self.flow, self.head, label='60hz')

        if np.any(target_flow) and np.any(tdh):
            self.ax[0].plot(target_flow, tdh,
                            '.-.',
                            color="red", 
                            label='system', 
                            markersize=5,
                            lw=0.75)
        
        self.ax[0].grid(True, alpha=0.5, which='both',)
        self.ax[0].set_title(title_str)
        self.ax[0].set_ylabel('head (ft)')
        self.ax[0].legend()
        self.ax[1].legend()
        self.fig.tight_layout()
        plt.show()

    def find_head(self, flow):
        ''' Returns head value from pump curve based on flow input.
            If flow is not a known value it will interprolate between the
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
    pump2 = Pump()
    pump.load_pump('Goulds 3657')
    pump2.load_pump('Grunfos CM1')
    '''
    for obs in pump.vfd_eff:
        for data in obs:
            print(data)
    '''
    system_flow = np.linspace(1, 150, 30)
    system_head = []
    for flow in system_flow:
        system_head.append(100 + 20*np.exp(-1/(flow*.005)))

    design_x = 50
    design_y = 60

    pump.plot_curve(system_flow, system_head, vfd=False, eff=True)
    pump2.plot_curve(design_x, design_y, eff=True)

    # TODO  Program halts after plt.show. 
    # Need to figure out howto show plots while running program.