import streamlit as st
from docx import Document
import os
from googletrans import Translator

# Set up translator for automatic English-to-Romanian translations
translator = Translator()

# Define the folder where your templates are stored
TEMPLATE_FOLDER = "aoreg/AOS"

# Helper function to check if the file exists
def check_file_exists(file_path):
    return os.path.exists(file_path)

# Helper function to fill templates
def fill_template(template_path, placeholders):
    if check_file_exists(template_path):
        doc = Document(template_path)
        for para in doc.paragraphs:
            for key, value in placeholders.items():
                if key in para.text:
                    para.text = para.text.replace(key, value)
        return doc
    else:
        st.error(f"Template file not found: {template_path}")
        return None

# Helper function to save document and check if successful
def save_document(doc, filename):
    if doc:
        doc.save(filename)
        return filename
    else:
        st.error("Document not saved because the template could not be loaded.")
        return None

# Initialize session state for user inputs and file paths
def initialize_session_state():
    if 'organization_name' not in st.session_state:
        st.session_state['organization_name'] = ''
    if 'generated_files' not in st.session_state:
        st.session_state['generated_files'] = {}

# Main Streamlit app
def main():
    # Initialize session state variables
    initialize_session_state()

    st.title("NGO Registration Assistant - Moldova")
    
    # Workflow selection
    workflow = st.radio("Choose a workflow:", ("Full Document Generation", "Manual Excerpt Generation"))

    if workflow == "Full Document Generation":
        st.subheader("Provide Details for Full Document Generation")

        # Section 1: Statut Form Inputs (all placeholders as text inputs)
        st.header("Section 1: Statut Information")

        organization_name = st.text_input("Complete name of the organization", value=st.session_state.organization_name)
        short_name = st.text_input("Short name (if applicable)")
        goal1 = st.text_input("Goal 1")
        goal2 = st.text_input("Goal 2")
        ceo = st.text_input("CEO (Chief Executive Officer)")
        mandate = st.text_input("Mandate")
        gadays = st.text_input("General Assembly Days (gadays)")
        egadays = st.text_input("Extraordinary General Assembly Days (egadays)")
        rightholders = st.text_input("Right Holders (no spaces)")
        founder1 = st.text_input("Founder 1")
        founder2 = st.text_input("Founder 2")
        founder3 = st.text_input("Founder 3")

        st.divider()  # Separation between sections

        # Section 2: Proces Verbal Inputs (individual text inputs)
        st.header("Section 2: Proces Verbal Information")
        governance = st.text_input("Governance details (board members, terms, administrator)")
        contact_info = st.text_input("Contact Information (address, email, phone)")

        st.divider()

        # Section 3: Registration Form Inputs (individual text input)
        st.header("Section 3: Registration Form Information")
        sediu = st.text_input("Sediu (official address of the organization)")

        # Update session state when inputs change
        st.session_state.organization_name = organization_name

        # Translate inputs to Romanian if necessary
        if st.checkbox("Translate from English to Romanian"):
            organization_name = translator.translate(organization_name, dest='ro').text
            short_name = translator.translate(short_name, dest='ro').text
            goal1 = translator.translate(goal1, dest='ro').text
            goal2 = translator.translate(goal2, dest='ro').text
            ceo = translator.translate(ceo, dest='ro').text
            mandate = translator.translate(mandate, dest='ro').text
            gadays = translator.translate(gadays, dest='ro').text
            egadays = translator.translate(egadays, dest='ro').text
            rightholders = translator.translate(rightholders, dest='ro').text
            founder1 = translator.translate(founder1, dest='ro').text
            founder2 = translator.translate(founder2, dest='ro').text
            founder3 = translator.translate(founder3, dest='ro').text
            governance = translator.translate(governance, dest='ro').text
            contact_info = translator.translate(contact_info, dest='ro').text
            sediu = translator.translate(sediu, dest='ro').text

        # Generate documents
        if st.button("Generate Documents"):
            # Define placeholders using double curly braces
            placeholders = {
                "{{organization_name}}": organization_name,
                "{{short_name}}": short_name,
                "{{goal1}}": goal1,
                "{{goal2}}": goal2,
                "{{ceo}}": ceo,
                "{{mandate}}": mandate,
                "{{gadays}}": gadays,
                "{{egadays}}": egadays,
                "{{rightholders}}": rightholders,
                "{{founder1}}": founder1,
                "{{founder2}}": founder2,
                "{{founder3}}": founder3,
                "{{governance}}": governance,
                "{{contact_info}}": contact_info,
                "{{sediu}}": sediu
            }

            # Reset session state for generated files
            st.session_state['generated_files'] = {}

            # Fill and save Statut
            statut_template = os.path.join(TEMPLATE_FOLDER, "Statut_template.docx")
            statut_doc = fill_template(statut_template, placeholders)
            statut_filename = f"{organization_name}_Statut.docx"
            statut_saved = save_document(statut_doc, statut_filename)
            if statut_saved:
                st.session_state['generated_files']["Statut"] = statut_saved

            # Fill and save Proces Verbal
            proces_verbal_template = os.path.join(TEMPLATE_FOLDER, "Proces_verbal_template.docx")
            proces_verbal_doc = fill_template(proces_verbal_template, placeholders)
            proces_verbal_filename = f"{organization_name}_Proces_Verbal.docx"
            proces_verbal_saved = save_document(proces_verbal_doc, proces_verbal_filename)
            if proces_verbal_saved:
                st.session_state['generated_files']["Proces Verbal"] = proces_verbal_saved

            # Fill and save Registration Form
            registration_form_template = os.path.join(TEMPLATE_FOLDER, "Registration_form.docx")
            registration_form_doc = fill_template(registration_form_template, placeholders)
            registration_form_filename = f"{organization_name}_Registration_Form.docx"
            registration_form_saved = save_document(registration_form_doc, registration_form_filename)
            if registration_form_saved:
                st.session_state['generated_files']["Registration Form"] = registration_form_saved

        # Display download buttons for all generated files
        if st.session_state['generated_files']:
            st.success("Documents generated successfully!")
            for doc_name, file_name in st.session_state['generated_files'].items():
                with open(file_name, "rb") as file:
                    st.download_button(f"Download {doc_name}", file, file_name=file_name)
        else:
            st.error("No documents could be generated. Please check the templates and try again.")

    elif workflow == "Manual Excerpt Generation":
        st.subheader("Provide Details for Manual Excerpt Generation")

        # Pre-fill inputs with previous values from session state
        organization_name = st.text_input("Complete name of the organization", value=st.session_state.organization_name)
        goal1 = st.text_input("Goal 1")
        governance = st.text_input("Governance details (board members, terms, administrator)")

        # Update session state when inputs change
        st.session_state.organization_name = organization_name

        if st.button("Generate Excerpts"):
            # Generate text excerpts with placeholders
            statut_excerpt = f"Goal 1: {goal1}\nGovernance: {governance}"
            proces_verbal_excerpt = f"Founders: {organization_name}\nGovernance: {governance}"

            # Display excerpts and provide copy functionality
            st.text_area("Excerpt for Statut", value=statut_excerpt)
            st.text_area("Excerpt for Proces Verbal", value=proces_verbal_excerpt)

            # Downloadable instruction documents
            instruction_text = "Insert the provided excerpts in the respective sections of the Statut and Proces Verbal templates."
            st.download_button("Download Instructions", instruction_text)

if __name__ == "__main__":
    main()
