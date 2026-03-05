import gc
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

# Global instances for the engines
analyzer: AnalyzerEngine = None
anonymizer: AnonymizerEngine = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global analyzer, anonymizer
    print("Initializing Presidio Analyzer and Anonymizer engines...")
    
    # Load engines. The spacy en_core_web_sm model is used by default in Presidio.
    # Since we downloaded it during the Docker build, it will be loaded locally without internet.
    analyzer = AnalyzerEngine()
    anonymizer = AnonymizerEngine()
    
    print("Engines initialized successfully.")
    yield
    
    # Clean up on shutdown to prevent memory leaks
    print("Shutting down and cleaning up memory...")
    analyzer = None
    anonymizer = None
    gc.collect()

app = FastAPI(
    title="CompliGate",
    description="Offline-capable microservice for PII anonymization using Microsoft Presidio and spaCy",
    version="1.0.0",
    lifespan=lifespan
)

class SanitizeRequest(BaseModel):
    text: str

class SanitizeResponse(BaseModel):
    anonymized_text: str

@app.post("/sanitize", response_model=SanitizeResponse)
async def sanitize_text(request: SanitizeRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    
    try:
        # Analyze the text for PII entities
        # By default it checks for standard PIIs like PERSON, EMAIL_ADDRESS, IBAN_CODE, etc.
        results = analyzer.analyze(text=request.text, entities=[], language='en')
        
        # Anonymize the found entities (e.g. replacing with <PERSON>, <EMAIL_ADDRESS>)
        anonymized_result = anonymizer.anonymize(text=request.text, analyzer_results=results)
        
        return SanitizeResponse(anonymized_text=anonymized_result.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
