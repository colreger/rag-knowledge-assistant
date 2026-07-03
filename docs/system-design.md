# System Design

## Purpose

The RAG Knowledge Assistant is an open-source web application that allows users to upload documents and ask questions about their content using Retrieval-Augmented Generation (RAG).

The system is designed with a modular architecture so that individual components can easily be replaced or extended.

---

# High-Level Architecture

## Document Ingestion Workflow

```
User
    │
    ▼
Frontend
    │
    ▼
Backend API
    │
    ▼
Document Service
    │
    ▼
Chunking Service
    │
    ▼
Embedding Service
    │
    ▼
Vector Database
```

## Question Answering Workflow

```
User
    │
    ▼
Frontend
    │
    ▼
Backend API
    │
    ▼
Retrieval Service
    │
    ▼
Vector Database
    │
    ▼
LLM Service
    │
    ▼
Answer
```

---

# Components

## Frontend

Provides the user interface for uploading documents and asking questions.

---

## Backend API

Coordinates all requests between the frontend and the backend services.

---

## Document Service

Reads uploaded documents and extracts their textual content.

---

## Chunking Service

Splits extracted text into smaller chunks that can be embedded efficiently.

---

## Embedding Service

Generates vector embeddings for every text chunk.

---

## Vector Database

Stores embeddings and performs semantic similarity search.

---

## Retrieval Service

Retrieves the most relevant text chunks for a user question.

---

## LLM Service

Generates the final answer using the retrieved context.

---

# Design Principles

- Modular architecture
- Single responsibility per component
- Replaceable services
- Separation of concerns
- Extensible design

---

# Current Status

Version 0.1

Only the high-level architecture is defined.

Implementation will be developed incrementally.
