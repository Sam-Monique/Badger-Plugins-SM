from badger import environment
from badger.interface import Interface
from .setup import CycleMagnet, SaveIm
import subprocess
import numpy as np
import yaml
import pandas as pd
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
        self.configs = None

        self.variables = {}

        self.intial_transmission = self.params['optional_transmission']


        self.times = []



    @staticmethod
    def list_vars():
        return['b1','b2','b3','b4','b5','b6','b7','b8']
    
    @staticmethod
    def list_obses():
        return['STEERING', 'RETURN_POSITION', 'X_CENTROID']

    @staticmethod
    def get_default_params():
        return {'tunename':'','quad_config':'','viewer':'',
                 'optimal_viewer_position':[0,0], 'viewer_size':[0,0],
                   'optional_transmission':0.0, 'transmission_tolerance':0.60,
                   }
    
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
            # wait_time = CycleMagnet(var)
            # time.sleep(wait_time)

        if x > current:
            wait_time = CycleMagnet(var)
            self.times.append(wait_time)

        self.variables[var] = x
        self.interface.set_value(var,x)

    def _get_obs(self, obs):

        if len(self.times) > 0:
            time.sleep(np.max(self.times))
            self.times = []
        
        if obs == 'STEERING':
            val = self.steer()
            return val
        
        elif obs == 'RETURN_POSTION':
            optimal_x, optimal_y = self.params['viewer_position']
            x, y, _, _, _, _ = self.image_analysis()
            val = ((optimal_x - x)**2 + (optimal_y - y)**2)**(1/2)
            return val
            
        elif obs == 'X_CENTROID':
            current_x_position, _, _, _, _, _ = self.image_analysis()
            return current_x_position
        

    def set_quads(self, quad_names, quad_values):
        for channel, value in quad_names, quad_values:
            self.interface.set_value(channel,value)

    def image_analysis(self):
        '''Read in Viewer Image Info From Text File'''
        time.sleep(15)  # consider changing this delay based on how long it actually takes, better to slighlty overestimate
        array_info = np.loadtxt('/user/e20008/sam/badger_viola/viola.txt')
        return array_info
    
    # def steer(self):

    #     '''Quantifies Steering with a Combination of Quads and Values'''

    #     if self.configs == None:
    #         with open(self.params['quad_config'], "r") as stream:
    #             self.configs = yaml.safe_load(stream)
        
        
    #     quad_dic = self.configs
    #     tunename = self.params['tunename']
    #     viewer = self.params['viewer']
    #     viewer_size = self.params['viewer_size']
    #     intial_transmission = self.intial_transmission
    #     transmission_tolerance = self.params['transmission_tolerance']



    #     for quad in quad_dic.keys():
    #         self.interface.set_value(quad, quad_dic[quad]['initial'])

    #     if intial_transmission == 0:
    #         _,_,_,_,_, total_counts = self.image_analysis()
    #         intial_transmission = total_count
    #         self.intial_transmission = total_count

    #     total_steering = 0

    #     SaveIm(f'{tunename}_INITIAL', viewer)

    #     for selected_quad in quad_dic.keys():
            
             

    #         x_positions = []
    #         transmissions = []

    #         for strengths in quad_dic[selected_quad]['ranges']:

    #             self.interface.set_value(selected_quad, strengths)

    #             x, y, x_rms, y_rms, xy_col, total_count = self.image_analysis()
    #             SaveIm(f'{tunename}_{selected_quad}_{strengths}',viewer)

    #             x_positions.append(x)
    #             transmissions.append(total_count)

    #         x_diff = x_positions[1] - x_positions[0]


    #         if (transmissions[0])/(intial_transmission) < transmission_tolerance or (transmissions[1])/(intial_transmission) < transmission_tolerance:

    #             x_diff = viewer_size

    #         total_steering += (x_diff)**2        
            

            
    #         self.interface.set_value(selected_quad, quad_dic[selected_quad]['initial'])


    #     return total_steering

    def steer(self):

        if self.configs == None:
            self.configs = pd.read_csv(self.params['quad_config'])

        quad_df = self.configs
        tunename = self.params['tunename']
        viewer = self.params['viewer']
        viewer_size_x, viewer_size_y = self.params['viewer_size']
        intial_transmission = self.intial_transmission
        transmission_tolerance = self.params['transmission_tolerance']

        if intial_transmission == 0:
                _,_,_,_,_, total_counts = self.image_analysis()
                intial_transmission = total_counts
                self.intial_transmission = total_counts


        quads = quad_df.keys()
        quad_strengths = quad_df.values

        x_positions = []
        y_positions = []
        transmission = []


        for quad_values in quad_strengths:
            self.set_quads(quads, quad_values)

            x, y, x_rms, y_rms, xy_col, total_count = self.image_analysis()
            SaveIm(f'{tunename}',viewer)

            x_positions.append(x)
            y_positions.append(y)

            if total_count/intial_transmission < transmission_tolerance:
                transmission.append[1]
            else:
                transmission.append[0]



        total_steering = 0


        for i in range(len(quad_strengths)):
            for j in range(i+1, len(quad_strengths)):
                if transmission[i] == 1 or transmission[j] == 1:
                    total_steering += (viewer_size_x)**2 + (viewer_size_y)**2
                else:
                    total_steering += (x_positions[i] - x_positions[j])**2 + (y_positions[i] - y_positions[j])**2


        return total_steering

