from operator import itemgetter
import numpy as np
from .gradient_decent import gradient_descent

def optimize(evaluate, params):
    step_inital, max_iter, min_step = itemgetter(
        'step_inital', 'max_iter', 'min_step')(params)
    
    _, _, _, x0 = evaluate(None)


    def _evaluate(x):
        y, _, _, _ = evaluate(np.array(x).reshape(1, -1))
        y = y[0]
        return y
    
    x_bounds = (0,1)
    x_initial = x0[0,0]
    
    gradient_descent(_evaluate, x_bounds,x_initial, max_iter, step_inital, min_step)


            
