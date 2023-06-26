from operator import itemgetter
import numpy as np
def optimize(evaluate, params):

    # _,_,_,x0 = evaluate(None)

    while True:
        evaluate(np.array([0.5]).reshape(-1,1))
