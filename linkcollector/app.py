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

# Replace with your Google Sheet ID
SHEET_ID = 'your_google_sheet_id'
SHEET_NAME = 'Sheet1'
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
