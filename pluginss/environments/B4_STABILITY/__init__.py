from badger import environment
from badger.interface import Interface
from .setup import GetHall, CycleMagnet
import time

class Environment(environment.Environment):
    name = 'SECAR_DIPOLE_MATCH'

    vranges = {
        'b4':[0,100],
    }

    def __init__(self, interface: Interface, params):
        super().__init__(interface, params)
        self.interface.pvs = {
            'b4':'SCR_BTS35:PSD_D1557:I_CSET',
        }
        self.first = True

    @staticmethod
    def list_vars():
        return ['b4']
    
    @staticmethod
    def list_obses():
        return ['b4_hall']
    
    @staticmethod
    def get_default_params():
        return {'set_value':0, 'cycle': True}

    def _get_vrange(self, var):
        return self.vranges[var]

    def _get_var(self, var):
        val = self.interface.get_value(var)

        return val
    
    def _set_var(self, var, x):
        
        if self.first:
            if self.params['cycle']:
                self.interface.set_value(var,self.params['set_value'])

                wait_time = CycleMagnet(var)
                time.sleep(wait_time)

            self.interface.set_value(var,self.params['set_value'])
            
            self.first = False

            
    
    def _get_obs(self, obs):

        if obs == 'b4_hall':
            time.sleep(1)
            val = GetHall('b4')
            return val