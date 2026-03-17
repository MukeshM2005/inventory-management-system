import streamlit as st
import pandas as pd
from database import get_all_products, get_categories, add_product


def show_products():

    st.title("📦 Product Management")

    st.divider()

    # ---------------------------
    # ADD PRODUCT
    # ---------------------------

    st.subheader("Add Product")

    categories = get_categories()

    category_options = {c["name"]: c["id"] for c in categories}

    name = st.text_input("Product Name", key="product_name")
    sku = st.text_input("SKU", key="product_sku")

    category_name = st.selectbox(
        "Category",
        list(category_options.keys()),
        key="product_category"
    )

    quantity = st.number_input("Quantity", min_value=0, value=0)
    unit = st.text_input("Unit", value="pcs")

    price = st.number_input("Price", min_value=0.0, value=0.0)

    reorder_level = st.number_input("Reorder Level", min_value=0, value=10)

    location = st.text_input("Warehouse Location")

    description = st.text_area("Description")

    if st.button("Add Product", key="add_product_btn"):

        success = add_product(
            name,
            sku,
            category_options[category_name],
            quantity,
            unit,
            price,
            reorder_level,
            location,
            description
        )

        if success:
            st.success("Product added successfully!")
            st.rerun()
        else:
            st.error("Error adding product")

    st.divider()

    # ---------------------------
    # PRODUCT TABLE
    # ---------------------------

    st.subheader("Product List")

    products = get_all_products()

    if products:
        df = pd.DataFrame(products)
        st.dataframe(df, width="stretch")
        
    else:
        st.info("No products added yet.")