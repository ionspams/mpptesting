import streamlit as st
import re
import gspread
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# Function to extract URLs from text
def extract_urls(text):
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    return url_pattern.findall(text)

# Function to get title from text (first 30 characters)
def get_title(text):
    return text[:30].strip()

# Function to connect to Google Sheets
def connect_to_sheets():
    creds = Credentials.from_authorized_user_info(info=st.secrets["gcp_service_account"])
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    client = gspread.authorize(creds)
    sheet = client.open(st.secrets["sheet_name"]).sheet1
    return sheet

# Function to save data to Google Sheets
def save_to_sheets(sheet, title, urls, content):
    sheet.append_row([title, ', '.join(urls), content])

# Function to load data from Google Sheets
def load_from_sheets(sheet):
    return sheet.get_all_values()[1:]  # Exclude header row

# Streamlit app
def main():
    st.title('URL Extractor App')

    # Connect to Google Sheets
    sheet = connect_to_sheets()

    # Input form
    user_input = st.text_area('Enter your text (including URLs):')
    if st.button('Submit'):
        urls = extract_urls(user_input)
        title = get_title(user_input)
        content = user_input[30:]  # Rest of the content

        # Save to Google Sheets
        save_to_sheets(sheet, title, urls, content)
        st.success('Data saved successfully!')

    # Display saved entries
    st.header('Saved Entries')
    entries = load_from_sheets(sheet)
    for entry in entries:
        title, urls, content = entry
        st.subheader(title)
        for url in urls.split(', '):
            st.markdown(f'[{url}]({url})')
        with st.expander('Read more'):
            st.write(content)

if __name__ == '__main__':
    main()
