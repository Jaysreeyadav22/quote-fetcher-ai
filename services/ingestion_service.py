import fitz

class IngestionService:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path

   
    def extract_text(self) -> str:
        # Extract text from the PDF using PyMuPDF
        pdf = fitz.open(self.pdf_path)
        text = ""
        for page in pdf:
            text += page.get_text() 
        return text
    
  
    def chunk_text(self, text: str) -> list[str]:
        # Chunk the text into smaller pieces (e.g., 5 sentences per chunk)
        sentences = [sentence.strip() for sentence in text.split('.') if sentence.strip()]
        chunks: list[str] = []

        for i in range(0, len(sentences), 8):
            group = sentences[i:i+8]
            chunk_text = '.'.join(group)
            if len(chunk_text) > 100:
                chunks.append(chunk_text)

        return chunks
        
       
  
    def load(self):
        # Load the PDF, extract text, chunk it, and return the chunks (skipping the first 4)
        text = self.extract_text()
        chunks = self.chunk_text(text)
        return chunks[4:]
    

    
    
