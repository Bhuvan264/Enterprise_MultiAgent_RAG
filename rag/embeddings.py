from langchain_ollama import OllamaEmbeddings

from chunker import chunk_documents
from loader import load_all_pdfs


def create_embeddings():
    print("Loading documents...")

    documents = load_all_pdfs()

    print("\nCreating chunks...")

    chunks = chunk_documents(documents)

    print("\nInitializing embedding model...")

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    print("Testing embedding generation...")

    test_embedding = embeddings.embed_query(
        "This is a test for our enterprise RAG system."
    )

    print(f"Embedding dimensions: {len(test_embedding)}")
    print("Embedding generation successful!")

    return embeddings, chunks


if __name__ == "__main__":
    embeddings, chunks = create_embeddings()

    print(f"\nTotal chunks ready for embedding: {len(chunks)}")