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

# Initialize session state for user inputs
def initialize_session_state():
    default_values = {
        'organization_name': '',
        'short_name': '',
        'objectives': '',
        'values': '',
        'history': '',
        'founders': '',
        'governance': '',
        'contact_info': '',
        'sediu': ''
    }

    for key, default_value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

# Main Streamlit app
def main():
    # Initialize session state variables
    initialize_session_state()

    st.title("NGO Registration Assistant - Moldova")
    
    # Workflow selection
    workflow = st.radio("Choose a workflow:", ("Full Document Generation", "Manual Excerpt Generation"))

    if workflow == "Full Document Generation":
        st.subheader("Provide Details for Full Document Generation")

        # Pre-fill inputs with previous values from session state
        organization_name = st.text_input("Complete name of the organization", value=st.session_state.organization_name)
        short_name = st.text_input("Short name (if applicable)", value=st.session_state.short_name)
        objectives = st.text_area("Objectives, Mission, Vision (user-specific)", value=st.session_state.objectives)
        values = st.text_area("Values and Principles (optional)", value=st.session_state.values)
        history = st.text_area("History or 'About the organization' (if applicable)", value=st.session_state.history)
        founders = st.text_area("List of founders (name, IDNP, domicile)", value=st.session_state.founders)
        governance = st.text_area("Governance details (board members, terms, administrator)", value=st.session_state.governance)
        contact_info = st.text_input("Contact Information (address, email, phone)", value=st.session_state.contact_info)
        sediu = st.text_input("Sediu (official address of the organization)", value=st.session_state.sediu)

        # Update session state when inputs change
        st.session_state.organization_name = organization_name
        st.session_state.short_name = short_name
        st.session_state.objectives = objectives
        st.session_state.values = values
        st.session_state.history = history
        st.session_state.founders = founders
        st.session_state.governance = governance
        st.session_state.contact_info = contact_info
        st.session_state.sediu = sediu

        # Translate inputs to Romanian if necessary
        if st.checkbox("Translate from English to Romanian"):
            st.session_state.organization_name = translator.translate(st.session_state.organization_name, dest='ro').text
            st.session_state.objectives = translator.translate(st.session_state.objectives, dest='ro').text
            st.session_state.values = translator.translate(st.session_state.values, dest='ro').text
            st.session_state.history = translator.translate(st.session_state.history, dest='ro').text
            st.session_state.founders = translator.translate(st.session_state.founders, dest='ro').text
            st.session_state.governance = translator.translate(st.session_state.governance, dest='ro').text
            st.session_state.contact_info = translator.translate(st.session_state.contact_info, dest='ro').text
            st.session_state.sediu = translator.translate(st.session_state.sediu, dest='ro').text

        # Generate documents
        if st.button("Generate Documents"):
            # Define placeholders
            placeholders = {
                "[ORGANIZATION_NAME]": st.session_state.organization_name,
                "[SHORT_NAME]": st.session_state.short_name,
                "[OBJECTIVES]": st.session_state.objectives,
                "[VALUES]": st.session_state.values,
                "[HISTORY]": st.session_state.history,
                "[FOUNDERS]": st.session_state.founders,
                "[GOVERNANCE]": st.session_state.governance,
                "[CONTACT_INFO]": st.session_state.contact_info,
                "[SEDIU]": st.session_state.sediu
            }

            # Store download links
            download_links = {}

            # Fill and save Statut
            statut_template = os.path.join(TEMPLATE_FOLDER, "Statut_template.docx")
            statut_doc = fill_template(statut_template, placeholders)
            statut_filename = f"{st.session_state.organization_name}_Statut.docx"
            statut_saved = save_document(statut_doc, statut_filename)
            if statut_saved:
                download_links["Statut"] = statut_saved

            # Fill and save Proces Verbal
            proces_verbal_template = os.path.join(TEMPLATE_FOLDER, "Proces_verbal_template.docx")
            proces_verbal_doc = fill_template(proces_verbal_template, placeholders)
            proces_verbal_filename = f"{st.session_state.organization_name}_Proces_Verbal.docx"
            proces_verbal_saved = save_document(proces_verbal_doc, proces_verbal_filename)
            if proces_verbal_saved:
                download_links["Proces Verbal"] = proces_verbal_saved

            # Fill and save Registration Form
            registration_form_template = os.path.join(TEMPLATE_FOLDER, "Registration_form.docx")
            registration_form_doc = fill_template(registration_form_template, placeholders)
            registration_form_filename = f"{st.session_state.organization_name}_Registration_Form.docx"
            registration_form_saved = save_document(registration_form_doc, registration_form_filename)
            if registration_form_saved:
                download_links["Registration Form"] = registration_form_saved

            # Show download links for successfully generated documents
            if download_links:
                st.success("Documents generated successfully!")
                for doc_name, file_name in download_links.items():
                    with open(file_name, "rb") as file:
                        st.download_button(f"Download {doc_name}", file, file_name=file_name)
            else:
                st.error("No documents could be generated. Please check the templates and try again.")

    elif workflow == "Manual Excerpt Generation":
        st.subheader("Provide Details for Manual Excerpt Generation")

        # Pre-fill inputs with previous values from session state
        organization_name = st.text_input("Complete name of the organization", value=st.session_state.organization_name)
        objectives = st.text_area("Objectives, Mission, Vision (user-specific)", value=st.session_state.objectives)
        governance = st.text_area("Governance details (board members, terms, administrator)", value=st.session_state.governance)

        # Update session state when inputs change
        st.session_state.organization_name = organization_name
        st.session_state.objectives = objectives
        st.session_state.governance = governance

        if st.button("Generate Excerpts"):
            # Generate text excerpts with placeholders
            statut_excerpt = f"Obiectivele organizației: {st.session_state.objectives}\nConducerea organizației: {st.session_state.governance}"
            proces_verbal_excerpt = f"Fondatori: {st.session_state.organization_name}\nDecizii de guvernare: {st.session_state.governance}"

            # Display excerpts and provide copy functionality
            st.text_area("Excerpt for Statut", value=statut_excerpt)
            st.text_area("Excerpt for Proces Verbal", value=proces_verbal_excerpt)

            # Downloadable instruction documents
            instruction_text = "Insert the provided excerpts in the respective sections of the Statut and Proces Verbal templates."
            st.download_button("Download Instructions", instruction_text)

if __name__ == "__main__":
    main()
