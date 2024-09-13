import streamlit as st
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import io

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

# Hard-coded orders data
orders_data = [
    {
        'ticket_id': 'TICKET001',
        'phone_number': '+1234567890',
        'contact_person': 'John Doe',
        'warehouse_name': 'Warehouse A',
        'products': ['Product 1', 'Product 2'],
        'documents_required': 2
    },
    # Add 9 more orders
    {
        'ticket_id': 'TICKET002',
        'phone_number': '+0987654321',
        'contact_person': 'Jane Smith',
        'warehouse_name': 'Warehouse B',
        'products': ['Product 3', 'Product 4'],
        'documents_required': 1
    },
    # ... (add more orders as needed)
]

# Simulate 10 orders
for i in range(3, 11):
    orders_data.append({
        'ticket_id': f'TICKET00{i}',
        'phone_number': f'+10000000{i}',
        'contact_person': f'Contact Person {i}',
        'warehouse_name': f'Warehouse {chr(64+i)}',
        'products': [f'Product {i}', f'Product {i+1}'],
        'documents_required': i % 3 + 1
    })

# Create a DataFrame for easy access
orders_df = pd.DataFrame(orders_data)

# Session state initialization
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'selected_order' not in st.session_state:
    st.session_state.selected_order = None
if 'documents_uploaded' not in st.session_state:
    st.session_state.documents_uploaded = False

# Step 1: Select Order
if st.session_state.step == 1:
    st.title("📦 Pomoha Warehouse Distribution System")
    st.header("Step 1: Select Order")

    ticket_ids = orders_df['ticket_id'].tolist()
    selected_ticket = st.selectbox("Select a Ticket ID", ticket_ids)

    if st.button("Proceed"):
        st.session_state.selected_order = orders_df[orders_df['ticket_id'] == selected_ticket].iloc[0]
        st.session_state.step = 2
        st.experimental_rerun()

# Step 2: Upload Documents
elif st.session_state.step == 2:
    st.header("Step 2: Upload Documents")

    order = st.session_state.selected_order
    st.write(f"**Contact Person:** {order['contact_person']}")
    st.write(f"**Phone Number:** {order['phone_number']}")
    st.write(f"**Warehouse Name:** {order['warehouse_name']}")
    st.write(f"**Products:** {', '.join(order['products'])}")
    st.write(f"**Documents Required:** {order['documents_required']}")

    uploaded_files = st.file_uploader(
        f"Upload {order['documents_required']} Passport Documents",
        accept_multiple_files=True,
        type=['png', 'jpg', 'jpeg', 'pdf']
    )

    if uploaded_files and len(uploaded_files) == order['documents_required']:
        if st.button("Validate Documents"):
            # For the prototype, validation is automatic
            st.success("Documents validated successfully!")
            st.session_state.documents_uploaded = True
            st.session_state.step = 3
            st.experimental_rerun()
    else:
        st.warning(f"Please upload exactly {order['documents_required']} documents.")

# Step 3: Capture Signature
elif st.session_state.step == 3:
    st.header("Step 3: Capture Signature")

    st.write("Please sign below:")

    # Create a canvas for signature
    from streamlit_drawable_canvas import st_canvas

    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=2,
        stroke_color="#000000",
        background_color="#FFFFFF",
        height=150,
        width=400,
        drawing_mode="freedraw",
        key="canvas",
    )

    if st.button("Submit Signature"):
        if canvas_result.image_data is not None:
            st.session_state.signature = canvas_result.image_data
            st.session_state.step = 4
            st.experimental_rerun()
        else:
            st.warning("Please provide a signature.")

# Step 4: Generate Receipt with Watermark
elif st.session_state.step == 4:
    st.header("Receipt")

    order = st.session_state.selected_order

    # Get current date and time without seconds
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Create watermark text
    watermark_text = (
        f"Date: {current_datetime}\n"
        f"Contact Person: {order['contact_person']}\n"
        f"Warehouse: {order['warehouse_name']}\n"
        f"Products: {', '.join(order['products'])}"
    )

    # Create an image from the signature data
    signature_image = Image.fromarray(st.session_state.signature.astype('uint8'), 'RGBA')

    # Add watermark to the signature image
    draw = ImageDraw.Draw(signature_image)
    font = ImageFont.load_default()
    text_position = (10, 10)
    draw.text(text_position, watermark_text, fill="black", font=font)

    # Display the final image
    st.image(signature_image, caption="Beneficiary Signature with Watermark")

    # Optionally, allow downloading the image
    buf = io.BytesIO()
    signature_image.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="Download Receipt",
        data=byte_im,
        file_name="receipt.png",
        mime="image/png",
    )

    st.success("Process completed successfully!")
    if st.button("Start Over"):
        st.session_state.step = 1
        st.experimental_rerun()
