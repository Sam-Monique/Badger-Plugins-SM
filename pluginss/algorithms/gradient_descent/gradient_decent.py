import numpy as np

def gradient_descent(start,f,  gradient, learn_rate, max_iter, tol=0.01):

    x = np.array(start)

    y = f(x)
    D = len(x)
    diff = np.zeros(D)

    function_evals = 1

    iterations = 0

    for _ in range(max_iter):

        y_new = y 

        for i in range(D):
            gradient_val , y_new = gradient(y_new, x,i)
            diff[i] = -learn_rate*gradient_val

            function_evals += 1

    
        if np.any(np.abs(diff)<tol):
            break    
        x +=  diff

        y = f(x)

        function_evals += 1
        iterations += 1

    print(f" Optimization Complete\n Current Function Evaluation: {y}\n Functional Evaluations: {function_evals}\n Iterations: {iterations}")