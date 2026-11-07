 
from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# 1. Documents folder ka path
DOCUMENTS_PATH = Path(__file__).parent / "documents"
print("Documents folder path:", DOCUMENTS_PATH)
print("Folder exists:", DOCUMENTS_PATH.exists())
print("TXT files:", list(DOCUMENTS_PATH.glob("*.txt")))

# 2. ChromaDB storage folder ka path
CHROMA_PATH = Path(__file__).resolve().parent.parent / "data" / "chroma_db"


# 3. Documents load karna
documents = []

for file_path in DOCUMENTS_PATH.glob("*.txt"):
    loader = TextLoader(str(file_path), encoding="utf-8")
    documents.extend(loader.load())


# 4. Text splitting
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)
print("Documents loaded:", len(documents))
print("Chunks created:", len(chunks))

if not chunks:
    raise ValueError(
        "No chunks found! Please check your documents folder and text files."
    )


# 5. Embedding model load karna
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


# 6. ChromaDB mein documents store karna
vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=str(CHROMA_PATH),
    collection_name="mithila_knowledge"
)


# 7. Result check karna
print("Documents loaded:", len(documents))
print("Chunks created:", len(chunks))
print("Chunks stored:", vector_store._collection.count())

print("\nChromaDB ingestion completed successfully!")
