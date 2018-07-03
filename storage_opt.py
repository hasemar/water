'''
fiddling around with optimizing storage and ERU's
'''
 from __future__ import print_function, division
 import numpy as np 
 from Water import *

 #### System Info #####
 system_name = 'My Water System'
 Q_fire = 1500    # gpm
 t_fire = 120     # minutes

 Qs = 150         # gpm
 daily_prod = 150 * 1440 * 0.60   # gpd
