from badger import environment
from badger.interface import Interface
from .setup import SaveIm
import subprocess

class Environment(environment.Environment):
    
    name = 'viewer_image'
    vranges = {
        'x1':[0,1],
    }

    def __init__(self, interface: Interface, params):
        super().__init__(interface, params)
        self.variables = {
            'x1':0
        }
    @staticmethod
    def list_vars():
        return['x1']
    
    @staticmethod
    def list_obses():
        return['D1515','D1542','D1638','D1688','D1783','D1836','D1879']

    @staticmethod
    def get_default_params():
        return {'tunename':'','dx':0.0,'dy':0.0}
    
    def _get_vrange(self, var):
        return self.vranges[var]

    def _get_var(self, var):
        val = self.variables[var]
        return val

    def _set_var(self, var, x):
        self.variables[var] = x

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
        