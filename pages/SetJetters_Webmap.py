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

m = leafmap.Map(center=[40, -100], zoom=2, height=600)


# # Load scenes from database
# scenes_query = "SELECT * from scenes;"
# scenes_df = pd.read_sql(scenes_query, con=conn)
# scenes_gdf = gpd.GeoDataFrame(scenes_df, geometry=gpd.points_from_xy(scenes_df.lng, scenes_df.lat), crs="EPSG:3857")
# scenes_gdf['created_at'] = scenes_df['created_at'].astype(str)
# scenes_gdf['updated_at'] = scenes_df['updated_at'].astype(str)

# m.add_gdf(scenes_gdf, "Scenes")

# # Load businesses from database
# businesses_query = "SELECT * from businesses;"
# businesses_df = pd.read_sql(businesses_query, con=conn)
# businesses_gdf = gpd.GeoDataFrame(businesses_df, geometry=gpd.points_from_xy(businesses_df.lng, businesses_df.lat), crs="EPSG:3857")
# businesses_gdf['created_at'] = businesses_df['created_at'].astype(str)
# businesses_gdf['updated_at'] = businesses_df['updated_at'].astype(str)

# m.add_gdf(businesses_gdf, "Businesses")

m.to_streamlit()
