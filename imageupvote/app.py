import streamlit as st
import requests
from PIL import Image, UnidentifiedImageError
from io import BytesIO

# GitHub Repository Details
RAW_GITHUB_URL = "https://raw.githubusercontent.com/ionspams/mpptesting/m4phub/imageupvote/"

# Function to fetch image list from images.txt
def fetch_image_list():
    image_list_url = f"{RAW_GITHUB_URL}images.txt"
    response = requests.get(image_list_url)
    if response.status_code == 200:
        return response.text.splitlines()
    else:
        st.error("Failed to fetch image list.")
        return []

# Function to fetch and display images with voting options
def display_images_with_votes(image_urls):
    for image_name in image_urls:
        image_url = f"{RAW_GITHUB_URL}{image_name}"
        try:
            response = requests.get(image_url)
            response.raise_for_status()  # Check if the request was successful
            # Ensure content is an image
            if 'image' in response.headers['Content-Type']:
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
            else:
                st.error(f"Failed to load image {image_name}. Content is not an image.")
        except UnidentifiedImageError:
            st.error(f"Failed to open image {image_name}. The image format might be unsupported.")
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch image {image_name}. Error: {str(e)}")

# Streamlit App UI
st.title("Pick and Choose - Image Upvote")

# Fetch image list from GitHub
image_list = fetch_image_list()

if image_list:
    display_images_with_votes(image_list)
else:
    st.write("No images found or failed to load images.")
