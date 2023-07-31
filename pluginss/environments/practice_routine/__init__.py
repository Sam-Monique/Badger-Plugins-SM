from typing import List
import numpy as np
from badger import environment
from badger.interface import Interface
import yaml
class Environment(environment.Environment):

    name = 'practice_routine'

    vranges = {
        'x1': [-4,1],
        'x2': [0,5],
        'x3':[-2,2],
        'x4':[-5,5],
        'x5':[-5,5],
    }

    def __init__(self, interface: Interface, params):
        super().__init__(interface, params)
        self.variables = {
            'x1': 0,
            'x2': 0,
            'x3':2,
            'x4':0,
            'x5':0,
        }
        

    @staticmethod
    def list_vars():
        return ['x1','x2','x3','x4','x5']
    
    @staticmethod
    def list_obses():
        return ['y1','y2','y3','y4']
    
    @staticmethod
    def get_default_params():
        return {}

    def _get_vrange(self, var):
        return self.vranges[var]

    def _get_var(self, var):
        return self.variables[var]

    def _set_var(self, var, x):
        self.variables[var] = x
    
    def _get_obs(self, obs):
        x1 = self.variables['x1']
        x2 = self.variables['x2']
        x3 = self.variables['x3']
        x4 = self.variables['x4']
        x5 = self.variables['x5']
        if obs == 'y1':
            return -x4**2-x5**2 +5

        elif obs == 'y2':
            return x4**2+x5**2

        elif obs == 'y3':
            
            return -(x3**2) + 1

        elif obs == 'y4':
            return x3**2
        

