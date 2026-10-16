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

def chunk_text(text, chunk_size=1000):
    # Split the document into chunks with a maximum size of
    # approximately 1000 characters.
    #
    # Previously, the text was split only at double line breaks.
    # PDF extraction does not always preserve paragraph breaks,
    # which could result in the entire PDF becoming one large chunk.
    chunks = []

    for start in range(0, len(text), chunk_size):
        chunk = text[start:start + chunk_size]
        chunks.append(chunk)

    return chunks