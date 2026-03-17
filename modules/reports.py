import streamlit as st
import pandas as pd
from database import get_all_products, get_transactions
from database import get_transactions_by_date
import plotly.express as px


def show_reports():

    st.title("📊 Reports")

    tab1, tab2, tab3 = st.tabs([
        "📦 Inventory Report",
        "🔄 Transactions Report",
        "📈 Analytics"
    ])
    # ---------------- INVENTORY REPORT ----------------

    with tab1:

        st.subheader("📦 Inventory Report")

        data = get_all_products()

        if data:

            df = pd.DataFrame(data)

            st.dataframe(df, width="stretch")

            csv = df.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="📥 Download Inventory CSV",
                data=csv,
                file_name="inventory_report.csv",
                mime="text/csv"
            )

        else:
            st.warning("No product data available")

    # ---------------- TRANSACTIONS REPORT ----------------

    with tab2:

        st.subheader("🔄 Transactions Report")

        data = get_transactions()

        if data:

            df = pd.DataFrame(data)

            st.dataframe(df, width="stretch")

            csv = df.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="📥 Download Transactions CSV",
                data=csv,
                file_name="transactions_report.csv",
                mime="text/csv"
            )

        else:
            st.warning("No transaction data available")

    with tab3:

        st.subheader("📈 Stock Movement Analytics")

        col1, col2 = st.columns(2)

        start_date = col1.date_input("From Date")
        end_date = col2.date_input("To Date")

        if start_date and end_date:

            data = get_transactions_by_date(start_date, end_date)

            if data:

                df = pd.DataFrame(data)

                fig = px.bar(
                    df,
                    x="date",
                    y="total",
                    color="type",
                    barmode="group",
                    title="Stock Movement Over Time",
                    color_discrete_map={
                        "IN": "green",
                        "OUT": "red"
                    }
                )

                st.plotly_chart(fig, width="stretch")

            else:
                st.warning("No data for selected date range")