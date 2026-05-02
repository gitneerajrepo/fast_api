# FastAPI Cohere Chatbot

A modern chatbot application built with FastAPI, LangChain, and Cohere API.

## Features

- 🤖 AI-powered chatbot using Cohere's LLM
- 💬 Conversation memory for context-aware responses
- ⚡ FastAPI for high-performance REST API
- 🔄 Simple REST endpoints for chat interactions
- 📚 Full API documentation with Swagger UI

## Prerequisites

- Python 3.8+
- Cohere API key (get one at [cohere.com](https://cohere.com))

## Installation

1. **Clone the repository** (if applicable)
   ```bash
   cd /workspaces/fast_api
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or using the installation command:
   ```bash
   pip install fastapi "fastapi[standard]" langchain langchain-community cohere python-dotenv pydantic
   ```

## Setup

1. **Create `.env` file** in the project root:
   ```bash
   cp .env.example .env
   ```

2. **Add your Cohere API key** to `.env`:
   ```
   COHERE_API_KEY=your_actual_cohere_api_key_here
   ```

## Running the Application

1. **Start the FastAPI server**:
   ```bash
   uvicorn main:app --reload
   ```
   
   The server will run at `http://localhost:8000`

2. **Access the API documentation**:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### 1. **GET `/`**
   Root endpoint with API information

### 2. **POST `/chat`**
   Send a message to the chatbot
   
   **Request:**
   ```json
   {
     "message": "What is machine learning?"
   }
   ```
   
   **Response:**
   ```json
   {
     "user_message": "What is machine learning?",
     "bot_response": "Machine learning is a subset of artificial intelligence..."
   }
   ```

### 3. **GET `/health`**
   Health check endpoint to verify chatbot status

### 4. **GET `/memory`**
   Get the current conversation history

### 5. **POST `/clear-memory`**
   Clear the conversation memory/history

## Testing with cURL

```bash
# Health check
curl http://localhost:8000/health

# Send a message
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello! How are you?"}'

# Get conversation history
curl http://localhost:8000/memory

# Clear memory
curl -X POST http://localhost:8000/clear-memory
```

## Testing with Python

```python
import requests

# Chat with the bot
response = requests.post(
    "http://localhost:8000/chat",
    json={"message": "What are the benefits of AI?"}
)
print(response.json())
```

## Project Structure

```
fast_api/
├── main.py              # FastAPI application with routes
├── chatbot.py           # LangChain chatbot implementation
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── .env                 # Environment variables (create this)
└── README.md            # This file
```

## Configuration

You can customize the chatbot behavior in `chatbot.py`:

- **Temperature**: Controls response randomness (0-1)
  - 0.0 = More deterministic
  - 1.0 = More random/creative
  
- **Max tokens**: Maximum length of generated responses

## Troubleshooting

### Issue: "Cohere API key not found"
- Ensure `.env` file exists with your API key
- Set the environment variable: `export COHERE_API_KEY=your_key`

### Issue: Connection errors
- Verify internet connection
- Check if Cohere API is accessible
- Verify your API key is valid

### Issue: Slow responses
- Cohere API might be rate-limited
- Consider adding delays between requests

## Next Steps & Enhancements

- Add message persistence (database)
- Implement user authentication
- Add rate limiting
- Store chat history
- Create a web UI frontend
- Add streaming responses
- Implement multi-user support

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [Cohere API Documentation](https://docs.cohere.com/)
- [Cohere Python SDK](https://docs.cohere.com/reference/implementations#python-sdk)

## License

MIT License

## Support

For issues and questions, please refer to the documentation links above.