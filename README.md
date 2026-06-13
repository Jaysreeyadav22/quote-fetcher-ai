# VoiceOfPages 📖

> Upload any book. Talk to its characters. Grounded in the actual text.

## Overview

VoiceOfPages lets you upload any book as a PDF and have a real conversation with its characters powered by the actual words of the book, not the internet.

Built for the GitHub Copilot Creative Apps Hackathon.

## Features

- 📚 Upload any book as a PDF
- 🎭 Chat with any character from the book in their authentic voice
- 🧠 Conversation history — characters remember what they said
- 🛡️ Grounded responses — answers come from the book text, not hallucination.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Angular 17 (standalone components) |
| Backend | FastAPI (Python) |
| Vector DB | ChromaDB |
| Embeddings | sentence-transformers |
| LLM | Azure AI Foundry — Llama 3.3 70B |
| Microsoft IQ | Azure AI Foundry (Foundry IQ) |

## Microsoft IQ Integration

All LLM responses are powered through **Azure AI Foundry**, fulfilling the Foundry IQ requirement. Book passages are retrieved semantically from ChromaDB and passed as grounded context to the model, reducing hallucination and ensuring character responses stay true to the source text.

## How GitHub Copilot Was Used

GitHub Copilot was used throughout the entire project build:

**Backend**
- Generated FastAPI endpoint boilerplate for upload, search and chat routes
- Suggested environment variable configuration and `.env` setup
- Assisted in debugging and resolving backend errors
- Generated ChromaDB integration and embedding service code
- Suggested sliding window chunking implementation

**Frontend**
- Generated Angular standalone component boilerplate
- Suggested `BehaviorSubject` state management pattern in the service layer
- Wrote HTTP client methods for upload and chat endpoints
- Generated SCSS styling for chat bubbles and upload screen
- Suggested `AfterViewChecked` scroll-to-bottom pattern for chat
- Copilot Chat used to debug CORS issues and Angular template errors

## Architecture

PDF Upload

↓

Text Extraction (PyMuPDF)

↓

Sentence-based Chunking (8 sentences per chunk)

↓

ChromaDB Vector Indexing (sentence-transformers embeddings)

↓

Semantic Search (top 3 relevant chunks retrieved)

↓

Azure AI Foundry — Llama 3.3 70B (grounded response)

↓

Angular Chat UI

## How to Run Locally

### Prerequisites
- Python 3.10+
- Node.js 20+
- Azure AI Foundry deployment (Llama 3.3 70B)

### Backend
```bash
cd quote-fetcher-ai
pip install -r requirements.txt
uvicorn main:app --reload
```

Add a `.env` file:

AZURE_ENDPOINT=your_azure_endpoint

AZURE_API_KEY=your_azure_api_key

AZURE_DEPLOYMENT=Llama-3.3-70B-Instruct

GROQ_API_KEY=your_groq_key  # fallback

### Frontend
```bash
cd voice-of-pages
npm install
ng serve
```

Open `http://localhost:4200`

## Deployment Path

| Component | Current | Production |
|---|---|---|
| Backend | Local (uvicorn) | Azure Container Apps |
| Frontend | Local (ng serve) | Azure Static Web Apps |
| Vector DB | Local (ChromaDB) | Azure Cosmos DB for MongoDB |

## Known Limitations

- Character quality depends on how much the book focuses on that character — minor characters may hallucinate
- Azure content filter may block certain book passages depending on content
- Large PDFs (500+ pages) may take longer to process on upload

## Demo

> "AI knows about your favourite books. It just can't read them. VoiceOfPages lets you upload any book you own and talk directly to its characters every response grounded in the actual text, not the internet."

---

Built with ❤️ using GitHub Copilot, Angular, FastAPI, ChromaDB and Azure AI Foundry.