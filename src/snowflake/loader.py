import pandas as pd
import streamlit as st
from .connection import get_connection

@st.cache_data(ttl=600)
def load_data():
    try:
        conn = get_connection()
        df = pd.read_sql("SELECT * FROM CUSTOMER_CHURN", conn)
    except:
        df = pd.read_csv("data/customer_churn.csv")
    return df