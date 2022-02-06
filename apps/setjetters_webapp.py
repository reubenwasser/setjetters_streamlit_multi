import streamlit as st
import leafmap
import asyncio
import numpy as np
import pandas as pd
import geopandas as gpd
from data.create_data import mysql_connection, create_table

def app():
    st.title('Web App')

    st.write("WIP: web app to view locations + perform queries")
    st.markdown("### Plot Data")
    
    # Work-around for Streamlit release defect (issue #744)
    # https://github.com/streamlit/streamlit/issues/744#issuecomment-686712930
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Connect to database and get read information to geopandas
    conn = mysql_connection()
    query = f"SELECT * from real_locations WHERE lng OR lat IS NOT NULL;"
    df = pd.read_sql(query, con=conn)
    df = df[['name', 'lat', 'lng']]
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lng, df.lat), crs="EPSG:4326")

    m = leafmap.Map()
    m.add_gdf(gdf, layer_name="real_locations")
    m.to_streamlit(width=700, height=500)


    # st.line_chart(df)