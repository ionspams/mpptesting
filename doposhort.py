import streamlit as st
import requests
import segno
import io

st.title("URL Shortener with Custom Suffix and QR Code")

# Sidebar settings for Bitly API key (optional)
st.sidebar.header("Settings")
bitly_api_key = st.sidebar.text_input("Bitly API Key (optional)", type="password")

# Main section for URL input and custom suffix
long_url = st.text_input("Enter the long URL")
custom_suffix = st.text_input("Enter custom suffix (optional)")
qr_only = st.checkbox("Generate QR Code only (without shortening URL)")

if st.button("Generate"):
    if not long_url:
        st.error("Please enter a long URL.")
    else:
        if qr_only:
            try:
                # Generate QR code without shortening URL
                qr = segno.make(long_url)
                buf = io.BytesIO()
                qr.save(buf, kind='png')
                buf.seek(0)
                buf.name = "qrcode.png"
                
                # Display the QR code
                st.image(buf, caption="QR Code", use_column_width=True)
            except Exception as e:
                st.error(f"Error generating QR code: {e}")
        else:
            if not bitly_api_key:
                st.warning("Please enter your Bitly API Key in the sidebar settings to shorten URLs.")
            else:
                headers = {
                    "Authorization": f"Bearer {bitly_api_key}",
                    "Content-Type": "application/json"
                }

                try:
                    # Step 1: Shorten the URL
                    data = {
                        "long_url": long_url,
                        "domain": "bit.ly"
                    }

                    response = requests.post("https://api-ssl.bitly.com/v4/shorten", headers=headers, json=data)

                    if response.status_code == 200:
                        short_url = response.json()["link"]
                        bitlink_id = response.json()["id"]
                        st.success(f"Short URL: {short_url}")
                        st.markdown(f"[{short_url}]({short_url})")

                        # Step 2: Add custom suffix if provided
                        if custom_suffix:
                            custom_data = {
                                "custom_bitlink": f"bit.ly/{custom_suffix}",
                                "bitlink_id": bitlink_id
                            }

                            custom_response = requests.post("https://api-ssl.bitly.com/v4/custom_bitlinks", headers=headers, json=custom_data)

                            if custom_response.status_code == 200:
                                custom_short_url = custom_response.json()["custom_bitlink"]
                                st.success(f"Custom Short URL: {custom_short_url}")
                                st.markdown(f"[{custom_short_url}]({custom_short_url})")
                            else:
                                st.error(f"Error creating custom short URL: {custom_response.status_code} - {custom_response.text}")

                        # Step 3: Generate QR code for the shortened URL
                        qr = segno.make(short_url)
                        buf = io.BytesIO()
                        qr.save(buf, kind='png')
                        buf.seek(0)
                        buf.name = "qrcode.png"

                        st.success("QR Code generated successfully")
                        st.image(buf, caption="QR Code", use_column_width=True)
                    else:
                        st.error(f"Error: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"Error processing request: {e}")

st.sidebar.markdown("[Get your Bitly API Key](https://dev.bitly.com/)")
