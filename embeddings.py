from sentence_transformers import SentenceTransformer
# aus Paket - Klasse herunterladen

# fertiges embedding modell
model = SentenceTransformer("all-MiniLM-L6-v2")

def create_embeddings(chunks):
    embeddings = model.encode(chunks)
    return embeddings

def create_query_embedding(query):
    embedding = model.encode(query)
    return embedding