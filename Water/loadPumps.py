import csv
from os import path
from Water import Pump

pumps_dir = path.join(path.dirname(__file__), 'pumps')


def load_pump(selection):
    '''loads pump data from /pump folder included in package directory. Pump data
    is in .csv format.
    '''
    f = []
    h = []
    ef = []
    available_pumps = {
    'Goulds 3657' : '3657_1-5X2_GOULDS_3500.csv',
    'Goulds 3642' : '3642_1x1-25_GOULDS_3500.csv',
    'Grunfos CM1' : 'CM1-2-A-GRUNFOS.csv',
    'Goulds 25GS50' : '25GS50-GOULDS_3500.csv',
    'Goulds 35GS50' : '35GS50-GOULDS_3500.csv',
    'Goulds 75GS100CB' : '75GS100CB-GOULDS_3500.csv',
    'Goulds 85GS100' : '85GS100-GOULDS_3500.csv',
    'Grundfos CMBE 5-62' : 'CMBE_5-62-GRUNFOS.csv',
    'Goulds 85GS75' : '85GS75-GOULDS_3500.csv',
    'Grundfos 85S100-9': '85S100-9-GRUNDFOS_3500.csv'
    }
    model = None
    rpm = None
    impeller = None
    bep = [None, None]
    mfg = None
    
    file_path = pumps_dir + '/' + available_pumps[selection]
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        
        for line in csv_reader:
            if line[0]:
                model = line[0]
                rpm = int(line[1])
                impeller = line[2]
                bep[0] = line[6]
                bep[1] = line[7]
                mfg = line[8]
            f.append(int(line[3]))
            h.append(int(line[4]))
            ef.append(float(line[5]))
        flow = f
        head = h
        eff = ef

for each_pump in available_pumps.keys():
    pump = Pump()
    pump.load_pump(each_pump)
    pump_data = {'model' : pump.model,
                 'mfg' : pump.mfg,
                 'flow' : pump.flow,
                 'head' : pump.head,
                 'eff' : pump.eff,
                 'bep' : pump.bep,
                 'rpm' : pump.rpm,
                 'impeller' : pump.impeller
                 }
    pump.add_pump(**pump_data)

pump.avaiablePumps()
