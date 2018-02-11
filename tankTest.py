from Tank import Tank

dims = {      #[tank1, tank2, tank3]
        'name' : ['Tank 1', 'Tank 2', 'Tank 3'],
        'diameter' : [10, 20, 30],
        'height' : [40, 50, 60],
        'freeboard' : [5, 2, 1],
        'deadstorage' : [1,2,3],
        'elevation' : [150,150,150]
        }

tanks = []
for n,d, h, fb, ds, el in zip(
                        dims['name'],
                        dims['diameter'],
                        dims['height'],
                        dims['freeboard'],
                        dims['deadstorage'],
                        dims['elevation']
                        ):
    tanks.append(Tank(n,d,h,fb,ds,el))

tanks[0].getInfo()
