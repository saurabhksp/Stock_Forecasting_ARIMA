import streamlit as st
import pandas_datareader.data as web
import datetime
import pandas as pd
import yfinance as yf
from pages.utils import capm_functions
from dateutil.relativedelta import relativedelta  # Import relativedelta
from style_utils import apply_custom_style
# setting page config
st.set_page_config(
    page_title="Calculate Beta",
    page_icon="chart_with_upwards_trend",
    layout="wide",
)

st.title('Capital Asset Pricing Model 📈')
apply_custom_style("app.png")


# getting input from user
col1, col2 = st.columns([1, 1])
with col1:
    stocks_list = st.multiselect("Choose 4 Stocks", 
        ('TSLA', 'AAPL', 'NFLX', 'MGM', 'MSFT', 'AMZN', 'NVDA', 'GOOGL'),
        ['TSLA', 'AAPL', 'MSFT', 'NFLX'],
        key="stock_list"
    )
with col2:
    year = st.number_input("Number of Years", 1, 10)

try:
    # downloading data for SP500
    end = datetime.date.today()
    start = end - relativedelta(years=year)  # Use relativedelta to subtract years from the current date

    SP500 = web.DataReader('SP500', 'fred', start, end)

    if SP500.empty:
        st.error("S&P 500 data could not be loaded.")
        st.stop()

    SP500.reset_index(inplace=True)
    SP500.columns = ['Date', 'sp500']

    st.write(f"SP500 data from {start} to {end}:")
    st.write(SP500.head())

    stocks_df = pd.DataFrame()
    for stock in stocks_list:
        try:
            data = yf.download(stock, start=start, end=end)
            if data.empty:
                st.warning(f"No data available for stock: {stock}")
            else:
                stocks_df[stock] = data['Close']
        except Exception as e:
            st.warning(f"Failed to download data for {stock}: {str(e)}")

    if stocks_df.empty:
        st.error("No stock data available. Please check your stock selections.")
        st.stop()

    stocks_df.reset_index(inplace=True)
    stocks_df['Date'] = pd.to_datetime(stocks_df['Date'])
    stocks_df['Date'] = stocks_df['Date'].apply(lambda x: str(x)[:10])
    stocks_df['Date'] = pd.to_datetime(stocks_df['Date'])

    st.write("Stock data for selected stocks:")
    st.write(stocks_df.head())

    stocks_df = pd.merge(stocks_df, SP500, on='Date', how='inner')

    st.write("Merged Dataframe:")
    st.write(stocks_df.head())

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('### Dataframe head')
        st.dataframe(stocks_df.head())
    with col2:
        st.markdown('### Dataframe tail')
        st.dataframe(stocks_df.tail())

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('### Price of all the Stocks')
        st.plotly_chart(capm_functions.interactive_plot(stocks_df))
    with col2:
        st.markdown('### Price of all the Stocks (After Normalizing)')
        st.plotly_chart(capm_functions.interactive_plot(capm_functions.normalize(stocks_df)))

    stocks_daily_return = capm_functions.daily_return(stocks_df)

    st.write("Daily returns for stocks:")
    st.write(stocks_daily_return.head())

    beta = {}
    alpha = {}

    for stock in stocks_daily_return.columns:
        if stock not in ['Date', 'sp500']:
            try:
                b, a = capm_functions.calculate_beta(stocks_daily_return, stock)
                beta[stock] = b
                alpha[stock] = a
            except Exception as e:
                st.warning(f"Failed to calculate beta for {stock}: {str(e)}")

    beta_df = pd.DataFrame(columns=['Stock', 'Beta Value'])
    beta_df['Stock'] = beta.keys()
    beta_df['Beta Value'] = [str(round(i, 2)) for i in beta.values()]

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('### Calculated Beta Value')
        st.dataframe(beta_df)

    rf = 0  # risk-free rate
    rm = stocks_daily_return['sp500'].mean() * 252  # annual market return
    return_df = pd.DataFrame()
    stock_list = []
    return_value = []
    for stock, value in beta.items():
        stock_list.append(stock)
        return_value.append(str(round(rf + (value * (rm - rf)), 2)))

    return_df['Stock'] = stock_list
    return_df['Return Value'] = return_value

    with col2:
        st.markdown('### Calculated Return using CAPM')
        st.dataframe(return_df)

except Exception as e:
    st.error(f"Error: {str(e)}")
