import snowflake.connector
import streamlit as st 

def get_connection():
    return snowflake.connector.connect(
        user=st.secrets("user"),
        password=st.secrets("password"),
        account=st.secrets("account"),
        warehouse=st.secrets("warehouse"),
        database=st.secrets("database"),
        schema=st.secrets("schema"), 
        role = st.secrets("role")
    )