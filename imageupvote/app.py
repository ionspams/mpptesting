import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# GitHub Repository Details
RAW_GITHUB_URL = "https://raw.githubusercontent.com/ionspams/mpptesting/m4phub/imageupvote/"

# Function to fetch images from the specific 'imageupvote' folder
def fetch_images_from_github():
    # Assuming the images are directly under 'imageupvote' in your repository
    images = ["image1.jpg", "image2.png", "image3.jpeg"]  # Replace with actual image names or automate if you have many
    return [f"{RAW_GITHUB_URL}{img}" for img in images]

# Function to display the voting interface
def display_images_with_votes(image_urls):
    for image_url in image_urls:
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        st.image(image, use_column_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👍 Upvote", key=f"upvote_{image_url}"):
                st.session_state[image_url] = st.session_state.get(image_url, 0) + 1
        with col2:
            if st.button("👎 Downvote", key=f"downvote_{image_url}"):
                st.session_state[image_url] = st.session_state.get(image_url, 0) - 1
        
        st.write(f"Votes: {st.session_state.get(image_url, 0)}")

# Streamlit App UI
st.title("Pick and Choose - Image Upvote")

# Fetch and display images
images = fetch_images_from_github()

if images:
    display_images_with_votes(images)
else:
    st.write("No images found in the 'imageupvote' folder.")
