from operator import itemgetter
from pymoo.optimize import minimize
from pymoo.core.problem import Problem
from pymoo.algorithms.moo.sms import SMSEMOA
import numpy as np

def optimize(evaluate, params):
    pop_size, n_gen, n_obs = itemgetter(
         'pop_size', 'n_gen', 'n_obs')(params)
    
    _, _, _, x0 = evaluate(None)
   
    if n_obs == None:

        y, _, _, _ = evaluate(x0)
        n_obs = len(y[0])

    D_x = len(x0[0])
    D_y = n_obs

    def _evaluate_(x):
        y, _, _, _ = evaluate(np.array(x).reshape(1, -1))
        y = y[0]
        return y 
    

    class ProblemWrapper(Problem):
        def _evaluate(self, xs, out, *args, **kwargs):
            res = []
            for x in xs:
                res.append(_evaluate_(x))
            
            out['F'] = np.array(res)

    lb = [0]*D_x
    ub = [1]*D_x

    problem = ProblemWrapper(n_var = D_x, n_obj = D_y, xl = lb, xu = ub)

    algo = SMSEMOA(pop_size= pop_size)

    stop_crit = ('n_gen', n_gen)

    results = minimize(problem= problem, algorithm= algo, termination= stop_crit)

    return results.F
