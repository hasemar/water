'''Pipe :

This module holds the data for a variety of fittings and pipe sizes.
It holds a class called Pipe that allows you to create Pipe objects
and calculate losses.

'''

from __future__ import print_function
import Water.tools as tools
from Water import Imperial_properties as WATER
import sqlite3
from os import path

BASE_DIR = path.dirname(path.abspath(__file__))
db_path = path.join(BASE_DIR, "water.db")

# dictionary of C-factor values used in Hazen-Williams equation
c_dict = {
    'PVC' : 150,
    'DI' : 130,
    'STEEL' : 150,
    'HDPE' : 140,
    'STAINLESS STEEL' : 140,
    'PE 4710' : 140,
    'GALVANIZED PIPE' : 120
}
# pipe dimension dictionary {sch:{nominal size:[OD, wall thickness}}  (inches)
pipe_dims = {
    40 : {
        1 : [1.315, 0.133],
        1.25 : [1.66, 0.140],
        1.5 : [1.9, 0.145],
        2 : [2.375, 0.154],
        2.5 : [2.875, 0.203],
        3 : [3.5, 0.216],
        4 : [4.5, 0.237],
        6 : [6.625, 0.28],
        8 : [8.625, 0.322],
        10 : [10.75, 0.365]
    },
    80 : {
        1 : [1.315, 0.179],
        1.25 : [1.66, 0.191],
        1.5 : [1.9, 0.2],
        2 : [2.375, 0.218],
        2.5 : [2.875, 0.276],
        3 : [3.5, 0.3],
        4 : [4.5, 0.337],
        6 : [6.625, 0.432],
        8 : [8.625, 0.5],
        10 : [10.75, 0.5]
    },
    52 : {
        3 : [3.96, 0.28],
        4 : [4.8, 0.29],
        6 : [6.9, 0.31],
        8 : [9.05, 0.33],
        10 : [11.1, 0.35],
        12 : [13.2, 0.37],
        14 : [15.3, 0.39],
        16 : [17.4, 0.40],
        18 : [19.5, 0.41],
        20 : [21.6, 0.41],
        24 : [25.8, 0.44]
    },
    'C900 DR-18' : {
        4 : [4.80, 0.267],
        6 : [6.90, 0.383],
        8 : [9.05, 0.503],
        10 : [11.10, 0.617],
        12 : [13.20, 0.733]
    },
    'DR 7' : {
        0.75 : [1.05, 0.150],
        1 : [1.315, 0.188],
        1.25 : [1.66, 0.237],
        1.5 : [1.90, 0.271],
        2 : [2.375, 0.339],
        3 : [3.5, 0.50],
        4 : [4.5, 0.643],
        5 : [5.375, 0.768],
        6 : [6.625, 0.946],
        7 : [7.125, 1.018],
        8 : [8.625, 1.232],
        10 : [10.75, 1.536],
        12 : [12.75, 1.821],
        14 : [14.0, 2.0],
        16 : [16.0, 2.286]
    },
    'SIDR 7' : {
        0.5 : [0.84, 0.069 ],
        0.75 : [1.05, 0.092],
        1 : [1.315, 0.117],
        1.25 : [1.66, 0.153],
        1.5 : [1.90, 0.179],
        2 : [2.375, 0.23]
    }
}

'''fitting dictionary:

    holds fitting shape and connection type. For each connection 
    type there is a kfactor list [geometry, k1, k_infinity]
'''

fitting_dict = {
    'elbow_90' : {
        'standard_threaded' : [1, 800, 0.4],
        'standard_glued' : [1, 800, 0.3],
        'standard_flanged' : [1, 800, 0.25],
        'long_radius' : [1.5, 800, 0.2],
        'mitered_1' : [1.5, 1000, 1.15,],
        'mitered_2' : [1.5, 800, 0.35],
        'mitered_3' : [1.5, 800, 0.3],
        'mitered_4' : [1.5, 800, 0.27],
        'mitered_5' : [1.5, 800, 0.25]
    },
    'elbow_45' : {
        'stardard_threaded' : [1, 500, 0.2],
        'stardard_glued' : [1, 500, 0.2],
        'standard_flanged' : [1, 500, 0.2],
        'standard' : [1, 500, 0.2],
        'long_radius' : [1.5, 500, 0.15],
        'mitered_1' : [None, 500, 0.25],
        'mitered_2' : [None, 500, 0.15]
    },
    'elbow_180' : {
        'standard_threaded' : [1, 1000, 0.60],
        'standard_glued' : [1, 800, 0.4],
        'standard_flanged' : [1, 1000, 0.35],
        'long_radius' : [1.5, 1000, 0.30]
    },
    'tee_branch' : {
        'standard_threaded' : [None, 500, 0.70],
        'standard_glued' : [1, 800, 0.75],
        'standard_flanged' : [None, 800, 0.80],
        'long_radius' : [None, 800, 0.40],
        'stub_in' : [None, 1000, 1.00]
    },
    'tee_through' : {
        'standard_threaded' : [1, 200, 0.10],
        'standard_glued' : [1, 800, 0.25],
        'standard_flanged' : [1, 150, 0.50],
        'stub_in' : [None, 100, 0]
    },
    'valve' : {
        'gate' : [1, 300, 0.10],
        'ball' : [0.9, 500, 0.15],
        'plug' : [0.9, 1000, 0.25],
        'globe' : [None, 1500, 4.0],
        'angle' : [None, 1000, 2.0],
        'diaphragm' : [None, 1000, 0.25],
        'butterfly' : [None, 800, 0.25],
        'lift_check' : [None, 2000, 10.0],
        'swing_check' : [None, 1500, 1.5],
        'tilt_disc_check' : [None, 1000, 0.50]
    }
}

class Pipe:
    '''Defines Pipe object to add pipe section and fittings for head loss calculations.

    See :doc:`data <data>` for available pipe properties.

    :param length: straight pipe length (ft)
    :param size: nominal pipe diamter (in)
    :param kind: pipe material, default 'PVC'
    :param sch: pipe schedule, default='C900 DR-18'
    :param  Re: Reynolds number, default=2000
    :type length: int
    :type size: float
    :type kind: string
    :type sch: variable depending on pipe material
    :type Re: int
    :return: Pipe object
    :rtype: object

    :Example:

    >>> from Water import Pipe
    >>> pipe = Pipe(length=10, size=4, kind='STEEL', sch=40)
     
    '''

    def __init__(self,length, size, kind='PVC', sch='C900 DR-18', Re=2000):
        self.kind = kind
        self.sch = sch
        self.size = size
        self.dims = pipe_dims[sch][size]
        self.length = length
        self.fitting_list = []
        self.reynolds = Re

    @property
    def outer_diameter(self):
        ''' outer diameter pipe property'''
        return self.dims[0]
    @property
    def inner_diameter(self):
        '''inner diameter pipe property'''
        return self.outer_diameter - 2 * self.dims[1]
    @property
    def volume(self):
        '''pipe volume property'''
        return tools.volume_cyl(self.inner_diameter/12, self.length)
    @property
    def area(self):
        '''pipe cross-sectional area property
           '''
        return self.volume/self.length
    @property
    def c_factor(self):
        ''':pipe material C-factor property'''
        return c_dict[self.kind]

    def search_material(self, material, coefficient=None):
        '''Checks sqlite database for existing material record

           :param material: pipe material
           :param coefficient: Hazen Williams coefficient for major pipe losses
           :type material: string
           :type coefficient: int
           :return: record(s) if one exists 
           :rtype: list
           
           '''
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        existing_params = {'material' : material, 'coefficient' : coefficient}
        
        if coefficient:
            sqlquery='''SELECT *
                        FROM 
                            hazen
                        WHERE material=:material AND coefficient=:coefficient'''
        else:
            sqlquery='''SELECT * 
                        FROM 
                            hazen 
                        WHERE material=:material''' 
        
        c.execute(sqlquery, existing_params)
        result = c.fetchall()        
        conn.commit()
        conn.close()
    
        return result
    
    def add_material(self, material, coefficient):
        '''Adds a record to the hazen williams coefficient table of the sqlite db

            :param material: pipe material
           :param coefficient: Hazen Williams coefficient for major pipe losses
           :type material: string
           :type coefficient: int
        '''

        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        # check if material currently exists in database
        exists = self.search_material(material, coefficient)
        
        if len(exists) == 0:
            sqlinsert = '''INSERT INTO 
                            hazen(
                                material,
                                coefficient) 
                            values(
                                :material,
                                :coefficient)'''

            params = {'material' : material, 'coefficient': coefficient}
            
            print('Material added to hazen table in database')
            c.execute(sqlinsert, params)
            conn.commit()
            conn.close()
        else:
            print('Material exists in the database, check below for specific parameters: ')
            for each_mat in exists:
                print(each_mat)
        
    def fitting(self, fitting_type=None, con_type=None, qty=1, Kvalue=None):
        '''Adds fitting to Pipe object's fitting_list to add to head loss
        
        :param fitting_type: keyword from fitting dictionary, (default None)  
        :param con_type: keyword from fitting dictionary, (default None)  
        :param qty: number of fittings in pipe object, (default 1)
        :param Kvalue: custom loss coefficient, (default None)   
        :type fitting_type: string  
        :type con_type: string  
        :type qty: int   
        :type kValue: float  
        :return: appends fitting onto Pipe object's fitting list

        :Example:

        >>> # using fitting in standard fittings dictionary
        >>> pipe.fitting(fitting_type='elbow_90', con_type='standard_threaded', qty=2)
         
        >>> # creating custom fitting
        >>> pipe.fitting('flow meter', 'flanged', qty=1, Kvalue=1.6)
        
        '''
        if fitting_type in fitting_dict and con_type in fitting_dict[fitting_type]:
            Kfactors = fitting_dict[fitting_type][con_type]
            if not Kvalue:
                Kvalue = Kfactors[1]/self.reynolds+Kfactors[2]*(1+1/self.inner_diameter)

        self.fitting_list.append((fitting_type, con_type, Kvalue,qty))
    
    def fitting_info(self):
        ''':return: list of fittings currently defined in pipe object
           :rtype: string

           :Example:

           >>> print(pipe.fitting_info())
              Fittings list:
              elbow_90, standard_threaded: Kvalue = 0.899, qty = 2  
              flow meter, flanged: Kvalue = 1.600, qty = 1

            '''
        info = 'Fittings list: \n'
        for fitting in self.fitting_list:
            info += '{}, {}: Kvalue = {:.3f}, qty = {} \n'.format(fitting[0],
                                                     fitting[1],
                                                     fitting[2],
                                                     fitting[3]
                                                     )
        return info

    def print_fitting(self):
        ''':return: prints out fitting dictionary for a quick reference'''

        for each_fitting in fitting_dict:
            print(each_fitting)

            for each_type in fitting_dict[each_fitting]:
                print('\t', each_type)

    def major_loss(self, flow):
        '''Uses `Hazen-Williams equation`_ to calculate major head loss for pipe object.  
  
           .. _Hazen-Williams equation: https://en.wikipedia.org/wiki/Hazen%E2%80%93Williams_equation   

           .. math:: h_{major} = \\frac{4.52 Q^{1.852}}{C^{1.852} \\  d^{4.8704}} \\cdot L    

           :param flow: in gallons per minute (gpm)  
           :type flow: int  
           :return: major head loss in ft of head
           :rtype: float

           :Example:

           >>> flow = 300  # gpm
           >>> pipe.major_loss(flow)
               0.4272... 

           '''
        h = (10.45 * self.length * flow**1.852)/(self.c_factor**1.852 * self.inner_diameter**4.8704)
        return h

    def minor_loss(self, flow):
        '''Uses `Minor Loss Equation`_ to calculate minor head loss through fittings in fittings_list.  
        
           .. _Minor Loss Equation: https://en.wikipedia.org/wiki/Minor_losses_in_pipe_flow#Minor_Losses   

           .. math:: h_{minor} = K_L\\cdot \\frac{v^2}{2g}      

           :param flow: flow in gallons per minute (gpm)  
           :type flow: int  
           :return: minor head loss in ft of head
           :rtype: float  
           
           :Example:

           >>> flow = 300  # gpm
           >>> pipe.minor_loss(flow)
               3.0168... 

           '''
        vel = tools.velocity(flow, self.inner_diameter)
        minor_loss = 0
        if len(self.fitting_list) > 0:
            for fitting in self.fitting_list:
                loss = fitting[2]*vel**2/(2*WATER.g) * fitting[3]
                minor_loss += loss
        return minor_loss

    def get_losses(self, flow):
        ''' Calculate the major and minor losses through the Pipe object.
        
        :param flow: in gallons per minute (gpm)
        :type flow: int
        :return: total losses (major + minor)
        :rtype: float
        
        :Example:

        >>> flow = 300  # gpm
        >>> pipe.get_losses(flow)
            3.4441...

           '''
        total_loss = self.major_loss(flow) + self.minor_loss(flow)
        return total_loss
        
#### test script to test functionality
if __name__=="__main__":
    print('test script:\n')
    length = 1000    # pipe length in ft
    size = 6         # nominal pipe diameter in inches
    flow = 300       # flow in gpm
    pipe_1 = Pipe(length, size)

    print('Pipe 1 info:\n',
          'Pipe Length = ',
          pipe_1.length,
          'ft \nHead Loss = ',
          round(pipe_1.major_loss(flow),2),
          'ft \nTotal Loss = ',
          round(pipe_1.get_losses(flow),2),
          'ft'
          ) 

    pipe_2 = Pipe(length, size, kind='STEEL', sch=40)

    pipe_2.fitting('elbow_90', 'standard_threaded', qty=2)
    pipe_2.fitting('tee_branch', 'standard_threaded', qty=3)

    losses = pipe_2.get_losses(flow)
    print('\nPipe 2 info:')
    print(pipe_2.fitting_info())
    print('total head loss: ', round(losses,2), 'ft')

    pipe_1.print_fitting()