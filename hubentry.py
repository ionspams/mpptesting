import streamlit as st
import matplotlib.pyplot as plt

# Dictionary for multilingual text
texts = {
    "welcome": {
        "en": "Welcome to the Moldova for Peace Hub Entry-Stand",
        "ro": "Bun venit la Standul de Intrare Moldova pentru Pace",
        "uk": "Ласкаво просимо до стенду входу Молдова за мир",
        "ru": "Добро пожаловать на стенд входа Молдова за мир"
    },
    "select_language": {
        "en": "Please select your language to continue:",
    },
    "visitor_type": {
        "en": "Are you an individual or representing an organization?",
        "ro": "Sunteți o persoană fizică sau reprezentați o organizație?",
        "uk": "Ви фізична особа чи представляєте організацію?",
        "ru": "Вы физическое лицо или представляете организацию?"
    },
    "individual": {
        "en": "Individual",
        "ro": "Persoană fizică",
        "uk": "Фізична особа",
        "ru": "Физическое лицо"
    },
    "organization": {
        "en": "Organization",
        "ro": "Organizație",
        "uk": "Організація",
        "ru": "Организация"
    },
    "do_you_have_account": {
        "en": "Do you or your family members have an account with Dopamoha?",
        "ro": "Aveți dvs. sau membrii familiei dvs. un cont pe Dopamoha?",
        "uk": "Чи є у вас або членів вашої родини обліковий запис на Dopamoha?",
        "ru": "Есть ли у вас или членов вашей семьи учетная запись на Dopamoha?"
    },
    "yes": {
        "en": "Yes",
        "ro": "Da",
        "uk": "Так",
        "ru": "Да"
    },
    "no": {
        "en": "No",
        "ro": "Nu",
        "uk": "Ні",
        "ru": "Нет"
    },
    "phone_number": {
        "en": "Enter your phone number:",
        "ro": "Introduceți numărul dvs. de telefon:",
        "uk": "Введіть свій номер телефону:",
        "ru": "Введите свой номер телефона:"
    },
    "choose_names": {
        "en": "Select the names of the visitors:",
        "ro": "Selectați numele vizitatorilor:",
        "uk": "Виберіть імена відвідувачів:",
        "ru": "Выберите имена посетителей:"
    },
    "number_of_visitors": {
        "en": "Number of visitors:",
        "ro": "Numărul de vizitatori:",
        "uk": "Кількість відвідувачів:",
        "ru": "Количество посетителей:"
    },
    "provide_name": {
        "en": "Enter your name:",
        "ro": "Introduceți numele dvs.:",
        "uk": "Введіть своє ім'я:",
        "ru": "Введите свое имя:"
    },
    "select_organization": {
        "en": "Select your organization:",
        "ro": "Selectați organizația dvs.:",
        "uk": "Виберіть свою організацію:",
        "ru": "Выберите вашу организацию:"
    },
    "select_position": {
        "en": "Select your position:",
        "ro": "Selectați poziția dvs.:",
        "uk": "Виберіть свою позицію:",
        "ru": "Выберите свою позицию:"
    },
    "project_manager": {
        "en": "Project Manager",
        "ro": "Manager de Proiect",
        "uk": "Менеджер проекту",
        "ru": "Менеджер проекта"
    },
    "country_director": {
        "en": "Country Director",
        "ro": "Director de Țară",
        "uk": "Директор країни",
        "ru": "Директор страны"
    },
    "monitoring_officer": {
        "en": "Monitoring Officer",
        "ro": "Ofițer de Monitorizare",
        "uk": "Офіцер моніторингу",
        "ru": "Офицер мониторинга"
    },
    "audit_officer": {
        "en": "Audit Officer",
        "ro": "Ofițer de Audit",
        "uk": "Аудитор",
        "ru": "Аудитор"
    },
    "data_enumerator": {
        "en": "Data Enumerator",
        "ro": "Enumărător de Date",
        "uk": "Оператор даних",
        "ru": "Оператор данных"
    },
    "visit_purpose": {
        "en": "Please select your purpose(s) of visit:",
        "ro": "Vă rugăm să selectați scopul/scopurile vizitei dvs.:",
        "uk": "Будь ласка, виберіть мету/мети вашого візиту:",
        "ru": "Пожалуйста, выберите цель/цели вашего визита:"
    },
    "receive_assistance": {
        "en": "Receive Assistance",
        "ro": "Primirea Asistenței",
        "uk": "Отримання допомоги",
        "ru": "Получить помощь"
    },
    "just_visit": {
        "en": "Just Visit",
        "ro": "Doar Vizita",
        "uk": "Просто відвідати",
        "ru": "Просто посетить"
    },
    "attend_event": {
        "en": "Attend an Event",
        "ro": "Participați la un Eveniment",
        "uk": "Відвідати захід",
        "ru": "Посетить мероприятие"
    },
    "attend_workshop": {
        "en": "Attend a Workshop or Focus Group",
        "ro": "Participați la un Atelier sau Grup de Lucru",
        "uk": "Відвідати семінар або фокус-групу",
        "ru": "Посетить мастер-класс или фокус-группу"
    },
    "offer_regular_service": {
        "en": "Offer a Regular Service",
        "ro": "Oferiți un Serviciu Regular",
        "uk": "Пропонувати регулярну послугу",
        "ru": "Предложить регулярную услугу"
    },
    "offer_single_service": {
        "en": "Offer a Single Occurrence Service",
        "ro": "Oferiți un Serviciu Unic",
        "uk": "Пропонувати одноразову послугу",
        "ru": "Предложить разовую услугу"
    },
    "provide_assistance": {
        "en": "Provide Assistance",
        "ro": "Oferiți Asistență",
        "uk": "Надати допомогу",
        "ru": "Оказать помощь"
    },
    "generate_ticket": {
        "en": "Generate Ticket",
        "ro": "Generați Bilet",
        "uk": "Згенерувати квиток",
        "ru": "Создать билет"
    },
    "generate_digital_ticket": {
        "en": "Generate Digital Ticket",
        "ro": "Generați Bilet Digital",
        "uk": "Згенерувати цифровий квиток",
        "ru": "Создать цифровой билет"
    },
    "generate_print_ticket": {
        "en": "Generate and Print Ticket",
        "ro": "Generați și Imprimați Bilet",
        "uk": "Згенерувати і роздрукувати квиток",
        "ru": "Создать и распечатать билет"
    },
    "ticket": {
        "en": "Ticket",
        "ro": "Bilet",
        "uk": "Квиток",
        "ru": "Билет"
    },
    "visitor_type_label": {
        "en": "Visitor Type:",
        "ro": "Tip de Vizitator:",
        "uk": "Тип відвідувача:",
        "ru": "Тип посетителя:"
    },
    "visit_type_label": {
        "en": "Visit Type:",
        "ro": "Tip de Vizită:",
        "uk": "Тип візиту:",
        "ru": "Тип визита:"
    },
    "destination_label": {
        "en": "Destination:",
        "ro": "Destinație:",
        "uk": "Призначення:",
        "ru": "Назначение:"
    },
    "map_link": {
        "en": "[Link to the map of the premises](http://example.com/map)",
        "ro": "[Link către harta sediului](http://example.com/map)",
        "uk": "[Посилання на карту приміщень](http://example.com/map)",
        "ru": "[Ссылка на карту помещения](http://example.com/map)"
    }
}

# Define service locations on the map
service_locations = {
    "Assistance Desk": (50, 50),
    "Reception": (10, 10),
    "Event Hall": (30, 30),
    "Workshop Room": (70, 70),
    "Service Office": (90, 90),
    "Service Desk": (80, 80),
    "Assistance Office": (60, 60)
}

def main():
    st.set_page_config(page_title="Moldova for Peace Entry-Stand", layout="centered")
    
    # Language selection page
    st.title("Moldova for Peace Hub Entry-Stand")
    st.markdown(f"<b>{texts['select_language']['en']}</b>", unsafe_allow_html=True)
    
    # Language selection as a single radio button group
    language = st.radio(
        "",
        ["English", "Română", "Українська", "Русский"],
        horizontal=True,
        index=0
    )
    
    lang_code = get_language_code(language)
    st.session_state['lang_code'] = lang_code

    # Display welcome message
    st.header(texts["welcome"][lang_code])

    # Select visitor type
    visitor_type = st.radio(
        texts["visitor_type"][lang_code],
        [texts["individual"][lang_code], texts["organization"][lang_code]],
        horizontal=True,
        index=0
    )

    if visitor_type == texts["individual"][lang_code]:
        handle_individual_workflow(lang_code)
    else:
        handle_organization_workflow(lang_code)

    # Options to generate and print ticket or generate digital ticket
    col1, col2 = st.columns(2)
    if col1.button(texts["generate_print_ticket"][lang_code]):
        ticket = generate_ticket(visitor_type, lang_code)
        st.write(ticket)
        st.markdown(texts["map_link"][lang_code])

    if col2.button(texts["generate_digital_ticket"][lang_code]):
        ticket = generate_ticket(visitor_type, lang_code)
        st.write(ticket)
        st.markdown(texts["map_link"][lang_code])
        # Logic to send ticket to Dopamoha (not implemented in this example)

def handle_individual_workflow(lang_code):
    st.subheader(texts["do_you_have_account"][lang_code])
    has_account = st.radio("", [texts["yes"][lang_code], texts["no"][lang_code]], index=0)

    if has_account == texts["yes"][lang_code]:
        phone_number = st.text_input(texts["phone_number"][lang_code])
        if len(phone_number) >= 9:
            visitor_names = st.multiselect(
                texts["choose_names"][lang_code],
                ["Андрій", "Марія", "Олександр", "Іван", "Катерина"]  # Example names in Russian
            )
    else:
        visitor_name = st.text_input(texts["provide_name"][lang_code])
        num_visitors = st.number_input(texts["number_of_visitors"][lang_code], min_value=1, max_value=10)

def handle_organization_workflow(lang_code):
    org_name = st.selectbox(
        texts["select_organization"][lang_code],
        ["Org1", "Org2", "Org3", "Org4", "Org5"],
        index=-1
    )
    position = st.selectbox(
        texts["select_position"][lang_code],
        [
            texts["project_manager"][lang_code],
            texts["country_director"][lang_code],
            texts["monitoring_officer"][lang_code],
            texts["audit_officer"][lang_code],
            texts["data_enumerator"][lang_code]
        ],
        index=-1
    )
    contact_name = st.text_input(texts["provide_name"][lang_code])

def generate_ticket(visitor_type, lang_code):
    ticket_details = {
        "visitor_type": visitor_type,
        "destination": "Destination"
    }
    return (
        f"{texts['ticket'][lang_code]}\n\n"
        f"{texts['visitor_type_label'][lang_code]} {ticket_details['visitor_type']}\n"
        f"{texts['destination_label'][lang_code]} {ticket_details['destination']}"
    )

def get_language_code(language):
    language_codes = {
        "English": "en",
        "Română": "ro",
        "Українська": "uk",
        "Русский": "ru"
    }
    return language_codes.get(language, "en")

def display_map(destination):
    fig, ax = plt.subplots()
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.plot(*service_locations[destination], 'ro')  # Mark the destination with a red dot
    ax.text(*service_locations[destination], destination, fontsize=12, ha='right')
    st.pyplot(fig)

if __name__ == "__main__":
    main()
