import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os, sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (LOG_RETURNS_PATH, RAW_DATA_PATH,
                    CONFIDENCE_LEVEL, SUMMARY_REPORT_PATH, STOCKS)

OUTPUT_CHART = 'outputs/charts/var_comparison.png'
COLORS = ['#2196F3','#FF5252','#69FF47','#FFD700',
          '#FF6B9D','#00E5FF','#FF9800','#E040FB','#76FF03','#F50057']

def calculate_historical_var(log_returns, confidence=0.95):
    """
    Historical VaR — uses actual past return distribution.
    More realistic than Monte Carlo for short-term risk.
    """
    percentile = (1 - confidence) * 100
    var_values = {}
    for stock in STOCKS:
        var_1day = np.percentile(log_returns[stock], percentile)
        var_values[stock] = round(abs(var_1day) * 100, 4)
    return var_values

def calculate_max_drawdown(close_prices):
    """
    Max Drawdown — biggest peak-to-trough loss in the period.
    Key metric for understanding worst-case loss.
    """
    drawdowns = {}
    for stock in STOCKS:
        prices = close_prices[stock].dropna()
        rolling_max = prices.cummax()
        drawdown = (prices - rolling_max) / rolling_max
        max_dd = drawdown.min()
        drawdowns[stock] = round(abs(max_dd) * 100, 2)
    return drawdowns

def calculate_sharpe_ratio(log_returns, risk_free_rate=0.05):
    """
    Sharpe Ratio — return per unit of risk.
    Higher = better risk-adjusted return.
    Risk-free rate: 5% (approx US Treasury rate)
    """
    sharpe = {}
    daily_rf = risk_free_rate / 252
    for stock in STOCKS:
        excess_return = log_returns[stock].mean() - daily_rf
        sharpe[stock] = round((excess_return / log_returns[stock].std()) * np.sqrt(252), 4)
    return sharpe

def plot_var_comparison(var_values, max_drawdowns):
    """Bar chart comparing VaR and Max Drawdown per stock."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    fig.patch.set_facecolor('#0d1117')

    stocks = list(var_values.keys())
    var_vals = list(var_values.values())
    dd_vals  = [max_drawdowns[s] for s in stocks]

    ax1.set_facecolor('#111827')
    bars = ax1.bar(stocks, var_vals, color=COLORS, alpha=0.85, edgecolor='none')
    ax1.set_title('1-Day Historical VaR (95%)', color='white', fontsize=13)
    ax1.set_ylabel('Potential Daily Loss (%)', color='white')
    ax1.tick_params(colors='white')
    ax1.set_xticks(range(len(stocks)))
    ax1.set_xticklabels(stocks, rotation=45, ha='right')
    for spine in ax1.spines.values(): spine.set_edgecolor('#333')
    for bar, val in zip(bars, var_vals):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                 f'{val:.2f}%', ha='center', va='bottom', color='white', fontsize=9)

    ax2.set_facecolor('#111827')
    bars2 = ax2.bar(stocks, dd_vals, color=COLORS, alpha=0.85, edgecolor='none')
    ax2.set_title('Maximum Drawdown (%)', color='white', fontsize=13)
    ax2.set_ylabel('Peak-to-Trough Loss (%)', color='white')
    ax2.tick_params(colors='white')
    ax1.set_xticks(range(len(stocks)))
    ax1.set_xticklabels(stocks, rotation=45, ha='right')
    for spine in ax2.spines.values(): spine.set_edgecolor('#333')
    for bar, val in zip(bars2, dd_vals):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                 f'{val:.1f}%', ha='center', va='bottom', color='white', fontsize=9)

    plt.tight_layout()
    plt.savefig(OUTPUT_CHART, dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    print(f"✅ VaR chart saved: {OUTPUT_CHART}")
    plt.close()

def save_final_report(var_values, max_drawdowns, sharpe_ratios, log_returns):
    """Save a text summary report."""
    now = datetime.now().strftime('%Y-%m-%d %H:%M')

    lines = [
        "=" * 60,
        "   ALPHAPULSE — INVESTMENT RISK SUMMARY REPORT",
        f"   Generated: {now}",
        "=" * 60,
        "",
        f"{'Stock':<8} {'VaR 95% (1D)':<16} {'Max Drawdown':<16} {'Sharpe Ratio':<14}",
        "-" * 55,
    ]

    for stock in STOCKS:
        lines.append(
            f"{stock:<8} {var_values[stock]:>8.2f}%         "
            f"{max_drawdowns[stock]:>8.2f}%         "
            f"{sharpe_ratios[stock]:>8.4f}"
        )

    lines += [
        "",
        "=" * 60,
        "LEGEND:",
        "  VaR 95% (1D) : Maximum expected daily loss 95% of the time",
        "  Max Drawdown  : Worst peak-to-trough loss in the period",
        "  Sharpe Ratio  : Return per unit of risk (>1 = good, >2 = great)",
        "=" * 60,
    ]

    report = "\n".join(lines)
    with open(SUMMARY_REPORT_PATH, 'w') as f:
        f.write(report)

    print(f"\n✅ Report saved: {SUMMARY_REPORT_PATH}")
    print("\n" + report)

if __name__ == "__main__":
    missing = [p for p in [LOG_RETURNS_PATH, RAW_DATA_PATH]
               if not os.path.exists(p)]
    if missing:
        print(f"❌ Missing files: {missing}")
        print("💡 Run scripts 01 → 05 first!")
    else:
        log_returns  = pd.read_csv(LOG_RETURNS_PATH, index_col=0, parse_dates=True)
        close_prices = pd.read_csv(RAW_DATA_PATH,    index_col=0, parse_dates=True)

        var_values    = calculate_historical_var(log_returns, CONFIDENCE_LEVEL)
        max_drawdowns = calculate_max_drawdown(close_prices)
        sharpe_ratios = calculate_sharpe_ratio(log_returns)

        plot_var_comparison(var_values, max_drawdowns)
        save_final_report(var_values, max_drawdowns, sharpe_ratios, log_returns)

        print("\n🎉 ALL DONE! Your AlphaPulse project is complete!")
        print("📊 Import CSV files from data/exports/ into Tableau.")
        print("🖼️  Charts are in outputs/charts/")
