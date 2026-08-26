import streamlit as st
from answer_machine import get_answer
from document_processor import read_txt_file, chunk_text
from embeddings import create_embeddings
from retriever import retrieve
from document_processor import read_txt_file, read_pdf_file, chunk_text

# Seitentitel im Browser-Tab und Überschrift auf der Seite
st.set_page_config(page_title="Knowledge Assistant")
st.title("RAG Knowledge Assistant")

# Sidebar: Platz für spätere Einstellungen 
with st.sidebar:
    st.header("Dokumente")
    uploaded_file = st.file_uploader(
        "Dokument hochladen",
        type=["pdf", "txt"],
    )
    if uploaded_file is not None:
        if uploaded_file.type == "text/plain":
            text = read_txt_file(uploaded_file)
        elif uploaded_file.type == "application/pdf":
            text = read_pdf_file(uploaded_file)

        chunks = chunk_text(text)
        embeddings = create_embeddings(chunks)
        st.write(chunks)

# Chatverlauf initialisieren, falls er noch nicht existiert
# (nur beim allerersten Laden der Seite nötig)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Bisherigen Chatverlauf anzeigen
# Bei jedem Neudurchlauf des Skripts wird die komplette Historie
# aus session_state erneut auf dem Bildschirm dargestellt
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Eingabefeld für neue Nachrichten
user_input = st.chat_input("Schreib deine Nachricht...")

if user_input:
    # 1. Nutzer-Nachricht speichern und anzeigen
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Assistant-Antwort erzeugen 
    # sucht den besten Abschnitt des hochgeladenen Docs
    context = retrieve(user_input, chunks, embeddings)
    # gibt zwei Dinge an llama: Frage des benutzers und gefundenen doc-chunk 
    assistant_response = get_answer(user_input, context)

    # 3. Bot-Antwort speichern und anzeigen
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
        with st.expander("Verwendete Quelle"):
            st.write(context)

