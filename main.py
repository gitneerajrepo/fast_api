"""
FastAPI application with LangChain-powered Cohere chatbot
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from chatbot import get_chatbot, CohereBot

# Initialize FastAPI app
app = FastAPI(
    title="Cohere Chatbot API",
    description="A chatbot powered by LangChain and Cohere API",
    version="1.0.0"
)

# Global chatbot instance
chatbot: CohereBot = None


class MessageRequest(BaseModel):
    """Request model for chat messages"""
    message: str


class MessageResponse(BaseModel):
    """Response model for chat messages"""
    user_message: str
    bot_response: str


@app.on_event("startup")
async def startup_event():
    """Initialize chatbot on startup"""
    global chatbot
    try:
        chatbot = get_chatbot()
    except ValueError as e:
        print(f"Warning: {e}")


@app.get("/")
def read_root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Cohere Chatbot API",
        "endpoints": {
            "chat": "/chat",
            "health": "/health",
            "docs": "/docs",
            "clear_memory": "/clear-memory"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    if chatbot is None:
        return {"status": "unhealthy", "message": "Chatbot not initialized"}
    return {"status": "healthy", "message": "Chatbot is running"}


@app.post("/chat", response_model=MessageResponse)
async def chat(request: MessageRequest) -> MessageResponse:
    """
    Send a message to the chatbot and get a response
    
    Args:
        request: MessageRequest containing the user's message
        
    Returns:
        MessageResponse with user message and bot response
    """
    if chatbot is None:
        raise HTTPException(
            status_code=503,
            detail="Chatbot service is not available. Please set COHERE_API_KEY environment variable."
        )
    
    if not request.message or not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )
    
    try:
        bot_response = chatbot.chat(request.message)
        return MessageResponse(
            user_message=request.message,
            bot_response=bot_response
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating response: {str(e)}"
        )


@app.post("/clear-memory")
async def clear_memory():
    """Clear the conversation memory"""
    if chatbot is None:
        raise HTTPException(
            status_code=503,
            detail="Chatbot service is not available"
        )
    
    chatbot.clear_memory()
    return {"message": "Conversation memory cleared"}


@app.get("/memory")
async def get_memory():
    """Get the current conversation history"""
    if chatbot is None:
        raise HTTPException(
            status_code=503,
            detail="Chatbot service is not available"
        )
    
    memory = chatbot.get_memory()
    return {"conversation_history": memory}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)