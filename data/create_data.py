import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

@st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock": lambda _: None})
def setjettersDB_connection():
    # Connection parameters
    host = st.secrets.mysql.host
    database = st.secrets.mysql.database
    user = st.secrets.mysql.user
    password = st.secrets.mysql.password

    db_connection_str = f"mysql+pymysql://{user}:{password}@{host}/{database}"
    sql_engine = create_engine(db_connection_str)
    return sql_engine

@st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock": lambda _: None})
def setjettersDB_query(query):
    # Connection parameters
    host = st.secrets.mysql.host
    database = st.secrets.mysql.database
    user = st.secrets.mysql.user
    password = st.secrets.mysql.password

    db_connection_str = f"mysql+pymysql://{user}:{password}@{host}/{database}"
    sql_engine = create_engine(db_connection_str)
    conn = sql_engine.raw_connection()
    df = pd.read_sql(query, con=conn)
    return df