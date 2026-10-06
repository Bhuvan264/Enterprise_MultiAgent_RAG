from rag.qa import ask_question


class RAGAgent:

    def __init__(self):
        self.name = "RAG Agent"

    def run(self, question):

        print(f"\n🤖 {self.name} activated")

        # Ask the RAG system
        result = ask_question(question)

        # Return answer and sources
        return {
            "answer": result["answer"],
            "sources": result["sources"]
        }


if __name__ == "__main__":

    agent = RAGAgent()

    question = "What is the remote work policy?"

    result = agent.run(question)

    print("\n==============================")
    print("FINAL ANSWER")
    print("==============================")

    print(result["answer"])

    print("\n==============================")
    print("SOURCES")
    print("==============================")

    for source in result["sources"]:
        print(
            f"- {source['source']} - Page {source['page']}"
        )