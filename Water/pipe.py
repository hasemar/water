'''
Pipe :
    This module holds the data for a variety of fittings and pipe sizes.
    It holds a class called Pipe that allows you to create Pipe objects
    and calculate losses.
'''

from __future__ import print_function
import Water.tools as tools
c_dict = {
    'PVC' : 140,
    'DI' : 130,
    'STEEL' : 150,
    'HDPE' : 140,
    'STAINLESS STEEL' : 140
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
    }
}

class Pipe:
    '''Pipe Class:
        object defined to add pipe section
        attributes:
            - length: straight pipe length (in ft)
            - size: nominal pipe diameter (in inches)
            - kind: pipe material (PVC, steel, etc.)
            - sch: pipe schedule, default=40, can also put PVC AWWA sizes
        properties:
            - inner diameter
            - outer diameter
            - c factor for hazen-williams equation
        methods:
            - major_loss: uses hazen-williams equation to find head loss in straight pipe
            - minor_loss: uses Darcy-Wiesbach equation to find head loss in fittings
            - get_losses: returns total losses in the pipe section
    '''
    def __init__(self,length, size, kind='PVC', sch='C900 DR-18'):
        self.kind = kind
        self.sch = sch
        self.size = size
        self.dims = pipe_dims[sch][size]
        self.length = length

    @property
    def outer_diameter(self):
        ''' returns outer diameter'''
        return self.dims[0]
    @property
    def inner_diameter(self):
        ''' returns inner diamter'''
        return self.outer_diameter - 2 * self.dims[1]
    @property
    def c_factor(self):
        ''' returns C factor for Hazen-Williams equation'''
        return c_dict[self.kind]

    def major_loss(self, flow):
        ''' returns major head loss by using Hazen-Williams equation '''
        h = (10.67 * self.length * flow**1.852)/(self.c_factor**1.852 * self.inner_diameter**4.8704)
        return h

    def minor_loss(self, flow, fittings):
        ''' returns minor head loss by using Darcy Wiesbach equation '''
        g = 32.2
        vel = tools.velocity(flow, self.inner_diameter)
        # fittings is a list of tuples, first tuple is fitting object, 2nd tuple is quanity
        minor_loss = 0
        for fitting in fittings:
            fitting[0].set_Kvalue()
            loss = fitting[0].Kvalue*vel**2/(2*g) * fitting[1]
            minor_loss += loss
        return minor_loss

    def get_losses(self, flow, fittings):
        ''' returns total head loss (major + minor)'''
        total_loss = self.major_loss(flow) + self.minor_loss(flow, fittings)
        return total_loss
        
#### test script to test functionality
if __name__=="__main__":
    print('test script:')
    length = 1000
    size = 6
    flow = 300
    nom_size = 8
    pipe_1 = Pipe(length, size)

    print('Pipe Length = ',
          pipe_1.length,
          'ft \nHead Loss = ',
          pipe_1.major_loss(flow),
          'ft') 
