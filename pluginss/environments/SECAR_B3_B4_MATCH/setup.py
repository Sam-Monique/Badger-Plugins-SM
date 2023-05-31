from epics import caget, caput, cainfo

mag_loc = {
'b1':'1489',
'b2':'1504',
'b3':'1547', 
'b4':'1557',
'b5':'1665',
'b6':'1678',
'b7':'1807',
'b8':'1826',
}
set_probe = 'SCR_BTS35:NMR1_D1489:PRB_CSET'
tlm_reading = 'SCR_BTS35:NMR_N0001:B_RD'

def GetMagnet(name):

    '''Takes any magnet name and returns its current readback value'''

    if   (name[0] == 'b' or name[0] == 't'):
        dev = 'PSD'
    elif (name[0] == 'q'):
        dev = 'PSQ'
    elif (name[0] == 'h' or name[0] == 's'):
        dev = 'PSS'
    elif (name[0] == 'o'):
        dev = 'PSO'

    #~ return caget(f'SCR_BTS35:{dev}_D{mag_loc[name]}:I_RD')
    #changed to read the setpoint because the difference between set and read makes the matching impossible sometimes
    return caget(f'SCR_BTS35:{dev}_D{mag_loc[name]}:I_CSET')


def CycleMagnet(name):

    '''Cycles the given magnet'''

    if   (name[0] == 'b'):
        dev = 'PSD'
    elif (name[0] == 'q'):
        dev = 'PSQ'
    elif (name[0] == 'h'):
        dev = 'PSS'
    elif (name[0] == 'o'):
        dev = 'PSO'

    cpstm = caget(f'SCR_BTS35:{dev}_D{mag_loc[name]}:CYCL_PSTM')
    iters = caget(f'SCR_BTS35:{dev}_D{mag_loc[name]}:CYCL_ITERS')

    time = cpstm*iters*2 + 30
    cycle_cmd = f'SCR_BTS35:{dev}_D{mag_loc[name]}:CYCL_CMD'

    caput(cycle_cmd, 1)
    print(f"Cycling {name}...wait {time/60} minutes")

    return time

def nmrRange():
    ''' Checks which range the NMR probes should be in and returns probe numbers for B1 and B2 '''
 
    irangeswitch= 43.4 

    b1_current = GetMagnet('b1')

    print("Checking probe ranges...")
    if (b1_current >= irangeswitch):
        b1 = 1
        b2 = 3
    else:
        b1 = 2
        b2 = 4

    return b1, b2
def GetHall(name):

    '''Gets Hall probe value of given magnet'''

    hall_pv = f'SCR_BTS35:HAL_D{mag_loc[name]}:B_RD'

    return caget(hall_pv)













 

