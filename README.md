# RAG Knowledge Assistant

A lightweight Retrieval-Augmented Generation (RAG) application for semantic document search and document-grounded question answering.

The application allows users to upload PDF or TXT documents, ask questions about their content, and receive answers generated from semantically retrieved document passages.

The project was built from scratch to understand and implement the core components of a RAG pipeline without relying on high-level RAG frameworks.

## Features

* Upload PDF and TXT documents
* Extract and process document text
* Split documents into text chunks
* Generate local semantic embeddings
* Retrieve relevant document passages using cosine similarity
* Generate document-grounded answers with an external LLM
* Display the retrieved source passage alongside the answer
* Reject questions that cannot be answered from the retrieved context
* Interactive chat interface built with Streamlit

## Architecture

```text
PDF / TXT document
        ↓
Text extraction
        ↓
Chunking
        ↓
Sentence Transformer
        ↓
Chunk embeddings
        ↓
        ┌─────────────────┐
        │  User question  │
        └────────┬────────┘
                 ↓
          Query embedding
                 ↓
        Cosine similarity
                 ↓
        Relevant document
             passage
                 ↓
       Question + Context
                 ↓
             LLM API
                 ↓
      Document-grounded
             answer
                 ↓
        Answer + Source
```

## How It Works

### 1. Document Processing

Uploaded TXT files are decoded directly, while PDF text is extracted using `pypdf`.

### 2. Chunking

The extracted text is divided into smaller passages. The current MVP uses paragraph-based chunking.

### 3. Embeddings

Document chunks are converted into vector representations using the `all-MiniLM-L6-v2` Sentence Transformer model.

Embeddings are generated locally.

### 4. Retrieval

The user's question is converted into an embedding using the same model.

Cosine similarity is used to compare the query embedding with the document chunk embeddings. The most similar chunk is selected as context.

### 5. Generation

The retrieved context and the user's question are sent to an LLM through an NVIDIA-hosted, OpenAI-compatible API.

The model is instructed to answer only from the supplied document context and to indicate when the question cannot be answered from it.

### 6. Source Display

The retrieved document passage is displayed alongside the generated answer, making it possible to inspect the context used by the model.

## Project Structure

```text
rag-knowledge-assistant/
│
├── frontend.py
│   └── Streamlit user interface and application flow
│
├── document_processor.py
│   └── TXT/PDF extraction and chunking
│
├── embeddings.py
│   └── Local embedding generation
│
├── retriever.py
│   └── Semantic retrieval using cosine similarity
│
├── answer_machine.py
│   └── LLM API communication and grounded prompting
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yaml
└── README.md
```

## Tech Stack

* Python
* Streamlit
* Sentence Transformers
* `all-MiniLM-L6-v2`
* PyPDF
* NVIDIA-hosted LLM API
* OpenAI-compatible Python client
* Docker
* Git / GitHub

## Installation

Clone the repository:

```bash
git clone https://github.com/colreger/rag-knowledge-assistant.git
cd rag-knowledge-assistant
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project directory:

```text
NVIDIA_API_KEY=your_api_key_here
```

The `.env` file is excluded from Git and should never be committed.

Start the application:

```bash
streamlit run frontend.py
```

## Current Limitations

This project is currently an MVP focused on implementing the fundamental RAG pipeline.

Current limitations include:

* Paragraph-based chunking rather than token-aware chunking
* Top-1 retrieval
* Embeddings are kept in memory
* No persistent vector database yet
* Single-document workflow
* Text-based PDFs only; scanned PDFs require OCR
* External LLM inference requires sending the retrieved document passage to the configured API provider

## Roadmap

* [x] Streamlit chat interface
* [x] TXT document processing
* [x] PDF document processing
* [x] Document chunking
* [x] Local embeddings
* [x] Semantic retrieval
* [x] Document-grounded LLM generation
* [x] Source passage display
* [x] Docker setup
* [ ] Token-aware chunking with overlap
* [ ] Top-k retrieval
* [ ] Persistent vector database
* [ ] Multi-document support
* [ ] Hybrid retrieval
* [ ] Configurable LLM providers
* [ ] Local LLM support
* [ ] Automated tests
* [ ] Deployment

## Why Build RAG From Scratch?

Many RAG frameworks abstract away document processing, embeddings, retrieval, and prompt construction.

This project intentionally implements these components separately to make the complete information flow transparent and to develop a deeper understanding of RAG system architecture.

The modular structure also makes individual components easier to test, replace, and extend.

## License

MIT License (planned)
