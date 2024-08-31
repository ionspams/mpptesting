import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import base64

# Title of the app
st.title("Services Mapping Dashboard")

# Function to download sample CSV
def get_table_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="sample_services.csv">Download Sample CSV</a>'
    return href

# Sample CSV Data with English headers
sample_data = pd.DataFrame({
    'organization': ['CASMED', 'WeWorld Community Center'],
    'place_name': ['Rural Public Library "Ion Druță"', 'WeWorld Community Center'],
    'category': ['Education', 'Domestic and Sexual Violence, Protection, Education'],
    'city': ['Donduşeni', 'Chişinau'],
    'district': ['Donduşeni', 'Chişinău'],
    'contact_info': ['casmed.md@gmail.com', 'elena.colesnicova@weworld.it'],
    'status': ['Active until December 2024', 'Active until December 2025'],
    'latitude': [47.85, 47.01],
    'longitude': [28.12, 28.84]
})

# Display sample CSV download link
st.markdown("If you're having trouble formatting your data, [download this sample CSV file](#).")
st.markdown(get_table_download_link(sample_data), unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file
    data = pd.read_csv(uploaded_file)

    # Filter active services
    active_services = data[data['status'].str.contains('active', case=False, na=False)]

    # Search bar for filtering
    search_query = st.text_input("Search by organization, place name, or category")

    if search_query:
        active_services = active_services[
            active_services['organization'].str.contains(search_query, case=False, na=False) |
            active_services['place_name'].str.contains(search_query, case=False, na=False) |
            active_services['category'].str.contains(search_query, case=False, na=False)
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
                popup=f"<b>{row['place_name']}</b><br>{row['organization']}<br>{row['category']}",
                tooltip=row['category']
            ).add_to(service_map)

        # Display the map
        folium_static(service_map)
    else:
        st.error("CSV file must contain 'latitude' and 'longitude' columns.")
