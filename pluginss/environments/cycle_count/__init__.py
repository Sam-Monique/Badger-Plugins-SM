from typing import List
import numpy as np
from badger import environment
from badger.interface import Interface
class Environment(environment.Environment):

    name = 'cycle_count'

    vranges = {
        'x1': [-2,2],
        'x2':[-2,2]
    }

    def __init__(self, interface: Interface, params):
        super().__init__(interface, params)
        self.variables = {
            'x1': 2,
            'x2': 2
        }
        self.cycle = 0

        self.exit = False


        

    @staticmethod
    def list_vars():
        return ['x1','x2']
    
    @staticmethod
    def list_obses():
        return ['y1']
    
    @staticmethod
    def get_default_params():
        return None

    def _get_vrange(self, var):
        return self.vranges[var]

    def _get_var(self, var):
        return self.variables[var]

    def _set_var(self, var, x):

        if x > self.variables[var]:
            self.cycle += 1
            # input(f"Press Enter to Continue")
        print(f"The Magnet has been cycled {self.cycle} times")
        self.variables[var] = x

    # def set_vars(self, vars: List[str], values: list):

    #     times = []
    #     for var, val in zip(vars, values):
    #         if val > self.variables[var]:
    #             self.cycle += 1
    #         print(f"The Magnet has been cycled {self.cycle} times")
    #         self.variables[var] = val


    
    def _get_obs(self, obs):
        x1 = self.variables['x1']
        x2 = self.variables['x2']

        if obs == 'y1': 
            val =  x1**2 - np.sin(x1) + x2**2 + 2*np.sin(x2)
            if val < 6:
                self.exit = True
            return x1**2
            # return x1**6 + x1**3 + np.sin(x1) + x2
           

