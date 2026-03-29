import pandas as pd
from backend.src.analysis.returns import calculate_returns


def test_returns():
    data = pd.DataFrame({"A": [1, 2, 3, 4]})
    returns = calculate_returns(data)
    assert not returns.empty