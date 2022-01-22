import streamlit as st
from multiapp import MultiApp
from apps import home, data_stats # import your app modules here

app = MultiApp()

# Add all your application here
app.add_app("Setjetters Web Map", home.app)
app.add_app("Spatial attributes update", data_stats.app)

# The main app
app.run()