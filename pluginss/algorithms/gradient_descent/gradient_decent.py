import numpy as np

def gradient_descent(start,f,  gradient, learn_rate, max_iter, tol=0.01):

    x = start
    print(F'x: {x}')
    y = f(x)

    for _ in range(max_iter):
        print(F"Iteration: {_+1}")
        diff = -learn_rate*gradient(y,x)

        if np.abs(diff)<tol:
            break    
        x +=  diff

        y = f(x)