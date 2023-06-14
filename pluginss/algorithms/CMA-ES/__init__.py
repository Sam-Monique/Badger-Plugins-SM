from operator import itemgetter
from cmaes import CMA
import numpy as np
import os

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

def optimize(evaluate, params):
    n_gen, pop_size = itemgetter(
         'n_gen', 'pop_size')(params)
    

    _,_,_, x0 = evaluate(None)

    D = len(x0[0])
    
    n_dim = D

    if D == 1:
        n_dim = 2

    def _evaluate(x):
        y, _, _, _ = evaluate(np.array(x).reshape(1, -1))
        y = y[0]
        return y
    
    vbounds = np.array([[0,1]*n_dim]).reshape(D,2)
   

    optimizer = CMA(mean=np.ones(n_dim)*0.5, sigma=0.1, bounds= vbounds, population_size= pop_size )

    for generation in range(n_gen):
        solutions = []

        for _ in range(optimizer.population_size):
            x = optimizer.ask()

            if D == 1:
                value = _evaluate(x[0])
            else:
                value = _evaluate(x)

            solutions.append((x, value))

        optimizer.tell(solutions)


