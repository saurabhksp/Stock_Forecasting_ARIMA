import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import datetime
import ta
from pages.utils.plotly_figure import plotly_table, close_chart, candlestick, RSI, Moving_average, MACD
from style_utils import apply_custom_style
# Set Streamlit page config
st.set_page_config(
    page_title="Stock Analysis",
    page_icon="📈",
    layout="wide",
)
st.title("📊 Stock Analysis")
apply_custom_style("app.png")


# Currency selector
currency = st.selectbox("Display Currency", ["INR", "USD", "EUR"])
    
# Get conversion rates
def get_conversion_rate(from_currency, to_currency):
    if from_currency == to_currency:
        return 1.0
    try:
        ticker = f"{from_currency}{to_currency}=X"
        fx = yf.Ticker(ticker)
        rate = fx.history(period="1d")["Close"].iloc[-1]
        return float(rate)
    except:
        return 1.0

currency_symbol = {"USD": "$", "INR": "₹", "EUR": "€"}[currency]

# Get conversion rate
native_currency = "USD"  # For foreign tickers like AAPL or GOOG
conversion_rate = get_conversion_rate(native_currency, currency)

# Show exchange rate if conversion was applied
if conversion_rate != 1.0:
    st.info(f"💱 Converted from {native_currency} to {currency} @ {conversion_rate:,.2f}")



# Input form
col1, col2, col3 = st.columns(3)
today = datetime.date.today()

with col1:
    ticker = st.text_input('Stock Ticker', 'AAPL')
with col2:
    start_date = st.date_input("Start Date", datetime.date(today.year - 1, today.month, today.day))
with col3:
    end_date = st.date_input("End Date", datetime.date(today.year, today.month, today.day))

st.subheader(ticker)

# Load Stock Info
try:
    stock = yf.Ticker(ticker)
    try:
        info = stock.get_info()  # New method (if using recent yfinance)
    except:
        info = stock.info        # Fallback for older versions

    summary = info.get("longBusinessSummary")
    sector = info.get("sector")
    employees = info.get("fullTimeEmployees")
    website = info.get("website")

    st.write(summary if summary else "📌 Summary not available for this ticker.")
    st.write("**Sector:**", sector or "N/A")
    st.write("**Full Time Employees:**", employees or "N/A")
    st.write("**Website:**", website or "N/A")

except Exception as e:
    st.error(f"Couldn't load stock info: {e}")

# Metrics tables
try:
    col1, col2 = st.columns(2)
    with col1:
        df = pd.DataFrame(index=['Market Cap', 'Beta', 'EPS', 'PE Ratio'])
        df[''] = [
            info.get("marketCap", "N/A"),
            info.get("beta", "N/A"),
            info.get("trailingEps", "N/A"),
            info.get("trailingPE", "N/A")
        ]
        st.plotly_chart(plotly_table(df), use_container_width=True)
    with col2:
        df = pd.DataFrame(index=['Quick Ratio', 'Revenue per Share', 'Profit Margins', 'Debt to Equity', 'Return on Equity'])
        df[''] = [
            info.get("quickRatio", "N/A"),
            info.get("revenuePerShare", "N/A"),
            info.get("profitMargins", "N/A"),
            info.get("debtToEquity", "N/A"),
            info.get("returnOnEquity", "N/A")
        ]
        st.plotly_chart(plotly_table(df), use_container_width=True)
except Exception as e:
    st.error(f"Error loading metrics: {e}")

# Get USD to INR conversion rate
def get_usd_to_inr():
    try:
        fx = yf.Ticker("USDINR=X")
        rate = fx.history(period="1d")["Close"].iloc[-1]
        return rate
    except:
        return 1

is_foreign = not ticker.endswith(".NS")
usd_to_inr = get_usd_to_inr() if is_foreign else 1

# Historical price data
data = yf.download(ticker, start=start_date, end=end_date)

if data.empty:
    st.warning(f"No data found for **{ticker}** between {start_date} and {end_date}. Please check the ticker or dates.")
    st.stop()
else:
    # Convert to INR if foreign ticker
    columns_to_convert = [col for col in ['Open', 'High', 'Low', 'Close', 'Adj Close'] if col in data.columns]
    data[columns_to_convert] = data[columns_to_convert] * usd_to_inr

    col1, col2, col3 = st.columns(3)
    last_close = float(data['Close'].iloc[-1])
    prev_close = float(data['Close'].iloc[-2])
    daily_change = last_close - prev_close
    col1.metric("Daily Change (INR)", f"₹{round(last_close, 2)}", f"₹{round(daily_change, 2)}")

    data.index = [str(i)[:10] for i in data.index]
    st.write('##### Historical Data (Last 10 days)')
    st.plotly_chart(plotly_table(data.tail(10).sort_index(ascending=False).round(3)), use_container_width=True)

# Styling
st.markdown("""<hr style="height:2px;border:none;color:#0078ff;background-color:#0078ff;" /> """, unsafe_allow_html=True)
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #e1efff;
        color: black;
    }
    div.stButton > button:hover {
        background-color: #0078ff;
        color: white;
    }
    </style>""", unsafe_allow_html=True)

# Time Period Buttons
col_buttons = st.columns(12)
period_buttons = ['5d', '1mo', '6mo', 'ytd', '1y', '5y', 'max']
period_labels = ['5D', '1M', '6M', 'YTD', '1Y', '5Y', 'MAX']
selected_period = ''

for i, label in enumerate(period_labels):
    with col_buttons[i]:
        if st.button(label):
            selected_period = period_buttons[i]

# Chart + Indicator
col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    chart_type = st.selectbox('', ('Candle', 'Line'))
with col2:
    indicators = st.selectbox('', ('RSI', 'Moving Average', 'MACD'))

# Load price data
chart_data = yf.Ticker(ticker).history(period='max')

# Convert to INR if needed
columns_to_convert = [col for col in ['Open', 'High', 'Low', 'Close', 'Adj Close'] if col in chart_data.columns]
if is_foreign:
    chart_data[columns_to_convert] = chart_data[columns_to_convert] * usd_to_inr

# Set period
period = selected_period if selected_period else '1y'

# Display charts
if chart_type == 'Candle':
    st.plotly_chart(candlestick(chart_data, period), use_container_width=True)
else:
    st.plotly_chart(close_chart(chart_data, period), use_container_width=True)

# Display indicators
if indicators == 'RSI':
    st.plotly_chart(RSI(chart_data, period), use_container_width=True)
elif indicators == 'MACD':
    st.plotly_chart(MACD(chart_data, period), use_container_width=True)
elif indicators == 'Moving Average':
    st.plotly_chart(Moving_average(chart_data, period), use_container_width=True)

