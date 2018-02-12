from Water import *

# Tank1 info
tank1_data = {          
        'name' : 'Tank 1',
        'diameter' : 10,
        'height' : 40,
        'freeboard' : 5,
        'deadstorage' : 1,
        'elevation' : 150
        }

tank = Tank(**tank1_data)
tank1 = Tank(name='sunny', diameter=100, height=400)
tank2 = Tank(name='shady', diameter=10, height=4000, deadstorage= 499)

tank.getInfo()
tank1.getInfo()
tank2.getInfo()


fitting1 = Fitting('elbow_90', 'standard_threaded', 2)
fitting2 = Fitting('tee_branch', 'standard_threaded', 2)
fitting2.set_Kvalue()

fitting1.getInfo()
fitting2.getInfo(detail=True)

pump = Pump()
pump.load_pump('Goulds 3657')
pump.plot_curve()