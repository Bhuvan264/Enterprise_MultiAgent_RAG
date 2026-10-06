from langchain_ollama import OllamaLLM

from rag.retriever import search_documents


class DocumentAgent:

    def __init__(self):
        self.name = "Document Agent"

    def run(self, question):

        print(f"\n📄 {self.name} activated")

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

        # Document analysis prompt
        prompt = f"""
You are an enterprise document analysis assistant.

Your job is to answer questions about enterprise documents.

IMPORTANT RULES:

1. Use ONLY the provided document context.
2. Do not use outside knowledge.
3. Do not invent information.
4. Identify the relevant document or documents.
5. Explain the information clearly.
6. Mention the document name and page when possible.
7. If the information is not present, say:
   "I could not find this information in the provided documents."

================ DOCUMENT CONTEXT ================

{context}

================ QUESTION ================

{question}

================ ANSWER ================
"""

        # Initialize Llama
        llm = OllamaLLM(
            model="llama3.2"
        )

        print("\nAnalyzing documents...")

        answer = llm.invoke(prompt)

        # Display sources
        print("\n==============================")
        print("DOCUMENT SOURCES")
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

        return answer


if __name__ == "__main__":

    agent = DocumentAgent()

    question = "Which document contains the remote work policy?"

    answer = agent.run(question)

    print("\n==============================")
    print("DOCUMENT AGENT ANSWER")
    print("==============================")

    print(answer)