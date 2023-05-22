from operator import itemgetter
import numpy as np
import optuna as opt

def optimize(evaluate, params):
    max_iter = itemgetter(
         'max_iter',)(params)
    

    def _evaluate(x):
        y, _, _, _ = evaluate(np.array(x).reshape(1, -1))
        y = y[0]
        return y
    
    def objective(trial):
        x = trial.suggest_float('x', 0, 1)
        return _evaluate(x)

    study = opt.create_study()
    study.optimize(objective, n_trials=max_iter)

