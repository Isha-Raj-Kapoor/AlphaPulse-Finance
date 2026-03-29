import numpy as np

def monte_carlo_simulation(returns, simulations=5000, days=252):
    mean = returns.mean()
    cov = returns.cov()

    results = []

    for _ in range(simulations):
        weights = np.random.random(len(mean))
        weights /= weights.sum()

        ret = (mean @ weights) * days
        risk = np.sqrt(weights.T @ cov @ weights) * np.sqrt(days)

        results.append([ret, risk])

    return np.array(results)