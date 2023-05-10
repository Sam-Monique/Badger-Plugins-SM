from badger import environment
from badger.interface import Interface
from .setup import SaveIm
import pandas as pd
import subprocess

class Environment(environment.Environment):
    
    name = 'SECAR_STEERING'
    vranges = {
        'B1':[0,100],
        'B2':[0,100],
        'B3':[0,100],
        'B4':[0,100],
        'B5':[0,100],
        'B6':[0,100],
        'B7':[0,100],
        'B8':[0,100],

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

        }

    @staticmethod
    def list_vars():
        return['B1','B2','B3','B4','B5','B6','B7','B8']
    
    @staticmethod
    def list_obses():
        return['D1515','D1542','D1638','D1688','D1783','D1836','D1879']

    @staticmethod
    def get_default_params():
        return {'tunename':'','dx':0.0,'dy':0.0,'quad_config':' '}
    
    def _get_vrange(self, var):
        return self.vranges[var]

    def _get_var(self, var):
        val = self.interface.get_value(var)
        return val

    def _set_var(self, var, x):
        self.interface.set_value(var,x)

    def _get_obs(self, obs):
        
        if obs == 'D1515':
            val = self.find_offset(obs)
            return val
        
        elif obs == 'D1542':
            val = self.find_offset(obs)
            return val
        
        elif obs == 'D1638':
            val = self.find_offset(obs)
            return val
        
        elif obs == 'D1688':
            val = self.find_offset(obs)
            return val
        
        elif obs == 'D1783':
            val = self.find_offset(obs)
            return val
        
        elif obs == 'D1836':
            val = self.find_offset(obs)
            return val
        
        elif obs == 'D1879':
            val = self.find_offset(obs)
            return val
        
        elif obs == 'D1515':
            val = self.steer('D1515')
            return val
        

    def get_offset(self,obs):

        path_to_image_analysis = 'C:/Users/sam/viewer-image-analysis/src/im_analysis.py'
        path_to_images = 'C:/Users/sam/viewer-image-analysis/D1542_images/2_22_images/'
        tunename = self.params['tunename']
        file_name = SaveIm(tunename,obs)
        output = subprocess.run([f'python3 {path_to_image_analysis} {path_to_images}{file_name}.tiff {obs}'],stdout=subprocess.PIPE)
        text  = output.stdout       
        nums = text.split()[-4:]
        nums = [float(s) for s in nums]
        return nums 
        
    def find_offset(self,obs):
        dx = self.params['dx']
        dy = self.params['dy']

        xdot,ydot,x,y = self.get_offset(obs)
        val = ((x - xdot-dx)**2+(y-ydot-dy)**2)**(0.5)
        return val
    
    def steer(self,viewer):
        
        config_file = self.params['quad_config']
        df = pd.read_csv(config_file)
        intials = {}

        for key in df.keys():
            intials[key] = self.interface.get_value(key)

        p_i = self.get_obs('DIS_FP1')

        total  = 0

        total  = 0
        for i in range(df.shape[0]):
            for key in df.keys():
                self.interface.set_value(key,df.iloc[i][key])
            p ,_ ,_ ,_ = self.get_offset(viewer)

            total += abs(p_i - p)

        for key in df.keys():
            self.interface.set_value(key,intials[key])

        return total
