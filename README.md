# 📚 Book Intelligence App

A RAG-powered app that lets you upload any book and interact with it using natural language. Search by emotion, extract quotes, get character summaries, or complete a partial quote — all grounded in the actual text of your book.

## What it does
- Upload any book as a PDF
- Search by emotion or feeling — *"I feel lost in love"*
- Extract relevant quotes and passages
- Get character and theme summaries
- Complete a partial quote from a hint

## Tech Stack
| Tool | Purpose |
|---|---|
| FastAPI | REST API backend |
| PyMuPDF | PDF text extraction |
| sentence-transformers | Local text embeddings (HuggingFace) |
| ChromaDB | Local vector database |
| Groq (LLaMA 3.3) | LLM for natural language responses |
| python-dotenv | Environment variable management |

## How it works
1. Upload a PDF → text is extracted and split into chunks
2. Each chunk is embedded into a vector using sentence-transformers
3. Vectors are stored in ChromaDB with the book as its own collection
4. User searches by emotion or query → query is embedded
5. ChromaDB finds the closest matching chunks
6. Groq reads those chunks and returns a grounded natural language response

## Setup

```bash
git clone https://github.com/yourusername/book-rag-app
cd book-rag-app
pip install -r requirements.txt
```

Add your Groq API key to `.env`:
Run the app:
```bash
uvicorn main:app --reload
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/upload` | Upload a PDF book |
| POST | `/search` | Search by emotion or query |

## Future Improvements
- Frontend UI for non-technical users
- Support for multiple books simultaneously
- Azure Blob Storage for PDF storage
- Azure AI Search + CosmosDB for production deployment
- User authentication
