import streamlit as st
import datetime
import pandas_datareader.data as web
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
from dateutil.relativedelta import relativedelta  # Import relativedelta
from pages.utils import capm_functions  # Ensure this file is working properly
from style_utils import apply_custom_style
# setting page config
st.set_page_config(
    page_title="CAPM",
    page_icon="chart_with_upwards_trend",
    layout="wide",
)

st.title('📈 Calculate Beta and Return for Individual Stock')

apply_custom_style("app.png")




# user input
col1, col2 = st.columns([1, 1])
with col1:
    stock = st.selectbox("Choose a stock", ('AAPL', 'TSLA', 'NFLX', 'MGM', 'MSFT', 'AMZN', 'NVDA', 'GOOGL'))
with col2:
    year = st.number_input("Number of Years", 1, 10)

# dates
end = datetime.date.today()
start = end - relativedelta(years=year)  # Use relativedelta to subtract years

# Load S&P 500 data using Yahoo Finance
try:
    SP500 = yf.download('^GSPC', start=start, end=end)
    SP500 = SP500[['Close']].reset_index()
    SP500.columns = ['Date', 'sp500']
except Exception as e:
    st.error(f"❌ Failed to load S&P 500 data: {e}")
    st.stop()

# Load stock data
stocks_df = yf.download(stock, start=start, end=end)

# Retry fallback if stock data is empty
if stocks_df.empty and year < 5:
    st.warning("⚠️ No data found for selected range. Retrying with 5-year range...")
    retry_start = end - relativedelta(years=5)  # Retry with 5-year range
    stocks_df = yf.download(stock, start=retry_start, end=end)

# Retry further if still empty for 10 years
if stocks_df.empty and year < 10:
    st.warning("⚠️ No data found for selected range. Retrying with 10-year range...")
    retry_start = end - relativedelta(years=10)  # Retry with 10-year range
    stocks_df = yf.download(stock, start=retry_start, end=end)

# Still empty? Stop and provide options to the user
if stocks_df.empty:
    st.error("❌ Stock data is empty. Please try a different stock or a longer time period.")
    st.warning("### You can try the following actions:")
    st.markdown("- **Try a different stock** from the list.")
    st.markdown("- **Increase the number of years** to get more data (e.g., try 5 or 10 years).")
    st.markdown("- **Ensure the stock is actively traded** (i.e., data availability from Yahoo Finance).")
    st.stop()

# Clean and merge data
stocks_df = stocks_df[['Close']]
stocks_df.columns = [f'{stock}']
stocks_df.reset_index(inplace=True)
stocks_df['Date'] = pd.to_datetime(stocks_df['Date'].astype(str).str[:10])
SP500['Date'] = pd.to_datetime(SP500['Date'])

merged_df = pd.merge(stocks_df, SP500, on='Date', how='inner')

# Check for valid merged data
if merged_df.empty:
    st.error("❌ No overlapping data found between stock and S&P 500.")
    st.stop()

# Daily return function
def daily_return(df):
    df_return = df.copy()
    numeric_cols = df_return.select_dtypes(include=[np.number]).columns

    for col in numeric_cols:
        df_return[col] = df_return[col].pct_change()
    
    df_return = df_return.fillna(0)

    # Re-attach Date if not included
    if 'Date' in df.columns and 'Date' not in df_return.columns:
        df_return['Date'] = df['Date']

    return df_return

# Calculate daily returns
stocks_daily_return = daily_return(merged_df)

# Check if valid returns exist
if stocks_daily_return[[stock, 'sp500']].dropna().shape[0] < 2:
    st.error("❌ Not enough valid return data to calculate Beta.")
    st.stop()

# Market return (annualized)
rm = stocks_daily_return['sp500'].mean() * 252

# Calculate Beta and Alpha using the provided capm function
beta, alpha = capm_functions.calculate_beta(stocks_daily_return, stock)

# Risk-free rate
rf = 0

# Expected return based on CAPM
return_value = round(rf + beta * (rm - rf), 2)

# Results
st.markdown(f'### 🧮 Beta: `{round(beta, 4)}`')
st.markdown(f'### 💰 Expected Return: `{return_value * 100:.2f}%`')

# Scatter Plot showing stock vs. S&P 500
fig = px.scatter(stocks_daily_return, x='sp500', y=stock, title=f'{stock} vs S&P 500')
fig.add_scatter(
    x=stocks_daily_return['sp500'],
    y=beta * stocks_daily_return['sp500'] + alpha,
    name='Expected Return Line',
    line=dict(color='crimson')
)
st.plotly_chart(fig, use_container_width=True)
