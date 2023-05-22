from operator import itemgetter
import numpy as np
from .gradient_decent import gradient_descent

def optimize(evaluate, params):
    learn_rate, max_iter, tol, gradient_step = itemgetter(
        'learn_rate', 'max_iter', 'tol', 'gradient_step')(params)
    
    _, _, _, x0 = evaluate(None)
    print(evaluate(None))

    def _evaluate(x):
        y, _, _, _ = evaluate(np.array(x).reshape(1, -1))
        y = y[0]
        return y
    
    x_bounds = (0,1)
    x_initial = x0[0]
    print(x_initial)

    def gradient(y,x, i):

        x[i] = x[i] - gradient_step
        print()
        y_step = _evaluate(x)

        print(F'Function at x - gradient:{x}')

        val = (y -y_step)/(gradient_step)
        print(f"gradient: {val}")
        return val, y_step

    gradient_descent(x_initial,_evaluate, gradient, learn_rate, max_iter, tol=tol )


            
