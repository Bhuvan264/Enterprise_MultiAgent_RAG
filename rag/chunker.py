from langchain_text_splitters import RecursiveCharacterTextSplitter

from loader import load_all_pdfs


def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = splitter.split_documents(documents)

    print(f"Original pages: {len(documents)}")
    print(f"Created chunks: {len(chunks)}")

    return chunks


if __name__ == "__main__":
    documents = load_all_pdfs()

    chunks = chunk_documents(documents)

    print("\n--- First chunk preview ---")
    print(chunks[0].page_content)

    print("\n--- First chunk metadata ---")
    print(chunks[0].metadata)