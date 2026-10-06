import chromadb
from langchain_ollama import OllamaEmbeddings


CHROMA_PATH = "vectorstore/chroma_db"
COLLECTION_NAME = "enterprise_documents"


def get_retriever():

    print("Connecting to ChromaDB...")

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    print(f"Collection loaded: {COLLECTION_NAME}")
    print(f"Total documents: {collection.count()}")

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    return collection, embeddings


def search_documents(query, top_k=5):

    collection, embeddings = get_retriever()

    print(f"\nSearching for: {query}")

    query_embedding = embeddings.embed_query(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results


if __name__ == "__main__":

    results = search_documents(
        "What is the remote work policy?"
    )

    print("\n===== SEARCH RESULTS =====")

    for i, document in enumerate(results["documents"][0]):

        print(f"\n--- Result {i + 1} ---")
        print(document[:500])

        print("\nMetadata:")
        print(results["metadatas"][0][i])