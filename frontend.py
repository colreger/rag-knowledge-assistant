import streamlit as st
from answer_machine import get_answer

# Seitentitel im Browser-Tab und Überschrift auf der Seite
st.set_page_config(page_title="Knowledge Assistant")
st.title("Knowledge Assistant (Echo Bot)")

# Sidebar: Platz für spätere Einstellungen und den Upload-Platzhalter
with st.sidebar:
    st.header("Dokumente")
    st.file_uploader(
        "Dokument hochladen (Platzhalter, noch ohne Funktion)",
        type=["pdf", "txt"],
    )

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

    # 2. eine Antwort erzeugen mit Random Answer Machine
    echo_response = get_answer(user_input)

    # 3. Bot-Antwort speichern und anzeigen
    st.session_state.messages.append({"role": "assistant", "content": echo_response})
    with st.chat_message("assistant"):
        st.markdown(echo_response)
