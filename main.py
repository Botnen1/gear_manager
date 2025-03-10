import streamlit as st
from pages import inventory, maintenance, pack_weight, wishlist, trip_logger, gear_insights

# Function to set background
import base64

def hide_streamlit_menu():
    st.markdown("""
        <style>
            /* Hide the Streamlit top menu */
            [data-testid="stSidebarNav"] {display: none;}
        </style>
    """, unsafe_allow_html=True)

# Call this function early in main.py
hide_streamlit_menu()

def custom_css():
    st.markdown("""
        <style>
            /* Sidebar Customization */
            [data-testid="stSidebar"] {
                background-color: #1E1E1E;
                padding-top: 20px;
                border-right: 2px solid rgba(255,255,255,0.1);
            }
            
            /* Sidebar Menu */
            [data-testid="stSidebarNav"] ul {
                font-size: 18px;
                font-weight: bold;
                color: white !important;
            }

            /* Sidebar Selected Item */
            [data-testid="stSidebarNav"] ul li[data-testid="stSidebarNavItem"]:hover {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 8px;
            }

            /* Page Title */
            h1 {
                color: #FFD700 !important;  /* Gold color for elegance */
                text-align: center;
            }

            /* Card Container */
            .gear-card {
                background: rgba(0, 0, 0, 0.7);
                padding: 15px;
                border-radius: 12px;
                color: white;
                box-shadow: 4px 4px 12px rgba(255, 255, 255, 0.1);
                margin-bottom: 15px;
            }

            /* Buttons */
            .stButton>button {
                background-color: #0078D4;
                color: white;
                border-radius: 8px;
                padding: 10px 15px;
                border: none;
                transition: 0.3s;
            }

            .stButton>button:hover {
                background-color: #005A9E;
                transform: scale(1.05);
            }
        </style>
    """, unsafe_allow_html=True)

# Call this function early in main.py
custom_css()


def set_bg(png_file):
    with open(png_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    css = f"""
    <style>
    /* Background image */
    .stApp {{
        background-image: url(data:image/png;base64,{encoded});
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    /* Wider page layout */
    .block-container {{
        max-width: 80%;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }}

    /* Transparent content containers */
    [data-testid="stVerticalBlock"] {{
        background-color: rgba(0, 0, 0, 0.75);
        padding: 15px;
        border-radius: 12px;
        color: white;
    }}

    /* Link color */
    a {{
        color: #6abcf5 !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)



# Set the background
set_bg("graphics/bg3.png")

# Your main app logic here:
def main():
    st.sidebar.title("Gear Manager")
    page = st.sidebar.radio("Navigate", [
        "Gear Inventory Tracker",
        "Pack Weight Calculator",
        #"Maintenance Scheduler",
        "Wishlist Tracker",
        #"Gear Inventory Insights",
        #"Trip Gear Logger"
    ])

    if page == "Gear Inventory Tracker":
        inventory.app()
    elif page == "Pack Weight Calculator":
        pack_weight.app()
    elif page == "Maintenance Scheduler":
        maintenance.app()
    elif page == "Wishlist Tracker":
        wishlist.app()
    elif page == "Trip Gear Logger":
        trip_logger.app()
    elif page == "Gear Insights":  # <-- New addition
        gear_insights.app()

if __name__ == "__main__":
    main()
