import chromadb
from chromadb.db.base import UniqueConstraintError
from chromadb.utils import embedding_functions
client = chromadb.PersistentClient(path="/Users/huangchao/Documents/it_learning/langchain-crash-course/4_rag/db/")  # data stored in 'db' folder
em = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="Huffon/sentence-klue-roberta-base")
try:
    collection = client.create_collection(name='article', embedding_function=em)
except UniqueConstraintError:  # already exist collection
    collection = client.get_collection(name='article', embedding_function=em)

collection.add(
        documents = ['NAVER Corporation Earnings Surprise', 'Samgsung Corporation Earnings Surprise'],
        ids = ['naver1', 'samsung1']
    )
# query
results = collection.query(
    query_texts='SamSam',
    n_results=1
)
print(results)