from badger import environment
from badger.interface import Interface
import numpy as np
import os
import pandas as pd
import yaml

class Environment(environment.Environment):
    name = 'SECAR_COSY'

    vranges = {
        'Q1':[0.95,1.05],
        'Q2':[0.95,1.05],
        'HEX1':[0.95,1.05],
        'Q3':[0.8,1.2],
        'Q4':[0.8,1.2],
        'Q5':[0.8,1.2],
        'HEX2':[0.95,1.05],
        'Q6':[0.95,1.05],
        'Q7':[0.95,1.05],
        'HEX3':[0.95,1.05],
        'OCT1':[0.95,1.05],
        'Q8':[0.95,1.05],
        'Q9':[0.95,1.05],
        'Q10':[0.95,1.05],
        'Q11':[0.95,1.05],
        'Q12':[0.95,1.05],
        'Q13':[0.95,1.05],
        'Q14':[0.95,1.05],
        'Q15':[0,2],
         'B1':[0.5,1.5],
         'B2':[0.5,1.5],
         'Q1_Q2':[-1,1],
         'Q1_Q2_Q3':[0.5,1.5],
         'm1':[-1,1],
         'dx':[-10,10]
     }

    def __init__(self, interface: Interface, params):
        super().__init__(interface, params)

        same = False
        if same:
            self.interface.path = os.getcwd() + '/'
        else:
            self.interface.path = '/Users/sam/Documents/GitHub/Badger-Plugins-SM/pluginss/'

        self.interface.file = 'SECAR_GammaOptics'
        
        self.interface.settings = {
            'Q1':(237,'M5'),
            'Q2':(251,'MQ'),
            'HEX1':(300,'MH'),
            'Q3':(314,'MQ'),
            'Q4':(328,'M5'),
            'Q5':(342,'MQ'),
            'HEX2':(385,'M5'),
            'Q6':(400,'MQ'),
            'Q7':(416,'MQ'),
            'HEX3':(452,'M5'),
            'OCT1':(466,'M5'),
            'Q8':(495,'M5'),
            'Q9':(509,'M5'),
            'Q10':(533,'M5'),
            'Q11':(547,'M5'),
            'Q12':(592,'MQ'),
            'Q13':(594,'MQ'),
            'Q14':(606,'MQ'),
            'Q15':(608,'MQ'),
            'B1':(271,'MC'),
            'B2':(285,'MC')
        }
        
        self.interface.set_temp_file()
        self.variables = {
            'Q1_Q2': 0,
            'Q1_Q2_Q3':1,
            'm1':0,
            'dx':0,
        }
        self.configs = None
        
    @staticmethod
    def list_vars():
        return ['Q1','Q2','HEX1','Q3','Q4','Q5','HEX1','Q6','Q7','HEX3','OCT1','Q8','Q9','Q10','Q11','Q12','Q13','Q14','Q15','B1','B2','Q1_Q2','Q1_Q2_Q3','m1', 'dx']
    
    @staticmethod
    def list_obses():
        return ['BEAM_SIZE_X_FP1','BEAM_SIZE_Y_FP1','BEAM_SIZE_X_FP2','BEAM_SIZE_Y_FP2','BEAM_SIZE_X_FP3','BEAM_SIZE_Y_FP3','BEAM_SIZE_X_FP4','BEAM_SIZE_Y_FP4','DIS_FP1','B2_B1_RATIO','STEER', 'TRANSMISSION_DSSD']
    
    @staticmethod
    def get_default_params():
        return None

    def _get_vrange(self, var):
        return self.vranges[var]

    def _get_var(self, var):

      
        if var in self.interface.settings.keys():

            return self.interface.get_value(var)

        elif var in self.variables.keys():
            return self.variables[var]



    def _set_var(self, var, x):

    
        if var in self.interface.settings.keys():

            self.interface.set_value(var,x)
        elif var =='Q1_Q2':
            m = 1.5
            N = x
            Q1 = 1 + N
            self.interface.set_value('Q1',Q1)
            Q2 = 1 + N*m
            self.interface.set_value('Q2',Q2)
            self.variables[var] = x
        elif var == 'Q1_Q2_Q3':
            A = np.array([1,1,1])
            A = A*x

            self.interface.set_value('Q1',A[0])
            self.interface.set_value('Q2',A[1])
            self.interface.set_value('Q3',A[2])
            self.variables[var] = x
        elif var == 'dx':
            self.interface.set_beam_offset(dx = x)
            self.variables[var] = x
        else:
            if self.configs is None:
                with open('/Users/sam/Documents/GitHub/Badger-Plugins-SM/pluginss/configs.yaml', "r") as stream:
                    self.configs = yaml.safe_load(stream)

            num = var[-1]
            pca = f"p{num}"

            PCA = self.configs[pca]

            for quad in PCA.keys():
                val = PCA[quad]['Q_i'] + x*PCA[quad]['b']
                self.interface.set_value(quad, val)

            self.variables[var] = x

    
    def _get_obs(self, obs):

        if obs == 'BEAM_SIZE_X_FP1':
            self.interface.run()
            val = self.interface.get_value(obs)
            return val
        elif obs == 'BEAM_SIZE_Y_FP1':
            self.interface.run()
            val = self.interface.get_value(obs)
            return val
        elif obs == 'BEAM_SIZE_X_FP2':
            self.interface.run()
            val = self.interface.get_value(obs)
            return val
        elif obs == 'BEAM_SIZE_Y_FP2':
            self.interface.run()
            val = self.interface.get_value(obs)
            return val
        elif obs == 'BEAM_SIZE_X_FP3':
            self.interface.run()
            val = self.interface.get_value(obs)
            return val
        elif obs == 'BEAM_SIZE_Y_FP3':
            self.interface.run()
            val = self.interface.get_value(obs)
            return val
        elif obs == 'BEAM_SIZE_X_FP4':
            self.interface.run()
            val = self.interface.get_value(obs)
            return val
        elif obs == 'BEAM_SIZE_Y_FP4':
            self.interface.run()
            val = self.interface.get_value(obs)
            return val
        elif obs == 'DIS_FP1':
            self.interface.run()
            x = self.interface.get_value('X_DIS')
            y = self.interface.get_value('Y_DIS')
            val = (x**2 + y**2)
            return val

        elif obs == 'B2_B1_RATIO':
            B1 = self.interface.get_value('B1')
            B2 = self.interface.get_value('B2')
            val = B2/B1
            return val
        
        elif obs == 'STEER':
            val = self.steer()
            return val
        
            
    
        
        elif obs == 'TRANSMISSION_DSSD':
            self.interface.run()
            val = self.interface.get_value('TRANSMISSION_DSSD')
            return val
        

    def set_quads(self, quad_names, quad_values):
            print(quad_names, quad_values)
            for channel, value in zip(quad_names, quad_values):
                self.interface.set_value(channel,value)

    def steer(self):

            if self.configs is None:
                self.configs = pd.read_csv('/Users/sam/Documents/GitHub/Badger-Plugins-SM/pluginss/pracitce.csv')

            quad_df = self.configs





            quads = list(quad_df.keys())
            quad_strengths = quad_df.values

            x_positions = []
            y_positions = []


            for quad_values in quad_strengths:
                self.set_quads(quads, quad_values)

                self.interface.run()
                x = self.interface.get_value('FC_X_DIS')
                y = self.interface.get_value('FC_Y_DIS')


                x_positions.append(x)
                y_positions.append(y)





            total_steering = 0


            for i in range(len(quad_strengths)):
                for j in range(i+1, len(quad_strengths)):

                    print(i,j)
                    print(x_positions[i], x_positions[j], y_positions[i], y_positions[j])
                    print((x_positions[i] - x_positions[j])**2 + (y_positions[i] - y_positions[j])**2)
                    total_steering += (x_positions[i] - x_positions[j])**2 + (y_positions[i] - y_positions[j])**2


            return total_steering