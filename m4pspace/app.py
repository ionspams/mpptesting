import streamlit as st
from datetime import datetime
import pandas as pd

# Temporary database to store requests
if 'requests' not in st.session_state:
    st.session_state['requests'] = []

# Helper function to display requests in a table
def display_requests():
    if st.session_state['requests']:
        df = pd.DataFrame(st.session_state['requests'])
        st.dataframe(df)
    else:
        st.write("No booking requests yet.")

# Streamlit page configuration
st.set_page_config(page_title="Moldova for Peace Hub", layout="centered")

# Sidebar navigation
page = st.sidebar.selectbox("Navigation", ["Booking Form", "Admin Panel", "Staff View"])

# --- Use Case 1: Booking Form ---
if page == "Booking Form":
    st.title("Request for Space Booking")

    with st.form("booking_form"):
        event_date = st.date_input("Choose the event date", datetime.now())
        start_time = st.time_input("Choose start time", datetime.now().time())

        duration_type = st.radio("Choose the duration type", ["Hours", "Minutes"])
        if duration_type == "Hours":
            duration_value = st.number_input("Number of hours", min_value=1, max_value=4, step=1)
        else:
            duration_value = st.number_input("Number of minutes", min_value=10, max_value=59, step=1)

        event_type = st.selectbox("Type of activity", ["Event", "Community Activity", "Work Hub", "Laboratory"])
        if event_type in ["Event", "Community Activity"]:
            event_title = st.text_input("Title of the activity")
        else:
            event_title = st.text_input("Name of the person booking")

        person_name = st.text_input("Name of the person booking this")
        if event_type in ["Event", "Community Activity"]:
            attendees = st.number_input("Number of people attending", min_value=1, max_value=150)
        else:
            attendees = st.number_input("Number of people attending", min_value=1, max_value=30)

        description = st.text_area("Short description of the event")

        equipment_needed = st.multiselect("Select equipment needed", ["Projector", "Microphone", "Speakers", "Laptop", 
                                                                     "Soldering Station", "Sewing Machine"])

        staff_assistance = st.multiselect("Need logistical assistance?", ["Sound technician", "Setup assistance", 
                                                                         "Cleanup crew"], max_selections=3)

        media_consent = st.radio("Will there be filming/photography?", ["Yes", "No"])
        if media_consent == "Yes":
            st.markdown("**You must agree to use our consent and branding forms.**")

        min_age = st.number_input("Minimum age of participants", min_value=0, max_value=150)
        max_age = st.number_input("Maximum age of participants", min_value=0, max_value=150)

        email = st.text_input("Email address")
        phone_number = st.text_input("Phone number")
        alt_phone_number = st.text_input("Alternative phone number")
        alt_contact_name = st.text_input("Alternative contact person")

        submitted = st.form_submit_button("Submit Request")

    if submitted:
        # Store the booking request
        st.session_state['requests'].append({
            "Event Date": event_date,
            "Start Time": start_time,
            "Duration": f"{duration_value} {duration_type}",
            "Event Type": event_type,
            "Title/Name": event_title,
            "Person Name": person_name,
            "Attendees": attendees,
            "Description": description,
            "Equipment Needed": ", ".join(equipment_needed),
            "Staff Assistance": ", ".join(staff_assistance),
            "Media Consent": media_consent,
            "Age Range": f"{min_age}-{max_age}",
            "Email": email,
            "Phone": phone_number,
            "Alternative Contact": alt_contact_name,
        })
        st.success("Your request has been submitted!")

# --- Use Case 2: Admin Panel ---
elif page == "Admin Panel":
    st.title("Admin Panel - Manage Bookings")

    if st.session_state['requests']:
        # Display the requests
        df = pd.DataFrame(st.session_state['requests'])
        request_to_review = st.selectbox("Select a request to review", df.index)
        request_details = df.loc[request_to_review]

        st.subheader("Request Details")
        st.write(request_details)

        # Admin actions: approve, reject, modify
        action = st.radio("Action", ["Approve", "Reject", "Modify"])
        if action == "Reject":
            reason = st.text_area("Reason for rejection")
        elif action == "Modify":
            st.text_input("Modify details here")

        if st.button("Submit Action"):
            if action == "Approve":
                st.success("Request approved!")
            elif action == "Reject" and reason:
                st.warning(f"Request rejected with reason: {reason}")
            elif action == "Modify":
                st.info("Request modified!")
    else:
        st.write("No requests to manage.")

# --- Use Case 3: Staff View ---
elif page == "Staff View":
    st.title("Staff View - Upcoming Events")

    # Display only approved requests
    st.write("View all upcoming events.")
    display_requests()

    # Staff can leave a comment for the admin
    if st.session_state['requests']:
        selected_event = st.selectbox("Select event to comment on", df.index)
        comment = st.text_area("Leave a comment for the admin")
        if st.button("Submit Comment"):
            st.success("Comment submitted to the admin!")
