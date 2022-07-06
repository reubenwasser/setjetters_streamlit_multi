from turtle import width
import streamlit as st
import numpy as np
import pandas as pd
import leafmap.leafmap as leafmap
import geopandas as gpd

from data.create_data import setjettersDB_connection
from data.create_data import setjettersDB_query

st.set_page_config(page_title="Map!", page_icon="🌍🎥")

st.title('Setjetters Webmap')

# Get connection
conn = setjettersDB_connection()
raw_conn = conn.raw_connection()

m = leafmap.Map()

# Load scenes from database
scenes_query = "SELECT * from scenes;"
scenes_df = pd.read_sql(scenes_query, con=conn).reindex(columns=['value', 'lat', 'lng'])

m.add_points_from_xy(scenes_df, y="lat", x='lng')
m.to_streamlit()

