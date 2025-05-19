import streamlit as st
import base64

def get_base64_image(image_path: str) -> str:
    """Encode image to base64 format."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def apply_custom_style(image_path: str = "app.png"):
    """Inject custom CSS for consistent background and sidebar styling."""
    img_base64 = get_base64_image(image_path)

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

        /* Dark overlay behind app */
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
            min-height: 100vh;
        }}

        /* Consistent sidebar styling */
        [data-testid="stSidebar"] {{
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-right: 1px solid rgba(255, 255, 255, 0.3);
        }}

        [data-testid="stSidebar"] .css-1cypcdb {{
            color: #0a1f44;
        }}

        /* Hide Streamlit's default header/footer and link icons */
        header {{ visibility: hidden; }}
        footer {{ visibility: hidden; }}
        .stMarkdown a {{ display: none !important; }}
        </style>
        """,
        unsafe_allow_html=True
    )
