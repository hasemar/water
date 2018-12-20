from __future__ import print_function, division
from math import pi, acos, sqrt
from numpy import linspace

c = 7.48052  # gal per cuft conversion

def get_gals(vol):
    gals = c * vol
    return gals

def horizontal_vol(L, R, height=None):
    if height:
        h = float(height) 
        v = L*(R**2 * acos((R-h)/R) - (R-h) * sqrt(2*R*h - h**2))
        return v
    else: # create a height lookup dictionary
        h_arr = linspace(0, 2*R, 1001)
        vol = []
        for h in h_arr:
            vol.append(L*(R**2 * acos((R-h)/R) - (R-h) * sqrt(2*R*h - h**2)))
            
        vol_lookup = dict(zip(vol, h_arr))
        return vol_lookup

class Tank:
    '''
        Tank Object arugments can be passed as a dict:
        example: 

        tank_data = {          
            'name' : 'string',
            'diameter' : int/float,
            'height' : int/float (default 0),
            'length' : int/float (default 0)
            'freeboard' : int/float (default 0),
            'deadstorage' : int/float (default 0),
            'elevation' : int/float (default 0)
            'shape' : 'string' (default vertical)
            }
        tank_1 = Tank(**tank_data)

        or individually like so:

        tank_2 = Tank(name='string', diameter=int/float, height=int/float )
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

        if self.shape == 'horizontal':
            v_dict = horizontal_vol(self.length, self.diameter/2)
            h = v_dict[vol] if vol in v_dict else v_dict[min(v_dict.keys(), key=lambda k: abs(k-vol))]
            return h
        else:
            h = v/self.area
            return h
        
    def getInfo(self, SB=0, ES=0, OS=0, FFS=0, total_vol=0, details=False):
        if self.shape == 'horizontal':
            info = '''
            {3:} \r\n
            Base Elevation:------------- {4:} ft
            Orientation:---------------- {5:}
            Tank Length:---------------- {6:} ft
            Tank Diameter:-------------- {7:} ft
            Tank Cross-Sectional Area:-- {0:.1f} ft^2 
            Total Volume:--------------- {1:.1f} gal
            Effective Volume:----------- {2:.1f} gal
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
            Base Elevation:------------- {4:} ft
            Orientation:---------------- {5:}
            Tank Height:---------------- {6:} ft
            Tank Diameter:-------------- {7:} ft
            Tank cross-sectional area:-- {0:.1f} ft^2
            Total volume:--------------- {1:.1f} gal
            Effective volume:----------- {2:.1f} gal
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
            vols = [vo * perc for vo in [FFS, SB, ES, OS]]
        
            # height referenced from base of tank
            total_h = self.getHeight(sum(vols)) + self.deadstorage + self.freeboard
            ds_vol = get_gals(self.deadstorage*self.area)
            fb_vol = get_gals(self.freeboard*self.area)
            total_calc_vol = ds_vol + fb_vol + sum(vols)
            vols.insert(0,ds_vol)
            vols.append(fb_vol)
            vols.append(total_calc_vol)
            
            info +='''
            Storage Partition    |    Vol (gal)    |    Height(ft)
            ------------------------------------------------------
            Dead Storage              {0:.1f}           {1:.1f}  
            Fire-Flow                 {2:.1f}           {3:.1f}
            Standby                   {4:.1f}           {5:.1f}
            Equalizing                {6:.1f}           {7:.1f}
            Operational               {8:.1f}           {9:.1f}
            Freeboard                 {10:.1f}          {11:.1f}
            ------------------------------------------------------
            TOTALS                    {12:.1f}            {13:.1f} 
            '''.format(
                ds_vol,
                self.deadstorage,
                FFS * perc,
                self.getHeight(FFS*perc),
                SB * perc,
                self.getHeight(SB*perc),
                ES * perc,
                self.getHeight(ES*perc),
                OS * perc,
                self.getHeight(OS*perc),
                fb_vol,
                self.freeboard,
                total_calc_vol,
                total_h
                )

        print(info)

if __name__=='__main__':
    print("Test Script")
    
    horiz_tank_data = {      
        'name' : 'horizontal tank',
        'diameter' : 7.83,
        'length' : 22,
        'freeboard' : 1,
        'deadstorage' : .1,
        'elevation' : 100,
        'shape' : 'horizontal'
        }

    vert_tank_data = {      
        'name' : 'vertical tank',
        'diameter' : 8,
        'height' : 10,
        'freeboard' : 1,
        'deadstorage' : .1,
        'elevation' : 100,
        'shape' : 'vertical'
        }

    h_tank = Tank(**horiz_tank_data)
    v_tank = Tank(**vert_tank_data)

    total = v_tank.vol + h_tank.vol

    h_tank.getInfo()
    v_tank.getInfo()
    h_tank.getInfo(SB=1000, ES=1000, OS=1000, total_vol=total, details=True)
    v_tank.getInfo(SB=1000, ES=1000, OS=1000, total_vol=total, details=True)
