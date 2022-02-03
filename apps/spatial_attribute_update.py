from curses import raw
from matplotlib.pyplot import table
import streamlit as st
import pandas as pd
from data.create_data import mysql_connection
from opencage.geocoder import OpenCageGeocode


def geocoder(table, selector):
    geocoder = OpenCageGeocode(st.secrets.opencage.api_key)

    cols = ["id"]

    my_bar = st.progress(0.0)
    progress_counter = 0
    progress_add = 1 / len(table.index)

    if "FLAG" in selector:
        cols.append("FLAG")
    if "TIMEZONE" in selector:
        cols.append("TIMEZONE")
    if "CITY" in selector:
        cols.append("CITY")
    if "CITY_DISTRICT" in selector:
        cols.append("CITY_DISTRICT")
    if "CONTINENT" in selector:
        cols.append("CONTINENT")
    if "COUNTRY" in selector:
        cols.append("COUNTRY")
    if "CURRENCY" in selector:
        cols.append("CURRENCY")
    if "STATE" in selector:
        cols.append("STATE")
    if "NEIGHBORHOOD" in selector:
        cols.append("NEIGHBORHOOD")
    if "ROAD" in selector:
        cols.append("ROAD")
    if "FULL_ADDRESS" in selector:
        cols.append("FULL_ADDRESS")

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
        if "COUNTRY" in selector:
            table.loc[index, 'COUNTRY'] = results[0].get("components").get("country")
        if "CURRENCY" in selector:
            table.loc[index, 'CURRENCY'] = results[0].get("components").get("currency")
        if "STATE" in selector:
            table.loc[index, 'STATE'] = results[0].get("components").get("state")
        if "NEIGHBORHOOD" in selector:
            table.loc[index, 'NEIGHBORHOOD'] = results[0].get("components").get("neighborhood")
        if "ROAD" in selector:
            table.loc[index, 'ROAD'] = results[0].get("components").get("road")
        if "FULL_ADDRESS" in selector:
            table.loc[index, 'FULL_ADDRESS'] = results[0].get("formatted")
        
        # st.write(f"{index} rows processed")


        # for percent_complete in range(len(table.index)):
        progress_counter = progress_counter + progress_add
        my_bar.progress(progress_counter)
        
    return table[cols]


def app():
    st.title('Spatial Attribute Database Update')
    st.write("Uses geocoder to derive spatial attributes and then populate the setjetters database with these")

    test = st.checkbox('Test (only first 10 rows)')
    update_db = st.checkbox('Update database')

    # get connection
    conn = mysql_connection()
    raw_conn = conn.raw_connection()

    # get tabke names
    cursor=raw_conn.cursor()
    cursor.execute("SHOW TABLES")
    table_list = []
    for table_name in cursor:
        table_name_fixed = table_name[0]
        table_list.append(table_name_fixed)

    #select table
    select_table = st.selectbox(
     'Which table would you like to retrieve spatial attributes for (From Opencage OSM geocoder)?',
     table_list)
    
    if test == True:
        query = f"SELECT * FROM {select_table} LIMIT 10;"
    else:
        query = f"SELECT * from {select_table};"

    df = pd.read_sql(query, con=conn)


    st.write(df)

    # select attributes
    options = ['FLAG', 'TIMEZONE', 'CITY', 'CITY_DISTRICT', 'CONTINENT', 'COUNTRY', 'CURRENCY', 'STATE', 'NEIGHBORHOOD', 'ROAD', 'FULL_ADDRESS']

    selected_options = st.multiselect(
     'Attributes to add', options, default=options)

    selected_options.append("id")

    if 'get_attributes' not in st.session_state:
        st.session_state.get_attributes_button_clicked = False

    # st.button("Submit query", on_click=geocoder(df, selected_options))
    if st.button('Get attributes'):
        st.session_state.get_attributes_button_clicked = True
        st.write('Geocoding.... This may take a while')

        geocode_df = geocoder(df, selected_options)
        st.write(geocode_df)

        if update_db:
            new_table_name = select_table + "_geocode"
            
            geocode_df.to_sql(new_table_name, conn, if_exists='replace')
            st.write(f"{new_table_name} added to the database, join by id onto {select_table} in order to integrate spatial attributes")




