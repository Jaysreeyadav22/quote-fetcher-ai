# 📚 Quote Fetcher AI

Semantic book quote search system powered by AI and Azure AI Search.

## 🚧 Status
Work in progress (WIP)

## 🧠 Stack
- FastAPI
- Azure AI Search (planned)
- Cosmos DB (planned)
- Azure OpenAI (planned)

## 🚀 Goal
Build a semantic quote discovery system using RAG architecture.

## 🏗️ Architecture Strategy (Local → Azure Migration Path)

This project is designed in a modular way so it can evolve from local development to cloud-based production deployment.

### 🟢 Current Implementation (Local / Free Tier)

- Embeddings: `sentence-transformers (all-MiniLM-L6-v2)`
- Vector Search: Planned local cosine similarity (FAISS/Chroma)
- Data Storage: JSON files (mock dataset)
- LLM: Not integrated yet

### 🔵 Planned Azure Upgrade Path

| Component | Current | Future Upgrade |
|----------|--------|----------------|
| Embeddings | sentence-transformers | Azure OpenAI Embeddings |
| Vector Search | FAISS / Chroma (planned) | Azure AI Search (vector DB) |
| LLM | Not implemented | Azure OpenAI GPT models |
| Storage | JSON | Cosmos DB |

### 🧠 Design Principle

The system is built using a **pluggable service architecture**, meaning each AI component can be swapped without changing core business logic.
