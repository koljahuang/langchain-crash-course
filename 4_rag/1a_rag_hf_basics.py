import os

from sentence_transformers import SentenceTransformer
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma

# Define the directory containing the text file and the persistent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "books", "odyssey.txt")
persistent_directory = os.path.join(current_dir, "db", "chroma_db")

# Check if the Chroma vector store already exists
if not os.path.exists(persistent_directory):
    print("Persistent directory does not exist. Initializing vector store...")

    # Ensure the text file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"The file {file_path} does not exist. Please check the path."
        )

    # Read the text content from the file
    loader = TextLoader(file_path)
    documents = loader.load()

    # Split the document into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0) # 1000 tokens
    docs = text_splitter.split_documents(documents)

    # Display information about the split documents
    print("\n--- Document Chunks Information ---")
    print(f"Number of document chunks: {len(docs)}")
    print(f"Sample chunk:\n{docs[0].page_content}\n")

    # Create embeddings function
    from chromadb.utils import embedding_functions
    import chromadb
    from chromadb.db.base import UniqueConstraintError
    em = embedding_functions.SentenceTransformerEmbeddingFunction()
 
    client = chromadb.PersistentClient(persistent_directory)  # data stored in 'db' folder

    try:
        collection = client.create_collection(name='article', embedding_function=em) # type: ignore
    except UniqueConstraintError:  # already exist collection
        collection = client.get_collection(name='article', embedding_function=em) # type: ignore

    collection.add(
        documents = [doc.page_content for doc in docs],
        ids = list(map(lambda x: str(x), list(range(len(docs))))),
    )