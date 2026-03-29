import numpy as np

def calculate_returns(data):
    returns = np.log(data / data.shift(1))
    return returns.dropna()