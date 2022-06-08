import streamlit as st
import numpy as np
import pandas as pd
import leafmap.kepler as leafmap
import geopandas as gpd

from data.create_data import setjettersDB_connection
from data.create_data import setjettersDB_query

st.set_page_config(page_title="Map!", page_icon="🌍🎥")

st.title('Setjetters data explorer webmap')

# Get connection
conn = setjettersDB_connection()
raw_conn = conn.raw_connection()

scenes_query = "SELECT * from scenes;"
scenes_df = pd.read_sql(scenes_query, con=conn)

scenes_gdf = gpd.GeoDataFrame(scenes_df, geometry=gpd.points_from_xy(scenes_df.lng, scenes_df.lat))
scenes_gdf['created_at'] = scenes_df['created_at'].astype(str)
scenes_gdf['updated_at'] = scenes_df['updated_at'].astype(str)


m = leafmap.Map(center=[40, -100], zoom=2, height=600, widescreen=False)
m.add_gdf(scenes_gdf, "Scenes")
m.to_streamlit()
