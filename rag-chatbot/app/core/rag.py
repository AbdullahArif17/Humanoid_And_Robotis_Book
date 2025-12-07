from typing import List, Dict, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from openai import OpenAI
from app.config import settings
from app.core.embeddings import embedding_generator
import logging

logger = logging.getLogger(__name__)


class RAGEngine:
    """Retrieval-Augmented Generation engine."""
    
    def __init__(self):
        # Initialize Qdrant client
        self.qdrant_client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key
        )
        self.collection_name = settings.qdrant_collection_name
        
        # Initialize OpenAI client
        self.openai_client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
    
    def retrieve_context(
        self, 
        query: str, 
        selected_text: Optional[str] = None,
        limit: int = None
    ) -> List[Dict]:
        """
        Retrieve relevant context from the vector database.
        
        Args:
            query: User's question
            selected_text: Optional text selected by user for context
            limit: Maximum number of chunks to retrieve
            
        Returns:
            List of relevant text chunks with metadata
        """
        if limit is None:
            limit = settings.max_context_chunks
        
        # Combine query with selected text if provided
        search_query = query
        if selected_text:
            search_query = f"{query}\n\nContext: {selected_text}"
        
        # Generate embedding for the query
        query_embedding = embedding_generator.generate_embedding(search_query)
        
        # Search in Qdrant
        try:
            search_results = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
                with_payload=True
            )
            
            # Extract and format results
            contexts = []
            for result in search_results:
                contexts.append({
                    'content': result.payload.get('content', ''),
                    'metadata': result.payload.get('metadata', {}),
                    'score': result.score
                })
            
            return contexts
        
        except Exception as e:
            logger.error(f"Error retrieving context from Qdrant: {e}")
            return []
    
    def generate_response(
        self,
        query: str,
        contexts: List[Dict],
        chat_history: List[Dict[str, str]] = None
    ) -> str:
        """
        Generate a response using retrieved context and chat history.
        
        Args:
            query: User's question
            contexts: Retrieved context chunks
            chat_history: Previous messages in the conversation
            
        Returns:
            Generated response
        """
        # Build context string
        context_str = "\n\n".join([
            f"[Source: {ctx['metadata'].get('source_file', 'Unknown')}]\n{ctx['content']}"
            for ctx in contexts
        ])
        
        # Build system prompt
        system_prompt = f"""You are an expert AI assistant for the "Physical AI & Humanoid Robotics" book. 
Your role is to help users understand concepts from the book by answering their questions accurately and clearly.

Use the following context from the book to answer the user's question. If the answer cannot be found in the context, say so clearly and offer to help with related topics that are covered in the book.

Context from the book:
{context_str}

Guidelines:
- Provide accurate, technical answers based on the book content
- Be clear and educational
- If referencing specific modules or sections, mention them
- If the question is outside the book's scope, acknowledge this
- Use code examples from the context when relevant
"""
        
        # Build messages
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add chat history if provided
        if chat_history:
            messages.extend(chat_history[-6:])  # Last 3 exchanges
        
        # Add current query
        messages.append({"role": "user", "content": query})
        
        # Generate response
        try:
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I apologize, but I encountered an error generating a response. Please try again."
    
    def chat(
        self,
        query: str,
        selected_text: Optional[str] = None,
        chat_history: List[Dict[str, str]] = None
    ) -> Dict[str, any]:
        """
        Complete RAG chat flow: retrieve context and generate response.
        
        Args:
            query: User's question
            selected_text: Optional selected text for context
            chat_history: Previous conversation messages
            
        Returns:
            Dictionary with response and metadata
        """
        # Retrieve relevant context
        contexts = self.retrieve_context(query, selected_text)
        
        # Generate response
        response = self.generate_response(query, contexts, chat_history)
        
        return {
            'response': response,
            'contexts_used': len(contexts),
            'sources': [ctx['metadata'].get('source_file', 'Unknown') for ctx in contexts]
        }


# Global instance
rag_engine = RAGEngine()
