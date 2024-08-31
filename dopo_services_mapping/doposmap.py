import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import requests
from io import StringIO
import base64

# Title of the app
st.title("Dopomoha.md Services Mapping Prototype")

# Disclaimer for Contact Info
st.markdown("""
**Disclaimer:** Contact information is currently not displayed publicly as it is not appropriate at this stage. 
This is a prototype, and not all parties have agreed to have their contact information displayed.
""")

# Function to fetch CSV from GitHub
def fetch_github_csv(repo, path, token):
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.json()['content']
        decoded_content = base64.b64decode(content).decode('utf-8')
        return pd.read_csv(StringIO(decoded_content))
    else:
        st.error("Failed to fetch the dataset from GitHub.")
        return None

# Replace with your own repository details
repo = "ionspams/m4p_secure"  # Your GitHub username/repository name
path = "smapping_proto.csv"  # The path to your CSV file within the repo
token = st.secrets["GITHUB_TOKEN"]  # GitHub token stored securely in Streamlit secrets

# Fetch and load the dataset
data = fetch_github_csv(repo, path, token)
if data is not None:
    # Check if all required columns are present
    required_columns = [
        'organization', 'place_name', 'category', 'city', 'district', 
        'contact_info', 'status', 'latitude', 'longitude', 
        'assistance_criteria', 'service_additional_details', 'pub_hotline', 'services_categories'
    ]
    
    if all(column in data.columns for column in required_columns):
        # Filter active services
        active_services = data[data['status'].str.contains('active', case=False, na=False)]

        # Search bar for filtering by city, district, organization, category, or services categories
        search_query = st.text_input("Search by organization, place name, category, city, district, or services categories")

        # Perform filtering based on search query
        if search_query:
            filtered_services = active_services[
                active_services['organization'].str.contains(search_query, case=False, na=False) |
                active_services['place_name'].str.contains(search_query, case=False, na=False) |
                active_services['category'].str.contains(search_query, case=False, na=False) |
                active_services['city'].str.contains(search_query, case=False, na=False) |
                active_services['district'].str.contains(search_query, case=False, na=False) |
                active_services['services_categories'].str.contains(search_query, case=False, na=False)
            ]
        else:
            filtered_services = active_services

        # Map setup - Display the map first
        if 'latitude' in filtered_services.columns and 'longitude' in filtered_services.columns:
            # Center the map on the average of the filtered coordinates
            map_center = [filtered_services['latitude'].mean(), filtered_services['longitude'].mean()]
            service_map = folium.Map(location=map_center, zoom_start=7)

            # Add markers to the map with detailed tooltips based on filtered results
            for _, row in filtered_services.iterrows():
                # Handle missing or non-string details gracefully
                additional_details = str(row.get('service_additional_details', ''))[:50]
                tooltip_content = (
                    f"<b>Place Name:</b> {row['place_name']}<br>"
                    f"<b>Status:</b> {row['status']}<br>"
                    f"<b>Assistance Criteria:</b> {row.get('assistance_criteria', 'N/A')}<br>"
                    f"<b>Service Additional Details:</b> {additional_details}..."  # Truncate long details
                    f"<br><b>Hotline:</b> {row.get('pub_hotline', 'N/A')}<br>"
                    f"<b>Organization:</b> {row['organization']}<br>"
                    f"<b>Services Categories:</b> {row['services_categories']}"
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

        # Display the table only if there are search results, and limit to 5 rows
        if search_query and not filtered_services.empty:
            st.write("### Services Table (Showing up to 5 results)")
            st.table(
                filtered_services[['organization', 'place_name', 'category', 'services_categories', 'city', 'district', 'status']].head(5)
            )
        elif search_query:
            st.warning("No matching services found.")

    else:
        st.error(f"CSV file is missing one or more required columns: {', '.join(required_columns)}")
