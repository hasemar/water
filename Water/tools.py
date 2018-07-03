'''
Tools to calculate water system
design aspects
'''

from __future__ import print_function, division
import numpy as np
from math import pi

def coeffs(num_ERUs):
    '''
    assigns C and F coefficients
    '''
    if num_ERUs < 51:
        return 3.0, 0
    elif num_ERUs > 50 and num_ERUs < 101:
        return 2.5, 25
    elif num_ERUs > 100 and num_ERUs < 251:
        return 2.0, 75
    elif num_ERUs > 250 and num_ERUs < 501:
        return 1.8, 125
    elif num_ERUs > 500:
        return 1.6, 225
    else:
        print("Number of ERU's must be a real number")

def PHD(MDD, num_ERUs):
    '''
    Peak Hour Demand:
    Enter Max Day Demand and Number of ERU's
    Also Retuns Average Hour and Lowest Hour Demand
    '''

    C, F = coeffs(num_ERUs)
    phd = (MDD/1440)*(C*num_ERUs + F) + 18
    ahd = phd/1.74
    lhd = ahd * 0.22

    return (phd, ahd, lhd)

def calc_hp(flow_rate, head, pump_eff=0.6, motor_eff=0.9):
    '''
    Horsepower Calculations:
    Enter flow and head in gpm and feet H20, and efficiencies
    Power units in horsepower
    '''
    water_hp = (flow_rate*head)/3960
    break_hp = water_hp/pump_eff
    input_hp = break_hp/motor_eff

    return (water_hp, break_hp, input_hp)

def velocity(flow, pipe_diam):
    '''
    Velocity Calculations:
    Enter flow in gpm and pipe_diameter in inches
    Units in feet per sec
    '''
    V = 0.4085*flow/(pipe_diam**2)

    return V

def flow(velocity, pipe_diam):
    '''
    Flow Calculation:
    Enter velocity in fps and pipe_diam in inches
    units in gpm
    '''
    Q = velocity * pipe_diam**2/0.4085

    return Q

def pipeDiameter(flow, velocity):
    '''
    pipe diameter Calculation:
    Enter velocity in fps and flow in gpm
    units in inches
    '''
    pipe_diam = (flow*0.4085/velocity)**0.5

    return pipe_diam

def reynolds(velocity, pipe_diam, nu=14.1e-6):
    '''
    Reynolds Number Calculation:
    Enter velocity(fps), pipe diameter(inches)
        nu = 14.1e-6 (default)
    '''
    d = pipe_diam/12
    re = velocity*d / nu

    if re >= 2300:
        laminar = False
    else:
        laminar = True

    return re, laminar

def volume_cyl(d, h):
    ''' volume of a cylinder using diameter'''
    return (pi*d**2 / 4)*h

def volume_box(length, width, height):
    ''' volume of a box '''
    return length*width*height

def ft2gal(cubic_feet):
    ''' cubic feet to gallon conversion'''
    return cubic_feet*7.481


########## Test Script ############
if __name__=="__main__":

    print('test script:')

    # Peak Hour Demand Calcs
    phd, ahd, lhd = PHD(100, 75)
    phd2,_,_ = PHD(50, 200)

    # Horse Power Calcs
    water_p, break_p, input_p = calc_hp(100, 120, 0.65, 0.95)
    water2_p, _, _ = calc_hp(230,50)

    # Flow and Velocity Calcs
    Q = 150 # gpm
    d = 3  # inches

    v = velocity(Q, d)
    q_func = flow(v, d)
    d_func = pipeDiameter(Q,v)

    # Reynolds Number
    Re, Lam = reynolds(v, d)
    if Lam:
        condition = 'Laminar'
    else:
        condition = 'Turbulent'

    # Volume Calculations
    vol1 = volume_cyl(5, 10)
    vol2 = volume_box(5, 10, 20)

    # cubic feet to gallon conversion
    gals = ft2gal(1000)
    
    # output string
    out = '''
        PHD = {0:.2f} gmp
        AHD = {15:.2f} gmp
        LHD = {16:.2F} gmp
        PHD2_raw = {1:f}
        hp_w1 = {2:.2f} hp
        hp_b1 = {3:.2f} hp
        hp_i1 = {4:.2f} hp
        hp_raw = {5:f}
        flow input = {6:.1f} gpm
        pipe diameter input = {7:.1f} in
        calculated velocity = {8:.2f} fps
        calculated flow = {9:.2f} gpm \r
        calculated diameter = {10:.2f} in
        Reynolds Number = {11:.2f}
        Flow Condition = {12:s}
        vol1 = {13:f}
        vol2 = {14:.2f}
        gallons = {17:.2f}
        '''.format(
            phd, phd2, water_p, break_p, input_p,
            water2_p, Q, d, v, q_func, d_func, Re,
            condition, vol1, vol2, ahd, lhd, gals)

    print(out)

