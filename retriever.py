from sentence_transformers import util
from embeddings import create_query_embedding

def retrieve(query, chunks, chunk_embeddings):
    query_embedding = create_query_embedding(query)
    # 0 weil nur eine frage, daher 1. zeile
    scores = util.cos_sim(query_embedding, chunk_embeddings)[0]
    # .item() macht aus dem einzelnen Tensor-Wert einen normalen Python-Zahlenwert/Listenindex
    best_index = scores.argmax().item()
    return chunks[best_index]
