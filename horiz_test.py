from math import sqrt, acos
from numpy import linspace

def horizontal_vol(L, R, height=None):
    if height: # use height in calculation

        h = height 
        v = L*(R**2 * acos((R-h)/R) - (R-h) * sqrt(2*R*h - h**2))
        return v
    else: # create a height lookup dictionary

        h_arr = linspace(0, 2*R, 11)
        vol = []

        for h in h_arr:
            vol.append(L*(R**2 * acos((R-h)/R) - (R-h) * sqrt(2*R*h - h**2)))
            
        vol_lookup = dict(zip(vol, h_arr))
        return vol_lookup

L = 20
R = 10
H = 2
vol_dic = horizontal_vol(L,R)
vol = horizontal_vol(L, R, H)

print vol_dic

print vol

print 'what the fuck dude'