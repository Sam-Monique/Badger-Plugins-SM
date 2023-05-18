def gradient_descent(f,x_bounds, x_initial, max_iter,step_initial,  min_step):

    inputs = [x_initial]
    outputs = [f(x_initial)]

    step = step_initial
    x = x_initial
    cycle_tally = 0
    for i in range(max_iter):

        if x - step >= x_bounds[0]:
            x = x -step
        else:
            x = x_bounds[0]

        if x > inputs[i]:
            cycle_tally += 1

        y = f(x)

        outputs.append(y)
        inputs.append(x)
        if y > outputs[i]:
            step = step/2
            if step < min_step:
                break
            else:
                x = inputs[i-1] + 2*step

            if x > x_bounds[1]:
                x = x_bounds[1]
        