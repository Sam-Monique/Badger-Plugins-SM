from badger import environment
from badger.interface import Interface
from .setup import SaveIm
import subprocess

class Environment(environment.Environment):
    
    name = 'viewer_image'
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
        return {'tunename':'','dx':0.0,'dy':0.0}
    
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
        

    def find_offset(self,obs):

        path_to_image_analysis = 'C:/Users/sam/viewer-image-analysis/src/im_analysis.py'
        path_to_images = 'C:/Users/sam/viewer-image-analysis/D1542_images/2_22_images/'
        tunename = self.params['tunename']
        dx = self.params['dx']
        dy = self.params['dy']


        file_name = SaveIm(tunename,obs)
        output = subprocess.run([f'python3 {path_to_image_analysis} {path_to_images}{file_name}.tiff {obs}'],stdout=subprocess.PIPE)
        text  = output.stdout       
        nums = text.split()[-4:]
        nums = [float(s) for s in nums]
        xdot,ydot,x,y = nums
        val = ((x - xdot-dx)**2+(y-ydot-dy)**2)**(0.5)
        return val
        '''
        if obs == 'D1542':
            
            file_name = SaveIm(tunename,obs)
            # output = subprocess.run(['powershell','-Command','python '+path_to_image_analysis+ ' '+path_to_images+'D1542_2_22_17_34_Q1_half_Q2-5_nom_B1-B2_tuned_048.tiff D1542'],stdout=subprocess.PIPE)
            # output = subprocess.run(['powershell','-Command',f'python {path_to_image_analysis} {path_to_images}D1542_2_22_17_34_Q1_half_Q2-5_nom_B1-B2_tuned_048.tiff {obs}'],stdout=subprocess.PIPE)
            output = subprocess.run(['powershell','-Command',f'python {path_to_image_analysis} {path_to_images}{file_name}.tiff {obs}'],stdout=subprocess.PIPE)

            text  = output.stdout
            nums = text.split()[-4:]
            nums = [float(s) for s in nums]
            xdot,ydot,x,y = nums

            val = ((x - xdot-dx)**2+(y-ydot-dy)**2)**(0.5)
            return val
            '''
        '''
        elif obs == 'D1542':
            
            file_name = SaveIm(tunename,obs)
            output = subprocess.run(['powershell','-Command',f'python {path_to_image_analysis} {path_to_images}{file_name}.tiff {obs}'],stdout=subprocess.PIPE)
            text  = output.stdout
            nums = text.split()[-4:]
            nums = [float(s) for s in nums]
            xdot,ydot,x,y = nums
            val = ((x - xdot)**2+(y-ydot)**2)**(0.5)
            return val
        elif obs == 'D1542':
            
            file_name = SaveIm(tunename,obs)
            output = subprocess.run(['powershell','-Command',f'python {path_to_image_analysis} {path_to_images}{file_name}.tiff {obs}'],stdout=subprocess.PIPE)
            text  = output.stdout
            nums = text.split()[-4:]
            nums = [float(s) for s in nums]
            xdot,ydot,x,y = nums
            val = ((x - xdot)**2+(y-ydot)**2)**(0.5)
            return val
        
        elif obs == 'D1542':
            
            file_name = SaveIm(tunename,obs)
            output = subprocess.run(['powershell','-Command',f'python {path_to_image_analysis} {path_to_images}{file_name}.tiff {obs}'],stdout=subprocess.PIPE)
            text  = output.stdout
            nums = text.split()[-4:]
            nums = [float(s) for s in nums]
            xdot,ydot,x,y = nums
            val = ((x - xdot)**2+(y-ydot)**2)**(0.5)
            return val
        '''
