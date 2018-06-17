'''
Fittings module:
    This module holds the data for a variety of fittings and pipe sizes.
    It holds a class called Fitting that allows you to create fitting objects
    and calculate K-values for minor losses.
'''
from __future__ import print_function

# fittings and pipe dictionaries
fitting = {
    'elbow_90' : {
        'standard_threaded' : [1, 800, 0.4],
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
        'standard_flanged' : [1, 1000, 0.35],
        'long_radius' : [1.5, 1000, 0.30]
    },
    'tee_branch' : {
        'standard_threaded' : [None, 500, 0.70],
        'standard_flanged' : [None, 800, 0.80],
        'long_radius' : [None, 800, 0.40],
        'stub_in' : [None, 1000, 1.00]
    },
    'tee_through' : {
        'standard_threaded' : [1, 200, 0.10],
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
    'C-900 DR-18' : {
        4 : [4.80, 0.267],
        6 : [6.90, 0.383],
        8 : [9.05, 0.503],
        10 : [11.10, 0.617],
        12 : [13.20, 0.733]
    }
}

# fittings class
class Fitting:
 
    def __init__(self, kind, con_type, size, sch=40):
        self.kind = kind
        self.con_type = con_type
        self.nominal = (size, sch)
        self.Kfactors = fitting[kind][con_type]
        self.size = pipe_dims[sch][size]
        self.Kvalue = 0.0

    @property
    def outer_diameter(self):
        return self.size[0]
    @property
    def inner_diameter(self):
        return self.outer_diameter - 2 * self.size[1]

    def set_Kvalue(self, Re=2000):
       self.Kvalue = self.Kfactors[1]/Re+self.Kfactors[2]*(1+1/self.inner_diameter)

    def getInfo(self, detail=False):
        info = '''
            Fitting: {} {}  Size: {} sch {} OD = {} ID = {}
            '''.format(
               self.con_type,
               self.kind,
               self.nominal[0],
               self.nominal[1],
               self.outer_diameter,
               self.inner_diameter
            )
        if detail:
            info += '''
            Kvalue: {}
            K1: {}
            K_inf: {}
            Geomerty: {} \n\r
            '''.format(
                self.Kvalue,
                self.Kfactors[1],
                self.Kfactors[2],
                self.Kfactors[0]
            )
        print(info)

if __name__=='__main__':
    print("Test Script")
    
    a = Fitting('elbow_90','standard_flanged',size=4, sch=80)
    Re = 10000
    a.set_Kvalue(Re)

    b = Fitting('tee_through','stub_in',size=6,sch='C-900 DR-18')

    a.getInfo()
    a.getInfo(detail=True)
    
    b.getInfo()
    b.getInfo(detail=True)
