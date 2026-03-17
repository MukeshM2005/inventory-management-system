import streamlit as st
from database import get_all_products, stock_in, stock_out


def show_stock():

    st.title("📦 Stock Management")

    products = get_all_products()

    if not products:
        st.info("No products available.")
        return

    product_options = {p["name"]: p["id"] for p in products}

    tab1, tab2 = st.tabs(["Stock IN", "Stock OUT"])

    # -------------------
    # STOCK IN
    # -------------------

    with tab1:

        st.subheader("Add Stock")

        product_name = st.selectbox(
            "Select Product",
            list(product_options.keys()),
            key="stock_in_product"
        )

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            value=1,
            key="stock_in_qty"
        )

        if st.button("Add Stock", key="stock_in_btn"):

            success = stock_in(product_options[product_name], quantity, st.session_state.user_id)

            if success:
                st.success("Stock added successfully")
                st.rerun()
            else:
                st.error("Error adding stock")

    # -------------------
    # STOCK OUT
    # -------------------

    with tab2:

        st.subheader("Remove Stock")

        product_name = st.selectbox(
            "Select Product",
            list(product_options.keys()),
            key="stock_out_product"
        )

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            value=1,
            key="stock_out_qty"
        )

        if st.button("Remove Stock", key="stock_out_btn"):

            success = stock_out(product_options[product_name], quantity, st.session_state.user_id)
            
            if success:
                st.success("Stock removed successfully")
                st.rerun()
            else:
                st.error("Not enough stock")