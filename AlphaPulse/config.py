STOCKS = [
    'AAPL', 'MSFT', 'GOOGL',   
    'JPM',  'BAC',              
    'JNJ',  'PFE',              
    'XOM',  'CVX',              
    'AMZN'                      
]

START_DATE = '2023-01-01'
END_DATE   = '2025-01-01'

MONTE_CARLO_RUNS  = 10000
FORECAST_DAYS     = 252        

CONFIDENCE_LEVEL  = 0.95       
ROLLING_WINDOW    = 30         

RAW_DATA_PATH         = 'data/raw/stock_data.csv'
LOG_RETURNS_PATH      = 'data/processed/log_returns.csv'
VOLATILITY_PATH       = 'data/processed/rolling_volatility.csv'
CORRELATION_PATH      = 'data/processed/correlation_matrix.csv'
TABLEAU_EXPORT_PATH   = 'data/exports/tableau_export.csv'
SUMMARY_REPORT_PATH   = 'outputs/reports/summary_metrics.txt'
