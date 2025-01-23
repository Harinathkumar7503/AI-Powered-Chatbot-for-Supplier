from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import os

from . import models, database
from .database import engine, get_db
from .chatbot.agent import process_chat_message
from pydantic import BaseModel

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Chatbot API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    query_type: str
    db_query_desc: Optional[str] = None

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage, db: Session = Depends(get_db)):
    try:
        # Process the message through our LangGraph workflow
        result = await process_chat_message(chat_message.message)
        
        # Extract relevant information from the result
        response = {
            "response": result["response"],
            "query_type": result["query_type"],
            "db_query_desc": result.get("db_query_desc")
        }
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/products", response_model=List[dict])
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return [{"id": p.id, "name": p.name, "brand": p.brand, "price": p.price} for p in products]

@app.get("/api/suppliers", response_model=List[dict])
def get_suppliers(db: Session = Depends(get_db)):
    suppliers = db.query(models.Supplier).all()
    return [{"id": s.id, "name": s.name, "categories": s.product_categories} for s in suppliers]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 