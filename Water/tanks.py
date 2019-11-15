from __future__ import print_function, division
from math import pi, acos, sqrt
from Water import tools

class Tank:
    '''Defines Tank object to calculate storage and other tank properties.\n
    Tank object arugments can be passed as a dict:\n
        *example:*\n 
        
        tank_data = {          
            'name' : 'string',
            'diameter' : int/float,
            'height' : int/float (default 0),
            'length' : int/float (default 0),
            'width' : int/float (default 0)
            'freeboard' : int/float (default 0),
            'deadstorage' : int/float (default 0),
            'elevation' : int/float (default 0)
            'shape' : 'string' (default vertical),
            'operational' : int/float (default 0),
            'equalizing' : int/float (default 0),
            'standby' : int/float (default 0),
            'fire' : int/float (default 0)
            }

        tank_1 = Tank(\**tank_data)

        *or individually like so:*

        tank_2 = Tank(name='string', diameter=int/float, height=int/float )
    
    '''
    
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.diameter = kwargs.get('diameter')              # ft
        self.height = kwargs.get('height', 0)               # ft
        self.freeboard = kwargs.get('freeboard', 0)         # ft
        self.deadstorage = kwargs.get('deadstorage', 0)     # ft
        self.elevation = kwargs.get('elevation', 0)         # ft
        self.shape = kwargs.get('shape', 'vertical')        # 'vertical' 'horizontal' 'box'
        self.length = kwargs.get('length', 0)               # ft
        self.width = kwargs.get('width', 0)                 # ft
        self.operational = kwargs.get('operational' 0)      # ft
        self.equalizing = kwargs.get('equalizing', 0)       # ft
        self.standby = kwargs.get('standby', 0)             # ft 
        self.fire = kwargs.get('fireflow', 0)           # ft

    @property
    def area(self):
        '''returns cross-sectional area of tank'''
        if self.shape == 'vertical' or self.shape == 'horizontal':
            a = pi * self.diameter**2 / 4
        elif self.shape == 'box':
            a = self.width * self.length
        else:
            print('tank shape must be vertical, horizontal or box')
            a = None
        return a
    @property
    def vol(self):
        '''returns dry volume of tank'''
        if self.shape == 'horizontal':
            return tools.cuft2gal(self.horizontal_vol(self.diameter))
        else:
            return tools.cuft2gal(self.area * self.height)   
    @property
    def useable(self):
        '''returns useable volume of tank'''
        if self.shape == 'horizontal':
            v_dead = tools.cuft2gal(self.horizontal_vol(self.deadstorage))
            v_free = tools.cuft2gal(self.horizontal_vol(self.freeboard))
            return self.vol - v_dead - v_free
        else:
            return tools.cuft2gal((self.height - self.deadstorage - self.freeboard) * self.area)
   
    def horizontal_vol(self, height):
        '''returns filled volume of horizontal tank at height'''
        L = self.length
        R = self.diameter/2
        h = height 
        v = L*(R**2 * acos((R-h)/R) - (R-h) * sqrt(2*R*h - h**2))
        
        return v

    def horizontal_vol_dict(self):
        '''returns a dict of volumes at heights ranging from 0 to self.diameter'''
        L = self.length
        R = self.diameter/2
        l = self.diameter/1001
        h_arr = [l* x for x in range(1001)]  # create an array much like np.linspace
        vol = []
        for h in h_arr:
            vol.append(L*(R**2 * acos((R-h)/R) - (R-h) * sqrt(2*R*h - h**2)))    
        vol_lookup = dict(zip(vol, h_arr))
        
        return vol_lookup
    
    def getPercent(self, vol, of_vol):
        '''percentage volume of total system volume'''
        return vol/of_vol

    def getHeight(self, vol):
        '''returns water level in ft at given volume'''
        v = tools.gal2cuft(vol) # change back to cu.ft

        if self.shape == 'horizontal':
            v_dict = self.horizontal_vol_dict()
            h = v_dict[vol] if vol in v_dict else v_dict[min(v_dict.keys(), key=lambda k: abs(k-vol))]
            return h
        else:
            h = v/self.area
            return h
        
    def getInfo(self, SB=0, ES=0, OS=0, FFS=0, total_vol=0, details=False):
        '''returns string of tank properties'''
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
        elif self.shape == 'box':
            info = '''
            {3:} \r\n
            Base Elevation:------------- {4:} ft
            Orientation:---------------- {5:}
            Tank Length:---------------- {6:} ft
            Tank Width:----------------- {7:} ft
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
                    self.width
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
            ds_vol = tools.cuft2gal(self.deadstorage*self.area)
            fb_vol = tools.cuft2gal(self.freeboard*self.area)
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

        return info

if __name__=='__main__':
    print("Test Script")
    
    horiz_tank_data = {      
        'name' : 'horizontal tank',
        'diameter' : 8,
        'length' : 22,
        'freeboard' : 1,
        'deadstorage' : .1,
        'elevation' : 100,
        'shape' : 'horizontal'
        }

    vert_tank_data = {      
        'name' : 'vertical tank',
        'diameter' : 8,
        'height' : 22,
        'freeboard' : 1,
        'deadstorage' : .1,
        'elevation' : 100,
        'shape' : 'vertical'
        }

    h_tank = Tank(**horiz_tank_data)
    v_tank = Tank(**vert_tank_data)

    total = v_tank.vol + h_tank.vol

    rep1 = h_tank.getInfo()
    print(rep1)

    rep2 = v_tank.getInfo()
    print(rep2)

    rep3 = h_tank.getInfo(SB=1000, ES=1000, OS=1000, total_vol=total, details=True)
    rep4 = v_tank.getInfo(SB=1000, ES=1000, OS=1000, total_vol=total, details=True)
    print(rep3)
    print(rep4)
