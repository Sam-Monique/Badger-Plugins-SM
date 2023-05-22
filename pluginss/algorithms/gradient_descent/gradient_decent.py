import numpy as np

def gradient_descent(start,f,  gradient, learn_rate, max_iter, tol=0.01):

    x = np.array(start)
    print(F'x: {x}')
    y = f(x)
    print(f'x is {x}, {start}')
    D = len(x)
    diff = np.zeros(D)


    for _ in range(max_iter):
        print(F"Iteration: {_+1}")

        y_new = y 

        for i in range(D):
            gradient_val , y_new = gradient(y_new, x,i)

            diff[i] = -learn_rate*gradient_val
            # x+= diff
            print(i+1)

        
        print(diff)
        if np.any(np.abs(diff)<tol):
            break    
        x +=  diff

        y = f(x)