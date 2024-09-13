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

# Define the translations
translations = {
    'en': {
        'title': "📦 Pomoha Warehouse Distribution System",
        'step1_title': "Step 1: Select Order",
        'select_ticket': "Select a Ticket ID",
        'proceed': "Proceed",
        'step2_title': "Step 2: Input Beneficiary Information",
        'contact_person': "Contact Person",
        'phone_number': "Phone Number",
        'warehouse_name': "Warehouse Name",
        'vouchers': "Vouchers",
        'family_size': "Family Size",
        'passport_input': "Enter passport serial and number for each person (one per line). Number of entries required: {family_size}",
        'proceed_to_signature': "Proceed to Signature",
        'step3_title': "Step 3: Capture Signature",
        'please_sign': "Please sign below:",
        'submit_signature': "Submit Signature",
        'step4_title': "Receipt",
        'download_receipt': "Download Receipt",
        'process_completed': "Process completed successfully!",
        'start_over': "Start Over",
        'warning_passport_numbers': "Please enter exactly {family_size} passport numbers.",
        'warning_signature': "Please provide a signature.",
        'receipt_caption': "Beneficiary Signature with Receipt Information",
    },
    'ru': {
        'title': "📦 Система распределения складов Pomoha",
        'step1_title': "Шаг 1: Выберите заказ",
        'select_ticket': "Выберите идентификатор билета",
        'proceed': "Продолжить",
        'step2_title': "Шаг 2: Введите информацию о получателе",
        'contact_person': "Контактное лицо",
        'phone_number': "Номер телефона",
        'warehouse_name': "Название склада",
        'vouchers': "Ваучеры",
        'family_size': "Размер семьи",
        'passport_input': "Введите серию и номер паспорта для каждого человека (по одному на строку). Требуется записей: {family_size}",
        'proceed_to_signature': "Перейти к подписи",
        'step3_title': "Шаг 3: Подпишите",
        'please_sign': "Пожалуйста, подпишите ниже:",
        'submit_signature': "Отправить подпись",
        'step4_title': "Квитанция",
        'download_receipt': "Скачать квитанцию",
        'process_completed': "Процесс успешно завершен!",
        'start_over': "Начать заново",
        'warning_passport_numbers': "Пожалуйста, введите ровно {family_size} номеров паспортов.",
        'warning_signature': "Пожалуйста, предоставьте подпись.",
        'receipt_caption': "Подпись получателя с информацией о квитанции",
    },
    'ro': {
        'title': "📦 Sistem de distribuție Pomoha pentru depozit",
        'step1_title': "Pasul 1: Selectați comanda",
        'select_ticket': "Selectați un ID de bilet",
        'proceed': "Continuă",
        'step2_title': "Pasul 2: Introduceți informațiile beneficiarului",
        'contact_person': "Persoană de contact",
        'phone_number': "Număr de telefon",
        'warehouse_name': "Numele depozitului",
        'vouchers': "Vouchere",
        'family_size': "Dimensiunea familiei",
        'passport_input': "Introduceți seria și numărul pașaportului pentru fiecare persoană (câte unul pe linie). Număr de intrări necesare: {family_size}",
        'proceed_to_signature': "Continuați la semnătură",
        'step3_title': "Pasul 3: Capturați semnătura",
        'please_sign': "Vă rugăm să semnați mai jos:",
        'submit_signature': "Trimiteți semnătura",
        'step4_title': "Chitanță",
        'download_receipt': "Descărcați chitanța",
        'process_completed': "Proces finalizat cu succes!",
        'start_over': "Începeți din nou",
        'warning_passport_numbers': "Vă rugăm să introduceți exact {family_size} numere de pașaport.",
        'warning_signature': "Vă rugăm să furnizați o semnătură.",
        'receipt_caption': "Semnătura beneficiarului cu informații despre chitanță",
    }
}

# Function to get the translation for the selected language
def t(key):
    return translations[st.session_state.lang].get(key, key)

# Sidebar for language selection
st.sidebar.title("Language")
language = st.sidebar.radio("", ('English', 'Русский', 'Română'))

# Map language selection to language codes
lang_codes = {'English': 'en', 'Русский': 'ru', 'Română': 'ro'}
st.session_state.lang = lang_codes[language]

# Hard-coded orders data
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

# Define a list of vouchers
vouchers_list = [
    'Voucher Linella',
    'Voucher Pharmacia Family',
    'Voucher Grocery',
    'Voucher Clothing Store',
    'Voucher Electronics',
    'Voucher Gas Station'
]

# Simulate additional orders
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
if 'passport_warning' not in st.session_state:
    st.session_state.passport_warning = ''
if 'signature_warning' not in st.session_state:
    st.session_state.signature_warning = ''

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
        st.session_state.passport_warning = t('warning_passport_numbers').format(family_size=order['family_size'])

def submit_signature():
    canvas_result = st.session_state.canvas_result
    if canvas_result.image_data is not None:
        st.session_state.signature = canvas_result.image_data
        st.session_state.step = 4
    else:
        st.session_state.signature_warning = t('warning_signature')

def start_over():
    st.session_state.step = 1
    st.session_state.selected_order = None
    st.session_state.documents_input = []
    st.session_state.signature = None

# Step 1: Select Order
if st.session_state.step == 1:
    st.title(t('title'))
    st.header(t('step1_title'))

    ticket_ids = orders_df['ticket_id'].tolist()
    st.selectbox(t('select_ticket'), ticket_ids, key='selected_ticket')

    st.button(t('proceed'), on_click=proceed_to_step2)

# Step 2: Input Beneficiary Information
elif st.session_state.step == 2:
    st.header(t('step2_title'))

    order = st.session_state.selected_order
    st.write(f"**{t('contact_person')}:** {order['contact_person']}")
    st.write(f"**{t('phone_number')}:** {order['phone_number']}")
    st.write(f"**{t('warehouse_name')}:** {order['warehouse_name']}")
    st.write(f"**{t('vouchers')}:** {', '.join(order['vouchers'])}")
    st.write(f"**{t('family_size')}:** {order['family_size']}")

    st.text_area(
        t('passport_input').format(family_size=order['family_size']),
        key="passport_numbers"
    )

    if st.session_state.passport_warning:
        st.warning(st.session_state.passport_warning)
        st.session_state.passport_warning = ''

    st.button(t('proceed_to_signature'), on_click=proceed_to_step3)

# Step 3: Capture Signature
elif st.session_state.step == 3:
    st.header(t('step3_title'))

    st.write(t('please_sign'))

    # Create a blank canvas for the signature
    canvas_width = 600
    canvas_height = 300

    canvas_result = st_canvas(
        fill_color="rgba(0, 0, 0, 0)",  # No fill color
        stroke_width=2,
        stroke_color="#000000",
        background_color="#FFFFFF",
        height=canvas_height,
        width=canvas_width,
        drawing_mode="freedraw",
        key="canvas",
    )

    st.session_state.canvas_result = canvas_result

    if st.session_state.signature_warning:
        st.warning(st.session_state.signature_warning)
        st.session_state.signature_warning = ''

    st.button(t('submit_signature'), on_click=submit_signature)

# Step 4: Display Receipt
elif st.session_state.step == 4:
    st.header(t('step4_title'))

    if st.session_state.signature is not None:
        # Convert the signature image data to a PIL Image
        signature_array = st.session_state.signature
        signature_image = Image.fromarray((signature_array).astype('uint8'), mode="RGBA")

        # Create watermark text with all required information
        order = st.session_state.selected_order
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")
        watermark_text = (
            f"{t('title')}\n"
            f"{t('step4_title')}\n"
            f"{t('contact_person')}: {order['contact_person']}\n"
            f"{t('phone_number')}: {order['phone_number']}\n"
            f"{t('warehouse_name')}: {order['warehouse_name']}\n"
            f"{t('family_size')}: {order['family_size']}\n"
            f"{t('vouchers')}: {', '.join(order['vouchers'])}\n"
            f"Documents: {', '.join(st.session_state.documents_input)}\n"
            f"Date: {current_datetime}"
        )

        # Create an image for the watermark text
        watermark_image = Image.new('RGB', (signature_image.width, signature_image.height), color='white')
        draw = ImageDraw.Draw(watermark_image)

        # Use default font to avoid errors
        font_size = 16
        font = ImageFont.load_default()
        text_position = (10, 10)
        draw.multiline_text(text_position, watermark_text, fill="black", font=font)

        # Combine the watermark image and the signature image
        combined_image = watermark_image.convert("RGBA")
        combined_image.alpha_composite(signature_image)

        # Display the final image
        st.image(combined_image, caption=t('receipt_caption'))

        # Optionally, allow downloading the image
        buf = io.BytesIO()
        combined_image.save(buf, format="PNG")
        byte_im = buf.getvalue()

        st.download_button(
            label=t('download_receipt'),
            data=byte_im,
            file_name="receipt.png",
            mime="image/png",
        )

        st.success(t('process_completed'))
    else:
        st.error(t('warning_signature'))

    st.button(t('start_over'), on_click=start_over)
