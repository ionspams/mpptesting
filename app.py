import streamlit as st
import re
import pandas as pd
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import json

# Constants
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1t5cpHnxn-voR-2ODERypf5lyE1oM71YLWgb7ikrgqmI'

# Use Streamlit secrets
CLIENT_CONFIG = {
    "web": {
        "client_id": st.secrets["google_oauth"]["client_id"],
        "client_secret": st.secrets["google_oauth"]["client_secret"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": [st.secrets["google_oauth"]["redirect_uri"]],
    }
}

# Function to extract URLs from text
def extract_urls(text):
    url_pattern = re.compile(r'(https?://\S+)')
    return url_pattern.findall(text)

# Function to process input text
def process_text(text):
    urls = extract_urls(text)
    title = text[:30] + ('...' if len(text) > 30 else '')
    content_without_urls = re.sub(r'https?://\S+', '', text)
    content = content_without_urls.strip()
    return title, urls, content

# OAuth Functions
def get_credentials():
    if 'credentials' not in st.session_state:
        st.session_state.credentials = None

    if not st.session_state.credentials or not st.session_state.credentials.valid:
        flow = Flow.from_client_config(
            CLIENT_CONFIG,
            scopes=SCOPES,
            redirect_uri=st.secrets["google_oauth"]["redirect_uri"]
        )
        auth_url, _ = flow.authorization_url(prompt='consent')
        st.write(f"[Click here to authorize]({auth_url}) to access Google Sheets.")

        # Get authorization code from the user
        auth_code = st.text_input("Enter the authorization code:")

        if auth_code:
            flow.fetch_token(code=auth_code)
            st.session_state.credentials = flow.credentials

    return st.session_state.credentials

# Main App
def main():
    st.title("URL Extractor App")

    credentials = get_credentials()

    if credentials:
        try:
            service = build('sheets', 'v4', credentials=credentials)
            sheet = service.spreadsheets()

            # Input Form
            with st.form("input_form", clear_on_submit=True):
                user_input = st.text_area("Enter text containing URLs")
                submitted = st.form_submit_button("Submit")
                if submitted and user_input:
                    title, urls, content = process_text(user_input)
                    # Append data to Google Sheets
                    values = [[title, ', '.join(urls), content]]
                    body = {'values': values}
                    sheet.values().append(
                        spreadsheetId=SPREADSHEET_ID,
                        range="Sheet1!A:C",
                        valueInputOption="RAW",
                        insertDataOption="INSERT_ROWS",
                        body=body
                    ).execute()
                    st.success("Data saved successfully!")

            # Display Data
            st.header("Saved Entries")
            result = sheet.values().get(
                spreadsheetId=SPREADSHEET_ID,
                range="Sheet1!A:C"
            ).execute()
            rows = result.get('values', [])
            df = pd.DataFrame(rows, columns=['Title', 'URLs', 'Content'])

            for index, row in df.iterrows():
                st.subheader(row['Title'])
                urls = row['URLs'].split(', ')
                for url in urls:
                    st.markdown(f"- [{url}]({url})")
                with st.expander("Read more"):
                    st.write(row['Content'])

        except Exception as e:
            st.error(f'An error occurred: {e}')

if __name__ == "__main__":
    main()
