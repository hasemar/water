from Water import *

system_name = 'Test System'
station_name = 'Test Station'
MDD = 500                # gpd/ERU
N = 1000
PHD = tools.PHD(MDD, N)  # gpm

# Define tank data 
tank_data = {          
        'name' : 'Tank 1',
        'diameter' : 30,
        'height' : 45,
        'freeboard' : 1,
        'deadstorage' : 2,
        'elevation' : 150,
        'shape' : 'vertical'
        }

# Instatiate tank object
tank = Tank(**tank1_data)

# from pump to suction header
pump2suc = Pipe(length=5, size=3, kind='STAINLESS STEEL', sch=40)
elbow = Fitting('elbow_90', 'standard_flanged', pump2suc.size, pump2suc.sch)



fitting1 = Fitting('elbow_90', 'standard_threaded', 2)
fitting2 = Fitting('tee_branch', 'standard_threaded', 2)
fitting2.set_Kvalue()

fitting1.getInfo()
fitting2.getInfo(detail=True)

pump = Pump()
pump.load_pump('Goulds 3657')
pump.plot_curve()