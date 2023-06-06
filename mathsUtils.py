def derivative_3_data(normalised_timestamp_acc, x_accel, y_accel, z_accel):
    x_derivative = []
    y_derivative = []
    z_derivative = []
    t_i = normalised_timestamp_acc[0]
    for i in range(1, len(normalised_timestamp_acc)):
        t_i1 = normalised_timestamp_acc[i]
        a_x = (x_accel[i] - x_accel[i-1]) / (t_i1 - t_i)
        a_y = (y_accel[i] - y_accel[i-1]) / (t_i1 - t_i)
        a_z = (z_accel[i] - z_accel[i-1]) / (t_i1 - t_i)
        x_derivative.append(a_x)
        y_derivative.append(a_y)
        z_derivative.append(a_z)
        t_i = t_i1

    x_derivative.append(x_derivative[-1])
    y_derivative.append(y_derivative[-1])
    z_derivative.append(z_derivative[-1])

    return x_derivative, y_derivative, z_derivative

def derivative(normalised_timestamp_acc, x_accel):
    x_derivative = []
    t_i = normalised_timestamp_acc[0]
    for i in range(1, len(normalised_timestamp_acc)):
        t_i1 = normalised_timestamp_acc[i]
        a_x = (x_accel[i] - x_accel[i-1]) / (t_i1 - t_i)
        x_derivative.append(a_x)
        t_i = t_i1

    x_derivative.append(x_derivative[-1])

    return x_derivative