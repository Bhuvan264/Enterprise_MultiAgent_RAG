import chromadb
from langchain_ollama import OllamaEmbeddings

from chunker import chunk_documents
from loader import load_all_pdfs


CHROMA_PATH = "vectorstore/chroma_db"
COLLECTION_NAME = "enterprise_documents"


def create_vectorstore():

    print("Loading documents...")

    documents = load_all_pdfs()

    print("\nCreating chunks...")

    chunks = chunk_documents(documents)

    print("\nInitializing embedding model...")

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    print("\nConnecting to ChromaDB...")

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    # Delete old collection if it exists
    try:
        client.delete_collection(COLLECTION_NAME)
        print("Old collection deleted.")
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME
    )

    print("\nCreating embeddings for chunks...")

    texts = [chunk.page_content for chunk in chunks]

    vectors = embeddings.embed_documents(texts)

    print(f"Generated {len(vectors)} embeddings.")

    print("\nStoring data in ChromaDB...")

    ids = [f"chunk_{i}" for i in range(len(chunks))]

    metadatas = [chunk.metadata for chunk in chunks]

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=vectors,
        metadatas=metadatas
    )

    print("\n✅ Vector store created successfully!")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Documents stored: {collection.count()}")


if __name__ == "__main__":
    create_vectorstore()