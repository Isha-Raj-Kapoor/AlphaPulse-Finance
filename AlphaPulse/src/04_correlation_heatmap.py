import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import LOG_RETURNS_PATH, CORRELATION_PATH

OUTPUT_CHART = 'outputs/charts/correlation_heatmap.png'

def calculate_correlation(log_returns):
    """Calculate Pearson correlation matrix between all stocks."""
    corr_matrix = log_returns.corr(method='pearson')
    corr_matrix.to_csv(CORRELATION_PATH)
    print(f"✅ Correlation matrix saved: {CORRELATION_PATH}")
    return corr_matrix

def plot_heatmap(corr_matrix):
    """Plot a styled correlation heatmap."""
    fig, ax = plt.subplots(figsize=(13, 10))
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#0d1117')

    mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)

    sns.heatmap(
        corr_matrix,
        mask=mask,
        annot=True,
        fmt='.2f',
        cmap='RdYlGn',          
        vmin=-1, vmax=1,
        center=0,
        square=True,
        linewidths=0.5,
        linecolor='#1a1a2e',
        cbar_kws={'shrink': 0.8, 'label': 'Correlation'},
        ax=ax,
        annot_kws={'size': 10, 'color': 'black', 'weight': 'bold'}
    )

    ax.set_title('Stock Correlation Heatmap\n(Green = Move Together | Red = Move Opposite)',
                 color='white', fontsize=14, pad=20)
    ax.tick_params(colors='white', labelsize=10)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)

    cbar = ax.collections[0].colorbar
    cbar.ax.yaxis.label.set_color('white')
    cbar.ax.tick_params(colors='white')

    plt.tight_layout()
    plt.savefig(OUTPUT_CHART, dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    print(f"✅ Heatmap saved: {OUTPUT_CHART}")
    plt.close()

def print_insights(corr_matrix):
    """Print the most correlated and least correlated pairs."""
    pairs = []
    stocks = corr_matrix.columns.tolist()
    for i in range(len(stocks)):
        for j in range(i+1, len(stocks)):
            pairs.append({
                'Stock A': stocks[i],
                'Stock B': stocks[j],
                'Correlation': round(corr_matrix.iloc[i, j], 4)
            })

    pairs_df = pd.DataFrame(pairs).sort_values('Correlation', ascending=False)

    print("\n--- 🔴 Most POSITIVELY Correlated (move together) ---")
    print(pairs_df.head(5).to_string(index=False))

    print("\n--- 🟢 Most NEGATIVELY Correlated (good diversification) ---")
    print(pairs_df.tail(5).to_string(index=False))

if __name__ == "__main__":
    if not os.path.exists(LOG_RETURNS_PATH):
        print("❌ Run 02_returns_calculation.py first!")
    else:
        log_returns = pd.read_csv(LOG_RETURNS_PATH, index_col=0, parse_dates=True)
        corr_matrix = calculate_correlation(log_returns)
        plot_heatmap(corr_matrix)
        print_insights(corr_matrix)
        print("\n✅ Heatmap COMPLETE! Now run: 05_rolling_volatility.py")
