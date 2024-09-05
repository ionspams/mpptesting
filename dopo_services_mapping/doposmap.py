import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import requests
from io import StringIO
import base64

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

# Sidebar for selecting the organization
st.sidebar.title("Select Organization")
organization = st.sidebar.radio(
    "Choose an organization to view its services:",
    ("Dopomoha.md", "PIN Moldova")
)

# GitHub repository and token details
repo = "ionspams/m4p_secure"  # Your GitHub username/repository name
token = st.secrets["GITHUB_TOKEN"]  # GitHub token stored securely in Streamlit secrets

# Set CSV path and text based on the selected organization
if organization == "Dopomoha.md":
    path = "smapping_proto.csv"
    st.title("Dopomoha.md Services Mapping Prototype")
    disclaimer_text = """
    **Disclaimer:** Contact information is currently not displayed publicly as it is not appropriate at this stage. 
    This is a prototype, and not all parties have agreed to have their contact information displayed.
    """
    search_instruction_text = """
    **Search Instructions**: You can search by typing the name of an organization or choose a district from the dropdown. 
    The suggestions in the search box are for districts, but you can manually type in any search term.
    """
else:
    path = "pinmapping.csv"
    st.title("PIN Moldova Services Mapping Prototype")
    disclaimer_text = """
    **Disclaimer:** Contact information is currently not displayed publicly as it is not appropriate at this stage. 
    This is a prototype, representing People in Need Moldova (PIN Moldova) services.
    """
    search_instruction_text = """
    **Search Instructions**: You can search by typing the name of an organization or choose a district from the dropdown. 
    The suggestions in the search box are for districts, but you can manually type in any search term.
    """

# Display the disclaimer
st.markdown(disclaimer_text)

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

        # Extract unique districts for the dropdown
        districts = active_services['district'].unique().tolist()

        # Instructions for the user
        st.markdown(search_instruction_text)

        # Search bar with districts dropdown
        search_query = st.text_input("Search by organization or select a district", "")
        selected_district = st.selectbox("Or select a district from the list", [""] + districts)

        # Combine search criteria
        if selected_district:
            search_query = selected_district

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

        # **Handle missing latitude/longitude values**
        if filtered_services['latitude'].isna().sum() > 0 or filtered_services['longitude'].isna().sum() > 0:
            st.warning("Some entries have missing location data and won't be displayed on the map.")
            # Drop rows where latitude or longitude are NaN
            filtered_services = filtered_services.dropna(subset=['latitude', 'longitude'])

        # Map setup - Display the map first
        if 'latitude' in filtered_services.columns and 'longitude' in filtered_services.columns and not filtered_services.empty:
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
            st.error("CSV file must contain valid 'latitude' and 'longitude' columns.")

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
