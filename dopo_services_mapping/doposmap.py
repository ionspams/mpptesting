import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Title of the app
st.title("Services Mapping Dashboard")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file
    data = pd.read_csv(uploaded_file)

    # Filter active services
    active_services = data[data['STATUS'].str.contains('active', case=False, na=False)]

    # Search bar for filtering
    search_query = st.text_input("Search by organization, service name, or category")

    if search_query:
        active_services = active_services[
            active_services['Організація'].str.contains(search_query, case=False, na=False) |
            active_services['Назва місця'].str.contains(search_query, case=False, na=False) |
            active_services['Категорії'].str.contains(search_query, case=False, na=False)
        ]

    # Map setup
    if 'latitude' in active_services.columns and 'longitude' in active_services.columns:
        # Center the map on the average of the coordinates
        map_center = [active_services['latitude'].mean(), active_services['longitude'].mean()]
        service_map = folium.Map(location=map_center, zoom_start=7)

        # Add markers to the map
        for _, row in active_services.iterrows():
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"<b>{row['Назва місця']}</b><br>{row['Організація']}<br>{row['Категорії']}",
                tooltip=row['Категорії']
            ).add_to(service_map)

        # Display the map
        folium_static(service_map)
    else:
        st.error("CSV file must contain 'latitude' and 'longitude' columns.")
