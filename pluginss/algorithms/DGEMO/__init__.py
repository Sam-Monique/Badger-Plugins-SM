from operator import itemgetter
import numpy as np
from pyGPGO.surrogates.GaussianProcess import GaussianProcess
from pyGPGO.acquisition import Acquisition
from pyGPGO.covfunc import squaredExponential
from pyGPGO.GPGO import GPGO
def optimize(evaluate, params):
    pop_size, n_gen, n_obs = itemgetter(
         'pop_size', 'n_gen', 'n_obs')(params)
    
    _, _, _, x0 = evaluate(None)
   
    if n_obs == None:
        print(x0)
        y, _, _, _ = evaluate(x0)
        n_obs = len(y[0])

    D_x = len(x0[0])
    D_y = n_obs

    def _evaluate(x):
        print(x)
        y, _, _, _ = evaluate(np.array(x).reshape(1, -1))
        y = y[0]
        return y 
    


    # Define the bounds of the search space
    bounds = []
    for i in range(D_x):
        bounds.append({'name': f'x{i}', 'type': 'continuous', 'domain': (0, 1)})

    bounds = {'name': f'x', 'type': 'continuous', 'domain': (0, 1)}

    # Initialize the Gaussian Process and Acquisition function
    cov_func = squaredExponential()
    gp = GaussianProcess(cov_func)
    acquisition_func = Acquisition(mode='ExpectedImprovement')

    # Initialize the DGEMO algorithm
    dgemoo = GPGO(gp, acquisition_func, _evaluate, bounds)






