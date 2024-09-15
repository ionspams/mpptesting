import streamlit as st
import gspread
import google.auth
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

# Define the scope for Google Sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# Load credentials from file or authenticate the user
def get_credentials():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    
    # If no valid credentials are available, request new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=8501)
        # Save the credentials for future use
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    
    return creds

# Get authenticated credentials
creds = get_credentials()

# Connect to Google Sheets
client = gspread.authorize(creds)

# **Provide Your Google Sheet ID Here**
SHEET_ID = '1t5cpHnxn-voR-2ODERypf5lyE1oM71YLWgb7ikrgqmI'  # <-- Replace this with your actual Google Sheet ID

# **Provide Your Sheet Name Here**
SHEET_NAME = 'Project1'  # <-- Replace this with your actual sheet/tab name, such as 'Sheet1' or any custom name

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
