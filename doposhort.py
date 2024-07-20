import streamlit as st
import requests

st.title("URL Shortener with Custom Suffix")

# Sidebar settings for Bitly API key
st.sidebar.header("Settings")
bitly_api_key = st.sidebar.text_input("Bitly API Key", type="password")

if not bitly_api_key:
    st.warning("Please enter your Bitly API Key in the sidebar settings.")
    st.stop()

# Main section for URL input and custom suffix
long_url = st.text_input("Enter the long URL")
custom_suffix = st.text_input("Enter custom suffix (optional)")

if st.button("Shorten URL"):
    if not long_url:
        st.error("Please enter a long URL.")
    else:
        headers = {
            "Authorization": f"Bearer {bitly_api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "long_url": long_url,
            "domain": "bit.ly"
        }

        if custom_suffix:
            data["custom_bitlinks"] = [f"bit.ly/{custom_suffix}"]

        response = requests.post("https://api-ssl.bitly.com/v4/shorten", headers=headers, json=data)

        if response.status_code == 200:
            short_url = response.json()["link"]
            st.success(f"Short URL: {short_url}")
            st.markdown(f"[{short_url}]({short_url})")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")

st.sidebar.markdown("[Get your Bitly API Key](https://dev.bitly.com/)")
