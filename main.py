import os
from fastapi import FastAPI
from services.ingestion_service import IngestionService
from services.embedding_service import EmbeddingService
from services.search_service import SearchService
from groq import Groq
from dotenv import load_dotenv
from fastapi import UploadFile, File




load_dotenv()


app = FastAPI()

# Initialize services
embedding_service = EmbeddingService()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))





@app.post("/search")
async def search(query: str , collection_name: str):
    search_service = SearchService(collection_name=collection_name, embedding_service=embedding_service)
    # code runs when /search endpoint is called
    results = search_service.search(query)
    # join chunks into a single string for Groq processing
    combined_text = " ".join(results)
    # call Groq API to generate a response based on the combined text and the user's query
    groq_response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",        
        messages=[
            {"role": "system", "content": "You are a literary assistant for the book. When a user asks about an emotion or topic, respond naturally without ever saying 'the passage mentions', 'the context states', or 'based on the provided context'. Instead speak directly about the book and its characters. Include relevant quotes naturally within your explanation. Keep the tone warm and insightful."}
        ] + [
            {"role": "user", "content": f"Context: {combined_text}\n\nQuestion: {query}"}
        ]
    )
    # return the generated response from Groq
    return {"response": groq_response.choices[0].message.content}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
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
    
    return {"message": f"File '{file.filename}' uploaded and processed successfully."}