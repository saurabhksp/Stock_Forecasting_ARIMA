import streamlit as st
import pandas as pd
from pages.utils.model_train import (
    get_data,
    get_rolling_mean,
    get_differencing_order,
    scaling,
    evaluate_model,
    get_forecast,
    inverse_scaling
)
from pages.utils.plotly_figure import plotly_table, Moving_average_forecast
from style_utils import apply_custom_style
# Streamlit page configuration
st.set_page_config(
    page_title="Stock Prediction",
    page_icon="chart_with_downwards_trend",
    layout="wide",
)

st.title("Stock Prediction")
apply_custom_style("app.png")


# User input section
col1, col2, col3 = st.columns(3)
with col1:
    ticker = st.text_input('Stock Ticker', 'AAPL')

rmse = 0

st.subheader(f'Predicting Next 30 days Close Price for: {ticker}')

# Fetch the data
close_price = get_data(ticker)

# Convert DataFrame to Series if needed
if isinstance(close_price, pd.DataFrame):
    close_price = close_price.squeeze()

# Validate data
if (close_price is None) or (close_price.empty) or (close_price.isnull().all()):
    st.error("Failed to fetch valid stock data.")
    st.stop()

# Get rolling mean
rolling_price = get_rolling_mean(close_price)

# Validate rolling mean
if (rolling_price is None) or (rolling_price.empty) or (rolling_price.isnull().all()):
    st.error("Rolling mean data is empty or invalid.")
    st.stop()

# Get differencing order
differencing_order = get_differencing_order(rolling_price)

# Scale the data
scaled_data, scaler = scaling(rolling_price)

# Evaluate model
rmse = evaluate_model(scaled_data, differencing_order)
st.write(f"**Model RMSE Score:** {rmse}")

# Forecast next 30 days
forecast = get_forecast(scaled_data, differencing_order)

# Inverse scale to original values
forecast['Close'] = inverse_scaling(scaler, forecast['Close'])

# Display forecast in table
st.write('##### Forecast Data (Next 30 days)')
fig_tail = plotly_table(forecast.sort_index(ascending=True).round(3))
fig_tail.update_layout(height=220)
st.plotly_chart(fig_tail, use_container_width=True)

# Combine historical and forecast data
forecast_full = pd.concat([rolling_price, forecast])

# Visualize the moving average forecast
st.plotly_chart(Moving_average_forecast(forecast_full.iloc[150:]), use_container_width=True)
