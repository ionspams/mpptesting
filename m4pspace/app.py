
import os
import streamlit as st
import pandas as pd
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import json

# Google API scopes for Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Authenticate Google Calendar API
def authenticate_google():
    creds = None

    # Load the credentials from the environment variable 'GOOGLE_CREDENTIALS'
    google_creds_json = os.getenv('GOOGLE_CREDENTIALS')

    if google_creds_json:
        google_creds_dict = json.loads(google_creds_json)
        flow = InstalledAppFlow.from_client_config(google_creds_dict, SCOPES)
        creds = flow.run_local_server(port=0)
    else:
        st.error("Google credentials not found in environment variables.")
    
    return creds

# Fetch upcoming events from Google Calendar
def list_calendar_events(service):
    now = datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events

# Generate a PDF for the selected event
def generate_pdf(event_data):
    pdf_filename = "event_details.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.drawString(100, 750, f"Event Details: {event_data['summary']}")
    c.drawString(100, 730, f"Date: {event_data['start'].get('dateTime', event_data['start'].get('date'))}")
    c.drawString(100, 710, f"Location: {event_data.get('location', 'Not specified')}")
    c.drawString(100, 690, "Action Items:")
    c.drawString(120, 670, "- Set up the event space")
    c.drawString(120, 650, "- Ensure all equipment is ready")
    c.drawString(120, 630, "- Assign staff responsibilities")
    c.save()
    return pdf_filename

# Streamlit app layout
st.set_page_config(page_title="Moldova for Peace Hub", layout="centered")

# Sidebar for navigation
page = st.sidebar.selectbox("Navigation", ["Booking Form", "Admin Panel", "Staff View"])

# Google Calendar Authentication
creds = authenticate_google()
service = build('calendar', 'v3', credentials=creds)

# --- Booking Form ---
if page == "Booking Form":
    st.title("Request for Space Booking")
    with st.form("booking_form"):
        event_date = st.date_input("Choose the event date", datetime.now())
        start_time = st.time_input("Choose start time", datetime.now().time())

        duration_type = st.radio("Choose the duration type", ["Hours", "Minutes"])
        if duration_type == "Hours":
            duration_value = st.number_input("Number of hours", min_value=1, max_value=4)
        else:
            duration_value = st.number_input("Number of minutes", min_value=10, max_value=59)

        event_type = st.selectbox("Type of activity", ["Event", "Community Activity", "Work Hub", "Laboratory"])
        event_title = st.text_input("Title of the activity" if event_type in ["Event", "Community Activity"] else "Name of the person booking")
        person_name = st.text_input("Name of the person booking")
        attendees = st.number_input("Number of people attending", min_value=1, max_value=150 if event_type in ["Event", "Community Activity"] else 30)
        description = st.text_area("Short description of the event")

        equipment_needed = st.multiselect("Select equipment needed", ["Projector", "Microphone", "Speakers", "Laptop", 
                                                                     "Soldering Station", "Sewing Machine"])
        staff_assistance = st.multiselect("Need logistical assistance?", ["Sound technician", "Setup assistance", "Cleanup crew"], max_selections=3)
        media_consent = st.radio("Will there be filming/photography?", ["Yes", "No"])

        email = st.text_input("Email address")
        phone_number = st.text_input("Phone number")
        alt_phone_number = st.text_input("Alternative phone number")
        alt_contact_name = st.text_input("Alternative contact person")
        
        submitted = st.form_submit_button("Submit Request")
    
    if submitted:
        st.success("Your request has been submitted!")
        # Add Google Calendar event here if necessary

# --- Admin Panel ---
elif page == "Admin Panel":
    st.title("Admin Panel - Manage Bookings")
    events = list_calendar_events(service)

    if events:
        for event in events:
            st.write(f"Event: {event['summary']} | Start: {event['start'].get('dateTime', event['start'].get('date'))}")
            if st.button(f"Generate PDF for {event['summary']}"):
                pdf_path = generate_pdf(event)
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(label="Download Event PDF", data=pdf_file, file_name="event_details.pdf")
    else:
        st.write("No upcoming events found.")

# --- Staff View ---
elif page == "Staff View":
    st.title("Staff View - Upcoming Events")
    events = list_calendar_events(service)

    if events:
        for event in events:
            st.write(f"Event: {event['summary']} - Date: {event['start'].get('dateTime', event['start'].get('date'))}")
    else:
        st.write("No events found.")
