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
    }

    def __init__(self, interface: Interface, params):
        super().__init__(interface, params)
        self.variables = {
            'x1': 0,
            'x2': 0,
        }
        with open(self.params['config'], "r") as stream:
            self.configs = yaml.safe_load(stream)

    @staticmethod
    def list_vars():
        return ['x1','x2']
    
    @staticmethod
    def list_obses():
        return ['y1','y2','y3']
    
    @staticmethod
    def get_default_params():
        return {'config':'configs.yaml'}

    def _get_vrange(self, var):
        return self.vranges[var]

    def _get_var(self, var):
        return self.variables[var]

    def _set_var(self, var, x):
        self.variables[var] = x
    
    def _get_obs(self, obs):
        x1 = self.variables['x1']
        x2 = self.variables['x2']

        if obs == 'y1':
            return ((x1)**2+(x2)**2)**(1/2)

        elif obs == 'y2':
            return (x1+x2)/2

        elif obs == 'y3':
            
            dic = self.configs
    


            for i, key  in enumerate(dic.keys()):
                none = list(dic.keys())
                select = none.pop(i)
            
                for channel in none:
                    print(channel)
                    print(dic[channel]['initial'])
                print(select)
                print(dic[select]['range'])

            return 0