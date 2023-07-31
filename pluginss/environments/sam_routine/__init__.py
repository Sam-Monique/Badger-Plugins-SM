import numpy as np
from badger import environment
from badger.interface import Interface

class Environment(environment.Environment):
    
    name = 'sam_routine'

    def __init__(self, interface: Interface, params):
        super().__init__(interface, params)
        self.variables = {
            'L':0,
            'W':0
        }

    @staticmethod
    def list_vars():
        return['L','W']
    
    @staticmethod
    def list_obses():
        return['A','P']

    @staticmethod
    def get_default_params():
        return None
    
    def _get_vrange(self, var):
        return [0, 5]

    def _get_var(self, var):
        return self.variables[var]

        
    def _set_var(self, var, x):
        self.variables[var] = x

    def _get_obs(self, obs):
        L = self.variables['L']
        W = self.variables['W']

        if obs == 'A':
            return L*W
        elif obs == 'P':
            return 2*L + 2*W
    
