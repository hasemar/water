'''
Tools to calculate water system
design aspects
'''

from __future__ import print_function, division
from math import pi, acos, sqrt, ceil

def coeffs(num_ERUs):
    '''C and F coefficients from  the `2019 DOH Water System Design Manual`_ Table 3-1 
    
    .. _2019 DOH Water System Design Manual: https://www.doh.wa.gov/Portals/1/Documents/Pubs/331-123.pdf?ver=2019-10-03-153237-220

    :param num_ERUs: number of Equivalent Residential Units
    :type num_ERUs: int
    :return: C and F Coefficients
    :rtype: tuple (C, F)

    :Example: 

    >>> from Water import tools
    >>> ERUs = 1500
    >>> C, F = tools.coeffs(ERUs)

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
    '''Peak Hour Demand Calculation from the `2019 DOH Water System Design Manual`_ Equation 3-1 
    
    .. _2019 DOH Water System Design Manual: https://www.doh.wa.gov/Portals/1/Documents/Pubs/331-123.pdf?ver=2019-10-03-153237-220

    .. math::

        PHD &= \\frac{ERU_{MDD}}{1440}(C N + F) + 18  

        \\text{where:}  

        PHD &= \\text{Peak Hourly Demand, total system (gpm)}  

        C &= \\text{Coefficent Associated with Ranges of ERUs}  

        N &= \\text{Number of ERUs based on MDD}  

        F &= \\text{Factor Associated with Ranges of ERUs}  

        ERU_{MDD} &= \\text{Maximum Day Demand (gpd/ERU)}  

    C and F coefficients are automatically calculated within PHD equation
        
    :param MDD: Maximum Day Demand (gpd/ERU)
    :type MDD: int
    :param num_ERUs: Number of ERUs based on MDD
    :return: Peak Hour Demand (gpm)
    :rtype: int/float


    '''

    C, F = coeffs(num_ERUs)
    phd = (MDD/1440)*(C*num_ERUs + F) + 18

    return phd

def equalizing_storage(PHD, Qs):
    '''Equalizing Storage calculation from the `2019 DOH Water System Design Manual`_ Equation 7-1 
    
    .. _2019 DOH Water System Design Manual: https://www.doh.wa.gov/Portals/1/Documents/Pubs/331-123.pdf?ver=2019-10-03-153237-220

    .. math::

        ES &= 150(PHD - Q_s)

        \\text{where:}   

        ES &= \\text{Equalizing Storage in gallons}  

    :param PHD: Peak Hour Demand in gallons per minute (gpm)
    :type PHD: int/float
    :param Qs: total source supply (gpm)
    :type Qs: int/float
    :return: Equalizing Storage component in gallons
    :rtype: int/float

    '''
    return (PHD-Qs)*150

def standby_storage(N,SBi, Td=1):
    '''Standby Storage calculation from the `2019 DOH Water System Design Manual`_ Equation 7-2 
    
    .. _2019 DOH Water System Design Manual: https://www.doh.wa.gov/Portals/1/Documents/Pubs/331-123.pdf?ver=2019-10-03-153237-220

    .. math::
        
        SB &= (N)(SB_i)(T_d)

        \\text{where:}

        SB &= \\text{Total Standby Storage component in gallons}

    :param N: number of Equivalent Residential Units (ERUs) based on MDD
    :type N: int
    :param SBi:  locally adopted unit SB volume in gallons per day per ERU (gpd/ERU)
    :type SBi: int
    :param Td: Number of days selected to meet water system-determined standard of reliability, *default 1* 
    :type Td: int
    :return: Total Standby Storage component in gallons
    :rtype: int

    '''

def calc_hp(flow_rate, head, pump_eff=0.6, motor_eff=0.9):
    '''Horsepower Calculations

    .. math::
    
        hp_{water}&=(Q)(TDH)\\bigg{(}\\frac{1\ psi}{2.308\ ft}\\bigg{)}\\bigg{(}\\frac{1\ hp}{1714 (psi\ gpm)}\\bigg{)}

        hp_{break}&=\\frac{hp_{water}}{\eta_{pump}}
        
        hp_{input}&=\\frac{hp_{break}}{\eta_{motor}}

        \\text{where:}\\quad \\eta_{pump} &= \\text{pump efficiency}, \\quad \\eta_{motor} = \\text{motor efficiency}

    :param flow_rate: pump flow rate in gallons per minute (gpm)
    :type flow_rate: int/float
    :param head: pump head in feet (ft)
    :type head: int/float
    :param pump_eff: pump efficiency, *default 0.6*
    :type pump_eff: float
    :param motor_eff: motor efficiency, *default 0.9*
    :type motor_eff: float
    :return: (water hp, break hp, input hp)
    :rtype: tuple

    :Example:

    .. code-block:: python

        from Water import tools

        # pumping parameters
        flow = 1000   # gpm
        head = 500    # ft of water

        water_hp, break_hp, input_hp = tools.calc_hp(flow, head)

        print(water_hp, break_hp, input_hp)

    >>>  126.26262626262626 210.43771043771042 233.81967826412267
    

    
    '''
    water_hp = (flow_rate*head)/3960
    break_hp = water_hp/pump_eff
    input_hp = break_hp/motor_eff

    return (water_hp, break_hp, input_hp)

def velocity(flow, pipe_diam):
    '''calculate water velocity through a pipe

    :param flow: flow in gpm
    :type flow: int/float
    :param pipe_diam: pipe diameter in inches
    :type pipe_diam: float
    :return: velocity in feet per second (FPS)
    
    '''
    Q = gpm2cuftps(flow)
    d = pipe_diam/12
    V = (4*Q)/(pi*d**2)

    return V

def flow(velocity, pipe_diam):
    '''calculate flow through a pipe

        :param velocity: water velocity in feet per second (FPS)
        :type velocity: int/float
        :param pipe_diam: pipe diameter in inches
        :type pipe_diam: int/float
        :return: flow through a pipe in gallons per minute (gpm)
        :rtype: float

    '''
    d = pipe_diam/12
    A = pi/4 * d**2
    Q= cuftps2gpm(velocity * A)

    return Q

def gpm2cuftps(gpm):
    ''' gallons per minute (gpm) to cubic feet per second (cuft/s) conversion
    
    :param gpm: gallons per minute (gpm)
    :type gpm: int/float
    :return: cubic feet per second (cuft/s)
    :rtype: float
    
     '''
    return gpm * 0.00222802

def cuftps2gpm(cuftps):
    ''' cubic feet per second (cuft/s) to gallons per minute (gpm) conversion
    
    :param cuftps: cubic feet per second (cuft/s)
    :type cuftps: int/float
    :return: gallons per minute (gpm)
    :rtype: float

    '''
    return cuftps * 448.831169

def pipeDiameter(flow, velocity):
    '''calculation for pipe diameter, given flow and velocity

    :param flow: flow in gallons per minute (gpm)
    :type flow: int/float
    :param velocity: velocity in feet per second (FPS)
    :type velocity: int/float
    :return: pipe diameter in inches
    :rtype: float
        
    '''
    pipe_diam = (flow*0.4085/velocity)**0.5

    return pipe_diam

def reynolds(pipe_diam, flow=None, vel=None, viscocity=1.3081):
    '''Reynolds Number Calculation

    :param pipe_diam: pipe diameter in inches
    :type pipe_diam: int/float
    :param flow: flow in gallons per minute (gpm), *default None*
    :type flow: int/float
    :param vel: velocity in feet per second (FPS), *default None*
    :type vel: int/float
    :param viscocity: viscocity in cSt *default 1.3081*
    :return: Reynolds Number
    :rtype: int

    '''
    if flow:
        re = (flow*pipe_diam/12) / (viscocity * pi * pipe_diam**2/4)
    elif vel:
        re = (pipe_diam/12)*vel/viscocity
    else:
        print('Must enter flow or velocity')

    return int(re) 

def volume_cyl(diameter, height):
    ''' calculate the  volume of a cylinder

    :param diameter: diameter of cylinder
    :type diameter: int/float
    :param height: height of cylinder
    :type height: int/float
    :return: volume of a cylinder in consistent units
    :rtype: float

    '''
    return (pi*diameter**2 / 4)*height

def volume_box(length, width, height):
    ''' calculate the volume of a box
    
    :param length: length of box
    :type length: int/float
    :param width: width of box
    :type width: int/float
    :param height: height of box
    :type height: int/float
    :return: volume of a box
    :rtype: float

    '''
    return length*width*height

def cuft2gal(cubic_feet):
    ''' cubic feet to gallon conversion
    
    :param cubic_feet: cubic feet
    :type cubic_feet: int/float
    :return: gallons
    :rtype: float

    '''
    return cubic_feet*7.4805

def gal2cuft(gallons):
    ''' gallon to cubic feet conversion
    
    :param gallons: gallons
    :type gallons: int/float
    :return: cubic feet
    :rtype: float

    '''
    return gallons/7.4805

def gal2acft(gallons):
    '''gallons to acre-feet conversion
    
    :param gallons: gallons
    :type gallons: int/float
    :return: acre feet
    :rtype: float

    '''
    return gallons/325851

def acft2gal(acft):
    '''acre-feet to gallons conversion
    
    :param acft: acre feet 
    :type acft: int/float
    :return: gallons
    :rtype: float
    
    '''
    return acft * 325851

def cuin2gal(cubic_inches):
    '''cubic inches to gallons conversion
    
    :param cubic_inches: cubic inches
    :type cubic_inches: int/float
    :return: gallons
    :rtype: float
    
    '''
    return cubic_inches/231

def gal2cuin(gallons):
    '''gallon to cubic inch conversion
    
    :param gallons: gallons
    :type gallons: int/float
    :return: cubic inches
    :rtype: float

     '''
    return gallons * 231

def minor_loss(velocity, k_val ):
    ''' minor head loss using the `Darcy-Weisbach equation`_  
        
    .. _Darcy-Weisbach equation: https://en.wikipedia.org/wiki/Darcy%E2%80%93Weisbach_equation   

    .. math:: h_{minor} = f_D \\cdot \\frac{1}{2g} \\cdot \\frac{v^2}{D}
    
    :param velocity: velocity in feet per second (FPS)
    :param k_val: K value
    :type velocity: int/float
    :type velocity: int/float
    :return: minor head loss in feet
    :rtype: float

     '''
    g = 32.2
    return k_val * velocity**2/(2*g)

def ft2psi(ft_of_head):
    '''feet of head to pounds per square inch (psi) conversion
    
    :param ft_of_head: feet of head
    :type ft_of_head: int/float
    :return: psi
    :rtype: float

     '''
    return ft_of_head * 0.433333333

def psi2ft(psi):
    ''' return psi to feet of head
    
    :param psi: pounds per square feet (psi)
    :type psi: int/float
    :return: feet of head
    :rtype: float

     '''
    return psi * 2.308

def hpn_size(cut_out, cut_in, num_cycles, max_flow, tank_diam, shape='horiztonal'):
    ''' hydro-pneumatic tank sizing calculation from the `2019 DOH Water System Design Manual`_ Equations 9-2 and 9-3 
    
    .. _2019 DOH Water System Design Manual: https://www.doh.wa.gov/Portals/1/Documents/Pubs/331-123.pdf?ver=2019-10-03-153237-220

    :param cut_out: nominal pump-off pressure in psi (P_1)
    :param cut_in: nominal pump-on pressure in psi (P_2)
    :param num_cycles: max number of cycles/hour/pump (Nc)
    :parma max_flow: estimated max flow from 1 pump (Qp)
    :param tank_diam: diameter of tank in inches
    :param shape: tank shape (must be 'horizontal' or 'vertical')
    :type cut_out: int/float
    :type cut_in: int/float
    :type num_cycles: int
    :type max_flow: int/float
    :type tank_diam: int/float
    :type shape: string
    :return: recommended volume for hydro-pnuematic tank
    :rtype: float
    
    '''
    assert (shape == 'horizontal' or shape == 'vertical'), "shape must be horizontal or vertical"

    R = tank_diam/2
    A_t = (pi*R**2)
    A_6 = (R**2 * acos((R-6)/R) - (R-6) * sqrt(2*R*6 - 6**2))
    MF = A_t / (A_t - A_6)
    
    V = ((cut_out + 14.7)*15*max_flow*MF)/((cut_out-cut_in)*num_cycles)
    if shape == 'vertical':
        V += 0.0204 * tank_diam**2
        
    return V

def bladder_size(cut_out, cut_in, num_cycles, max_flow, bladder_vol):
    ''' Bladder Tank sizing from the `2019 DOH Water System Design Manual`_ Equation 9-1
    
    .. _2019 DOH Water System Design Manual: https://www.doh.wa.gov/Portals/1/Documents/Pubs/331-123.pdf?ver=2019-10-03-153237-220

    :param cut_out: nominal pump-off pressure in psi
    :param  cut_in: nominal pump-on pressure in psi
    :param num_cycles: max number of cycles/hour/pump
    :param max_flow: estimated max flow from 1 pump
    :param bladder_vol: volume of bladder tank in gallons
    :type cut_out: int/float
    :type cut_in: int/float
    :type num_cycles: int
    :type max_flow: int/float
    :type bladder_vol: int/float
    :return: number of bladder tanks
    :rtype: int

    '''
    R = 15*(cut_out+14.7)*(cut_in+14.7) / ((cut_out-cut_in)*(cut_in+9.7))
    T = R*max_flow / (num_cycles * bladder_vol)

    return ceil(T)

def air_dump_valve_size(cut_out, cut_in, tank_vol, evac_time=5, info=False, **kwargs):
    '''"Air Dump" valve orifice size calculation. Sizes the minimum theoretical orifice 
    diameter of an air release valve to evaculate a volume of air in a given period of 
    time. This function assumes a starting water level in the tank at half full and a
    required dump air volume when the tank is empty. 

    .. math::

        A = \\frac{W}{C K P_1 K_b} \\sqrt{\\frac{T Z}{M}}
    
    where A = orifice area

    :param cut_out: nominal pump off pressure in psi
    :param cut_in:  nominal pump on pressure in psi
    :param tank_vol: volume of H-PN tank in gallons
    :param evac_time: time to empty entire tank in minutes *default 5*
    :param info: print report *default false*
    :param \**kwargs: keyword arguments
    :type cut_out: int/float
    :type cut_in: int/float
    :type tank_vol: int/float
    :type evac_time: int
    :type info: boolean
    :type \**kwargs: dictionary
    :return: theoretical orifice size, if info==true then it will print a report
    :rtype: float
    :keyword arguments:
        :R: (*int/float*) -  ideal gas constant in ftlb/Rankine *default 53.35*
        :T: (*int/float*) - air temperature in Rankine *default 527.7*
        :Z: (*int/float*) - compressibility factor *default 1*
        :C: (*int/float*) - gas constant based upon the ratio of specific heats *default 356*
        :K: (*int/float*) - coefficient of discharge *default 0.975*
        :k_b: (*int/float*) - backpressure correction factor *default 1*
        :M: (*int/float*) - molecular weight of of air in lbm/lbmol *default 28.97*

     '''
    # Keyword arguments
    R = kwargs.get('R', 53.35)  # R constant in ftlb/Rankine
    T = kwargs.get('T', 527.7)  # Air temp  in Rankine
    Z = kwargs.get('Z', 1)  
    C = kwargs.get('C', 356)  # gas constant
    K = kwargs.get('K', 0.975)
    k_b = kwargs.get('k_b', 1)
    M = kwargs.get('M', 28.97)

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
    
def pressure_relief_valve_size(cut_out, tank_vol, capacity=None, info=False, **kwargs):
    ''' pressure relief valve sizing  calculation for ASME VIII valve on a H-PN tank

    .. math::

        A = \\frac{W}{C K P_1 K_b} \\sqrt{\\frac{T Z}{M}}
    
    where A = orifice area

    :param cut_out: nominal pump off pressure in psi
    :type cut_out: int/float
    :param tank_vol: volume of H-PN tank in gallons
    :type tank_vol: int/float
    :param capacity: required relieving capacity in SCFM *default None* (see note)
    :type capacity: int/float 
    :param info: print a report of the results
    :type info: boolean
    :param \**kwargs: keyword arguments
    :type \**kwargs: dictionary
    :return: returns the minimum orifice diameter of a H-PN tank
    :rtype: float
    :keyword arguments:
        :R: (*int/float*) - ideal gas constant in ftlb/Rankine *default 53.35*
        :T: (*int/float*) - air temperature in Rankine *default = 527.7*
        :Z: (*int/float*) - compressibility factor *default 1*
        :K: (*int/float*) - coefficient of discharge *default 0.878*
        :k_b: (*int/float*) - backpressure coefficient *default 1*
        :M: molecular weight of air in lbm/lbmol *default 28.97* 

    if capacity is **None** then it will use the WWS standard compressor capacity

    '''

    R = kwargs.get('R', 53.35)
    T = kwargs.get('T', 527.7)
    Z = kwargs.get('Z', 1)
    C = kwargs.get('C', 356)
    K = kwargs.get('K', 0.878)
    k_b = kwargs.get('k_b', 1)
    M = kwargs.get('M', 28.97)
    
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

    :param velocity: velocity in feet per second (FPS) *default None*
    :param headloss: head loss in feet of water *default None*
    :param K: resistance coefficient *default None*
    :type velocity: int/float
    :type headloss: int/float
    :type K: int/float
    :return: resistance coefficient or headloss
    :rtype: float

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
    ''' calculates AWWA allowable leakage for a pressure test on a water main

        .. math::

            L = \\frac{N d \\sqrt{P_{test}}}{7400}

        :param pipe_diam: pipe diameter in inches (in)
        :param test_pressure: test pressure in psi
        :param linear_feet: length of pipe being tested (ft)
        :param hydrants: number of hydrants *default 0*
        :param interties: number of interties *default 0*
        :param valves: number of valves *default 0*
        :param end_caps: number of end caps *default 0*
        :return: water leakage in gph and gpm
        :rtype: tuple

    '''
    lf = linear_feet/20
    hyd = hydrants * 5
    vlv = valves * 2
    N = lf + hyd + interties + vlv + end_caps

    L_gph = N * pipe_diam * sqrt(test_pressure) / 7400
    L_gpm = L_gph/60

    return L_gph, L_gpm

def makeup_water(diam_before, diam_after, depth_before, depth_after):
    ''' Enter dimensions of frustrum or cylynder to return volume. 
        
    :param diam_before: container diameter before pumping
    :param diam_after: container diameter after pumping
    :param depth_before: water level before pumping
    :param depth_after: water level after pumping
    :type diam_before: int/float:
    :type depth_after: int/float
    :return: volume of water in a cylindrical or conical container
    :rtype: int/float

    '''

    h = abs(depth_before - depth_after)
    V = (pi * h * (diam_before**2 + diam_before*diam_after + diam_after**2)) / 12
    return V

def wellhead_CFR(Q, H, n=0.22, t_list=[1,5,10]):
    ''' Returns fixed radius wellhead contribution zones (CFR) from the 
    `2019 DOH Water System Design Manual`_ Equation 9-1
    
    .. _2019 DOH Water System Design Manual: https://www.doh.wa.gov/Portals/1/Documents/Pubs/331-123.pdf?ver=2019-10-03-153237-220

    :param Q: pumping rate in cubic ft/yr
    :param H: well open interval in ft
    :param n: aquifer porosity *default 0.22*
    :param t_list: times in years *default [1, 5, 10]
    :type Q: int/float
    :type H: int/float
    :type n: float
    :type t_list: list
    :return: radii of well head contribution zones for listed years
    :rtype: list

    '''
    r = [sqrt(Q*t/(pi*n*H)) for t in t_list]

    return r

def max_pump_elevation(elevation, NPSHr, Losses, SF=1.5, **kwargs):
    '''Returns maximum elevation pump suction can be above water level

    :param elevation: elevation of pump in ft
    :param NPSHr: net positive suction head required in ft
    :param Losses: suction side head loss in ft
    :param SF: safety factor *default 1.5*
    :param \**kwargs: keyword arguments
    :type elevation: int/float
    :type NPSHr: int/float
    :type Losses: int/float
    :type SF: int/float
    :type \**kwargs: dictionary
    :return: maximum pump elevation ft
    :rtype: int/float

    Negative number indicates ft of head that must be supplied
    to suction line.

    Positive number indicates how far pump can be above water level.
    
    '''

    # Barometric Pressure Constants
    Pb = kwargs.get('Pb', 29.92126)   # in. Hg
    Tb = kwargs.get('Tb', 288.15)     # K
    R = kwargs.get('R', 8.9494596*10**4)  # lb·ft^2
    g = kwargs.get('g', 32.17405)    #ft/s^2
    M = kwargs.get('M', 28.9644)   # lb/lb-mol
    Pv = kwargs.get('Pv', 0.75)    # vapor pressure of water at 50F in ft
    
    # atm pressure at elevation
    P = Pb*exp((-g*M*elevation)/(R*Tb))

    # convert inches Hg to ft of head
    P = P*1.132925

    # max pump height
    Z = P - NPSHr - Losses - Pv - SF

    return Z 

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

