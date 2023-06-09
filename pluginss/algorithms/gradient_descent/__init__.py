from operator import itemgetter
import numpy as np
from .gradient.gradient_decent import gradient_descent

def optimize(evaluate, params):
    learn_rate, max_iter, tol, gradient_step = itemgetter(
        'learn_rate', 'max_iter', 'tol', 'gradient_step')(params)
    print(learn_rate, max_iter, tol, gradient_step)
    _, _, _, x0 = evaluate(None)

    def _evaluate(x):
        y, _, _, _ = evaluate(np.array(x).reshape(1, -1))
        y = y[0]
        return y
    
    x_bounds = (0,1)
    x_initial = x0[0]

    def gradient(y,x, i):

        x[i] = x[i] - gradient_step
        y_step = _evaluate(x)
        val = (y -y_step)/(gradient_step)
        
        return val, y_step

    results = gradient_descent(x_initial,_evaluate, gradient, learn_rate, max_iter, tol=tol )
    return results

            
