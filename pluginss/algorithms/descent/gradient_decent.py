def gradient_descent(f,x_bounds, x_initial, max_iter,step_initial,  min_step):

    inputs = [x_initial]
    outputs = [f(x_initial)]

    step = step_initial
    x = x_initial

    for i in range(max_iter):

        if x - step >= x_bounds[0]:
            x = x -step
        else:
            x = x_bounds[0]


        y = f(x)

        outputs.append(y)
        inputs.append(x)
        if y > outputs[i]:
            step = step/2
            if step < min_step:
                break
            else:
                x = inputs[i-1] + step

            if x > x_bounds[1]:
                x = x_bounds[1]
        