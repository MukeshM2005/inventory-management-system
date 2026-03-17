import streamlit as st
import pandas as pd
import plotly.express as px
from database import (
    get_dashboard_stats,
    get_products_by_category,
    get_stock_movement,
    get_low_stock_products
)

def show_dashboard():

    st.title("📊 Dashboard")

    # ---------------- METRICS ----------------

    stats = get_dashboard_stats()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📦 Total Products", stats["total_products"])
    col2.metric("💰 Inventory Value", f"₹ {stats['total_value']}")
    col3.metric("⚠️ Low Stock Items", stats["low_stock"])
    col4.metric("🔄 Today's Transactions", stats["today_transactions"])

    st.divider()

    # ---------------- CHARTS ----------------

    st.subheader("📦 Inventory Overview")

    # -------- PIE CHART --------

    category_data = get_products_by_category()

    if category_data:

        df = pd.DataFrame(category_data)

        fig = px.pie(
            df,
            names="category",
            values="total_stock",
            title="Current Available Stock by Category"
        )

        fig.update_traces(textinfo="percent+label")


        st.plotly_chart(fig, width="stretch")

    else:
        st.warning("No stock data available")

    st.divider()

    # -------- BAR CHART --------

    movement_data = get_stock_movement()

    if movement_data:

        df2 = pd.DataFrame(movement_data)

        fig2 = px.bar(
            df2,
            x="category",
            y="total",
            color="type",
            barmode="group",
            title="Stock Movement by Category (IN vs OUT)",
            color_discrete_map={
                "IN": "green",
                "OUT": "red"
            }
        )

        st.plotly_chart(fig2, width="stretch")

    else:
        st.warning("No transaction data available")

    st.divider()

    # ---------------- LOW STOCK ----------------

    st.subheader("⚠️ Low Stock Alert")

    low_stock_data = get_low_stock_products()

    if low_stock_data:

        df_low = pd.DataFrame(low_stock_data)

        df_low["Status"] = "🔴 LOW"

        st.dataframe(df_low, width="stretch")

    else:
        st.success("✅ All products are sufficiently stocked")