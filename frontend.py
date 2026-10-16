import streamlit as st

from answer_machine import get_answer
from document_processor import read_txt_file, read_pdf_file, chunk_text
from embeddings import create_embeddings, create_query_embedding
from vector_store import store_chunks, query_chunks


# Configure the browser tab and display the application title.
st.set_page_config(page_title="Knowledge Assistant")
st.title("RAG Knowledge Assistant")


# --------------------------------------------------
# DOCUMENT UPLOAD
# --------------------------------------------------

# Remember which document has already been processed.
# Streamlit reruns the complete script after every interaction.
# Without this state, the same PDF would be chunked, embedded,
# and stored in ChromaDB again every time the user asks a question.
if "processed_file" not in st.session_state:
    st.session_state.processed_file = None


with st.sidebar:
    st.header("Dokumente")

    uploaded_file = st.file_uploader(
        "Dokument hochladen",
        type=["pdf", "txt"],
    )

    # Process the document only if a file is uploaded
    # and it has not already been processed in this session.
    if (
        uploaded_file is not None
        and st.session_state.processed_file != uploaded_file.name
    ):

        if uploaded_file.type == "text/plain":
            text = read_txt_file(uploaded_file)

        elif uploaded_file.type == "application/pdf":
            text = read_pdf_file(uploaded_file)

        # Split the document into smaller chunks.
        chunks = chunk_text(text)

        # Create embeddings only once for this uploaded document.
        embeddings = create_embeddings(chunks)

        # Store the chunks and embeddings in ChromaDB.
        store_chunks(
            chunks,
            embeddings,
            uploaded_file.name,
        )

        # Remember that this document has already been processed.
        st.session_state.processed_file = uploaded_file.name

        st.success("Dokument wurde verarbeitet und in ChromaDB gespeichert.")


# --------------------------------------------------
# CHAT HISTORY
# --------------------------------------------------

# Initialize the chat history only on the first Streamlit run.
#
# Streamlit reruns this entire script after user interactions.
# session_state allows the previous messages to survive those reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display all previous messages from the current session.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --------------------------------------------------
# USER QUESTION
# --------------------------------------------------

user_input = st.chat_input("Schreib deine Nachricht...")


if user_input:

    print("DEBUG 1: User input received")

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    print("DEBUG 2: Creating query embedding")

    query_embedding = create_query_embedding(user_input)

    print("DEBUG 3: Query embedding created")
    print("DEBUG 4: Querying ChromaDB")

    retrieved_chunks = query_chunks(
        query_embedding,
        n_results=3,
    )

    print("DEBUG 5: ChromaDB finished")

    context = "\n\n".join(retrieved_chunks)

    print("DEBUG 6: Calling LLM")

    assistant_response = get_answer(
        user_input,
        context,
    )

    print("DEBUG 7: LLM finished")

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_response,
        }
    )

    with st.chat_message("assistant"):
        st.markdown(assistant_response)

    print("DEBUG 8: Answer displayed")