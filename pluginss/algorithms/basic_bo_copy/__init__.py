import numpy as np
from operator import itemgetter
from bayes_opt import BayesianOptimization
from bayes_opt import UtilityFunction
from bayes_opt import Events

def optimize(evaluate, params):
    start_from_current, random_state, init_points, n_iter, accept_val = itemgetter(
        'start_from_current', 'random_state', 'init_points', 'n_iter','accept_val')(params)

    _, _, _, x0 = evaluate(None)
    D = x0.shape[1]

    def _evaluate(**kwargs):
        var_list = [kwargs[f'v{i}'] for i in range(D)]
        X = np.array(var_list).reshape(1, -1)
        Y, _, _, _ = evaluate(X)


        # BO assume a maximize problem
        return -Y[0,0]

    # bounds on input params
    pbounds = {}
    for i in range(D):
        pbounds[f'v{i}'] = (0, 1)
        
    opt = BayesianOptimization(
        f=_evaluate,
        pbounds=pbounds,
        random_state=random_state,
        verbose=0,
        allow_duplicate_points= True
    )

    # _init_points = init_points
    D = len(x0[0])

    rng = np.random.RandomState(seed = random_state)
    initial_p = rng.rand(init_points, D) 
    initial_p = initial_p.flatten()
    initial_p.sort()
    initial_p = initial_p[::-1]
    initial_p = initial_p.reshape(init_points, D)

    # if start_from_current:
    #     opt.probe(params=x0[0], lazy=True)
    #     _init_points -= 1

    if start_from_current:
        initial_p[0] = x0[0]
    
    for p in initial_p:
        opt.probe(params=p)
    


    acq = UtilityFunction(kind= 'ucb')

    # optimizer.maximize(
    #     init_points=_init_points,
    #     n_iter=n_iter,
    #     acquisition_function= acq
    # )

    opt._prime_subscriptions()
    opt.dispatch(Events.OPTIMIZATION_START)
    # opt._prime_queue(init_points)
    iteration = 0
    while not opt._queue.empty or iteration < n_iter:
        try:
            x_probe = next(opt._queue)
        except StopIteration:
            acq.update_params()
            x_probe = opt.suggest(acq)
            iteration += 1
        opt.probe(x_probe, lazy=False)
        y = opt.res[-1]['target']
        if accept_val != None:
            if y > -accept_val:
                break