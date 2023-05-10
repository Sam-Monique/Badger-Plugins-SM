from badger import environment
from badger.interface import Interface

class Environment(environment.Environment):
    name = 'SECAR_routine'

    vranges = {
        'x1':[0,1]

    }

    def __init__(self, interface: Interface, params):
        super().__init__(interface, params)
        self.variables = {
            'x1':0.5

        }
        
    @staticmethod
    def list_vars():
        return ['x1']
    
    @staticmethod
    def list_obses():
        return ['Q1']
    
    @staticmethod
    def get_default_params():
        return None

    def _get_vrange(self, var):
        return self.vranges[var]

    def _get_var(self, var):
        return self.variables[var]

    def _set_var(self, var, x):
        self.variables[var] = x
    
    def _get_obs(self, obs):
        if obs == 'Q1':
            #Q1 = self.interface.get_value(obs)
            return 1
        
