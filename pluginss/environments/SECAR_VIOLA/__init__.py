from badger import environment
from badger.interface import Interface
from setup1 import CycleMagnet, SaveIm
import subprocess
import numpy as np
import yaml
import time

class Environment(environment.Environment):
    
    name = 'SECAR_STEERING'
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
            'b1':'SCR_BTS35:PSD_D1489:I_CSET',
            'b2':'SCR_BTS35:PSD_D1504:I_CSET',
            'b3':'SCR_BTS35:PSD_D1547:I_CSET',
            'b4':'SCR_BTS35:PSD_D1557:I_CSET',
            'b5':'SCR_BTS35:PSD_D1665:I_CSET',
            'b6':'SCR_BTS35:PSD_D1678:I_CSET',
            'b7':'SCR_BTS35:PSD_D1807:I_CSET',
            'b8':'SCR_BTS35:PSD_D1826:I_CSET',

        }
        with open(self.params['quad_config'], "r") as stream:
            self.configs = yaml.safe_load(stream)

        self.variables = {}

        self.intial_transmission = self.params['optional_transmission']


    @staticmethod
    def list_vars():
        return['b1','b2','b3','b4','b5','b6','b7','b8']
    
    @staticmethod
    def list_obses():
        return['STEERING', 'RETURN_POSITION']

    @staticmethod
    def get_default_params():
        return {'tunename':'','quad_config':'', 'viola_loc':'', 'viewer':'', 'optimal_viewer_position':0.0, 'viewer_size':0.0, 'optional_transmision':0.0}
    
    def _get_vrange(self, var):
        return self.vranges[var]

    def _get_var(self, var):
        val = self.interface.get_value(var)
        return val

    def _set_var(self, var, x):

        try:
            current = self.variable[var]
        except KeyError:
            current = x

        if x > current:
            CycleMagnet(var)

        self.variables[var] = x
        self.interface.set_value(var,x)

    def _get_obs(self, obs):
        
        if obs == 'STEERING':
            val = self.steer()
            return val
        
        elif obs == 'RETURN_POSTION':
            optimal_x_position = self.params['viewer_position']
            current_x_position, _, _, _, _, _ = self.image_analysis()
            val = (optimal_x_position - current_x_position)**2
            return val
            

        

        
    def image_analysis(self):
        time.sleep(3)
        subprocess.run(f"python badger_viola.py {self.params['viola_loc']}")
        array_info = np.loadtxt()
        return array_info
    
    def steer(self):
        
        
        quad_dic = self.configs
        tunename = self.params['tunename']
        viewer = self.params['viewer']
        viewer_size = self.params['viewer_size']
        intial_transmission = self.intial_transmission
        transmission_tolerance = 0.60



        for quad in quad_dic.keys():
            self.interface.set_value(quad, quad_dic[quad]['initial'])

        if intial_transmission == 0:
            _,_,_,_,_, total_counts = self.image_analysis()
            intial_transmission = total_count
            self.intial_transmission = total_count

        total = 0

        SaveIm(tunename, viewer)

        for selected_quad in quad_dic.keys():
            
             

            x_positions = []
            transmissions = []

            for strengths in quad_dic[selected_quad]['ranges']:
                self.interface.set_value(selected_quad, strengths)
                x, y, x_rms, y_rms, xy_col, total_count = self.image_analysis()

                x_positions.append(x)
                transmissions.append(total_count)

            x_diff = x_positions[1] - x_positions[0]


            if (transmissions[0])/(intial_transmission) < transmission_tolerance or (transmissions[1])/(intial_transmission) < transmission_tolerance:

                x_diff = viewer_size

            total += (x_diff)**2        
            

            
            self.interface.set_value(selected_quad, quad_dic[selected_quad]['initial'])


        return total

