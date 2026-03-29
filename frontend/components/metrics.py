import numpy as np


def get_metrics(mc):
    return {
        "avg_return": round(mc["Return"].mean(), 4),
        "avg_risk": round(mc["Risk"].mean(), 4),
        "var_5": round(np.percentile(mc["Return"], 5), 4),
    }