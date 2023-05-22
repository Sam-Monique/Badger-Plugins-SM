from operator import itemgetter
import numpy as np
from skopt import gp_minimize

def optimize(evaluate, params):
    max_iter = itemgetter(
         'max_iter',)(params)
    

    def _evaluate(x):
        y, _, _, _ = evaluate(np.array(x).reshape(1, -1))
        y = y[0,0]
        return y
    
    _,_,_,x0 = evaluate(None)

    D = len(x0[0])

    space = [(0,1)]*D

    gp_minimize(_evaluate, space, n_calls= max_iter, n_initial_points= 5)
