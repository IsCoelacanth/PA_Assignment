def scaler(x):
    m = min(x)
    M = max(x)
    for i in range(len(x)):
        x[i] = (x[i] - m)/(M-m)
    return x