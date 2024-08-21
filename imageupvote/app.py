import streamlit as st
import os
import requests
from PIL import Image
from io import BytesIO

# GitHub Repository Details
GITHUB_REPO = "https://github.com/<username>/<repository>"  # Replace with your GitHub repo URL
RAW_GITHUB_URL = "https://raw.githubusercontent.com/<username>/<repository>/main/"  # Replace <username> and <repository> with your details

# Function to fetch images from a specific folder in the GitHub repo
def fetch_images_from_github(folder):
    url = f"{RAW_GITHUB_URL}{folder}/"
    response = requests.get(url)
    images = []
    if response.status_code == 200:
        images = [f"{url}{img}" for img in response.text.splitlines() if img.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    return images

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
st.title("Pick and Choose")

# Sidebar for selecting project folders
project_folder = st.sidebar.selectbox("Select Project Folder", os.listdir("path_to_local_repo"))  # Replace with dynamic GitHub fetch
st.sidebar.write("Select a project to view images and vote")
st.sidebar.button("Hide Sidebar")

if project_folder:
    st.write(f"Project: {project_folder}")
    images = fetch_images_from_github(project_folder)
    
    if images:
        display_images_with_votes(images)
    else:
        st.write("No images found in this project folder.")

# Run this app with `streamlit run app.py` and replace the GitHub URL parts with actual details.
