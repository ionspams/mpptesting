import streamlit as st
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import io
import numpy as np
import random

# Import st_canvas correctly
from streamlit_drawable_canvas import st_canvas

# Set page configuration
st.set_page_config(page_title="Pomoha Warehouse Distribution", page_icon="📦", layout="centered")

# Apply custom CSS for colors (blue and yellow)
st.markdown("""
    <style>
    .reportview-container {
        background-color: #f0f2f6;
    }
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)

# Define a list of vouchers
vouchers_list = [
    'Voucher Linella',
    'Voucher Pharmacia Family',
    'Voucher Grocery',
    'Voucher Clothing Store',
    'Voucher Electronics',
    'Voucher Gas Station'
]

# Hard-coded orders data with vouchers
orders_data = [
    {
        'ticket_id': 'TICKET001',
        'phone_number': '+1234567890',
        'contact_person': 'John Doe',
        'warehouse_name': 'Warehouse A',
        'vouchers': ['Voucher Linella', 'Voucher Pharmacia Family'],
        'family_size': 2  # Number of people in the family
    },
    {
        'ticket_id': 'TICKET002',
        'phone_number': '+0987654321',
        'contact_person': 'Jane Smith',
        'warehouse_name': 'Warehouse B',
        'vouchers': ['Voucher Grocery', 'Voucher Clothing Store'],
        'family_size': 1  # Number of people in the family
    },
    # Additional orders
]

# Simulate 10 orders
for i in range(3, 11):
    orders_data.append({
        'ticket_id': f'TICKET00{i}',
        'phone_number': f'+10000000{i}',
        'contact_person': f'Contact Person {i}',
        'warehouse_name': f'Warehouse {chr(64+i)}',
        'vouchers': random.sample(vouchers_list, k=random.randint(2, len(vouchers_list))),
        'family_size': i % 3 + 1  # Random family sizes for demo
    })

# Create a DataFrame for easy access
orders_df = pd.DataFrame(orders_data)

# Session state initialization
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'selected_order' not in st.session_state:
    st.session_state.selected_order = None
if 'documents_input' not in st.session_state:
    st.session_state.documents_input = []
if 'signature' not in st.session_state:
    st.session_state.signature = None

# Define callback functions
def proceed_to_step2():
    selected_ticket = st.session_state.selected_ticket
    st.session_state.selected_order = orders_df[orders_df['ticket_id'] == selected_ticket].iloc[0]
    st.session_state.step = 2

def proceed_to_step3():
    passport_numbers = st.session_state.passport_numbers.strip()
    passports_entered = [line.strip() for line in passport_numbers.split('\n') if line.strip()]
    order = st.session_state.selected_order
    if len(passports_entered) == order['family_size']:
        st.session_state.documents_input = passports_entered
        st.session_state.step = 3
    else:
        st.session_state.passport_warning = f"Please enter exactly {order['family_size']} passport numbers."

def submit_signature():
    canvas_result = st.session_state.canvas_result
    if canvas_result.image_data is not None:
        st.session_state.signature = canvas_result.image_data
        st.session_state.step = 4
    else:
        st.session_state.signature_warning = "Please provide a signature."

def start_over():
    st.session_state.step = 1
    st.session_state.selected_order = None
    st.session_state.documents_input = []
    st.session_state.signature = None

# Step 1: Select Order
if st.session_state.step == 1:
    st.title("📦 Pomoha Warehouse Distribution System")
    st.header("Step 1: Select Order")

    ticket_ids = orders_df['ticket_id'].tolist()
    st.session_state.selected_ticket = st.selectbox("Select a Ticket ID", ticket_ids, key='selected_ticket')

    st.button("Proceed", on_click=proceed_to_step2)

# Step 2: Input Beneficiary Information
elif st.session_state.step == 2:
    st.header("Step 2: Input Beneficiary Information")

    order = st.session_state.selected_order
    st.write(f"**Contact Person:** {order['contact_person']}")
    st.write(f"**Phone Number:** {order['phone_number']}")
    st.write(f"**Warehouse Name:** {order['warehouse_name']}")
    st.write(f"**Vouchers:** {', '.join(order['vouchers'])}")
    st.write(f"**Family Size:** {order['family_size']} (Number of passport numbers required)")

    st.session_state.passport_numbers = st.text_area(
        f"Enter passport serial and number for each person (one per line). Number of entries required: {order['family_size']}",
        key="passport_numbers"
    )

    if 'passport_warning' in st.session_state:
        st.warning(st.session_state.passport_warning)
        del st.session_state.passport_warning

    st.button("Proceed to Signature", on_click=proceed_to_step3)

# Step 3: Capture Signature
elif st.session_state.step == 3:
    st.header("Step 3: Capture Signature")

    st.write("Please sign below:")

    order = st.session_state.selected_order

    # Get current date and time without seconds
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Create watermark text with all required information
    watermark_text = (
        f"Date: {current_datetime}\n"
        f"Ticket ID: {order['ticket_id']}\n"
        f"Contact Person: {order['contact_person']}\n"
        f"Phone Number: {order['phone_number']}\n"
        f"Warehouse: {order['warehouse_name']}\n"
        f"Family Size: {order['family_size']}\n"
        f"Vouchers: {', '.join(order['vouchers'])}\n"
        f"Documents: {', '.join(st.session_state.documents_input)}"
    )

    # Adjust canvas dimensions
    canvas_width = 600  # Increased width for better readability
    canvas_height = 500  # Increased height to accommodate more text

    # Create an image for the watermark text
    watermark_image = Image.new('RGBA', (canvas_width, canvas_height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(watermark_image)

    # Use default font to avoid errors
    font_size = 16
    font = ImageFont.load_default()
    text_position = (10, 10)
    draw.multiline_text(text_position, watermark_text, fill="black", font=font)

    # Create a canvas component with the watermark image as background
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 3)",  # Transparent fill
        stroke_width=2,
        stroke_color="#000000",
        background_image=watermark_image,
        update_streamlit=True,
        height=canvas_height,
        width=canvas_width,
        drawing_mode="freedraw",
        key="canvas",
    )

    st.session_state.canvas_result = canvas_result

    if 'signature_warning' in st.session_state:
        st.warning(st.session_state.signature_warning)
        del st.session_state.signature_warning

    st.button("Submit Signature", on_click=submit_signature)

# Step 4: Display Receipt
elif st.session_state.step == 4:
    st.header("Receipt")

    if st.session_state.signature is not None:
        # Convert the image data to a PIL Image
        signature_array = st.session_state.signature
        signed_image = Image.fromarray((signature_array).astype('uint8'), mode="RGBA")

        # Display the final image
        st.image(signed_image, caption="Beneficiary Signature with Receipt Information")

        # Optionally, allow downloading the image
        buf = io.BytesIO()
        signed_image.save(buf, format="PNG")
        byte_im = buf.getvalue()

        st.download_button(
            label="Download Receipt",
            data=byte_im,
            file_name="receipt.png",
            mime="image/png",
        )

        st.success("Process completed successfully!")
    else:
        st.error("No signature found. Please go back and provide a signature.")

    st.button("Start Over", on_click=start_over)
