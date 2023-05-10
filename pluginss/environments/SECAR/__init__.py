from badger import environment
from badger.interface import Interface


class Environment(environment.Environment):
    
    name = 'SECAR'
    vranges = {
        'Q1':[0,100],
        'Q2':[0,100],
        'Q3':[0,100],
        'Q4':[0,100],
        'Q5':[0,100],
        'Q6':[0,100],
        'Q7':[0,100],
        'Q8':[0,100],
        'Q9':[0,100],
        'Q10':[0,100],
        'Q11':[0,100],
        'Q12':[0,100],
        'Q13':[0,100],
        'Q14':[0,100],
        'Q15':[0,100],
        'B1':[0,100],
        'B2':[0,100],
        'B3':[0,100],
        'B4':[0,100],
        'B5':[0,100],
        'B6':[0,100],
        'B7':[0,100],
        'B8':[0,100],
        'H1':[0,100],
        'H2':[0,100],
        'H3':[0,100],
        'O1':[0,100],

    }

    def __init__(self, interface: Interface, params):
        super().__init__(interface, params)
        self.interface.pvs = {
            'Q1':'SCR_BTS35:PSQ_D1475:I_CSET',
            'Q2':'SCR_BTS35:PSQ_D1479:I_CSET',
            'Q3':'SCR_BTS35:PSQ_D1525:I_CSET',
            'Q4':'SCR_BTS35:PSQ_D1532:I_CSET',
            'Q5':'SCR_BTS35:PSQ_D1538:I_CSET',
            'Q6':'SCR_BTS35:PSQ_D1572:I_CSET',
            'Q7':'SCR_BTS35:PSQ_D1578:I_CSET',
            'Q8':'SCR_BTS35:PSQ_D1648:I_CSET',
            'Q9':'SCR_BTS35:PSQ_D1655:I_CSET',
            'Q10':'SCR_BTS35:PSQ_D1692:I_CSET',
            'Q11':'SCR_BTS35:PSQ_D1701:I_CSET',
            'Q12':'SCR_BTS35:PSQ_D1787:I_CSET',
            'Q13':'SCR_BTS35:PSQ_D1793:I_CSET',
            'Q14':'SCR_BTS35:PSQ_D1842:I_CSET',
            'Q15':'SCR_BTS35:PSQ_D1850:I_CSET',
            'B1':'SCR_BTS35:PSD_D1489:I_CSET',
            'B2':'SCR_BTS35:PSD_D1504:I_CSET',
            'B3':'SCR_BTS35:PSD_D1547:I_CSET',
            'B4':'SCR_BTS35:PSD_D1557:I_CSET',
            'B5':'SCR_BTS35:PSD_D1665:I_CSET',
            'B6':'SCR_BTS35:PSD_D1678:I_CSET',
            'B7':'SCR_BTS35:PSD_D1807:I_CSET',
            'B8':'SCR_BTS35:PSD_D1826:I_CSET',
            'H1':'SCR_BTS35:PSS_D1519:I_CSET',
            'H2':'SCR_BTS35:PSS_D1564:I_CSET',
            'H3':'SCR_BTS35:PSS_D1614:I_CSET',
            'O1':'SCR_BTS35:PSO_D1620:I_CSET',

        }

    @staticmethod
    def list_vars():
        return['Q1','Q2','Q3','Q4','Q5','Q6','Q7','Q8','Q9','Q10','Q11','Q12','Q13','Q14','Q15','B1','B2','B3','B4','B5','B6','B7','B8','H1','H2','H3','O1']
    
    @staticmethod
    def list_obses():
        return['B3_B4_MATCH']

    @staticmethod
    def get_default_params():
        return {'tunename':'','dx':0.0,'dy':0.0}
    
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