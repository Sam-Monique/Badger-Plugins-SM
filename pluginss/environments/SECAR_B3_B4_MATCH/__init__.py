from badger import environment
from badger.interface import Interface
from .setup import GetHall, CycleMagnet, nmrRange, set_probe, tlm_reading
from epics import caput, caget
import time

class Environment(environment.Environment):
    name = 'SECAR_B3_B4_MATCH'

    vranges = {
        'b1':[0,100],
        'b2':[0,100],
        'b3':[0,100],
        'b4':[0,100],
        'b5':[0,100],
        'b6':[0,100],
        'b7':[0,100],
        'b8':[0,100],  
    }

    def __init__(self, interface: Interface, params):
        super().__init__(interface, params)
        self.interface.pvs = {
            'b3':'SCR_BTS35:PSD_D1547:I_CSET',
            'b4':'SCR_BTS35:PSD_D1557:I_CSET',
        }

        self.variables = {}

    @staticmethod
    def list_vars():
        return ['b1','b2','b3','b4','b5','b6','b7','b8']
    
    @staticmethod
    def list_obses():
        return ['B1_B2_MATCH','B3_B4_MATCH']
    
    @staticmethod
    def get_default_params():
        return {'cycle': True}

    def _get_vrange(self, var):
        return self.vranges[var]

    def _get_var(self, var):
        val = self.interface.get_value(var)

        return val
    
    def _set_var(self, var, x):

        if self.params['cycle']:
            try:
                current = self.variable[var]
            except KeyError:
                current = x
               

            if x > current:
                wait_time = CycleMagnet(var)
                time.sleep(wait_time)

        self.variables[var] = x
        self.interface.set_value(var,x)


        self.interface.set_value(var,x)
    
    def _get_obs(self, obs):

        if obs == 'B1_B2_MATCH':

            b1_probe, b2_probe = nmrRange()
            caput(set_probe, b1_probe)
            time.sleep(10)
            b1_nmr_h = caget(tlm_reading)
            #b2
            caput(set_probe, b2_probe)
            time.sleep(10)
            b2_nmr_h = caget(tlm_reading)

            cal = abs(b1_nmr_h-b2_nmr_h)**2

        elif obs == 'B3_B4_MATCH':
            # b3 = self.interface.get_value('SCR_BTS35:HAL_D1547:B_RD')
            # b4 = self.interface.get_value('SCR_BTS35:HAL_D1557:B_RD')

            b3 = GetHall('b3')
            b4 = GetHall('b4')
            val = abs(b4-b3)**2
            return val
        
        elif obs == 'B5_B6_MATCH':
            # b3 = self.interface.get_value('SCR_BTS35:HAL_D1547:B_RD')
            # b4 = self.interface.get_value('SCR_BTS35:HAL_D1557:B_RD')

            b5 = GetHall('b5')
            b6 = GetHall('b6')
            val = abs(b4-b3)**2
            return val