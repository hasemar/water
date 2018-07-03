'''
Pipe Class
   
'''
from __future__ import print_function

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

    def __init__(self, length, size, kind='PVC', sch='C900 DR-18'):
        self.kind = kind
        self.sch = sch
        self.size = pipe_dims[sch][size]
        self.length = length
        self.c_factor = c_dict[kind]

    @property
    def outer_diameter(self):
        return self.size[0]
    @property
    def inner_diameter(self):
        return self.outer_diameter - 2 * self.size[1]


if __name__=="__main__":
    print('test script:')

    pipe_1 = Pipe(100, 6)

    print(pipe_1.length) 

    '''
    Notes:  Make this class a super class for fittings to inherent pipe size and type
    This class will also be a subclass of losses class
    '''