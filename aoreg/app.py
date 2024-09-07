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

# Helper function to save document
def save_document(doc, filename):
    if doc:
        doc.save(filename)
    else:
        st.error("Document not saved because the template could not be loaded.")

# Main Streamlit app
def main():
    st.title("NGO Registration Assistant - Moldova")
    
    # Workflow selection
    workflow = st.radio("Choose a workflow:", ("Full Document Generation", "Manual Excerpt Generation"))

    if workflow == "Full Document Generation":
        st.subheader("Provide Details for Full Document Generation")

        # Collect user inputs
        organization_name = st.text_input("Complete name of the organization")
        short_name = st.text_input("Short name (if applicable)")
        objectives = st.text_area("Objectives, Mission, Vision (user-specific)")
        values = st.text_area("Values and Principles (optional)")
        history = st.text_area("History or 'About the organization' (if applicable)")
        founders = st.text_area("List of founders (name, IDNP, domicile)")
        governance = st.text_area("Governance details (board members, terms, administrator)")
        contact_info = st.text_input("Contact Information (address, email, phone)")
        sediu = st.text_input("Sediu (official address of the organization)")

        # Translate inputs to Romanian if necessary
        if st.checkbox("Translate from English to Romanian"):
            organization_name = translator.translate(organization_name, dest='ro').text
            objectives = translator.translate(objectives, dest='ro').text
            values = translator.translate(values, dest='ro').text
            history = translator.translate(history, dest='ro').text
            founders = translator.translate(founders, dest='ro').text
            governance = translator.translate(governance, dest='ro').text
            contact_info = translator.translate(contact_info, dest='ro').text
            sediu = translator.translate(sediu, dest='ro').text

        # Generate documents
        if st.button("Generate Documents"):
            # Define placeholders
            placeholders = {
                "[ORGANIZATION_NAME]": organization_name,
                "[SHORT_NAME]": short_name,
                "[OBJECTIVES]": objectives,
                "[VALUES]": values,
                "[HISTORY]": history,
                "[FOUNDERS]": founders,
                "[GOVERNANCE]": governance,
                "[CONTACT_INFO]": contact_info,
                "[SEDIU]": sediu
            }

            # Fill and save Statut
            statut_template = os.path.join(TEMPLATE_FOLDER, "Statut_template.doc")
            statut_doc = fill_template(statut_template, placeholders)
            statut_filename = f"{organization_name}_Statut.doc"
            save_document(statut_doc, statut_filename)

            # Fill and save Proces Verbal
            proces_verbal_template = os.path.join(TEMPLATE_FOLDER, "Proces_verbal_template.doc")
            proces_verbal_doc = fill_template(proces_verbal_template, placeholders)
            proces_verbal_filename = f"{organization_name}_Proces_Verbal.doc"
            save_document(proces_verbal_doc, proces_verbal_filename)

            # Fill and save Registration Form
            registration_form_template = os.path.join(TEMPLATE_FOLDER, "Registration_form.docx")
            registration_form_doc = fill_template(registration_form_template, placeholders)
            registration_form_filename = f"{organization_name}_Registration_Form.docx"
            save_document(registration_form_doc, registration_form_filename)

            # Provide download links
            if statut_doc and proces_verbal_doc and registration_form_doc:
                st.success("Documents generated successfully!")
                st.download_button("Download Statut", open(statut_filename, "rb"), file_name=statut_filename)
                st.download_button("Download Proces Verbal", open(proces_verbal_filename, "rb"), file_name=proces_verbal_filename)
                st.download_button("Download Registration Form", open(registration_form_filename, "rb"), file_name=registration_form_filename)

    elif workflow == "Manual Excerpt Generation":
        st.subheader("Provide Details for Manual Excerpt Generation")

        # Collect user inputs (same as full generation)
        organization_name = st.text_input("Complete name of the organization")
        objectives = st.text_area("Objectives, Mission, Vision (user-specific)")
        governance = st.text_area("Governance details (board members, terms, administrator)")

        if st.button("Generate Excerpts"):
            # Generate text excerpts with placeholders
            statut_excerpt = f"Obiectivele organizației: {objectives}\nConducerea organizației: {governance}"
            proces_verbal_excerpt = f"Fondatori: {organization_name}\nDecizii de guvernare: {governance}"

            # Display excerpts and provide copy functionality
            st.text_area("Excerpt for Statut", value=statut_excerpt)
            st.text_area("Excerpt for Proces Verbal", value=proces_verbal_excerpt)

            # Downloadable instruction documents
            instruction_text = "Insert the provided excerpts in the respective sections of the Statut and Proces Verbal templates."
            st.download_button("Download Instructions", instruction_text)

if __name__ == "__main__":
    main()
