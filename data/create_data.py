import pandas as pd
import streamlit as st
import mysql.connector
from sqlalchemy import create_engine



def create_table(n=7):
    df = pd.DataFrame({"x": range(1, 11), "y": n})
    df['x*y'] = df.x * df.y
    return df

# TODO change to DB credentials to secret management
@st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock": lambda _: None})
def mysql_connection():
    # Connection parameters
    host = st.secrets.mysql.host
    database = st.secrets.mysql.database
    user = st.secrets.mysql.user
    password = st.secrets.mysql.password

    db_connection_str = f"mysql+pymysql://{user}:{password}@{host}/{database}"
    sql_engine = create_engine(db_connection_str)
    # db = sql_engine.raw_connection()
    # db=mysql.connector.connect(host=host, user=user, password=password,database=database)
    # df = pd.read_sql(query, con=conn)
    return sql_engine

@st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock": lambda _: None})
def mySQL_query(query):
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