import streamlit as st
from modules.login import show_login_page
from modules.dashboard import show_dashboard
from modules.products import show_products
from modules.stock import show_stock
from modules.transactions import show_transactions
from modules.reports import show_reports


st.set_page_config(
    page_title="Inventory Management System",
    page_icon="📦",
    layout="wide"
)


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


if not st.session_state.logged_in:

    show_login_page()

else:
    
    menu = st.sidebar.selectbox(
    "Navigation",
    ["Dashboard", "Products", "Stock", "Transactions", "Reports"]
    )

    if menu == "Dashboard":
        show_dashboard()

    elif menu == "Products":
        show_products()

    elif menu == "Stock":
        show_stock()

    elif menu == "Transactions":
        show_transactions()
    
    elif menu == "Reports":
        show_reports()
        
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()