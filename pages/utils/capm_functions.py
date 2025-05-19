import plotly.express as px
import numpy as np
import pandas as pd

# Function to plot interactive plot
def interactive_plot(df):
    fig = px.line()
    for i in df.columns[1:]:
        fig.add_scatter(x=df['Date'], y=df[i], name=i)
    fig.update_layout(
        width=450,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

# Normalize prices relative to first available price
def normalize(df):
    x = df.copy()
    for col in x.columns[1:]:
        x[col] = x[col] / x[col].iloc[0]
    return x

# Calculate daily returns (safe version)
def daily_return(df):
    df_daily_return = df.copy()
    numeric_cols = df_daily_return.select_dtypes(include=[np.number]).columns

    for col in numeric_cols:
        df_daily_return[col] = df_daily_return[col].pct_change()
    
    df_daily_return = df_daily_return.fillna(0)

    # Re-attach Date if not included
    if 'Date' in df.columns and 'Date' not in df_daily_return.columns:
        df_daily_return['Date'] = df['Date']

    return df_daily_return

# Calculate Beta and Alpha using linear regression
def calculate_beta(stocks_daily_return, stock):
    try:
        X = stocks_daily_return['sp500']
        Y = stocks_daily_return[stock]

        if len(X) < 2 or len(Y) < 2:
            raise ValueError("Not enough data points to calculate beta.")

        # Perform linear regression: Y = a + bX
        beta, alpha = np.polyfit(X, Y, 1)
        return beta, alpha
    except Exception as e:
        print(f"Error calculating beta: {e}")
        return np.nan, np.nan
