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
    "visit_type_individual": {
        "en": "Please select your purpose of visit:",
        "ro": "Vă rugăm să selectați scopul vizitei:",
        "uk": "Будь ласка, виберіть мету візиту:",
        "ru": "Пожалуйста, выберите цель визита:"
    },
    "visit_type_organization": {
        "en": "Please select your purpose of visit:",
        "ro": "Vă rugăm să selectați scopul vizitei:",
        "uk": "Будь ласка, виберіть мету візиту:",
        "ru": "Пожалуйста, выберите цель визита:"
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
    
    language = st.radio(
        "",
        ["English", "Română", "Українська", "Русский"],
        format_func=lambda lang: lang
    )
    
    lang_code = get_language_code(language)
    st.session_state['lang_code'] = lang_code

    # Display welcome message
    st.header(texts["welcome"][lang_code])

    # Select visitor type
    visitor_type = st.radio(
        texts["visitor_type"][lang_code],
        [texts["individual"][lang_code], texts["organization"][lang_code]]
    )

    # Select visit type based on visitor type
    if visitor_type == texts["individual"][lang_code]:
        visit_type = st.selectbox(
            texts["visit_type_individual"][lang_code],
            [
                texts["receive_assistance"][lang_code],
                texts["just_visit"][lang_code],
                texts["attend_event"][lang_code],
                texts["attend_workshop"][lang_code]
            ]
        )
    else:
        visit_type = st.selectbox(
            texts["visit_type_organization"][lang_code],
            [
                texts["offer_regular_service"][lang_code],
                texts["offer_single_service"][lang_code],
                texts["provide_assistance"][lang_code],
                texts["just_visit"][lang_code]
            ]
        )

    # Display recommended service location and map
    destination = get_destination(visit_type, lang_code)
    st.write(f"{texts['destination_label'][lang_code]} {destination}")
    display_map(destination)

    # Options to generate and print ticket or generate digital ticket
    col1, col2 = st.columns(2)
    if col1.button(texts["generate_print_ticket"][lang_code]):
        ticket = generate_ticket(visitor_type, visit_type, lang_code)
        st.write(ticket)
        st.markdown(texts["map_link"][lang_code])

    if col2.button(texts["generate_digital_ticket"][lang_code]):
        ticket = generate_ticket(visitor_type, visit_type, lang_code)
        st.write(ticket)
        st.markdown(texts["map_link"][lang_code])
        # Logic to send ticket to Dopamoha (not implemented in this example)

def generate_ticket(visitor_type, visit_type, lang_code):
    ticket_details = {
        "visitor_type": visitor_type,
        "visit_type": visit_type,
        "destination": get_destination(visit_type, lang_code)
    }
    return (
        f"{texts['ticket'][lang_code]}\n\n"
        f"{texts['visitor_type_label'][lang_code]} {ticket_details['visitor_type']}\n"
        f"{texts['visit_type_label'][lang_code]} {ticket_details['visit_type']}\n"
        f"{texts['destination_label'][lang_code]} {ticket_details['destination']}"
    )

def get_destination(visit_type, lang_code):
    destinations = {
        texts["receive_assistance"][lang_code]: "Assistance Desk",
        texts["just_visit"][lang_code]: "Reception",
        texts["attend_event"][lang_code]: "Event Hall",
        texts["attend_workshop"][lang_code]: "Workshop Room",
        texts["offer_regular_service"][lang_code]: "Service Office",
        texts["offer_single_service"][lang_code]: "Service Desk",
        texts["provide_assistance"][lang_code]: "Assistance Office",
    }
    return destinations.get(visit_type, "General Area")

def display_map(destination):
    fig, ax = plt.subplots()
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.plot(*service_locations[destination], 'ro')  # Mark the destination with a red dot
    ax.text(*service_locations[destination], destination, fontsize=12, ha='right')
    st.pyplot(fig)

def get_language_code(language):
    language_codes = {
        "English": "en",
        "Română": "ro",
        "Українська": "uk",
        "Русский": "ru"
    }
    return language_codes.get(language, "en")

if __name__ == "__main__":
    main()
