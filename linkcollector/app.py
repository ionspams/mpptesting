import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re

# Google Sheets credentials setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("your_credentials.json", scope)
client = gspread.authorize(creds)

# Open your Google Sheet by ID
SHEET_ID = 'your_google_sheet_id'
sheet = client.open_by_key(SHEET_ID).sheet1

# Function to extract links from the text
def extract_links(text):
    url_regex = r'https?://[^\s]+'
    return re.findall(url_regex, text)

# Function to summarize text (first sentence)
def summarize_text(text):
    sentences = text.split('. ')
    return sentences[0] + '.' if sentences else text

# Function to segment text into paragraphs
def segment_text(text, max_chunk_size=750):
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    segments = []
    for paragraph in paragraphs:
        sentences = paragraph.split('. ')
        current_segment = ''
        for sentence in sentences:
            if len(current_segment) + len(sentence) + 2 <= max_chunk_size:
                current_segment += sentence + '. '
            else:
                segments.append(current_segment.strip())
                current_segment = sentence + '. '
        if current_segment:
            segments.append(current_segment.strip())
    return segments

# Function to create expandable sections for each chunk
def create_expandable_sections(title, link, content):
    # Display the clickable link title
    st.markdown(f"### [{title}]({link})", unsafe_allow_html=True)
    
    # Create the Read More section for the content
    with st.expander("Read more"):
        for segment in segment_text(content):
            st.write(segment)
        
        # Display the link again for convenience
        st.markdown(f"[{link}]({link})", unsafe_allow_html=True)

# Fetch data from the Google Sheet
def get_sheet_data():
    rows = sheet.get_all_records()
    return rows

# Streamlit app
st.title("My ChatGPT Links")

# Fetch and display all data
sheet_data = get_sheet_data()

# Loop through all the rows in the Google Sheet and display them
for row in sheet_data:
    link = row['Link']
    title = row['Title']
    content = row['Content']
    create_expandable_sections(title, link, content)
