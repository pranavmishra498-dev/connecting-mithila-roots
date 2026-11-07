
from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# 1. ChromaDB folder path
CHROMA_PATH = Path(__file__).resolve().parent.parent / "data" / "chroma_db"


# 2. Same embedding model load karna
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


# 3. Existing ChromaDB connect karna
vector_store = Chroma(
    collection_name="mithila_knowledge",
    embedding_function=embeddings,
    persist_directory=str(CHROMA_PATH)
)


# 4. Retriever create karna
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)


# 5. User question se relevant documents retrieve karna
def retrieve_documents(question: str):

    results = retriever.invoke(question)

    return results


# 6. Testing
if __name__ == "__main__":

    question = "Who was Vidyapati?"

    documents = retrieve_documents(question)

    print("\nUser Question:", question)
    print("\nRetrieved Documents:")

    for i, doc in enumerate(documents, start=1):

        print(f"\nResult {i}:")
        print(doc.page_content)
        print("Source:", doc.metadata)
