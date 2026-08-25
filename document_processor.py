from pypdf import PdfReader

def read_txt_file(uploaded_file):
    text = uploaded_file.read().decode("utf-8")
    return text

def read_pdf_file(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text

def chunk_text(text):
    chunks = text.split("\n\n")
    return chunks