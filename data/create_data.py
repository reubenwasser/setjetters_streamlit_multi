import pandas as pd
import numpy as np

def create_table(n=7):
    df = pd.DataFrame({"x": range(1, 11), "y": n})
    df['x*y'] = df.x * df.y
    return df

# TODO change to DB credentials to secret management
@st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock": lambda _: None})
def init_connection():
    db_connection_str = 'mysql+pymysql://admin:NumberSheep@setjetters1.c2ipvnggy6hj.us-east-2.rds.amazonaws.com/setjetters_export'
    sql_engine = create_engine(db_connection_str)
    return sql_engine.raw_connection()
    # return mysql.connector.connect(user = "admin", database = "setjetters_export", host = "setjetters1.c2ipvnggy6hj.us-east-2.rds.amazonaws.com", password = "NumberSheep")

conn = init_connection()