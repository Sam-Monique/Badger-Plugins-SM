import numpy as np

# def gradient_descent(start,f,  gradient, learn_rate, max_iter, tol=0.01):

#     x = np.array(start)

#     y = f(x)
#     D = len(x)
#     diff = np.zeros(D)

#     function_evals = 1

#     iterations = 0

#     for _ in range(max_iter):

#         y_new = y 

#         for i in range(D):
#             gradient_val , y_new = gradient(y_new, x,i)
#             diff[i] = -learn_rate*gradient_val

#             if diff[i] < -0.5 or diff[i] > 0.5:
#                 learn_rate = np.abs(0.25/gradient_val)
#                 diff[i] = np.sign(0.25)

#             function_evals += 1

    
#         if np.any(np.abs(diff)<tol):
#             break    
#         x +=  diff

#         y = f(x)

#         function_evals += 1
#         iterations += 1

#     print(f" Optimization Complete\n Current Function Evaluation: {y[0]}\n Functional Evaluations: {function_evals}\n Iterations: {iterations}")
def gradient_descent(start,f,  gradient, initial_step, max_iter, tol=0.01):

    x_list = []
    y_list = []
    x = np.array(start)

    y = f(x)

    x_list.append(x)
    y_list.append(y)
    
    D = len(x)
    diff = np.zeros(D)
    learn_rates = np.zeros(D)

    function_evals = 1

    iterations = 0


    for _ in range(max_iter):

        y_new = y 

        for i in range(D):
            gradient_val , y_new = gradient(y_new, x,i)
            if _ == 0:
                learn_rate = abs(initial_step/gradient_val)
                
            diff[i] = -learn_rate*gradient_val


            function_evals += 1

    
        if np.any(np.abs(diff)<tol):
            break    
        x +=  diff

        y = f(x)
        x_list.append(x)
        y_list.append(y)
        
        function_evals += 1
        iterations += 1

    print(f" Optimization Complete\n Current Function Evaluation: {y[0]}\n Functional Evaluations: {function_evals}\n Iterations: {iterations}")

    return x_list, y_list