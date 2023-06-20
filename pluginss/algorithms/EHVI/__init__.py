from operator import itemgetter
import numpy as np

import math

import gpflow
import numpy as np
import tensorflow as tf
import trieste
from trieste.acquisition.function import ExpectedHypervolumeImprovement
from trieste.acquisition.rule import EfficientGlobalOptimization
from trieste.data import Dataset
from trieste.models import TrainableModelStack
from trieste.models.gpflow import build_gpr, GaussianProcessRegression
from trieste.space import Box, SearchSpace
from trieste.objectives.multi_objectives import MultiObjectiveTestProblem
from trieste.acquisition.multi_objective.pareto import (
    Pareto,
    get_reference_point,
)
np.random.seed(1793)
tf.random.set_seed(1793)


def optimize(evaluate, params):
    num_initial, num_samples, n_obs = itemgetter(
         'num_initial', 'num_samples', 'n_obs')(params)
    
    _, _, _, x0 = evaluate(None)
   
    if n_obs == None:
        y, _, _, _ = evaluate(x0)
        n_obs = len(y[0])

    D_x = len(x0[0])
    D_y = n_obs

    def _evaluate(xs):
        ys = np.zeros((xs.shape[0], n_obs))

        for i,x in enumerate(xs):
            
            y, _, _, _ = evaluate(np.array(x).reshape(1, -1))

            ys[i] = y
        
        return ys
    



    observer = trieste.objectives.utils.mk_observer(_evaluate)

    mins = [0]*D_x
    maxs = [1]*D_x
    search_space = Box(mins, maxs)
    num_objective = D_y

    num_initial_points = num_initial
    initial_query_points = search_space.sample(num_initial_points)
    initial_data = observer(initial_query_points)


    def build_stacked_independent_objectives_model(
        data: Dataset, num_output: int, search_space: SearchSpace
    ) -> TrainableModelStack:
        gprs = []
        for idx in range(num_output):
            single_obj_data = Dataset(
                data.query_points, tf.gather(data.observations, [idx], axis=1)
            )
            gpr = build_gpr(single_obj_data, search_space, likelihood_variance=1e-7)
            gprs.append((GaussianProcessRegression(gpr), 1))

        return TrainableModelStack(*gprs)


    model = build_stacked_independent_objectives_model(
        initial_data, num_objective, search_space
    )

    ehvi = ExpectedHypervolumeImprovement()
    rule: EfficientGlobalOptimization = EfficientGlobalOptimization(builder=ehvi)

    num_steps = num_samples
    bo = trieste.bayesian_optimizer.BayesianOptimizer(observer, search_space)
    result = bo.optimize(num_steps, initial_data, model, acquisition_rule=rule)




