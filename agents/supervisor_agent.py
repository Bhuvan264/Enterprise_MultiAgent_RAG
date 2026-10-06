from agents.rag_agent import RAGAgent
from agents.summary_agent import SummaryAgent
from agents.document_agent import DocumentAgent


class SupervisorAgent:

    def __init__(self):

        self.name = "Supervisor Agent"

        # Initialize specialized agents
        self.rag_agent = RAGAgent()
        self.summary_agent = SummaryAgent()
        self.document_agent = DocumentAgent()

    # ==========================================
    # FAST QUESTION CLASSIFICATION
    # ==========================================

    def classify_question(self, question):

        question_lower = question.lower().strip()

        # ------------------------------------------
        # SUMMARY REQUESTS
        # ------------------------------------------

        summary_keywords = [
            "summarize",
            "summary",
            "summarise",
            "overview",
            "main points",
            "key points",
            "give me a summary",
            "briefly explain"
        ]

        for keyword in summary_keywords:

            if keyword in question_lower:

                return "SUMMARY"


        # ------------------------------------------
        # DOCUMENT REQUESTS
        # ------------------------------------------

        document_keywords = [
            "which document",
            "what document",
            "which pdf",
            "what pdf",
            "document contains",
            "pdf contains",
            "document name",
            "available documents",
            "available pdf"
        ]

        for keyword in document_keywords:

            if keyword in question_lower:

                return "DOCUMENT"


        # ------------------------------------------
        # DEFAULT → RAG
        # ------------------------------------------

        return "RAG"


    # ==========================================
    # RUN SUPERVISOR
    # ==========================================

    def run(self, question):

        print("\n==============================")
        print("🧠 SUPERVISOR AGENT")
        print("==============================")

        print(
            f"User Question: {question}"
        )

        # Fast classification
        decision = self.classify_question(
            question
        )

        print(
            f"\n🧠 Supervisor Decision: {decision}"
        )


        # ==========================================
        # SUMMARY AGENT
        # ==========================================

        if decision == "SUMMARY":

            print(
                "\n➡️ Routing to Summary Agent"
            )

            summary = self.summary_agent.run(
                question
            )

            return {
                "answer": summary,
                "sources": []
            }


        # ==========================================
        # DOCUMENT AGENT
        # ==========================================

        elif decision == "DOCUMENT":

            print(
                "\n➡️ Routing to Document Agent"
            )

            answer = self.document_agent.run(
                question
            )

            return {
                "answer": answer,
                "sources": []
            }


        # ==========================================
        # RAG AGENT
        # ==========================================

        else:

            print(
                "\n➡️ Routing to RAG Agent"
            )

            return self.rag_agent.run(
                question
            )


# ==========================================
# DIRECT TEST
# ==========================================

if __name__ == "__main__":

    supervisor = SupervisorAgent()


    # Test 1
    question = "What is the remote work policy?"

    result = supervisor.run(
        question
    )

    print(
        "\n=============================="
    )

    print("FINAL ANSWER")

    print(
        "=============================="
    )

    print(
        result["answer"]
    )

    print(
        "\n=============================="
    )

    print("SOURCES")

    print(
        "=============================="
    )

    for source in result["sources"]:

        print(
            f"- "
            f"{source['source']} - "
            f"Page {source['page']}"
        )