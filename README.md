# AlphaPulse — Investment Risk & Volatility Monitor
**Zaalima Development Pvt. Ltd | Internship Project 2**

---

## What This Project Does
AlphaPulse is a financial analytics tool that:
- Downloads real stock market data (10 stocks across 5 sectors)
- Calculates daily log returns and volatility
- Runs **10,000 Monte Carlo simulations** to forecast portfolio risk
- Generates **correlation heatmaps** between stocks
- Calculates **Value at Risk (VaR)** and **Max Drawdown**
- Exports everything to **Tableau** for interactive dashboards

---

## Setup

### 1. Install Python packages
```bash
pip install -r requirements.txt
```

### 2. Run scripts IN ORDER
```bash
python src/01_data_collection.py
python src/02_returns_calculation.py
python src/03_monte_carlo.py
python src/04_correlation_heatmap.py
python src/05_rolling_volatility.py
python src/06_var_calculation.py
```

---

## Project Structure
```
AlphaPulse/
├── config.py                    ← Change stocks/dates here
├── requirements.txt
├── src/
│   ├── 01_data_collection.py    ← Week 1
│   ├── 02_returns_calculation.py← Week 2
│   ├── 03_monte_carlo.py        ← Week 2
│   ├── 04_correlation_heatmap.py← Week 3
│   ├── 05_rolling_volatility.py ← Week 3
│   └── 06_var_calculation.py    ← Week 4
├── data/
│   ├── raw/                     ← Downloaded stock prices
│   ├── processed/               ← Calculated metrics
│   └── exports/                 ← Tableau-ready CSV
└── outputs/
    ├── charts/                  ← All generated charts
    └── reports/                 ← Final summary report
```

---

## Key Concepts
| Term | Simple Explanation |
|------|--------------------|
| **Log Return** | Daily % change in stock price |
| **Monte Carlo** | Run 10,000 random future scenarios |
| **VaR (95%)** | "I'm 95% sure I won't lose more than X% today" |
| **Max Drawdown** | Biggest loss from peak to bottom |
| **Sharpe Ratio** | How much return you get per unit of risk |
| **Correlation** | Do two stocks move together or opposite? |

---

*Confidential — Zaalima Development Pvt. Ltd*
