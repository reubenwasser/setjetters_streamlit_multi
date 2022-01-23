import streamlit as st
from data.create_data import mySQL_query
from opencage.geocoder import OpenCageGeocode


def geocoder(table, selector):
    geocoder = OpenCageGeocode(st.secrets.opencage.api_key)

    for index, row in table.iterrows():
        results = geocoder.reverse_geocode(row.lat, row.lng)
        if "FLAG" in selector:
            table.loc[index, 'FLAG'] = results[0].get("annotations").get("flag")
        if "TIMEZONE" in selector:
            table.loc[index, 'TIMEZONE'] = results[0].get("annotations").get("timezone").get("name")
        if "CITY" in selector:
            table.loc[index, 'CITY'] = results[0].get("components").get("city")
        if "CITY_DISTRICT" in selector:
            table.loc[index, 'CITY_DISTRICT'] = results[0].get("components").get("city_district")
        if "CONTINENT" in selector:
            table.loc[index, 'CONTINENT'] = results[0].get("components").get("continent")
        # table.loc[index, 'COUNTRY'] = results[0].get("components").get("country")
        # table.loc[index, 'CURRENCY'] = results[0].get("components").get("currency")
        # table.loc[index, 'STATE'] = results[0].get("components").get("state")
        # table.loc[index, 'NEIGHBORHOOD'] = results[0].get("components").get("neighborhood")
        # table.loc[index, 'ROAD'] = results[0].get("components").get("road")
        # table.loc[index, 'FULL_ADDRESS'] = results[0].get("formatted")


def app():
    st.title('Spatial Attribute Database Update')

    st.write("Uses geocoder to derive spatial attributes and then populate the setjetter database with these")

    query = "SELECT * from real_locations;"
    df = mySQL_query(query)
    st.write(df)

    options = ['FLAG', 'TIMEZONE', 'CITY', 'CITY_DISTRICT', 'CONTINENT']

    selected_options = st.multiselect(
     'Attributes to add', options, default=options)

    # st.button("Submit query", on_click=geocoder(df, selected_options))
    if st.button('Get spatial Attributes!!!'):
        st.write('Geocoding....')
        geocoder(df, selected_options)

        st.write(df)



