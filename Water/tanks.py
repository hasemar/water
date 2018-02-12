from math import pi
c = 7.48052
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

    # def __init__(self, name, diameter, height, freeboard=0, deadeadstorage=0, elevation=0):
    #     self.name = name
    #     self.diameter = diameter
    #     self.height = height
    #     self.freeboard =freeboard
    #     self.deadstorage = deadstorage
    #     self.elevation = elevation

    @property
    def area(self):
        return pi * self.diameter * self.diameter / 4
    @property
    def gal_per_ft(self):
        return self.area * c 
    @property
    def vol(self):
        return self.gal_per_ft * self.height
    @property
    def useable(self):
        return (self.height - self.deadstorage - self.freeboard) * self.gal_per_ft
   
    def getPercent(self, vol, of_vol):
         return vol/of_vol

    def getHeight(self, vol):
        return vol/self.gal_per_ft

    def getInfo(self):
        info = '''
               {4:} \r\n
               This tank has an area of {0:.1f} ft^2 \r\n
               Its volume is {1:.1f} ft^3 \r\n
               Its useable vol is {2:.1f} ft^3 \r\n
               The useable volume is {3:.3f} times the total volume.
               '''.format(
                          self.area,
                          self.vol,
                          self.useable,
                          self.getPercent(self.useable, self.vol),
                          self.name
                         )
        print info