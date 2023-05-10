from badger import environment
from badger.interface import Interface

class Environment(environment.Environment):
    name = 'SECAR_LIN_COMB'

    vranges = {
        'N':[-10,10]

    }

    def __init__(self, interface: Interface, params):
        super().__init__(interface, params)
        B3_init = 60.0
        B4_init = 60.0
        self.interface.set_value('SCR_BTS35:PSD_D1547:I_CSET',B3_init)
        self.interface.set_value('SCR_BTS35:PSD_D1557:I_CSET',B4_init)
        self.B3_init = B3_init
        self.B4_init = B4_init
        # or 
        self.B3_init = self.interface.get_value('SCR_BTS35:PSD_D1547:I_CSET')
        self.B4_init = self.interface.get_value('SCR_BTS35:PSD_D1557:I_CSET')

    
        
        self.variables = {
            'N':1
        }

    @staticmethod
    def list_vars():
        return ['N']
    
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
      
        B3_init = self.B4_init
        B4_init = self.B4_init
        
        if var == 'N': 
            m = 1
            setB3 = B3_init + x
            setB4 = B4_init + x*m
            self.interface.set_value('SCR_BTS35:PSD_D1547:I_CSET',setB3)
            self.interface.set_value('SCR_BTS35:PSD_D1557:I_CSET',setB4)
            self.variables[var] = x

    def _get_obs(self, obs):
        if obs == 'y1':
            
            return