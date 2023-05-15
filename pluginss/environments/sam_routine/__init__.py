import numpy as np
from badger import environment
from badger.interface import Interface

class Environment(environment.Environment):
    
    name = 'sam_routine'

    def __init__(self, interface: Interface, params):
        super().__init__(interface, params)
        self.variables = {
            'x1':0,
        }
        self.eek = {
            'x2':0
        }
    @staticmethod
    def list_vars():
        return['x1','x2']
    
    @staticmethod
    def list_obses():
        return['y1']

    @staticmethod
    def get_default_params():
        return {'name':0.0, 'INIT:x1':0}
    
    def _get_vrange(self, var):
        return [0, 1.57]

    def _get_var(self, var):
        if var in self.variables.keys():
            return self.variables[var]
        elif var in self.eek.keys():
            return self.eek[var]
        
    def _set_var(self, var, x):
        if var == "x1":
            self.variables[var] = x
        elif var == "x2":
            self.eek[var] = x

    def _get_obs(self, obs):
        x1 = self.variables['x1']
        x2 = self.eek['x2']
        if obs == 'y1':
            return (np.sin(x1))*(np.exp(-(x1)**2)) + x2
