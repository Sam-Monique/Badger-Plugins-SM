from .setup import CycleMagnet,GetHall, tlm_reading
from epics import caget
import time
import numpy as np


def close(values, tol):

    near = True

    for i in range(len(values)):
        for j in range(i+1,len(values)):
            if not np.isclose(values[i], values[j], atol= tol):
                near = False
    
    return near

def check_stability(name, time_elapse, num_prev, tolerance):
    continue_routine = False
    previous = []

    while not continue_routine:

        time.sleep(time_elapse)
        try:
            val = GetHall(name)
        except:
            val = caget(tlm_reading)

        previous.append(val)

        if len(previous) < num_prev:
            continue_routine = False

        else:
            last = previous[-num_prev:]
            if close(last, tolerance):
                continue_routine = True


def check_stabilities(names, time_elapse, num_prev, tolerance):
    continue_routine = False
    previous = {}

    for name in names:
        previous[name] = []

    while not continue_routine:

        time.sleep(time_elapse)
        for name in names:
            if name not in ['b1','b2']:

                val = GetHall(name)
            else:
                val = caget(tlm_reading)

            previous[name].append(val)

        if len(previous) < num_prev:
            continue_routine = False

        else:
            cont = 0
            for name in names:

                last = previous[name][-num_prev:]
                if not close(last, tolerance):
                    cont += 1
            
            if cont == 0:
                continue_routine = True






