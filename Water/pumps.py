'''Pumps Module:
    This module calculates and produces pump curves based on mfg's data points
'''
from __future__ import print_function, division
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
from os import path

BASE_DIR = path.dirname(path.abspath(__file__))
db_path = path.join(BASE_DIR, "pumps.db")

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
    - load_pump: loads a pump from the pumps database
    - add_pump: adds a pump to the database
    - delete_pump: deletes a pump from the database
    - check_pump: check for a specific pump in the database
    - available_pumps: see all pumps in the database
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
    def __init__(self):
        self.flow = []
        self.head = []
        self.eff = []
        self.bep = [None, None]
        self.model = None
        self.mfg = None
        self.rpm = None
        self.impeller = None
        self.fig = None
        self.ax = None
        self.affinity_data = []

    def check_pump(self, pump_model, impeller=None):
        '''Checks database for existing pump
            pump_model: dtype=string
            impeller: dtype=string (default=None)'''

        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        existing_params = {'model' : pump_model, 'impeller' : impeller}
        
        if impeller:
            sqlquery='''SELECT * 
                        FROM 
                            pumps 
                        WHERE model=:model AND impeller=:impeller'''   
        else:
            sqlquery='''SELECT * 
                        FROM 
                            pumps 
                        WHERE model=:model''' 
    
        c.execute(sqlquery, existing_params)
        exists = c.fetchall()        
        conn.commit()
        conn.close()
    
        return exists

    def add_pump(self, **kwargs):
        '''Adds pump to pumps.db
            Use dictionary to specify parameters
            kwargs = 
                    {'model' : dtype=string model name,
                     'mfg' : dtype=string manufacturer,
                     'flow' : dtype=list length=8,
                     'head' : dtype=list length=8,
                     'eff' : dtype=list length=8,
                     'bep' : dtype=list [flow, head] of best efficiency point,
                     'rpm' : dtype=int motor rpm,
                     'impeller' : dtype=float impeller diameter} 
        '''
        self.flow = kwargs.get('flow', [])
        self.head = kwargs.get('head', [])
        self.eff = kwargs.get('eff', [])
        self.bep = kwargs.get('bep', [None, None])
        self.model = kwargs.get('model', None)
        self.mfg = kwargs.get('mfg', None)
        self.rpm = kwargs.get('rpm', None)
        self.impeller = kwargs.get('impeller', None)

        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        # check if pump currently exists in database
        exists = self.check_pump(self.model, self.impeller)
        
        if len(exists) == 0:
            sqlinsert = '''INSERT INTO 
                            pumps(
                                manufacturer,
                                model,
                                maxFlow,
                                minFlow,
                                bestFlow,
                                maxHead,
                                minHead,
                                bestHead,
                                bestEff,
                                rmp,
                                impeller,
                                flowArray,
                                headArray,
                                effArray) 
                            values(
                                :mfg,
                                :model,
                                :maxFlow,
                                :minFlow,
                                :bestFlow,
                                :maxHead,
                                :minHead,
                                :bestHead,
                                :bestEff,
                                :rpm,
                                :impeller,
                                :flowArray,
                                :headArray,
                                :effArray)'''

            params = {'mfg' : self.mfg,
                    'model': self.model,
                    'maxFlow' : max(self.flow),
                    'minFlow' : min(self.flow),
                    'bestFlow' : self.bep[0],
                    'maxHead' : max(self.head),
                    'minHead' : min(self.head),
                    'bestHead' : self.bep[1],
                    'bestEff': max(self.eff),    
                    'rpm' : self.rpm,
                    'impeller': self.impeller,
                    'flowArray' : str(self.flow),
                    'headArray' : str(self.head),
                    'effArray' : str(self.eff)}
            print('Pump added to database')
            c.execute(sqlinsert, params)
            conn.commit()
            conn.close()
        else:
            print('Pump Model exists in the database, check below for specific parameters:')
            for each_pump in exists:
                print(each_pump[:12])
        
    def available_pumps(self):
        '''returns pump table from pumps.db'''
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('''SELECT
                        pumpID,
                        manufacturer,
                        model,
                        bestFlow,
                        bestHead
                     FROM
                        pumps''')
        for eachPump in c.fetchall():
            print(eachPump)
        conn.commit()
        conn.close()
        
    def load_pump(self, mfg, model, impeller=None):
        '''loads pump from pumps.db
            Parameters
            ----------
            
            mfg: pump manufacturer dtype=string
            model: pump model dtype=string
            impeller: pump impeller size dtype=string (default=None)'''
        multiples = self.check_pump(model, impeller)
        print(multiples)
        if len(multiples) == 0:
            print('Pump does not exist in database.')
        elif len(multiples) > 1:
            print('Multiple pump models found in database, please include impeller diameter to select pump.')
        else:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            params = {'mfg' : mfg, 'model' : model, 'impeller' : impeller}
            if impeller == None:
                sqlquery = '''SELECT * FROM pumps
                              WHERE manufacturer=:mfg AND model=:model;
                           '''
            else:
                sqlquery = '''SELECT * FROM pumps
                              WHERE manufacturer=:mfg AND model=:model AND impeller=:impeller
                            '''
            c.execute(sqlquery, params)

            pump = c.fetchall()
            if len(pump) > 0:
                pump = pump[0]
                self.mfg = pump[1]
                self.model = pump[2]
                self.bep = (pump[5], pump[8])
                self.rpm = pump[10]
                self.impeller = pump[11]
                fstring = pump[12].strip('[]').split(',')
                hstring = pump[13].strip('[]').split(',')
                estring = pump[14].strip('[]').split(',')

                for f,h,e in zip(fstring, hstring, estring):
                    self.flow.append(int(f))
                    self.head.append(int(h))
                    self.eff.append(float(e))
                print('Pump loaded from database')

    def delete_pump(self, pump_id):
        '''deletes a pump record from the database
            enter pump_id of pump to be deleted '''

        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        params = {'pumpID' : pump_id}
        c.execute('''SELECT * FROM pumps
                     WHERE pumpID=:pumpID''',params)
        if len(c.fetchall()) > 0:
            c.execute('''DELETE FROM pumps
                         WHERE pumpID=:pumpID''',params)
            print('pumpID', pump_id, 'was deleted from the database.')
        else:
            print('No pumps with pumpID', pump_id, 'was found in the database')
        conn.commit()
        conn.close()
        
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
        '''returns a matplotlib plot of the pump curve.
            Default is to plot affinitized curves with full speed curve. 
            User has option to add system curve and efficiency curve
        '''
        if self.impeller:
            title_str = 'Pump: ' + self.model + ' - ' + str(self.rpm) + ' RPM - ' + str(self.impeller) + '" impeller'
        else:
            title_str = 'Pump: ' + self.model + ' - ' + str(self.rpm) + ' RPM'

        self.fig, self.ax = plt.subplots(2,1,figsize=(8,4.95))
        plt.style.use('seaborn-whitegrid')
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
        plt.draw()

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

########################################
if __name__=="__main__":
    print('test script:')

    pump = Pump()
    pump2 = Pump()
    pump.load_pump('Goulds', '3657 1.5x2 -6: 3SS')
    pump2.load_pump('Grundfos', 'CM10-2-A-S-G-V-AQQV')
    
    system_flow = np.linspace(1, 150, 30)
    system_head = []
    for flow in system_flow:
        system_head.append(100 + 20*np.exp(-1/(flow*.005)))

    design_x = 50
    design_y = 60

    pump.plot_curve(system_flow, system_head, vfd=False, eff=True)
    pump2.plot_curve(design_x, design_y, eff=True)
    
    plt.show()
     
    ## example of pump database use

    new_pump_data = {
                    'model' : 'test pump',
                    'mfg' : 'Acme',
                    'flow' : [1,2,3,4,5,6,7,8],
                    'head' : [8,7,6,5,4,3,2,1],
                    'eff' : [.1,.2,.3,.4,.5,.6,.7,.8],
                    'bep' : [5,5],
                    'rpm' : 1800,
                    'impeller' : '5.5'
                    }

    pump.add_pump(**new_pump_data)
    pump.available_pumps()

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''Select pumpID
                 From
                    pumps
                 Where
                    model='test pump'
             ''')
    pump_id = c.fetchall()    
    pump.delete_pump(pump_id=pump_id[0][0])
    pump.available_pumps()

    conn.commit()
    conn.close()