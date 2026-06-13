import os
from fastapi import FastAPI
from services.ingestion_service import IngestionService
from services.embedding_service import EmbeddingService
from services.search_service import SearchService
from groq import Groq
from dotenv import load_dotenv
from fastapi import UploadFile, File
from openai import AzureOpenAI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel





load_dotenv()


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
embedding_service = EmbeddingService()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))




azure_client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    api_key=os.getenv("AZURE_API_KEY"),
    api_version="2024-02-01"
)



class ChatRequest(BaseModel):
    history: list[dict] = []

@app.post("/search")
async def search(query: str , collection_name: str):
    try:
        # Validate environment variables
        azure_endpoint = os.getenv("AZURE_ENDPOINT")
        azure_deployment = os.getenv("AZURE_DEPLOYMENT")
        
        if not azure_endpoint or not azure_deployment:
            return {"error": f"Missing Azure config. AZURE_ENDPOINT: {bool(azure_endpoint)}, AZURE_DEPLOYMENT: {bool(azure_deployment)}"}
        
        search_service = SearchService(collection_name=collection_name, embedding_service=embedding_service)
        # code runs when /search endpoint is called
        results = search_service.search(query)
        # join chunks into a single string for Groq processing
        combined_text = " ".join(results)
        
       # LLM Client - Azure AI Foundry (primary)
        azure_response = azure_client.chat.completions.create(
            model=azure_deployment,
            messages=[
               {"role": "system", "content": (
    "You are a literary assistant. "
    "Answer questions based only on the provided context passages from the book. "
    "Be thoughtful and insightful in your responses. "
    "Never say 'the passage mentions' or 'the context states'. "
    "Speak directly about the book and its themes."
)}
            ] + [
                {"role": "user", "content": f"Context: {combined_text}\n\nQuestion: {query}"}
            ]
        )
        # return the generated response from Azure
        return {"response": azure_response.choices[0].message.content}
    # GROQ FALLBACK - uncomment to switch back
# groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    except Exception as e:
        print(f"Error in /search: {str(e)}")
        return {"error": str(e)}
    

@app.post("/chat")
async def chat(
    query: str,
    character_name: str,
    collection_name: str,
    request: ChatRequest
):
    try:
        search_service_instance = SearchService(
            collection_name=collection_name,
            embedding_service=embedding_service
        )
        results = search_service_instance.search(query, top_k=3)
        combined_text = " ".join(results)[:2000]

        messages = [
            {
                "role": "system",
                "content": (
                   f"You are {character_name}, a character from a literary work. "
f"Speak only from the provided context and conversation history. "
f"If the context is insufficient, say 'The pages do not speak of this.' "
f"Never use asterisks or action descriptions like *smiles* or *laughs*. "
f"Speak naturally in first person only. "
f"Respond to the user's message naturally — if greeted, greet back briefly before continuing. "
f"Be brief, authentic, and true to the character. "
f"Context: {combined_text}"
                )
            }
        ]
        messages.extend(request.history)
        messages.append({"role": "user", "content": query})

        response = azure_client.chat.completions.create(
            model=os.getenv("AZURE_DEPLOYMENT"),
            messages=messages
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        # Save the uploaded file to a temporary location
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # Process the uploaded PDF file
        ingestion_service = IngestionService(pdf_path=temp_file_path)
        chunks = ingestion_service.load()
        # create a new search service instance for the new collection
        search_service = SearchService(collection_name=f"{file.filename}_collection", embedding_service=embedding_service)
        search_service.index_chunks(chunks)
        # Remove the temporary file after processing
        os.remove(temp_file_path)
        
        return {
    "message": f"File '{file.filename}' uploaded successfully.",
    "collection_name": f"{file.filename}_collection"
                }
    except Exception as e:
        print(f"Error in /upload: {str(e)}")
        return {"error": str(e)}