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
    'longitude': [28.12, 28.84],
    'assistance_criteria': ['Criteria 1', 'Criteria 2'],
    'service_additional_details': ['Details 1', 'Details 2'],
    'pub_hotline': ['+373 67700250', '+373 60949091']
})

# Display sample CSV download link
st.markdown("If you're having trouble formatting your data, [download this sample CSV file](#).")
st.markdown(get_table_download_link(sample_data), unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file
    data = pd.read_csv(uploaded_file)

    # Check if all required columns are present
    required_columns = [
        'organization', 'place_name', 'category', 'city', 'district', 
        'contact_info', 'status', 'latitude', 'longitude', 
        'assistance_criteria', 'service_additional_details', 'pub_hotline'
    ]
    
    if all(column in data.columns for column in required_columns):
        # Filter active services
        active_services = data[data['status'].str.contains('active', case=False, na=False)]

        # Search bar for filtering by city, district, organization, or category
        search_query = st.text_input("Search by organization, place name, category, city, or district")

        if search_query:
            active_services = active_services[
                active_services['organization'].str.contains(search_query, case=False, na=False) |
                active_services['place_name'].str.contains(search_query, case=False, na=False) |
                active_services['category'].str.contains(search_query, case=False, na=False) |
                active_services['city'].str.contains(search_query, case=False, na=False) |
                active_services['district'].str.contains(search_query, case=False, na=False)
            ]

        # Display a simple table
        st.write("### Services Table")
        st.dataframe(active_services[['organization', 'place_name', 'category', 'city', 'district', 'contact_info', 'status']])

        # Map setup
        if 'latitude' in active_services.columns and 'longitude' in active_services.columns:
            # Center the map on the average of the coordinates
            map_center = [active_services['latitude'].mean(), active_services['longitude'].mean()]
            service_map = folium.Map(location=map_center, zoom_start=7)

            # Add markers to the map with detailed tooltips
            for _, row in active_services.iterrows():
                # Handle missing or non-string details gracefully
                additional_details = str(row.get('service_additional_details', ''))[:50]
                tooltip_content = (
                    f"<b>Place Name:</b> {row['place_name']}<br>"
                    f"<b>Status:</b> {row['status']}<br>"
                    f"<b>Assistance Criteria:</b> {row.get('assistance_criteria', 'N/A')}<br>"
                    f"<b>Service Additional Details:</b> {additional_details}..."  # Truncate long details
                    f"<br><b>Hotline:</b> {row.get('pub_hotline', 'N/A')}<br>"
                    f"<b>Organization:</b> {row['organization']}"
                )
                folium.Marker(
                    location=[row['latitude'], row['longitude']],
                    popup=tooltip_content,
                    tooltip=row['place_name']
                ).add_to(service_map)

            # Display the map
            folium_static(service_map)
        else:
            st.error("CSV file must contain 'latitude' and 'longitude' columns.")
    else:
        st.error(f"CSV file is missing one or more required columns: {', '.join(required_columns)}")
