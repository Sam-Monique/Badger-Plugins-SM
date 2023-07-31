from badger import environment
from badger.interface import Interface
from .setup import SaveIm, GetHall, nmrRange, set_probe, tlm_reading
from .cycle import CycleMagnet
from epics import caput, caget
from check_stability import check_stabilities
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

        self.intial_transmission = None

        self.nmr = {}

        self.nmr_loc = None


        self.times = []



    @staticmethod
    def list_vars():
        return['b1','b2','b3','b4','b5','b6','b7','b8']
    
    @staticmethod
    def list_obses():
        return['STEERING', 'RETURN_POSITION', 'X_CENTROID', 'Y_CENTROID','b1_nmr','b2_nmr','b3_hall','b4_hall','b5_hall','b6_hall','b7_hall','b8_hall' ]

    @staticmethod
    def get_default_params():
        return {'tunename':'','quad_config':'','viewer':'',
                 'optimal_viewer_position':[0,0], 'viewer_size':[0,0],
                   'optional_transmission':0.0, 'transmission_tolerance':0.60,
                   'nmr_location':''
                   }
    
    def _get_vrange(self, var):
        return self.vranges[var]

    def _get_var(self, var):
        try:
            val = self.variables[var]
        except KeyError:
            val = self.interface.get_value(var)
        return val

    def _set_var(self, var, x):

        try:
            current = self.variable[var]
        except KeyError:
            current = x


        if x > current:
            wait_time = CycleMagnet(var)
            self.times.append(wait_time)
        else:
            self.times.append(0)

        self.variables[var] = x

    def _get_obs(self, obs):

        if self.intial_transmission is None:
            self.params['optional_transmission']

        if self.nmr_loc is None:
            self.params['nmr_location']
        if len(self.times) > 0:
            time.sleep(np.max(self.times))
            self.times = []
        
            for dipole in self.variables:
                self.interface.set_value(dipole,self.variables[dipole])

            if 'b1' and 'b2' not in self.variables:
                check_stabilities(self.variables, )

            elif 'b1' and 'b2' in self.variables:
                
                b1_probe, b2_probe = nmrRange()

                if self.nmr_loc == 'b1':
                    check_stabilities(['b1'])
                    self.nmr['b1'] = caget(tlm_reading)
                    caput(set_probe, b2_probe)
                    time.sleep(10)
                    check_stabilities(['b2'])
                    self.nmr['b2'] = caget(tlm_reading)
                    self.nmr_loc = 'b2'

                else:
                    check_stabilities(['b2'])
                    self.nmr['b2'] = caget(tlm_reading)
                    caput(set_probe, b1_probe)
                    time.sleep(10)
                    check_stabilities(['b1'])
                    self.nmr['b1'] = caget(tlm_reading)
                    self.nmr_loc = 'b1'

            else:
                b1_probe, b2_probe = nmrRange()

                if 'b1' in self.variables:
                    if self.nmr_loc == 'b1':
                        check_stabilities(['b1'])
                        self.nmr['b1'] = caget(tlm_reading)
                        if 'b2' not in self.nmr:
                            caput(set_probe, b2_probe)
                            time.sleep(10)
                            self.nmr['b2'] = caget(tlm_reading)
                            self.nmr_loc = 'b2'

                    else:
                        self.nmr['b2'] = caget(tlm_reading)
                        caput(set_probe, b1_probe)
                        time.sleep(10)
                        check_stabilities(['b1'])
                        self.nmr['b1'] = caget(tlm_reading)
                        self.nmr_loc = 'b1'
                
                elif 'b2' in self.variables:
                    if self.nmr_loc == 'b1':
                        self.nmr['b1'] = caget(tlm_reading)
                        caput(set_probe, b2_probe)
                        time.sleep(10)
                        check_stabilities(['b2'])
                        self.nmr['b2'] = caget(tlm_reading)
                        self.nmr_loc = 'b2'

                    else:
                        check_stabilities(['b2'])
                        self.nmr['b2'] = caget(tlm_reading)
                        if 'b1' not in self.nmr:
                            caput(set_probe, b1_probe)
                            time.sleep(10)
                            self.nmr['b1'] = caget(tlm_reading)
                            self.nmr_loc = 'b1'
        
        if obs == 'STEERING':
            val = self.steer()
            return val
        elif obs == 'STEERING_X':
            val = self.steer(dim= 'X')
            return val
        elif obs == 'STEERING_Y':
            val = self.steer(dim = 'Y')
            return val
        
        elif obs == 'RETURN_POSTION':
            optimal_x, optimal_y = self.params['viewer_position']
            x, y, _, _, _, _ = self.image_analysis()
            val = ((optimal_x - x)**2 + (optimal_y - y)**2)**(1/2)
            return val
            
        elif obs == 'X_CENTROID':
            x, _, _, _, _, _ = self.image_analysis()
            return x
        
        elif obs == 'Y_CENTROID':
            _, y, _, _, _, _ = self.image_analysis()
            return y
        
        elif obs.split(sep= '_')[1] == 'hall':
            val = GetHall(obs.split(sep= '_')[0])
            return val

        elif obs.split(sep= '_')[1] == 'nmr':

            try:
                val = self.nmr[obs.split(sep='_')[0]]
            except KeyError:
                if obs.split(sep='_')[0] != self.nmr_loc:

                    b1_probe, b2_probe = nmrRange()
                    if obs.split(sep='_')[0] == 'b1':
                        caput(set_probe, b1_probe)
                    else:
                        caput(set_probe, b2_probe)

                    time.sleep(10)
                val = caget(tlm_reading)
            return val
        

        

        

    def set_quads(self, quad_names, quad_values):
        for channel, value in zip(quad_names, quad_values):
            self.interface.set_value(channel,value)

    def image_analysis(self, wait_period = 0):
        '''Read in Viewer Image Info From Text File'''
        time.sleep(wait_period)  # consider changing this delay based on how long it actually takes, better to slighlty overestimate
        array_info = np.loadtxt('/user/e20008/sam/badger_viola/viola.txt')
        return array_info
    


    def steer(self, dim = 'Abs'):

        if self.configs is None:
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


        quads = list(quad_df.keys())
        quad_strengths = quad_df.values

        x_positions = []
        y_positions = []
        transmission = []


        for quad_values in quad_strengths:
            self.set_quads(quads, quad_values)

            x, y, x_rms, y_rms, xy_col, total_count = self.image_analysis(wait_period = 10)
            SaveIm(f'{tunename}',viewer)

            x_positions.append(x)
            y_positions.append(y)

            if total_count/intial_transmission < transmission_tolerance:
                transmission.append[1]
            else:
                transmission.append[0]

            if total_count > self.intial_transmission:
                self.intial_transmission = total_count



        total_steering = 0

        if dim == 'X':
            viewer_size_y = 0
            y_positions = np.zeros(len(y_positions))

        if dim == 'Y':
            viewer_size_x = 0
            x_positions = np.zeros(len(x_positions))



        for i in range(len(quad_strengths)):
            for j in range(i+1, len(quad_strengths)):
                if sum(transmission) > 0:
                    total_steering += (viewer_size_x)**2 + (viewer_size_y)**2
                else:
                    total_steering += (x_positions[i] - x_positions[j])**2 + (y_positions[i] - y_positions[j])**2


        return total_steering



