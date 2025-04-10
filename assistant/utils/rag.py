import requests
import json
import os
from .embeddings import get_vectorstore

def query_with_rag(query, model_name, ollama_host):
    """Query using RAG (Retrieval Augmented Generation)"""
    print(f"RAG query with model: {model_name}, ollama host: {ollama_host}")
    
    # Get relevant documents from vector store
    vectorstore = get_vectorstore()
    docs = vectorstore.similarity_search(query, k=3)
    
    # Extract and format context
    context = "\n\n".join([doc.page_content for doc in docs])
    
    # Create prompt with context
    prompt = f"""You are a helpful personal assistant that provides information about your creator based on their portfolio and personal information.
    
CONTEXT INFORMATION:
{context}

Based only on the context information provided above, please answer the following question. Try to include as much inforation as possible but dont provide information which is not true.
If you don't know the answer or the information is not in the context, just say "I don't have that information about my creator."

Question: {query}

Answer:"""

    # Query Ollama
    try:
        print(f"Sending request to {ollama_host}/api/generate")
        response = requests.post(
            f"{ollama_host}/api/generate",
            json={
                "model": model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "top_p": 0.9,
                }
            },
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"Error from Ollama: Status {response.status_code}, Response: {response.text}")
            raise Exception(f"Error from Ollama: {response.text}")
        
        result = response.json()
        return result["response"]
    except Exception as e:
        print(f"Error in RAG query: {str(e)}")
        import traceback
        traceback.print_exc()
        raise