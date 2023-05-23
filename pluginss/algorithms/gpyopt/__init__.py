from operator import itemgetter
import numpy as np
from GPyOpt.methods import BayesianOptimization
def optimize(evaluate, params):
    max_iter = itemgetter(
         'max_iter',)(params)
    

    def _evaluate(x):
        y, _, _, _ = evaluate(np.array(x).reshape(1, -1))
        y = y[0,0]
        return y
    
    _,_,_,x0 = evaluate(None)

    D = len(x0[0])

    bound = []

    for i in range(D):
        dict = {}
        dict['name'] = f"var_{i+1}"
        dict['type'] = 'discrete'
        dict['domain'] = (0,1)

    opt = BayesianOptimization(_evaluate, domain = bound)

    opt.run_optimization(max_iter=max_iter)