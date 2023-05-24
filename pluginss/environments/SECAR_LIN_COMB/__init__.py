from badger import environment
from badger.interface import Interface
import yaml

class Environment(environment.Environment):
    name = 'SECAR_LIN_COMB'

    vranges = {
        'm1':[-1,1],
        'm2':[-1,1],

    }

    def __init__(self, interface: Interface, params):
        super().__init__(interface, params)

        self.interface.pvs = {
        'q1':'SCR_BTS35:PSQ_D1475:I_CSET',
        'q2':'SCR_BTS35:PSQ_D1479:I_CSET',
        'q3':'SCR_BTS35:PSQ_D1525:I_CSET',
        'q4':'SCR_BTS35:PSQ_D1532:I_CSET',
        'q5':'SCR_BTS35:PSQ_D1538:I_CSET',
        'q6':'SCR_BTS35:PSQ_D1572:I_CSET',
        'q7':'SCR_BTS35:PSQ_D1578:I_CSET',
        'q8':'SCR_BTS35:PSQ_D1648:I_CSET',
        'q9':'SCR_BTS35:PSQ_D1655:I_CSET',
        'q10':'SCR_BTS35:PSQ_D1692:I_CSET',
        'q11':'SCR_BTS35:PSQ_D1701:I_CSET',
        'q12':'SCR_BTS35:PSQ_D1787:I_CSET',
        'q13':'SCR_BTS35:PSQ_D1793:I_CSET',
        'q14':'SCR_BTS35:PSQ_D1842:I_CSET',
        'q15':'SCR_BTS35:PSQ_D1850:I_CSET',

        }
        
        self.variables = {
            'm1':0,
            'm2':0,
        }

    @staticmethod
    def list_vars():
        return ['m1','m2', 'm3', 'm4']
    
    @staticmethod
    def list_obses():
        return ['X_BEAM_SPOT_SIZE_FP2','X_BEAM_SPOT_SIZE_FP2','FC_INTENSITY_FP4']
    
    @staticmethod
    def get_default_params():
        return {'PCA',''}

    def _get_vrange(self, var):
        return self.vranges[var]

    def _get_var(self, var):     
        return self.variables[var]
    
    def _set_var(self, var, x):

        if self.configs == None:
            with open(self.params['PCA'], "r") as stream:
                self.configs = yaml.safe_load(stream)

        num = var[-1]
        pca = f"p{num}"

        PCA = self.configs[pca]

        for quad in PCA.keys():
            val = PCA[quad]['Q_i'] + x*PCA[quad]['b']
            self.interface.set_value(quad, val)
        

    def _get_obs(self, obs):
        
        if obs == 'X_BEAM_SPOT_SIZE_FP2':
            return 0
        elif obs == 'X_BEAM_SPOT_SIZE_FP3':
            return 0

        elif obs == 'FC_INTENSITY_FP4':
            return 0
        