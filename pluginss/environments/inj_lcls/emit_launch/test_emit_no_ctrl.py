import os
import sys
import time
import numpy as np
import matlab_wrapper


class Matlab(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Matlab, cls).__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self, *args, **kwargs):
        root = kwargs.get('root', None)
        if not root:
            root = os.getenv('MATLAB_ROOT')
        print('Starting Matlab Session')
        print('root',root)
        self.session = matlab_wrapper.MatlabSession(matlab_root=root)


local_path = os.path.dirname(os.path.abspath(__file__))
#base_ocelot_path = '/home/physics/adiha/optimizer_injector_2021_02_16/'
#sys.path.append(base_ocelot_path)


#local_path = os.path.dirname(os.path.abspath(__file__))
ml = Matlab()
ml.session.eval("addpath('{}')".format(local_path))

def launch_emittance_measurment():
    emittance = -1
    
    ml.session.eval('clearvars') #clear variables
    ml.session.eval('emittance_x = matlab_test()')
    
    emittance_x = ml.session.workspace.emittance_x
    print('emittance ',emittance_x)
    return emittance_x

for i in range(0,3):
    datain = launch_emittance_measurment()

    print(i)
    print(datain)

