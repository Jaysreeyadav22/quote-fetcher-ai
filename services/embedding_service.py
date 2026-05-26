from sentence_transformers import SentenceTransformer

class EmbeddingService:
    def __init__(self, model_name: str = 'paraphrase-MiniLM-L3-v2'):
        # Initialize the SentenceTransformer model for generating embeddings
        self.model = SentenceTransformer(model_name)

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        # Generate embeddings for a batch of texts
        return self.model.encode(texts).tolist()

    def embed(self, text: str) -> list[float]:
        # Generate an embedding for the given text
        return self.model.encode(text).tolist()