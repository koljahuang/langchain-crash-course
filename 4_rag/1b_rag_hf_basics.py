import os
import chromadb

from langchain_community.vectorstores import Chroma
from chromadb.utils import embedding_functions

# Define the persistent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
persistent_directory = os.path.join(current_dir, "db", "chroma_db")

client = chromadb.PersistentClient(persistent_directory)  # data stored in 'db' folder
em = embedding_functions.SentenceTransformerEmbeddingFunction()  # default is all-MiniLM-L6-v2 model
collection = client.get_collection(name='article', embedding_function=em)  # type: ignore

question = "Who is Odysseus' wife?"
collection = client.get_collection(name='article', embedding_function=em)  # type: ignore
results = collection.query(
    query_texts=question,
    n_results=1
)
print(results)