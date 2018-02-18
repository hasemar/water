from math import pi, acos, sqrt
from numpy import linspace

c = 7.48052  # gal per cuft conversion

def get_gals(vol):
    gals = c * vol
    return gals

def horizontal_vol(L, R, height=None):
    if height:
        h = height 
        v = L*(R**2 * acos((R-h)/R) - (R-h) * sqrt(2*R*h - h**2))
        return v
    else: # create a height lookup dictionary
        h_arr = linspace(0, 2*R, 11)
        vol = []
        for h in h_arr:
            vol.append(L*(R**2 * acos((R-h)/R) - (R-h) * sqrt(2*R*h - h**2)))
            
        vol_lookup = dict(zip(vol, h_arr))
        print vol
        print h_arr
        return vol_lookup

class Tank:
    '''
        Tank Object arugments can be passed as a dict:
        example: 

        tank_data = {          
            'name' : 'string',
            'diameter' : int/float,
            'height' : int/float (default 0),
            'length' = int/float (default 0)
            'freeboard' : int/float (default 0),
            'deadstorage' : int/float (default 0),
            'elevation' : int/float (default 0)
            'shape' : 'string' (default vertical)
            }
        Tank(**kwargs)

        or individually like so:

        Tank(name='string', diameter=int/float, height=int/float )
    '''
    
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.diameter = kwargs.get('diameter')
        self.height = kwargs.get('height', 0)
        self.freeboard = kwargs.get('freeboard', 0)
        self.deadstorage = kwargs.get('deadstorage', 0)
        self.elevation = kwargs.get('elevation', 0)
        self.shape = kwargs.get('shape', 'vertical')
        self.length = kwargs.get('length', 0)

    @property
    def area(self):
        r = self.diameter / 2
        return pi * r*r
    
    @property
    def vol(self):
        if self.shape == 'horizontal':
            return get_gals(horizontal_vol(self.length, self.diameter/2, self.diameter))
        else:
            return get_gals(self.area * self.height)
        
    @property
    def useable(self):
        if self.shape == 'horizontal':
            r = self.diameter/2
            v_dead = get_gals(horizontal_vol(self.length, r, self.deadstorage))
            v_free = get_gals(horizontal_vol(self.length, r, self.freeboard))
            return self.vol - v_dead - v_free
        else:
            return get_gals((self.height - self.deadstorage - self.freeboard) * self.area)
   
    def getPercent(self, vol, of_vol):
         return vol/of_vol

    def getHeight(self, vol):
        v = vol/c  # change back to cu.ft
        print 'getHeight volume = ' + str(v) + 'ft^3'
        if self.shape == 'horizontal':
            v_dict = horizontal_vol(self.length, self.diameter/2)
            h = v_dict[vol] if vol in v_dict else v_dict[min(v_dict.keys(), key=lambda k: abs(k-vol))]
            return h
        else:
            h = vol/self.area
            return h
        
    def getInfo(self, SB=0, ES=0, OS=0, total_vol=0, details=False):
        if self.shape == 'horizontal':
            info = '''
            {3:} \r\n
            Base Elevation: {4:} ft \r\n
            Orientation: {5:} \r\n
            Tank Length: {6:} ft \r\n
            Tank Diameter: {7:} ft \r\n
            Tank Cross-Sectional Area: {0:.1f} ft^2 \r\n
            Total Volume: {1:.1f} gal \r\n
            Effective Volume: {2:.1f} gal \r\n
            '''.format(
                        self.area,
                        self.vol,
                        self.useable,
                        self.name,
                        self.elevation,
                        self.shape,
                        self.length,
                        self.diameter
                        )
        else:
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
    
    horiz_tank_data = {      
        'name' : 'horizontal tank',
        'diameter' : 20,
        'length' : 20,
        'freeboard' : 1,
        'deadstorage' : 2,
        'elevation' : 157,
        'shape' : 'horizontal'
        }

    vert_tank_data = {      
        'name' : 'vertical tank',
        'diameter' : 20,
        'height' : 22,
        'freeboard' : 1,
        'deadstorage' : 2,
        'elevation' : 157,
        'shape' : 'vertical'
        }

    h_tank = Tank(**horiz_tank_data)
    v_tank = Tank(**vert_tank_data)

    total = v_tank.vol + h_tank.vol

    dead_vol = horizontal_vol(h_tank.length, h_tank.diameter/2, h_tank.deadstorage)
    num_vol = horizontal_vol(20, 10, 2)
    vols = horizontal_vol(h_tank.length, h_tank.diameter/2)
    print vols
    print h_tank.deadstorage
    print h_tank.length
    print h_tank.diameter/2
    print dead_vol
    print num_vol
    #tank.getInfo()
   # tank.getInfo(SB=100, ES=100, OS=100, total_vol=total, details=True)
