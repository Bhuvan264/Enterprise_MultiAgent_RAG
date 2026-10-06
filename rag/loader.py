from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader


DOCUMENTS_DIR = Path("data/documents")


def load_all_pdfs():
    documents = []

    pdf_files = list(DOCUMENTS_DIR.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found.")
        return documents

    print(f"Found {len(pdf_files)} PDF files.")

    for pdf_file in pdf_files:
        print(f"\nLoading: {pdf_file.name}")

        loader = PyPDFLoader(str(pdf_file))
        pdf_documents = loader.load()

        for document in pdf_documents:
            document.metadata["source"] = pdf_file.name

        documents.extend(pdf_documents)

        print(f"Pages loaded: {len(pdf_documents)}")

    print(f"\nTotal pages loaded: {len(documents)}")

    return documents


if __name__ == "__main__":
    docs = load_all_pdfs()

    if docs:
        print("\n--- First document preview ---")
        print(docs[0].page_content[:1000])
        print("\nMetadata:")
        print(docs[0].metadata)