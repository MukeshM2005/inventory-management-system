import streamlit as st
import pandas as pd
from database import get_transactions


def show_transactions():

    st.title("📋 Transaction History")

    transactions = get_transactions()

    if transactions:

        df = pd.DataFrame(transactions)

        st.dataframe(df, width="stretch")
        
    else:
        
        st.info("No transactions yet.")