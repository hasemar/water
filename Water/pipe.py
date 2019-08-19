'''Pipe :
    This module holds the data for a variety of fittings and pipe sizes.
    It holds a class called Pipe that allows you to create Pipe objects
    and calculate losses.
'''

from __future__ import print_function
import Water.tools as tools

c_dict = {
    'PVC' : 150,
    'DI' : 130,
    'STEEL' : 150,
    'HDPE' : 140,
    'STAINLESS STEEL' : 140,
    'GALVANIZED PIPE' : 120
}

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
        2 : [2.375, 0.271],
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
        'standard' : [1, 500, 0.20],
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
    '''Pipe Class:
        object defined to add pipe section and fittings
        attributes:
            - length: straight pipe length (in ft)
            - size: nominal pipe diameter (in inches)
            - kind: pipe material (PVC, steel, etc.)
            - sch: pipe schedule, default=40, can also put PVC AWWA sizes
            - fitting_list: list of fittings for pipe section
            - reynolds: reynolds number (default to 2000 - laminar)
        properties:
            - inner diameter
            - outer diameter
            - c factor for hazen-williams equation
        methods:
            - major_loss: uses hazen-williams equation to find head loss in straight pipe
            - minor_loss: uses Darcy-Wiesbach equation to find head loss in fittings
            - fitting: appends a fitting to the fitting_list
            - fitting_info: returns string of fitting info in fitting_list
            - print_fittings: prints fittings dictionary for reference
            - get_losses: returns total losses in the pipe section
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
        '''returns outer diameter'''
        return self.dims[0]
    @property
    def inner_diameter(self):
        '''returns inner diamter'''
        return self.outer_diameter - 2 * self.dims[1]
    @property
    def volume(self):
        '''returns volume inside of the pipe in cuft'''
        return tools.volume_cyl(self.inner_diameter/12, self.length)
    @property
    def area(self):
        '''returns pipe area'''
        return self.volume/self.length
    @property
    def c_factor(self):
        '''returns C factor for Hazen-Williams equation'''
        return c_dict[self.kind]
    
    def fitting(self, fitting_type=None, con_type=None, qty=1, Kvalue=None):
        '''adds fitting to Pipe object's fitting_list to add to head loss'''
        if fitting_type in fitting_dict and con_type in fitting_dict[fitting_type]:
            Kfactors = fitting_dict[fitting_type][con_type]
            if not Kvalue:
                Kvalue = Kfactors[1]/self.reynolds+Kfactors[2]*(1+1/self.inner_diameter)

        self.fitting_list.append((fitting_type, con_type, Kvalue,qty))
    
    def fitting_info(self):
        '''returns string list of fittings currently defined in pipe object'''
        info = 'Fittings list: \n'
        for fitting in self.fitting_list:
            info += '{}, {}: Kvalue = {:.3f}, qty = {} \n'.format(fitting[0],
                                                     fitting[1],
                                                     fitting[2],
                                                     fitting[3]
                                                     )
        return info

    def print_fitting(self):
        '''prints out fittings dictionary for reference'''
        for each_fitting in fitting_dict:
            print(each_fitting)
            for each_type in fitting_dict[each_fitting]:
                print('\t', each_type)

    def major_loss(self, flow):
        '''returns major head loss by using Hazen-Williams equation '''
        h = (10.45 * self.length * flow**1.852)/(self.c_factor**1.852 * self.inner_diameter**4.8704)
        return h

    def minor_loss(self, flow):
        '''returns minor head loss by using Darcy Wiesbach equation '''
        g = 32.2
        vel = tools.velocity(flow, self.inner_diameter)
        minor_loss = 0
        if len(self.fitting_list) > 0:
            for fitting in self.fitting_list:
                loss = fitting[2]*vel**2/(2*g) * fitting[3]
                minor_loss += loss
        return minor_loss

    def get_losses(self, flow):
        '''returns total head loss (major + minor)'''
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