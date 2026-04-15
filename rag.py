import os
import time
import shutil
import chromadb
from sentence_transformers import SentenceTransformer

CHUNK_SIZE    = 400
CHUNK_OVERLAP = 50
TOP_K         = 3
DATA_FOLDER   = "data"
STORE_FOLDER  = "vector_store"

print("  [RAG] Loading embedding model...")
embedder   = SentenceTransformer("all-MiniLM-L6-v2")
print("  [RAG] Embedding model ready.")

chroma     = chromadb.PersistentClient(path=STORE_FOLDER)
collection = chroma.get_or_create_collection(
    name="adk_rag_docs",
    metadata={"hnsw:space": "cosine"}
)


def read_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_documents(folder=DATA_FOLDER):
    docs = []
    if not os.path.exists(folder):
        print(f"  [RAG] No data/ folder found.")
        return docs
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        if filename.endswith(".txt"):
            text = read_txt(path)
            docs.append({"filename": filename, "text": text})
            print(f"  [RAG] Loaded: {filename} ({len(text)} chars)")
    return docs


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start  = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def index_documents():
    existing = collection.count()
    if existing > 0:
        print(f"  [RAG] Already indexed ({existing} chunks). Skipping.")
        return

    docs = load_documents()
    if not docs:
        print("  [RAG] No documents to index.")
        return

    all_chunks = []
    all_ids    = []
    all_meta   = []

    for doc in docs:
        chunks = chunk_text(doc["text"])
        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            all_ids.append(f"{doc['filename']}_chunk_{i}")
            all_meta.append({"source": doc["filename"], "chunk": i})

    print(f"  [RAG] Embedding {len(all_chunks)} chunks...")
    embeddings = embedder.encode(all_chunks).tolist()

    collection.add(
        documents=all_chunks,
        embeddings=embeddings,
        ids=all_ids,
        metadatas=all_meta,
    )
    print(f"  [RAG] Indexed {len(all_chunks)} chunks successfully.")


def retrieve(question, top_k=TOP_K, min_relevance=62.0):
    if collection.count() == 0:
        return None

    question_vector = embedder.encode([question]).tolist()

    results = collection.query(
        query_embeddings=question_vector,
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"]
    )

    chunks    = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    similarities = [round((1 - (d / 2)) * 100, 1) for d in distances]

    if similarities[0] < min_relevance:
        return None

    context_parts = []
    for chunk, meta, sim in zip(chunks, metadatas, similarities):
        if sim >= min_relevance:
            context_parts.append(
                f"[Source: {meta['source']} | Relevance: {sim}%]\n{chunk}"
            )

    return "\n\n---\n\n".join(context_parts) if context_parts else None