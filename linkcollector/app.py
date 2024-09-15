import streamlit as st
import gspread
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os

# Define the scope for Google Sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# Load credentials from Streamlit secrets or authenticate the user
def get_credentials():
    creds = None
    
    # Check if we have saved user credentials
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    
    # If no valid credentials, initiate OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config({
                "installed": {
                    "client_id": st.secrets["google_oauth"]["client_id"],
                    "client_secret": st.secrets["google_oauth"]["client_secret"],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "redirect_uris": ["http://localhost:8501"]
                }
            }, SCOPES)
            creds = flow.run_local_server(port=8501)
        
        # Save credentials for future use
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    
    return creds

# Get authenticated credentials
creds = get_credentials()

# Connect to Google Sheets
client = gspread.authorize(creds)

# Provide Your Google Sheet ID Here
SHEET_ID = '1t5cpHnxn-voR-2ODERypf5lyE1oM71YLWgb7ikrgqmI'  # Replace this with your actual Google Sheet ID

# Provide Your Sheet Name Here
SHEET_NAME = 'Project1  # Replace with the actual sheet/tab name

# Open the Google Sheet by ID and access the specific worksheet by name
sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

# Fetch data from Google Sheets
def get_sheet_data():
    rows = sheet.get_all_records()
    return rows

st.title("My ChatGPT Links")

# Fetch and display data from Google Sheets
sheet_data = get_sheet_data()

for row in sheet_data:
    st.write(f"Title: {row['Title']}, Link: {row['Link']}, Content: {row['Content']}")
