from langchain_ollama import OllamaLLM

from rag.retriever import search_documents


class SummaryAgent:

    def __init__(self):
        self.name = "Summary Agent"

    def run(self, question):
        print(f"\n📝 {self.name} activated")

        # Retrieve relevant documents
        results = search_documents(question, top_k=5)

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
DOCUMENT {i + 1}
Source: {source}
Page: {page}

Content:
{document}
"""
            )

        context = "\n".join(context_parts)

        # Summary prompt
        prompt = f"""
You are an enterprise document summarization assistant.

Your task is to summarize the information from the provided documents.

IMPORTANT RULES:

1. Use ONLY the provided document context.
2. Do not use outside knowledge.
3. Do not invent information.
4. Include the main points and important details.
5. Keep the summary clear and easy to understand.
6. Use bullet points when appropriate.
7. Mention the relevant source document.
8. If the context does not contain enough information, say:
   "I could not find enough information in the provided documents."

================ DOCUMENT CONTEXT ================

{context}

================ REQUEST ================

{question}

================ SUMMARY ================
"""

        # Initialize Llama
        llm = OllamaLLM(
            model="llama3.2"
        )

        print("\nGenerating summary...")

        # Generate summary
        summary = llm.invoke(prompt)

        # Display sources
        print("\n==============================")
        print("SOURCES")
        print("==============================")

        for i, metadata in enumerate(metadatas):

            source = metadata.get(
                "source",
                "Unknown"
            )

            page = metadata.get(
                "page_label",
                metadata.get("page", "Unknown")
            )

            print(
                f"{i + 1}. {source} - Page {page}"
            )

        return summary


if __name__ == "__main__":

    agent = SummaryAgent()

    question = "Summarize the remote work policy."

    summary = agent.run(question)

    print("\n==============================")
    print("SUMMARY")
    print("==============================")

    print(summary)