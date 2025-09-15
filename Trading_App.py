import streamlit as st
import base64

# Function to encode the image
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Load and encode the background image
img_base64 = get_base64_image("app.png")

# Page configuration
st.set_page_config(
    page_title="Trading App Dashboard",
    page_icon="📈",
    initial_sidebar_state="collapsed",
    layout="wide",
)

# Inject custom CSS styling
st.markdown(
    f"""
    <style>
    html, body {{
        height: 100%;
        margin: 0;
        padding: 0;
        background-image: url("data:image/png;base64,{img_base64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }}

    /* Dark overlay */
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        height: 100%;
        width: 100%;
        background: rgba(0, 0, 0, 0.4);
        z-index: -1;
    }}

    .stApp {{
        background-color: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 0;
        min-height: 100vh;
        animation: fadeIn 1s ease-in;
    }}

    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}

    h1, h2, h3 {{
        color: #0a1f44;
    }}

    .service-card {{
        background-color: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }}

    .service-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1);
    }}

    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.3);
    }}

    [data-testid="stSidebar"] .css-1cypcdb {{
        color: #0a1f44;
    }}

    /* Hide Streamlit system UI */
    header {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
    .stMarkdown a {{ display: none !important; }}
    </style>
    """,
    unsafe_allow_html=True
)

# Main content
st.title("Trading Guide App :bar_chart:")
st.markdown("## 📋 We provide the following services")

cols = st.columns(2)

with cols[0]:
    st.markdown("""
    <div class="service-card">
        <h4>1 : Stock Information</h4>
        <p>Explore real-time and historical stock data to support informed decisions.</p>
        <p>Visualize price trends and compare stocks easily.</p>
        <p>Monitor performance with dynamic charts and metrics.</p>
    </div>

    <div class="service-card">
        <h4>3 : CAPM Return</h4>
        <p>Calculate the expected return of stocks based on risk and market dynamics.</p>
        <p>Input risk-free rate and market return to evaluate.</p>
        <p>Understand how market volatility affects returns.</p>
    </div>
    """, unsafe_allow_html=True)

with cols[1]:
    st.markdown("""
    <div class="service-card">
        <h4>2 : Stock Prediction</h4>
        <p>Get predicted stock prices for the next 30 days using ML forecasting models.</p>
        <p>Utilize models like ARIMA, LSTM for forecasting.</p>
        <p>Evaluate prediction confidence and performance metrics.</p>
    </div>

    <div class="service-card">
        <h4>4 : CAPM Beta</h4>
        <p>Determine Beta values and expected returns for individual equities.</p>
        <p>Compare stock volatility against the market.</p>
        <p>Refine investment strategy with beta insights.</p>
    </div>
    """, unsafe_allow_html=True)