from badger import environment
from badger.interface import Interface

class Environment(environment.Environment):
    name = 'SECAR_TEST_SET'

    vranges = {
        'B4:SET':[0,100]

    }

    def __init__(self, interface: Interface, params):
        super().__init__(interface, params)
        self.interface.pvs = {
            'B4:SET':'SCR_BTS35:PSD_D1557:I_CSET'
        }

    @staticmethod
    def list_vars():
        return ['B4:SET']
    
    @staticmethod
    def list_obses():
        return ['B3_B4_MATCH']
    
    @staticmethod
    def get_default_params():
        return None

    def _get_vrange(self, var):
        return self.vranges[var]

    def _get_var(self, var):
        val = self.interface.get_value(var)

        return val
    
    def _set_var(self, var, x):
        self.interface.set_value(var,x)
    
    def _get_obs(self, obs):
        if obs == 'B3_B4_MATCH':
            B3 = self.interface.get_value('SCR_BTS35:HAL_D1547:B_RD')
            B4 = self.interface.get_value('SCR_BTS35:HAL_D1557:B_RD')
            val = abs(B4-B3)
            return val