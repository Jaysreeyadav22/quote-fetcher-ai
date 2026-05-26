import chromadb

from services.embedding_service import EmbeddingService



class SearchService:
    def __init__(self, collection_name: str  , embedding_service: EmbeddingService ):
        # Initialize the ChromaDB client and create a collection for storing chunks and their embeddings
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.client.get_or_create_collection(name=collection_name)
        self.embedding_service = embedding_service

    def index_chunks(self, chunks):
        # Index the chunks and their embeddings in the ChromaDB collection
        embedding = self.embedding_service.embed_batch(chunks)
        self.collection.add(
            documents=chunks,
            embeddings=embedding,
            ids=[str(i) for i in range(len(chunks))]
        )

    def search(self, query: str, top_k: int = 5):
        # Generate an embedding for the query and perform a similarity search in the ChromaDB collection
        query_embedding = self.embedding_service.embed(query)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        return results['documents'][0]
