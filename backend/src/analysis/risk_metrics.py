import numpy as np

def calculate_var(returns, confidence=0.05):
    return np.percentile(returns, confidence * 100)