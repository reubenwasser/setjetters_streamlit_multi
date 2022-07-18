# from turtle import width
import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.plugins import MarkerCluster
# import numpy as np
import pandas as pd
import leafmap.leafmap as leafmap
import geopandas as gpd

from data.create_data import setjettersDB_connection
from data.create_data import setjettersDB_query

@st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock": lambda _: None})
def loadScenes(gdf, gdf_list):
    scenes_gdf_list = [[point.xy[1][0], point.xy[0][0]] for point in gdf.geometry]
    i = 0
    for coordinates in gdf_list:
    #assign a color marker for the type of volcano, Strato being the most common
        # if geo_df.Type[i] == "Stratovolcano":
        #     type_color = "green"
        # elif geo_df.Type[i] == "Complex volcano":
        #     type_color = "blue"
        # elif geo_df.Type[i] == "Shield volcano":
        #     type_color = "orange"
        # elif geo_df.Type[i] == "Lava dome":
        #     type_color = "pink"
        # else:
        #     type_color = "purple"


        # Place the markers with the popup labels and data
        folium.Marker(location = coordinates,
                                popup =
                                # "Year: " + str(geo_df.Year[i]) + '<br>' +
                                # "Name: " + str(geo_df.Name[i]) + '<br>' +
                                # "Country: " + str(geo_df.Country[i]) + '<br>'
                                str(scenes_gdf.name[i]) + '<br>'
                                f'<input type="number" value="1" min="0.1" max="10" id="radius" name="radius"><button onclick="searchBusinesses()">Query nearby businesses</button>',
                                # "Coordinates: " + str(geo_df_list[i]),
                                icon = folium.Icon(color = "%s" % "green")).add_to(marker_cluster)
        i = i + 1

st.set_page_config(page_title="Map!", page_icon="🌍🎥")

st.title('Setjetters Webmap')

scenes_df = setjettersDB_query("SELECT * from scenes;")

scenes_gdf = gpd.GeoDataFrame(scenes_df, crs="EPSG:4326", geometry=gpd.points_from_xy(x=scenes_df.lng, y=scenes_df.lat))

scenes_gdf_list = [[point.xy[1][0], point.xy[0][0]] for point in scenes_gdf.geometry]

# st.write(scenes_gdf)

# center on Liberty Bell, add marker
m = folium.Map()

# folium.Marker(
#     [39.949610, -75.150282], 
#     popup="Liberty Bell", 
#     tooltip="Liberty Bell"
# ).add_to(m)

marker_cluster = MarkerCluster().add_to(m)

loadScenes(scenes_gdf, scenes_gdf_list)


# call to render Folium map in Streamlit
st_data = st_folium(m, width = 725)

with st.expander("Expand to see data returned to Python"):
    st_data

if st_data["last_object_clicked"] == None:
    st.sidebar.write("Click on a scene marker to query for nearby businesses")


