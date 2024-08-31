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

    # Display the data
    st.write("### Uploaded Data", data)

    # Map setup
    if 'latitude' in data.columns and 'longitude' in data.columns:
        # Center the map on the average of the coordinates
        map_center = [data['latitude'].mean(), data['longitude'].mean()]
        service_map = folium.Map(location=map_center, zoom_start=7)

        # Add markers to the map
        for _, row in data.iterrows():
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"{row['Назва місця']} - {row['Організація']}",
                tooltip=row['Категорії']
            ).add_to(service_map)

        # Display the map
        folium_static(service_map)
    else:
        st.error("CSV file must contain 'latitude' and 'longitude' columns.")
