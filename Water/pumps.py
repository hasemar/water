'''Pumps Module:

    This module calculates and produces pump curves based on mfg's data points
'''
from __future__ import print_function, division
import matplotlib.pyplot as plt
from numpy import linspace, any, interp, array
import sqlite3
from os import path

BASE_DIR = path.dirname(path.abspath(__file__))
db_path = path.join(BASE_DIR, "water.db")

class Pump:
    '''Defines Pump object to plot and/or affinitized pump curve and performance  
       
       :param target_flow: target flow (gpm), *default None*
       :type target_flow: int
       :param target_head: target head (feet of water) *default None*
       :type target_head: int

       :Example:  

       >>> from Water import Pump
       >>> pump_1 = Pump(target_flow=100, target_head=250)
       
    '''     
    def __init__(self, target_flow=None, target_head=None):
        self.target_flow = target_flow
        self.target_head = target_head
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

    def search_pump(self, pump_model, impeller=None):
        '''Checks sqlite database for existing pump record

           :param pump_model: pump model
           :param impeller: impeller diameter in inches, *default None*
           :type pump_model: string
           :type impeller: float
           :return: pump record if one exists 
           :rtype: list
           
           '''
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
        if exists:
            return exists
        else:
            print("Pump could not be found in database")
            return None

    def add_pump(self, **kwargs):
        '''Add a pump to the sqlite3 database  

           :param \**kwargs: Use dictionary to specify parameters  
           :type \**kwargs: dictionary
           :keyword Arguments: 
                :model: (*string*) - pump model 
                :mfg: (*string*) - pump manufacturer  
                :flow: (*list*) - pump flows in acending order (gpm)  
                :mfg: (*string*) - pump manufacturer  
                :flow: (*list*) - pump flows in acending order (gpm)  
                :head: (*list*) - pump head in respective to flow  (ft)   
                :eff: (*list*) - pump efficiencies respective to flow and head  
                :bep: (*list*) - [flow, head] for best efficiency point    
                :rpm: (*int*) - motor rpm  
                :impeller: (*float*) - impeller diameter (inches)  
            
        :Example: 

        .. code-block::  python  

            kwargs = {
                'model' : 'abc123',
                'mfg' : 'Acme',
                'flow' : [0, 10, 20 ,30, 40, 50, 60, 70],
                'head' : [300, 280, 275, 270, 250, 240, 220, 200],
                'eff' : [0.50, 0.53, 0.58, 0.61, 0.66, 0.70, 0.68, 0.63],
                'bep' : [220, 0.70],
                'rpm' : 1800,
                'impeller' : 5.125
                }

            pump_1.add_pump(**kwargs) 
          
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
        exists = self.search_pump(self.model, self.impeller)
        
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
        '''Loads pump data from sqlite3 database into pump object
            
           :param mfg: pump manufacturer  
           :type mfg: string  
           :param model: pump model   
           :type model: string
           :param impeller: pump impeller size in inches, *default None*  
           :type impeller: float
           
           :Example:

           >>> pump_2 = Pump()
           >>> pump_2.load_pump('Goulds', '3657 1.5x2 -6: 3SS')

           '''
        multiples = self.search_pump(model, impeller)
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
            enter pump_id of pump to be deleted 
            
            :param pump_id: pump id from pump table in database
            :type pump_id: int

            '''

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
        '''affinitized array of pump flows property'''
        return self._affinitize(self.flow, 1)

    @property
    def vfd_head(self):
        '''affinitized array of heads property'''
        return self._affinitize(self.head, 2)

    @property
    def vfd_eff(self):
        '''affinitized array of efficiencies property'''
        return self._affinitize(self.eff, 3)

    def _affinitize(self, pump_data, pwr):
        '''creates affinitized curves for flow, head and efficiency for motor speeds at:  

        Frequency =\n
        - 60 hz
        - 50 hz
        - 40 hz
        - 30 hz
        - 20 hz
        - 10 hz
        '''
        percent_speed = (linspace(60,10,6)/60)**pwr
        
        for percent in percent_speed:
            self.affinity_data.append([data * percent for data in pump_data])
        return self.affinity_data

    def plot_curve(self, 
                   target_flow=None, 
                   tdh=None, 
                   vfd=True, 
                   eff=False, 
                   num_pumps=1, 
                   show=False, 
                   **kwargs):
        '''creates a matplotlib plot of the pump curve.
            Default is to plot affinitized curves with full speed curve. 
            User has option to add parallel pumps, system curve and efficiency curve.
            Parallel pump curves only work when vfd=False.

        :param target_flow: flow point to plot (gpm), *default None*  
        :type target_flow: int/float
        :param tdh: Total Dynamic Head (ft), *default None*  
        :type tdh: int/float  
        :param vfd: turn on/off affinitized pump curves, *default True*    
        :type vfd: boolean
        :param eff: turn on/off pump efficiency curve, *default False*
        :type eff: boolean
        :param num_pumps: number of pumps in parallel *default 1*  
        :type num_pumps: int  
        :param show: show plot (keep false if using in an .ipynb file), *default False*
        :type show: boolean
        :param \**kwargs: matplotlib.pyplot.plot keyword arguments
        :return: pump curve for pump object
        :rtype: matplotlib.pyplot plot 

        :Example: 

        Plotting a pump curve with one design point with efficiency curve

        .. code-block:: python
            
            # design parameters
            FLOW = 100    # gpm
            TDH = 111            # ft head

            # define pump object and load pump data
            pump_1 = Pump()
            pump_1.load_pump('Goulds', '3657 1.5x2 -6: 3SS')

            # plot curve without affinitized curves and with efficiency curve
            pump_1.plot_curve(target_flow=FLOW, tdh=TDH, vfd=False, eff=True, show=True)

        .. image:: pump_ex1.png

        See :doc:`Pump Class Example <tutorial>` for affinitize curve functionality and how to 
        plot a system curve along with the pump curve. 
        
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
                self.ax[0].plot(self.flow, h, label=l, **kwargs)
        else:
            for n in range(1,num_pumps+1):
                self.ax[0].plot(array(self.flow)*n, self.head, label='pump # ' + str(n), **kwargs)

        if any(target_flow) and any(tdh):
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
        if show:
            plt.show()

    def find_head(self, flow):
        ''' Returns head value from pump curve based on flow input.
            If flow is not a known value it will interprolate between the
            two closest points on the curve.

        :param flow: pump flow (gpm)
        :type flow: int/float  
        :return: head value from curve data
        :rtype: float
        
        :Example:  
        
        >>> Q = 125
        >>> h = pump_1.find_head(Q)
        >>> print(h, 'ft')
            100.125 ft
            
        '''
        try:
            if flow in self.flow:
                head = self.head[self.flow.index(flow)]
            else:
                head = interp(flow, self.flow, self.head)
        except ValueError:
            print("Value not found, check you numbers")

        return head

########################################
if __name__=="__main__":
    from numpy import exp

    print('test script:')

    pump = Pump()
    pump2 = Pump()
    pump.load_pump('Goulds', '3657 1.5x2 -6: 3SS')
    pump2.load_pump('Grundfos', 'CM10-2-A-S-G-V-AQQV')
    
    system_flow = linspace(1, 150, 30)
    system_head = []
    for flow in system_flow:
        system_head.append(100 + 20*exp(-1/(flow*.005)))

    design_x = 50
    design_y = 60

    pump.plot_curve(system_flow, system_head, vfd=False, eff=True, num_pumps=2)
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