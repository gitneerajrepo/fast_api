"""
LangChain-based chatbot using Cohere API
"""

import os
from typing import Optional
from dotenv import load_dotenv
from langchain_community.llms.cohere import Cohere

# Load environment variables
load_dotenv()

class CohereBot:
    """A chatbot powered by Cohere API using LangChain"""
    
    def __init__(self, api_key: Optional[str] = None, temperature: float = 0.7):
        """
        Initialize the Cohere chatbot
        
        Args:
            api_key: Cohere API key (defaults to COHERE_API_KEY env var)
            temperature: Temperature for response generation (0-1)
        """
        self.api_key = api_key or os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("Cohere API key not found. Set COHERE_API_KEY environment variable.")
        
        # Initialize Cohere LLM
        self.llm = Cohere(
            cohere_api_key=self.api_key,
            temperature=temperature,
            max_tokens=256
        )
        
        # Store conversation history
        self.chat_history = []
        
        # System prompt for the assistant
        self.system_prompt = "You are a helpful and friendly AI assistant."
    
    def chat(self, user_input: str) -> str:
        """
        Send a message and get a response from the chatbot
        
        Args:
            user_input: The user's message
            
        Returns:
            The chatbot's response
        """
        # Keep last 5 messages for context
        context_messages = self.chat_history[-10:] if self.chat_history else []
        
        # Build prompt with context
        context_str = "\n".join(context_messages) if context_messages else "No previous context."
        
        prompt = f"""{self.system_prompt}

Previous conversation:
{context_str}

User: {user_input}
Assistant:"""
        
        # Get response from Cohere LLM
        response = self.llm.invoke(prompt)
        
        # Store in history
        self.chat_history.append(f"User: {user_input}")
        self.chat_history.append(f"Assistant: {response}")
        
        return response.strip()
    
    def clear_memory(self):
        """Clear the conversation memory"""
        self.chat_history.clear()
    
    def get_memory(self) -> str:
        """Get the conversation history"""
        return "\n".join(self.chat_history)


# Global chatbot instance
def get_chatbot(api_key: Optional[str] = None) -> CohereBot:
    """Factory function to get or create a chatbot instance"""
    return CohereBot(api_key=api_key)


# Initialize global chatbot instance
def get_chatbot(api_key: Optional[str] = None) -> CohereBot:
    """Factory function to get or create a chatbot instance"""
    return CohereBot(api_key=api_key)
