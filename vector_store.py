# ChromaDB is the vector database used by the RAG application.
#
# Previously, document embeddings were stored only temporarily in
# Python memory and compared manually using cosine similarity
# inside retriever.py.
#
# ChromaDB will take over two main responsibilities:
# 1. Store the embeddings and corresponding document chunks.
# 2. Retrieve the chunks that are semantically most similar
#    to a user's question.
#
# The Python package is called "chromadb".
# Importing it allows this module to create and interact with
# a local ChromaDB instance.
import chromadb

# Create a persistent ChromaDB client.
#
# "Persistent" means that Chroma stores its database files on disk
# instead of keeping everything only in memory.
#
# The path defines the local directory where ChromaDB stores its data.
# If the application is restarted, the stored vectors can be loaded again.
#
# This is our first step from temporary in-memory retrieval toward
# persistent vector storage.
client = chromadb.PersistentClient(path="./chroma_db")

# Create or load the collection that stores the document chunks.
#
# A collection groups related vectors, documents, IDs, and metadata.
# It is conceptually similar to a table in a traditional database,
# although ChromaDB is designed specifically for vector retrieval.
#
# "get_or_create_collection" is useful during development:
# - If the collection does not exist yet, Chroma creates it.
# - If it already exists, Chroma loads the existing collection.
#
# This prevents us from creating a new collection every time
# the Streamlit application is restarted.
collection = client.get_or_create_collection(
    name="document_chunks"
)

# Store document chunks and embeddings using document-specific IDs.
#
# The source name is included in every ID so that chunks from
# different uploaded documents do not receive identical IDs.
#
# Example:
# annual_report.pdf -> annual_report.pdf_chunk_0
# research.txt      -> research.txt_chunk_0
#
# This allows multiple documents to coexist in the same
# ChromaDB collection without simple ID collisions.


def store_chunks(chunks, embeddings, source_name):
    ids = [
        f"{source_name}_chunk_{index}"
        for index in range(len(chunks))
    ]

    collection.upsert(  # update&insert
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist()
    )

# Search ChromaDB for the document chunks that are most
# semantically similar to the user's question.
#
# The query embedding is created with the same embedding model
# that was used for the document chunks. This is essential because
# query and document vectors must exist in the same vector space
# in order to compare their semantic similarity.
#
# n_results=3 implements Top-k retrieval with k=3:
# instead of returning only one chunk, ChromaDB returns the
# three most relevant chunks.
def query_chunks(query_embedding, n_results=3):
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=n_results
    )

    return results["documents"][0]