import streamlit as st
import re

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
def create_expandable_sections(text, links):
    summary = summarize_text(text)
    st.write(f"**{summary[:30]}...**")

    with st.expander("Read more"):
        for segment in segment_text(text):
            st.write(segment)
        
        # Display the links
        for link in links:
            st.markdown(f"[{link}]({link})", unsafe_allow_html=True)

# Streamlit app
st.title("My ChatGPT Links")

# Form to input text and links
with st.form("link_form"):
    input_text = st.text_area("Enter Title, Text, and Links", height=150)
    submitted = st.form_submit_button("Add Link")

if submitted and input_text:
    links = extract_links(input_text)
    create_expandable_sections(input_text, links)
