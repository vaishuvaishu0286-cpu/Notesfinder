import streamlit as st
import io

from pypdf import PdfReader
from docx import Document

from database import (
    create_database,
    add_note,
    search_notes,
    get_all_notes
)

from ocr_utils import extract_text


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="NoteFinder AI",
    page_icon="📚",
    layout="wide"
)


# =========================================================
# CREATE DATABASE
# =========================================================

create_database()


# =========================================================
# PDF TEXT EXTRACTION
# =========================================================

def extract_pdf_text(file_bytes):

    text = ""

    try:

        pdf = PdfReader(
            io.BytesIO(file_bytes)
        )

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:

                text += page_text + "\n"

    except Exception as error:

        st.error(
            f"PDF reading error: {error}"
        )

    return text.strip()


# =========================================================
# DOCX TEXT EXTRACTION
# =========================================================

def extract_docx_text(file_bytes):

    text = ""

    try:

        document = Document(
            io.BytesIO(file_bytes)
        )

        for paragraph in document.paragraphs:

            if paragraph.text.strip():

                text += paragraph.text + "\n"

    except Exception as error:

        st.error(
            f"Word file reading error: {error}"
        )

    return text.strip()


# =========================================================
# GET FILE TYPE
# =========================================================

def get_file_type(filename):

    filename = filename.lower()

    if filename.endswith(
        (".jpg", ".jpeg", ".png", ".webp")
    ):

        return "image"

    elif filename.endswith(".pdf"):

        return "pdf"

    elif filename.endswith(".docx"):

        return "docx"

    return "unknown"


# =========================================================
# EXTRACT TEXT FROM FILE
# =========================================================

def process_file(file):

    filename = file.name

    file_bytes = file.getvalue()

    file_type = get_file_type(
        filename
    )

    # IMAGE
    if file_type == "image":

        text = extract_text(
            file_bytes
        )

    # PDF
    elif file_type == "pdf":

        text = extract_pdf_text(
            file_bytes
        )

    # WORD
    elif file_type == "docx":

        text = extract_docx_text(
            file_bytes
        )

    else:

        text = ""

    return (
        file_bytes,
        file_type,
        text
    )


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title(
    "📚 NoteFinder AI"
)

st.sidebar.write(
    "OCR-Based Study Notes Retrieval"
)

st.sidebar.divider()

page = st.sidebar.radio(
    "MENU",
    [
        "🏠 Dashboard",
        "📷 Scan Notes",
        "🔎 Find Notes",
        "🗂️ All Notes"
    ]
)


# =========================================================
# GET NOTES
# =========================================================

notes = get_all_notes()

total_notes = len(notes)

total_words = 0

for note in notes:

    text = note[4] or ""

    total_words += len(
        text.split()
    )


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.title(
        "📚 NoteFinder AI"
    )

    st.header(
        "Find your notes in seconds"
    )

    st.write(
        "Upload study notes as images, PDF or Word "
        "documents. NoteFinder extracts the text "
        "and helps you find the right note by "
        "topic or keyword."
    )

    st.success(
        "⚡ OCR + Document Search Powered Study Tool"
    )

    st.divider()

    st.header(
        "📊 Your Notes"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📚 Saved Notes",
            total_notes
        )

    with col2:

        st.metric(
            "🔤 Words Extracted",
            total_words
        )

    with col3:

        st.metric(
            "🔍 Recognition",
            "OCR"
        )

    with col4:

        st.metric(
            "⚡ Search",
            "Fast"
        )

    st.divider()

    st.header(
        "✨ What can you do?"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.subheader(
            "📷 Scan Notes"
        )

        st.write(
            "Upload note images, PDFs or Word "
            "documents and extract their text."
        )

    with col2:

        st.subheader(
            "🔎 Search Topics"
        )

        st.write(
            "Search concepts, definitions, "
            "subjects or keywords."
        )

    with col3:

        st.subheader(
            "📄 Find Your Notes"
        )

        st.write(
            "View the relevant note and "
            "its extracted text."
        )

    st.divider()

    st.header(
        "📝 Recently Added"
    )

    if not notes:

        st.info(
            "📚 No notes yet. Go to Scan Notes "
            "and upload your first note."
        )

    else:

        for note in notes[:3]:

            filename = note[1]
            file_type = note[2]
            file_data = note[3]
            text = note[4] or ""

            col1, col2 = st.columns(
                [1, 2]
            )

            with col1:

                if file_type == "image":

                    st.image(
                        file_data,
                        use_container_width=True
                    )

                elif file_type == "pdf":

                    st.info(
                        "📄 PDF Document"
                    )

                elif file_type == "docx":

                    st.info(
                        "📝 Word Document"
                    )

            with col2:

                st.subheader(
                    "📄 " + filename
                )

                if text:

                    st.write(
                        text[:300]
                    )

                else:

                    st.warning(
                        "No text found."
                    )

            st.divider()


# =========================================================
# SCAN NOTES
# =========================================================

elif page == "📷 Scan Notes":

    st.title(
        "📷 Scan Notes"
    )

    st.write(
        "Upload your study notes."
    )

    st.info(
        "Supported formats: JPG, JPEG, PNG, WEBP, PDF, DOCX"
    )

    files = st.file_uploader(
        "Choose your study notes",
        type=[
            "jpg",
            "jpeg",
            "png",
            "webp",
            "pdf",
            "docx"
        ],
        accept_multiple_files=True
    )

    if files:

        st.success(
            f"✅ {len(files)} file(s) selected"
        )

        st.subheader(
            "Selected Files"
        )

        for file in files:

            file_type = get_file_type(
                file.name
            )

            if file_type == "image":

                icon = "🖼️"

            elif file_type == "pdf":

                icon = "📄"

            else:

                icon = "📝"

            st.write(
                f"{icon} {file.name}"
            )

        st.divider()

        if st.button(
            "🚀 Scan & Save Notes",
            type="primary",
            use_container_width=True
        ):

            progress = st.progress(
                0
            )

            saved = 0
            skipped = 0

            for index, file in enumerate(files):

                try:

                    (
                        file_bytes,
                        file_type,
                        text
                    ) = process_file(file)

                    if text.strip():

                        added = add_note(
                            file.name,
                            file_type,
                            file_bytes,
                            text
                        )

                        if added:

                            saved += 1

                        else:

                            skipped += 1

                    else:

                        skipped += 1

                        st.warning(
                            f"⚠️ No text found in {file.name}"
                        )

                except Exception as error:

                    st.error(
                        f"Error processing "
                        f"{file.name}: {error}"
                    )

                    skipped += 1

                progress.progress(
                    (index + 1) / len(files)
                )

            if saved > 0:

                st.success(
                    f"🎉 {saved} note(s) saved successfully!"
                )

                st.balloons()

            if skipped > 0:

                st.warning(
                    f"⚠️ {skipped} file(s) skipped."
                )

    else:

        st.write(
            "👆 Choose your notes above."
        )


# =========================================================
# FIND NOTES
# =========================================================

elif page == "🔎 Find Notes":

    st.title(
        "🔎 Find Notes"
    )

    st.write(
        "Search your saved notes using a keyword."
    )

    keyword = st.text_input(
        "Search Topic",
        placeholder="Example: Normalization"
    )

    if keyword.strip():

        results = search_notes(
            keyword.strip()
        )

        if results:

            st.success(
                f"Found {len(results)} matching note(s)"
            )

            for note in results:

                filename = note[1]
                file_type = note[2]
                file_data = note[3]
                text = note[4] or ""

                col1, col2 = st.columns(
                    [1, 2]
                )

                with col1:

                    if file_type == "image":

                        st.image(
                            file_data,
                            caption=filename,
                            use_container_width=True
                        )

                    elif file_type == "pdf":

                        st.info(
                            "📄 PDF Document"
                        )

                        st.download_button(
                            "⬇️ Download PDF",
                            data=file_data,
                            file_name=filename,
                            mime="application/pdf",
                            key=f"pdf_{note[0]}"
                        )

                    elif file_type == "docx":

                        st.info(
                            "📝 Word Document"
                        )

                        st.download_button(
                            "⬇️ Download Word File",
                            data=file_data,
                            file_name=filename,
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            key=f"docx_{note[0]}"
                        )

                with col2:

                    st.subheader(
                        "📄 " + filename
                    )

                    st.write(
                        "Matching keyword:"
                    )

                    st.success(
                        keyword
                    )

                    with st.expander(
                        "📖 View Extracted Text"
                    ):

                        st.write(
                            text
                        )

                st.divider()

        else:

            st.warning(
                "🔎 No matching notes found."
            )


# =========================================================
# ALL NOTES
# =========================================================

elif page == "🗂️ All Notes":

    st.title(
        "🗂️ All Notes"
    )

    st.write(
        f"{total_notes} note(s) stored in your library."
    )

    if not notes:

        st.info(
            "📚 No notes available."
        )

    else:

        for note in notes:

            note_id = note[0]
            filename = note[1]
            file_type = note[2]
            file_data = note[3]
            text = note[4] or ""

            col1, col2 = st.columns(
                [1, 2]
            )

            with col1:

                if file_type == "image":

                    st.image(
                        file_data,
                        caption=filename,
                        use_container_width=True
                    )

                elif file_type == "pdf":

                    st.info(
                        "📄 PDF Document"
                    )

                    st.download_button(
                        "⬇️ Download PDF",
                        data=file_data,
                        file_name=filename,
                        mime="application/pdf",
                        key=f"all_pdf_{note_id}"
                    )

                elif file_type == "docx":

                    st.info(
                        "📝 Word Document"
                    )

                    st.download_button(
                        "⬇️ Download Word File",
                        data=file_data,
                        file_name=filename,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key=f"all_docx_{note_id}"
                    )

            with col2:

                st.subheader(
                    "📄 " + filename
                )

                st.write(
                    text[:300]
                )

                with st.expander(
                    "📖 View Full Extracted Text"
                ):

                    st.write(
                        text
                    )

            st.divider()