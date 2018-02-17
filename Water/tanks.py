from math import pi, acos, sqrt
import numpy as np

c = 7.48052  # gal per cuft conversion

def get_gals(vol):
    gals = c * vol
    return gals

def horizontal_vol(L, R):
    h_arr = np.linspace(0, 2*R, 100)
    vol = []
    
    for h in h_arr:
        vol = L*(R**2 * acos((R-h)/R) - (R-h) * sqrt(2*R*h - h^2))
        
    vol_lookup = dict(zip(h_arr, vol))
    
    return vol_lookup

class Tank:
    '''
    Tank(**kwargs)
        Tank Object arugments can be passed as a dict
        tank_data = {          
            'name' : 'string',
            'diameter' : int/float,
            'height' : int/float,
            'freeboard' : int/float (default 0),
            'deadstorage' : int/float (default 0),
            'elevation' : int/float (default 0)
            'shape' : 'string' (default vertical)
            }
        or
        Tank(name='string',diameter=int/float, height=int/float )
    '''
    
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.diameter = kwargs.get('diameter')
        self.height = kwargs.get('height')
        self.freeboard = kwargs.get('freeboard', 0)
        self.deadstorage = kwargs.get('deadstorage', 0)
        self.elevation = kwargs.get('elevation', 0)
        self.shape = kwargs.get('shape', 'vertical')
        self.length = 0

    @property
    def area(self):
        r = self.diameter / 2
        return pi * r*r
        
    @property
    def gal_per_ft(self):
        return self.area * c
    
    @property
    def vol(self):
        if self.shape == 'horizontal':
            
            v_dict = horizontal_vol(self.length, self.diameter/2)
            return v_dict[max(v_dict)]

        else:
            return self.gal_per_ft * self.height
        
    @property
    def useable(self):
        r = self.diameter/2
        
        if self.shape == 'horizontal':

            return 
        else:
            return (self.height - self.deadstorage - self.freeboard) * self.gal_per_ft
   
    def getPercent(self, vol, of_vol):
         return vol/of_vol

    def getHeight(self, vol):
        r = self.diameter/2
        if self.shape == 'horizontal':
            a_dead = r**2*(pi - acos((r-self.deadstorage)/r)) + 2*(r**2 - self.deadstorage * r)*(r - self.deadstorage)* sqrt(1 - ((r - self.deadstorage)/r)**2)/(r-self.deadstorage)
            v_dead = a_dead *self.length
            ft = np.arange(self.deadstorage, self.diameter, 0.01)
            v_arr = []
            for increment in ft:
                if increment < self.diameter/2:
                    v_arr.append((r**2*(pi - acos((r-increment)/r)) - 2*(r**2 - increment * r)*(r - increment)* sqrt(1 - ((r - increment)/r)**2)/(r-increment))*self.length)
                else:
                    v_arr.append((r**2*(pi - acos((r-increment)/r)) + 2*(r**2 - increment * r)*(r - increment)* sqrt(1 - ((r - increment)/r)**2)/(r-increment))*self.length)

            h = find_nearest(v_arr, vol)
                
        else:
            h = vol/self.gal_per_ft
            return h
        
    def getInfo(self, SB=0, ES=0, OS=0, total_vol=0, details=False):
        info = '''
           {3:} \r\n
           Base Elevation: {4:} ft \r\n
           Orientation: {5:} \r\n
           Tank Height: {6:} ft \r\n
           Tank Diameter: {7:} ft \r\n
           Tank cross-sectional area: {0:.1f} ft^2 \r\n
           Total volume: {1:.1f} gal \r\n
           Effective volume: {2:.1f} gal \r\n
           '''.format(
                      self.area,
                      self.vol,
                      self.useable,
                      self.name,
                      self.elevation,
                      self.shape,
                      self.height,
                      self.diameter
                     )
        if details:
            perc = self.getPercent(self.useable, total_vol)
            info +='''
            Standby volume: {0:.1f} gal --> Equivalent height: {1:.1f} ft from base \n\r
            Equalizing volume: {2:.1f} gal --> Equivalent height: {3:.1f} ft from base \n\r
            Operational volume: {4:.1f} gal --> Equivalent height: {5:.1f} ft from base \n\r
            From the bottom of Equalizing Storage, the height is: {6:.1f} ft from base \n\r
            Operational Storage operates in a {7:.2f} ft range \n\r
            '''.format(
                       SB * perc,
                       self.getHeight(SB * perc) + self.deadstorage,
                       ES * perc,
                       self.getHeight(ES * perc) + self.getHeight(SB * perc) + self.deadstorage,
                       OS * perc,
                       self.getHeight(OS * perc) + self.getHeight(ES * perc) + self.getHeight(SB * perc) + self.deadstorage,
                       self.getHeight(SB * perc) + self.deadstorage,
                       self.getHeight(OS*perc)
                      )
            
        print info


if __name__=='__main__':
    print "Test Script"
    
    tank_data = {          
        'name' : 'test',
        'diameter' : 10,
        'height' : 20,
        'freeboard' : 1,
        'deadstorage' : 1,
        'elevation' : 100,
        'shape' : 'horizontal'
        }

    tank = Tank(**tank_data)
    tank.length = 20
    total = 2*tank.vol
    
    tank.getInfo(SB=100, ES=100, OS=100, total_vol=total, details=True)

    


