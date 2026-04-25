import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (LOG_RETURNS_PATH, MONTE_CARLO_RUNS,
                    FORECAST_DAYS, CONFIDENCE_LEVEL, STOCKS)

OUTPUT_CHART = 'outputs/charts/monte_carlo_distribution.png'
OUTPUT_PATHS = 'outputs/charts/monte_carlo_paths.png'

def run_monte_carlo(log_returns, stock='AAPL'):
    """
    Run Monte Carlo simulation for a single stock.
    Returns simulated final prices after FORECAST_DAYS.
    """
    returns = log_returns[stock]
    mean    = returns.mean()
    std     = returns.std()
    last_price = 100  

    print(f"\n🎲 Running {MONTE_CARLO_RUNS:,} simulations for {stock}...")
    print(f"   Mean daily return : {mean:.6f}")
    print(f"   Daily volatility  : {std:.6f}")

    all_paths = np.zeros((MONTE_CARLO_RUNS, FORECAST_DAYS))

    for i in range(MONTE_CARLO_RUNS):
        daily_returns = np.random.normal(mean, std, FORECAST_DAYS)
        price_path = last_price * np.exp(np.cumsum(daily_returns))
        all_paths[i] = price_path

    return all_paths

def calculate_var(final_prices, confidence=0.95):
    """Calculate Value at Risk (VaR)."""
    percentile = (1 - confidence) * 100
    var_price   = np.percentile(final_prices, percentile)
    var_loss    = 100 - var_price    
    return var_price, var_loss

def plot_distribution(final_prices, stock, var_price):
    """Plot the bell-shaped distribution of final prices."""
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#0d1117')

    ax.hist(final_prices, bins=100, color='#2196F3', alpha=0.7,
            edgecolor='none', density=True)

    ax.axvline(var_price, color='#FF5252', linewidth=2,
               label=f'95% VaR — ${var_price:.2f}')

    median = np.median(final_prices)
    ax.axvline(median, color='#69FF47', linewidth=2, linestyle='--',
               label=f'Median — ${median:.2f}')

    ax.set_title(f'Monte Carlo Distribution — {stock} ({MONTE_CARLO_RUNS:,} simulations)',
                 color='white', fontsize=14, pad=15)
    ax.set_xlabel('Portfolio Value after 1 Year (Starting $100)', color='white')
    ax.set_ylabel('Probability Density', color='white')
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_edgecolor('#333')
    ax.legend(facecolor='#1a1a2e', labelcolor='white', fontsize=11)

    plt.tight_layout()
    plt.savefig(OUTPUT_CHART, dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    print(f"✅ Distribution chart saved: {OUTPUT_CHART}")
    plt.close()

def plot_paths(all_paths, stock):
    """Plot 200 sample simulation paths."""
    fig, ax = plt.subplots(figsize=(14, 6))
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#0d1117')

    sample_idx = np.random.choice(MONTE_CARLO_RUNS, 200, replace=False)
    for i in sample_idx:
        ax.plot(all_paths[i], color='#2196F3', alpha=0.05, linewidth=0.8)

    mean_path = all_paths.mean(axis=0)
    ax.plot(mean_path, color='#FFD700', linewidth=2, label='Mean Path')

    ax.set_title(f'Monte Carlo Paths — {stock} (200 of {MONTE_CARLO_RUNS:,} shown)',
                 color='white', fontsize=14)
    ax.set_xlabel('Trading Days', color='white')
    ax.set_ylabel('Portfolio Value ($)', color='white')
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_edgecolor('#333')
    ax.legend(facecolor='#1a1a2e', labelcolor='white')

    plt.tight_layout()
    plt.savefig(OUTPUT_PATHS, dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    print(f"✅ Paths chart saved: {OUTPUT_PATHS}")
    plt.close()

if __name__ == "__main__":
    if not os.path.exists(LOG_RETURNS_PATH):
        print("❌ Run 02_returns_calculation.py first!")
    else:
        log_returns = pd.read_csv(LOG_RETURNS_PATH, index_col=0, parse_dates=True)

        results = {}
        for stock in STOCKS:
            all_paths   = run_monte_carlo(log_returns, stock)
            final_prices = all_paths[:, -1]       
            var_price, var_loss = calculate_var(final_prices, CONFIDENCE_LEVEL)

            results[stock] = {
                'VaR_95_Price' : round(var_price, 2),
                'VaR_95_Loss%' : round(var_loss,  2),
                'Median_Price' : round(np.median(final_prices), 2),
                'Best_Case'    : round(np.percentile(final_prices, 95), 2),
                'Worst_Case'   : round(np.percentile(final_prices, 5),  2),
            }

            print(f"   ✅ {stock} — VaR Loss: {var_loss:.2f}% | Median Final: ${np.median(final_prices):.2f}")

        all_paths_aapl = run_monte_carlo(log_returns, 'AAPL')
        plot_distribution(all_paths_aapl[:, -1], 'AAPL',
                          calculate_var(all_paths_aapl[:, -1])[0])
        plot_paths(all_paths_aapl, 'AAPL')

        print("\n--- Monte Carlo Results Summary ---")
        summary = pd.DataFrame(results).T
        print(summary.to_string())

        print("\n✅ Monte Carlo COMPLETE! Now run: 04_correlation_heatmap.py")
