import chromadb
from chromadb.utils import embedding_functions

def create_vector_db():
    chroma_client = chromadb.Client()

    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    # Create collection
    collection = chroma_client.get_or_create_collection(
        name="hr_handbook",
        embedding_function=emb_fn
    )

    raw_text = """PASTE YOUR FULL HR HANDBOOK TEXT HERE"""

    # Split into chunks
    raw_chunks = raw_text.split("##")

    clean_chunks = [chunk.strip() for chunk in raw_chunks if chunk.strip()]

    chunk_ids = [f"chunk_{i}" for i in range(len(clean_chunks))]

    # Add only if empty (avoid duplicates)
    if collection.count() == 0:
        collection.add(ids=chunk_ids, documents=clean_chunks)

    return collection