import streamlit as st
import requests
import qrcode
from PIL import Image
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
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(long_url)
                qr.make(fit=True)

                img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

                # Save the image to a buffer
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                buf.seek(0)

                # Display the QR code
                st.image(buf, caption="QR Code", use_column_width=True)
            except Exception as e:
                st.error(f"Error generating QR code: {e}")
                st.text(f"Exception details: {e}")
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
                        qr_response = requests.get(f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink_id}/qr", headers=headers)

                        if qr_response.status_code == 200:
                            qr_code_url = qr_response.json()["qr_code"]
                            st.success("QR Code generated successfully")
                            st.image(qr_code_url, caption="QR Code")
                        else:
                            st.error(f"Error generating QR code: {qr_response.status_code} - {qr_response.text}")
                    else:
                        st.error(f"Error: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"Error processing request: {e}")
                    st.text(f"Exception details: {e}")

st.sidebar.markdown("[Get your Bitly API Key](https://dev.bitly.com/)")
