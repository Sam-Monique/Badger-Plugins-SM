from operator import itemgetter
import numpy as np
from .gradient_decent import gradient_descent

def optimize(evaluate, params):
    step_inital, max_iter, min_step = itemgetter(
        'step_inital', 'max_iter', 'min_step')(params)
    
    _, _, _, x0 = evaluate(None)
    D = x0.shape[1]    

    # for i in range(max_iter):
    #     Y, I,E, X = evaluate(x0)

    def _evaluate(x):
        y, _, _, _ = evaluate(np.array(x).reshape(1, -1))
        y = y[0]
        return y
    print(type(min_step))
    x_bounds = (0,1)
    x_initial = x0[0,0]
    print(step_inital)
    gradient_descent(_evaluate, x_bounds,x_initial, max_iter, step_inital, min_step)


            
