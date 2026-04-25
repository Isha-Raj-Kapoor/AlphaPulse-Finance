import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import LOG_RETURNS_PATH, VOLATILITY_PATH, ROLLING_WINDOW, STOCKS

OUTPUT_CHART_ALL  = 'outputs/charts/rolling_volatility_all.png'
OUTPUT_CHART_GRID = 'outputs/charts/rolling_volatility_grid.png'

COLORS = ['#2196F3','#FF5252','#69FF47','#FFD700',
          '#FF6B9D','#00E5FF','#FF9800','#E040FB','#76FF03','#F50057']

def calculate_rolling_volatility(log_returns):
    """Calculate annualized 30-day rolling volatility."""
    rolling_vol = log_returns.rolling(window=ROLLING_WINDOW).std() * np.sqrt(252)
    rolling_vol.dropna(inplace=True)
    rolling_vol.to_csv(VOLATILITY_PATH)
    print(f"✅ Volatility data saved: {VOLATILITY_PATH}")
    return rolling_vol

def plot_all_together(rolling_vol):
    """Plot all stocks on one chart."""
    fig, ax = plt.subplots(figsize=(16, 7))
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#0d1117')

    for i, stock in enumerate(STOCKS):
        ax.plot(rolling_vol.index, rolling_vol[stock] * 100,
                label=stock, color=COLORS[i], linewidth=1.5, alpha=0.85)

    ax.set_title(f'{ROLLING_WINDOW}-Day Rolling Volatility — All Stocks (Annualized %)',
                 color='white', fontsize=14)
    ax.set_xlabel('Date', color='white')
    ax.set_ylabel('Annualized Volatility (%)', color='white')
    ax.tick_params(colors='white')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.xticks(rotation=45)

    for spine in ax.spines.values():
        spine.set_edgecolor('#333')

    ax.legend(facecolor='#1a1a2e', labelcolor='white', fontsize=9,
              ncol=5, loc='upper right')
    ax.grid(axis='y', color='#333', linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig(OUTPUT_CHART_ALL, dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    print(f"✅ All-stocks chart saved: {OUTPUT_CHART_ALL}")
    plt.close()

def plot_grid(rolling_vol):
    """Plot each stock separately in a 2×5 grid."""
    fig, axes = plt.subplots(2, 5, figsize=(20, 8))
    fig.patch.set_facecolor('#0d1117')
    axes_flat = axes.flatten()

    for i, stock in enumerate(STOCKS):
        ax = axes_flat[i]
        ax.set_facecolor('#111827')
        vol_pct = rolling_vol[stock] * 100
        ax.fill_between(rolling_vol.index, vol_pct, alpha=0.3, color=COLORS[i])
        ax.plot(rolling_vol.index, vol_pct, color=COLORS[i], linewidth=1.5)
        ax.set_title(stock, color='white', fontsize=12, fontweight='bold')
        ax.tick_params(colors='white', labelsize=7)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        for spine in ax.spines.values():
            spine.set_edgecolor('#333')
        ax.grid(axis='y', color='#333', linestyle='--', alpha=0.4)

        avg_vol = vol_pct.mean()
        ax.axhline(avg_vol, color='white', linewidth=0.8,
                   linestyle='--', alpha=0.6)
        ax.text(0.02, 0.95, f'Avg: {avg_vol:.1f}%',
                transform=ax.transAxes, color='white',
                fontsize=8, va='top')

    fig.suptitle(f'{ROLLING_WINDOW}-Day Rolling Volatility Grid (Annualized %)',
                 color='white', fontsize=15, y=1.01)
    plt.tight_layout()
    plt.savefig(OUTPUT_CHART_GRID, dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    print(f"✅ Grid chart saved: {OUTPUT_CHART_GRID}")
    plt.close()

def print_volatility_summary(rolling_vol):
    """Print average volatility ranking."""
    avg_vol = (rolling_vol.mean() * 100).sort_values(ascending=False)
    print("\n--- Volatility Ranking (Highest → Lowest) ---")
    for stock, vol in avg_vol.items():
        bar = '█' * int(vol / 2)
        print(f"  {stock:6s}  {vol:5.1f}%  {bar}")

if __name__ == "__main__":
    if not os.path.exists(LOG_RETURNS_PATH):
        print("❌ Run 02_returns_calculation.py first!")
    else:
        log_returns = pd.read_csv(LOG_RETURNS_PATH, index_col=0, parse_dates=True)
        rolling_vol = calculate_rolling_volatility(log_returns)
        plot_all_together(rolling_vol)
        plot_grid(rolling_vol)
        print_volatility_summary(rolling_vol)
        print("\n✅ Volatility COMPLETE! Now run: 06_var_calculation.py")
