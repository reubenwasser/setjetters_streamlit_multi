import streamlit as st
from multiapp import MultiApp
from apps import spatial_attribute_update, setjetters_webapp # import your app modules here

app = MultiApp()

# Add all your application here
app.add_app("Setjetters Web Map", setjetters_webapp.app)
app.add_app("Spatial attributes update", spatial_attribute_update.app)

# The main app
app.run()