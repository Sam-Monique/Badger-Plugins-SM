import numpy as np
from operator import itemgetter
# from bayes_opt import BayesianOptimization
# from bayes_opt import UtilityFunction
# from bayes_opt import Events
# from bayes_opt import ConstraintModel
from .bayes.bayesian_optimization import BayesianOptimization
from .bayes.util import UtilityFunction
from .bayes.event import Events
from .bayes.constraint import ConstraintModel




def optimize(evaluate, params):
    start_from_current, random_state, init_points, n_iter, accept_val, acq_func, n_constraints = itemgetter(
        'start_from_current', 'random_state', 'init_points', 'n_iter','accept_val','acq_func','n_constraints')(params)

    _, _, _, x0 = evaluate(None)


    D = x0.shape[1]

    class InequalityTracker():
        def __init__(self):
            pass
        def update(self,values):
            self.inequalities = values
        def get(self):
            return self.inequalities
    
    IneqTrack = InequalityTracker()

    def _evaluate(**kwargs):
        var_list = [kwargs[f'v{i}'] for i in range(D)]
        X = np.array(var_list).reshape(1, -1)
        Y, I, E, _ = evaluate(X)
        IneqTrack.update(I)

        # BO assume a maximize problem
        return -Y[0,0]
    def inequalities(**kwargs):
        
        I = IneqTrack.get()
        print(I)
        if n_constraints == 1:

            return I[0,0]
        else: 
            return I[0]

    ineq_lb = [0]*n_constraints
    ineq_ub = [np.inf]*n_constraints
    constraint = ConstraintModel(
        fun=inequalities,
        lb=ineq_lb,
         ub= ineq_ub,
        )
    
    # bounds on input params
    pbounds = {}
    for i in range(D):
        pbounds[f'v{i}'] = (0, 1)
    
    if n_constraints == 0:
        opt = BayesianOptimization(
        f=_evaluate,
        pbounds=pbounds,
        random_state=False,
        verbose=0,
        allow_duplicate_points= True
        )
    else:

        opt = BayesianOptimization(
            f=_evaluate,
            pbounds=pbounds,
            constraint=constraint,
            random_state=False,
            verbose=0,
            allow_duplicate_points= True
        )

    D = len(x0[0])

    if random_state != False and random_state != 'stratified':
        rng = np.random.RandomState(seed = random_state)
        initial_p = rng.rand(init_points, D) 
        initial_p = initial_p.flatten()
        initial_p.sort()
        initial_p = initial_p[::-1]
        initial_p = initial_p.reshape(init_points, D)


    elif random_state == 'stratified':
        def initital(n):
            points = []
            for i in range(n):
                points.append(np.random.uniform(1 - (1/n)*(i+1),1 - (1/n)*(i)))
            return points
        
        initial_p = initital(init_points)

    else:
        
        initial_p = np.linspace(0,1,init_points)
        initial_p = initial_p[::-1]
        initial_p = initial_p.reshape(init_points, D)

    if start_from_current:
        initial_p[0] = x0[0]


    for p in initial_p:
        opt.probe(params=p)
    
 
    if acq_func in ['ucb','poi','ei']:
        acq = UtilityFunction(kind= acq_func)
    else:
        raise RuntimeError(f'Acquistion Function {acq_func} is not a viable option! Plese choose from ucb, poi or ei !')

    opt._prime_subscriptions()
    opt.dispatch(Events.OPTIMIZATION_START)
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
            if y > -float(accept_val):
                break


    return opt.res