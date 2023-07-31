from setup import SetMagnet, GetMagnet
import threading
import time

dipole_ranges = {'b1':[0,180],
                 'b2':[0,180],
                 'b3':[0,180],
                 'b4':[0,180],
                 'b5':[0,180],
                 'b6':[0,180],
                 'b7':[0,180],
                 'b8':[0,180],
                 }

ramping_rate = 5

def Cycle(mag):

    current_val = GetMagnet(mag)

    while (current_val + ramping_rate) < dipole_ranges[mag][1]:

        SetMagnet(mag, current_val + ramping_rate)

        current_val += ramping_rate

        time.sleep(1)

    SetMagnet(mag, dipole_ranges[mag][1])

    time.sleep(30)

    current_val = dipole_ranges[mag][1]

    while current_val > ramping_rate + dipole_ranges[mag][0]:

        SetMagnet(mag, current_val - ramping_rate)

        current_val -= ramping_rate

        time.sleep(1)

    SetMagnet(mag, dipole_ranges[mag][0])

    time.sleep(30)

    current_val = dipole_ranges[mag][0]

    while current_val > ramping_rate + dipole_ranges[mag][0]:

        SetMagnet(mag, current_val + ramping_rate)

        current_val += ramping_rate

        time.sleep(1)

    SetMagnet(mag, dipole_ranges[mag][1])


def GetTime(mag):
    current_val = GetMagnet(mag)


    time = (dipole_ranges[mag][1]-current_val)/ramping_rate + 2*(dipole_ranges[mag][1]-dipole_ranges[mag][0])/ramping_rate +60

    return time

def CycleMagnet(mag):

    time = GetTime(mag)
    
    thread = threading.Thread(target=Cycle, args= (mag,))
    thread.start()

    return time
