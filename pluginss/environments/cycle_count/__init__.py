from typing import List
import numpy as np
from badger import environment
from badger.interface import Interface
class Environment(environment.Environment):

    name = 'cycle_count'

    vranges = {
        'x1':[85,115]
    }

    def __init__(self, interface: Interface, params):
        super().__init__(interface, params)
        self.variables = {
            'x1': 115
        }
        self.cycle = 0



        

    @staticmethod
    def list_vars():
        return ['x1']
    
    @staticmethod
    def list_obses():
        return ['y1', 'cycles']
    
    @staticmethod
    def get_default_params():
        return {'noise': 1e-6}

    def _get_vrange(self, var):
        return self.vranges[var]

    def _get_var(self, var):
        return self.variables[var]

    def _set_var(self, var, x):

        if x > self.variables[var]:
            self.cycle += 1
        self.variables[var] = x



    
    def _get_obs(self, obs):
        x1 = self.variables['x1']

        noise = float(self.params['noise'])
           
        if obs == 'y1':
            b3 = 0.34773# + np.random.uniform(-1e-6, 1e-6)

            b4 = x1*(0.34773/105.2) + np.random.random_integers(-noise/1e-6,noise/1e-6)*1e-6  #np.random.uniform(-1e-6, 1e-6)

            val = (b4-b3)**2

            return val
        
        elif obs == 'cycles':
            return self.cycle
