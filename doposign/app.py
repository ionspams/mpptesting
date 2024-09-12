import streamlit as st
import streamlit_drawable_canvas as st_canvas
from datetime import datetime
import random

# Set up Dopamoha color theme
st.set_page_config(page_title="Pomoha System", page_icon=":package:", layout="wide")

# Mock data for 10 warehouse orders
orders = [
    {"ticket_id": f"TCK-{random.randint(1000, 9999)}", 
     "contact_person": f"Person {i}", 
     "phone_number": f"+12345678{i}", 
     "products": ["Rice", "Sugar", "Oil", "Pasta"], 
     "warehouse": "Warehouse A"} 
    for i in range(10)
]

# Session state to store selected order and passport inputs
if 'selected_order' not in st.session_state:
    st.session_state.selected_order = None
if 'passports' not in st.session_state:
    st.session_state.passports = [""] * 5

st.title("Pomoha Warehouse Distribution Prototype")
st.markdown("## Order and Passport Validation")

# Step 1: Select an Order
order_names = [f"{order['ticket_id']} - {order['contact_person']}" for order in orders]
selected_order = st.selectbox("Select an Order", order_names)

if selected_order:
    # Fetch the order based on selection
    order_index = order_names.index(selected_order)
    st.session_state.selected_order = orders[order_index]
    st.write("### Order Details")
    st.write(f"Ticket ID: {st.session_state.selected_order['ticket_id']}")
    st.write(f"Contact Person: {st.session_state.selected_order['contact_person']}")
    st.write(f"Phone Number: {st.session_state.selected_order['phone_number']}")
    st.write(f"Products: {', '.join(st.session_state.selected_order['products'])}")
    st.write(f"Warehouse: {st.session_state.selected_order['warehouse']}")

# Step 2: Enter Passport Numbers (up to 5)
st.markdown("## Enter Passport Numbers")
passports = st.session_state.passports
for i in range(5):
    passports[i] = st.text_input(f"Passport {i+1}", passports[i])

# Step 3: Validation (mock validation)
st.markdown("### Validation Step")
validate_button = st.button("Validate Passports")
if validate_button:
    st.success("Passports validated successfully!")

# Step 4: Signature Canvas with Watermark
st.markdown("## Signature")
canvas_width = 600
canvas_height = 400

# Draw canvas
signature_canvas = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Fill color with transparency
    stroke_width=2,
    stroke_color="#000000",
    background_color="#FFFFFF",
    height=canvas_height,
    width=canvas_width,
    drawing_mode="freedraw",
    key="canvas",
)

# Display watermark information on the canvas
if st.session_state.selected_order:
    order_details = st.session_state.selected_order
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    watermark = f"""
    Date: {current_time}\n
    Contact Person: {order_details['contact_person']}\n
    Warehouse: {order_details['warehouse']}\n
    Products: {', '.join(order_details['products'])}
    """
    st.write(f"### Watermark Details:\n{watermark}")

    # Simulate adding the watermark to the canvas (for demo purposes)
    st.markdown(f"Watermark: **{watermark}**")

# Step 5: Save signature or take action on the canvas data
if st.button("Submit Signature"):
    if signature_canvas.image_data is not None:
        st.success("Signature captured and saved!")
    else:
        st.error("Please sign on the canvas before submitting.")

# Step 6: Display a thank you message
st.markdown("### Thank You for using Pomoha Warehouse Distribution System Prototype!")
