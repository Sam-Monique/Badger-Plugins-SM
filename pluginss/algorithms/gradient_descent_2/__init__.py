from operator import itemgetter
import numpy as np
from gradient_descent import GradientDescent

def optimize(evaluate, params):
    learn_rate, max_iter, tol, gradient_step = itemgetter(
        'learn_rate', 'max_iter', 'tol', 'gradient_step')(params)
    
    _, _, _, x0 = evaluate(None)
    
    x_bounds = (0,1)
    x_initial = x0[0]
    D = len(x0[0])

    def gradient(x, i):

        y = _evaluate(x)
        x[i] = x[i] - gradient_step
        y_step = _evaluate(x)
        val = (y -y_step)/(gradient_step)
        
        return val

    for i in range(D):

        def _evaluate(x):
            x_initial[i] = x
            y, _, _, _ = evaluate(np.array(x_initial).reshape(1, -1))
            y = y[0]
            return y
        
        def gradient(x):
            y = _evaluate(x)
            x = x - gradient_step
            y_step = _evaluate(x)
            val = (y -y_step)/(gradient_step)
            return val

        opt = GradientDescent(_evaluate, gradient, x_initial[i], learning_rate=learn_rate, tolerance = tol, max_iterations=max_iter)
        x_new = opt.fit()

        x_initial[i] = x_new

    result,_,_,_ = evaluate(np.array(x_initial).reshape(1, -1))            
    print(result[0,0])