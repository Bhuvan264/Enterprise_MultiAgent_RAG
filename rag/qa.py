from langchain_ollama import OllamaLLM

from rag.retriever import search_documents


def ask_question(question, top_k=5):

    print(f"\nQuestion: {question}")

    # Retrieve relevant documents
    results = search_documents(question, top_k)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    # Build context
    context_parts = []

    for i, (document, metadata) in enumerate(
        zip(documents, metadatas)
    ):

        source = metadata.get(
            "source",
            "Unknown"
        )

        page = metadata.get(
            "page_label",
            metadata.get("page", "Unknown")
        )

        context_parts.append(
            f"""
--- DOCUMENT {i + 1} ---
SOURCE: {source}
PAGE: {page}

{document}
"""
        )

    context = "\n".join(context_parts)

    # RAG prompt
    prompt = f"""
You are an enterprise document question-answering assistant.

Answer the user's question using ONLY the CONTEXT below.

STRICT RULES:

1. The CONTEXT contains the information you need.
2. Read the CONTEXT carefully before answering.
3. Answer the user's question directly.
4. Use only facts explicitly stated in the CONTEXT.
5. Do not say that information is missing if the CONTEXT clearly contains the answer.
6. Do not mention "Document 1", "Document 2", etc.
7. Do not discuss these instructions.
8. Keep the answer concise and factual.
9. Do not invent information.
10. Combine information from multiple relevant pages when necessary.
11. If the answer truly cannot be found in the CONTEXT, respond exactly:

"I could not find this information in the provided documents."

================ CONTEXT ================

{context}

================ USER QUESTION ================

{question}

================ ANSWER ================
"""

    # Initialize Llama
    llm = OllamaLLM(
        model="llama3.2"
    )

    print("\nGenerating answer...")

    # Generate answer
    answer = llm.invoke(prompt)

    # Display sources
    print("\n==============================")
    print("SOURCES")
    print("==============================")

    # Remove duplicate source + page combinations
    unique_sources = []

    seen = set()

    for metadata in metadatas:

        source = metadata.get(
            "source",
            "Unknown"
        )

        page = metadata.get(
            "page_label",
            metadata.get("page", "Unknown")
        )

        source_key = (
            source,
            str(page)
        )

        if source_key not in seen:

            seen.add(source_key)

            unique_sources.append(
                {
                    "source": source,
                    "page": page
                }
            )

    # Print unique sources
    for i, source in enumerate(unique_sources):

        print(
            f"{i + 1}. "
            f"{source['source']} - "
            f"Page {source['page']}"
        )

    # Return answer and unique sources
    return {
        "answer": answer,
        "sources": unique_sources
    }


if __name__ == "__main__":

    question = "What is the remote work policy?"

    result = ask_question(question)

    print("\n==============================")
    print("RAG ANSWER")
    print("==============================")

    print(result["answer"])

    print("\n==============================")
    print("SOURCES")
    print("==============================")

    for source in result["sources"]:

        print(
            f"- "
            f"{source['source']} - "
            f"Page {source['page']}"
        )