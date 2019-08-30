'''
Tools to calculate water system
design aspects
'''

from __future__ import print_function, division
from math import pi, acos, sqrt, ceil

def coeffs(num_ERUs):
    '''assigns C and F coefficients from DOH manual'''
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
    '''Peak Hour Demand:
        Enter Max Day Demand and Number of ERU's
        Also Returns Average Hour and Lowest Hour Demand
    '''

    C, F = coeffs(num_ERUs)
    phd = (MDD/1440)*(C*num_ERUs + F) + 18
    ahd = phd/1.74
    lhd = ahd * 0.22

    return (phd, ahd, lhd)

def equalizing_storage(PHD, Qs):
    '''Equalizing Storage Calc from DOH design manual'''
    return (PHD-Qs)*150

def calc_hp(flow_rate, head, pump_eff=0.6, motor_eff=0.9):
    '''Horsepower Calculations:
        Returns Water HP, Break HP and Total HP
        Enter flow and head in gpm and feet H20, and efficiencies
        Power units in horsepower
    '''
    water_hp = (flow_rate*head)/3960
    break_hp = water_hp/pump_eff
    input_hp = break_hp/motor_eff

    return (water_hp, break_hp, input_hp)

def velocity(flow, pipe_diam):
    '''Velocity Calculations:
        Enter flow in gpm and pipe_diameter in inches
        Returns velocity in FPS
    '''
    V = 0.4085*flow/(pipe_diam**2)

    return V

def flow(velocity, pipe_diam):
    '''Flow Calculation:
        Enter velocity in fps and pipe_diam in inches
        Returns Flow in gpm
    '''
    Q = velocity * pipe_diam**2/0.4085

    return Q

def gpm2cuftps(gpm):
    ''' gpm to cuft per sec conversion '''
    return gpm * 0.002228
def cuftps2gpm(cuftps):
    ''' cuft per sec to gpm conversion'''
    return cuftps * 448.831169

def pipeDiameter(flow, velocity):
    '''pipe diameter calculation:
        Enter velocity in fps and flow in gpm
        Reutrns diameter in inches
    '''
    pipe_diam = (flow*0.4085/velocity)**0.5

    return pipe_diam

def reynolds(pipe_diam, flow=None, vel=None, viscocity=1.3081):
    '''Reynolds Number Calculation:
        Enter flow (gpm), pipe diameter(inches)
        viscosity in cSt = 1.3081 (default)
    '''
    if flow:
        re = (flow*pipe_diam/12) / (viscocity * pi * pipe_diam**2/4)
    elif vel:
        re = (pipe_diam/12)*vel/viscocity
    else:
        print('Must enter flow or velocity')

    if re > 2300:
        laminar = False
    else:
        laminar = True

    return re, laminar

def volume_cyl(d, h):
    ''' volume of a cylinder using diameter
        returns volume consistent with inputs
    '''
    return (pi*d**2 / 4)*h

def volume_box(length, width, height):
    ''' volume of a box
        returns volume in units consistent with inputs
    '''
    return length*width*height

def cuft2gal(cubic_feet):
    ''' cubic feet to gallon conversion'''
    return cubic_feet*7.4805

def gal2cuft(gallons):
    ''' gallon to cubic feet conversion'''
    return gallons/7.4805

def gal2acft(gallons):
    ''' convert gallons to acre-feet '''
    return gallons/325851

def acft2gal(acft):
    ''' convert acre-feet to gallons '''
    return acft * 325851

def cuin2gal(cubic_inches):
    ''' convert cubic inches to gallons '''
    return cubic_inches/231

def gal2cuin(gallons):
    ''' converts gallons to cubic inches '''
    return gallons * 231

def minor_loss(vel, k_val ):
    ''' minor head loss using FPS '''
    g = 32.2
    return k_val * vel**2/(2*g)

def report_losses(losses, flow, name):
    '''prints high and low flow head loss for given inputs
        report_losses(list, list, str)
       if only one value is passed for both losses and flow
       it will only report one losses value

    '''
    if losses is list and flow is list:
        output = '{}: {:.2f} ft @ {:.1f} gpm -- {:.2f} ft @ {:.1f} gpm'.format(name,
                                                                           losses[0],
                                                                           flow[0], 
                                                                           losses[-1],
                                                                           flow[-1])
    else:
        output = '{}: {:.2f} ft @ {:.2f} gpm'.format(name,
                                                     losses,
                                                     flow)

    return output

def ft2psi(ft_of_head):
    ''' convert feet of head to psi '''
    return ft_of_head * 0.43333

def psi2ft(psi):
    ''' return psi to feet of head '''
    return psi * 2.308

def hpn_size(cut_out, cut_in, num_cycles, max_flow, tank_diam):
    ''' Hydro Pneumatic Tank Sizing

        cut_out = nominal pump-off pressure in psi
        cut_in = nominal pump-on pressure in psi
        num_cycles = max number of cycles/hour/pump
        max_flow = estimated max flow from 1 pump
        tank_diam = diameter of tank in inches
    '''
    
    R = tank_diam/2
    A_t = (pi*R**2)
    A_6 = (R**2 * acos((R-6)/R) - (R-6) * sqrt(2*R*6 - 6**2))
    MF = A_t / (A_t - A_6)
    
    V = ((cut_out + 14.7)*15*max_flow*MF)/((cut_out-cut_in)*num_cycles)
    return V

def bladder_size(cut_out, cut_in, num_cycles, max_flow, bladder_vol):
    ''' Bladder Tank sizing

        cut_out = nominal pump-off pressure in psi
        cut_in = nominal pump-on pressure in psi
        num_cycles = max number of cycles/hour/pump
        max_flow = estimated max flow from 1 pump
        bladder_vol = volume of bladder tank in gallons
        '''
    R = 15*(cut_out+14.7)*(cut_in+14.7) / ((cut_out-cut_in)*(cut_in+9.7))
    T = R*max_flow / (num_cycles * bladder_vol)
    return ceil(T)

def air_dump_valve_size(cut_out, cut_in, tank_vol, evac_time=5, info=False):
    ''' Air Dump Valve Sizing :
        cut_out = nominal pump off pressure in psi
        cut_in = nominal pump on pressure in psi
        tank_vol = volume of H-PN tank in gallons
        evac_time = time to empty entire tank in minutes (default 5)
        info = print report (default false)
    '''
    # Constants
    R = 53.35  # R constant in ftlb/Rankine
    T = 527.7  # Air temp  in Rankine
    Z = 1
    C = 356
    K = .975
    k_b = 1
    M = 28.97
    # Calcs
    V_tank = tank_vol / 7.481   # cuft
    V_air = V_tank/2      # air vol in tank (half full)
    P_avg = (cut_out + cut_in)/ 2   # avg pressure
    # In No-Water Event...
    P_empty = P_avg * V_air / V_tank   # in psi
    m = (P_empty*V_tank) / (R*T) * 144  # in lbs of air
    # theoretical orifice dims
    W = (m/evac_time) * 60   # mean dischage in lb/hr
    A = (W * sqrt(T*Z)) / (C * K * (P_empty + 14.7) * k_b * sqrt(M))
    D = sqrt(4*A/pi)
    if info:
        report = '''
            Pressure in No-Water Event = {0:.2f} psi
            Mass of Air in Tank = {1:.2f} lbs
            Mean Discharge Rate = {2:.2f} lbs/hr
            Theoretical Orifice Dims:
                                Area = {3:.3f} in^2
                                Diameter = {4:.3f} in
            '''.format(
                P_empty, m, W, A, D)
        
        if D <= .5:
            report += '\nApco Valve #200 with 1/2" diameter OK'
        print(report)
    return D
    
def pressure_relief_valve_size(
                                cut_out,
                                tank_vol,
                                capacity=None,
                                R=53.35,
                                T=527.7,
                                Z=1,
                                C=356,
                                K=0.878,
                                k_b=1,
                                M=28.97,
                                info=False
                                ):
    ''' pressure Relief Valve Sizing :
        cut_out = nominal pump off pressure in psi
        tank_vol = volume of H-PN tank in gallons
        capacity = required relieving capacity in SCFM
                if None then it will lenearly interpolate from cut_out press
                using WWS standard compressor

        # Constants (defauts)
        R = 53.35  # R constant in ftlb/Rankine
        T = 527.7  # Air temp  in Rankine
        Z = 1
        C = 356
        K = .878
        k_b = 1
        M = 28.97
        info = print report (default false)

    '''
    orifice_area = {'D' : 0.121,
                    'E' : 0.216,
                    'F' : 0.337,
                    'G' : 0.553,
                    'H' : 0.864,
                    'J' : 1.415}
    
    
    # Calcs
    V_tank = tank_vol / 7.481   # cuft
    V_air = V_tank/2      # air vol in tank (half full)
    P_1 = round(cut_out * 1.1)

    # assuming California Air Tools Compressor flow rate
    if capacity is None: 
        capacity = -.022*cut_out + 7.28  # CFM

    # mass of air per minute
    m_dot = (cut_out * capacity *144) / (R*T)  # in lbs of air/min
    delta_m = ((P_1-cut_out)*V_air*144) / (R*T)
    m = (m_dot + delta_m) # lbs of air/min

    # theoretical orifice dims
    W = m * 60   # mean dischage in lb/hr
    A = (W * sqrt(T*Z)) / (C * K * (P_1 + 14.7) * k_b * sqrt(M))
    D = sqrt(4*A/pi)
    

    if info:
        report = '''
            Pressure Setpoint = {0:.2f} psi
            Volumetric Flow of Air Contribuited by compressor = {7:.2f}
            Mass of air contributed by compressor = {4:.2f}
            Mass of built up air to be discharged = {5:.2f}
            Total Mass of Air to be Discharged = {6:.2f}
            Mean Discharge Rate = {1:.2f} lbs/hr
            Theoretical Orifice Dims:
                                Area = {2:.3f} in^2
                                Diameter = {3:.3f} in
            '''.format(
                P_1, W, A, D, m_dot, delta_m, m, capacity)
            
        print(report)
    return A

def resistance(velocity=None, headloss=None, K=None):
    ''' calculates resistance coefficient or headloss
        depending on what is given

        Enter velociy in FPS
        Enter headloss in feet
        OR
        Enter K
    '''
    g = 32.2
    
    if headloss and not K:
        K = (2*g*headloss)/velocity**2
        return K
    elif K and not headloss:
        headloss = K * (velocity**2/(2*g))
        return headloss
    else:
        print('must enter headloss or K value')
        
def leakage(pipe_diam, test_pressure, linear_feet, hydrants=0, interties=0, valves=0, end_caps=0):
    ''' calculates allowable leakage for a pressure test:

        Enter: 
            pipe diameter in inches
            test pressure in psi
            linear_feet of pipe run
            number of hydrants
            number of interties
            number of valves
            number of end caps
    '''
    lf = linear_feet/20
    hyd = hydrants * 5
    vlv = valves * 2
    N = lf + hyd + interties + vlv + end_caps

    L_gph = N * pipe_diam * sqrt(test_pressure) / 7400
    L_gpm = L_gph/60

    return L_gph, L_gpm

def makeup_water(diam_before, diam_after, depth_before, depth_after):
    ''' Enter dimensions of frustrum or cylynder to return volume
        
        Used to estimate the volume of water in a trash can. 
        Units must be uniform.
        Arguments:
            diam_before = can diameter before pumping
            diam_after = can diameter after pumping
            depth_before = water level before pumping
            depth_after - water level after pumping
        '''
    h = abs(depth_before - depth_after)
    V = (pi * h * (diam_before**2 + diam_before*diam_after + diam_after**2)) / 12
    return V

def wellhead_CFR(Q, H, n=0.22, t_list=[1,5,10]):
    ''' Returns fixed radius wellhead contribution zones (CFR):
        Default is 1 year, 5 year, and 10 year radii
        Enter:
            Q = pumping rate in cubic ft/yr
            H = open interval in ft
            n = aquifer porosity (defaults to 0.22)
            t = time in years (default list [1,5,10])
    '''
    r = [sqrt(Q*t/(pi*n*H)) for t in t_list]

    return r

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
    Re, Lam = reynolds(d, vel=v)
    if Lam:
        condition = 'Laminar'
    else:
        condition = 'Turbulent'

    # Volume Calculations
    vol1 = volume_cyl(5, 10)
    vol2 = volume_box(5, 10, 20)

    # cubic feet to gallon conversion
    gals = cuft2gal(1000)

    # allowable leakage calc
    leak_gph, leak_gpm = leakage(8, 245, 1460, 1, 2, 3)
    
    # makeup water volume (volume of a frustrum)
    mw = makeup_water(18, 17.5, 19, 18)

    # bladder tank sizing
    bt = bladder_size(86, 67, 6, 90, 34)

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
        allowable leakage = {18:.2f} gph or {19:.3f} gpm
        makeup water = {20:.3f} cubic inches or {21:.3f} gals
        number of bladder tanks = {22:.1f} tanks
        '''.format(
            phd, phd2, water_p, break_p, input_p,
            water2_p, Q, d, v, q_func, d_func, Re,
            condition, vol1, vol2, ahd, lhd, gals,
            leak_gph, leak_gpm, mw, cuin2gal(mw), bt)

    print(out)
    pressure_relief_valve_size(95, 500, info=True)

