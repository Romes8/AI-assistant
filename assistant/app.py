import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from utils.embeddings import document_loader, create_embeddings, get_vectorstore
from utils.rag import query_with_rag

app = Flask(__name__)
# Enable CORS for WordPress integration
CORS(app, origins="*")

# Check and print environment variables
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
print(f"OLLAMA_HOST from env: {OLLAMA_HOST}")

# Force use of docker network name if not explicitly set
if OLLAMA_HOST == "http://localhost:11434":
    print("WARNING: OLLAMA_HOST not set properly, forcing to http://ollama:11434")
    OLLAMA_HOST = "http://ollama:11434"
    # Set it back in the environment for any child processes
    os.environ["OLLAMA_HOST"] = OLLAMA_HOST

MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2:3b")
DATA_DIR = "/app/data"

def initialize():
    try:
        # Create data directory if it doesn't exist
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
            print(f"Created directory: {DATA_DIR}")
            
            # Create a sample file if directory was empty
            with open(os.path.join(DATA_DIR, "sample.txt"), "w") as f:
                f.write("This is a sample document for the LLM assistant.")
            print("Created sample document")
        
        # Check if the directory has files
        files = os.listdir(DATA_DIR)
        if not files:
            print("Warning: Data directory exists but is empty. Creating a sample file.")
            with open(os.path.join(DATA_DIR, "sample.txt"), "w") as f:
                f.write("This is a sample document for the LLM assistant.")
            
        print(f"Loading documents from {DATA_DIR}...")
        documents = document_loader(DATA_DIR)
        create_embeddings(documents)
        print("✅ Successfully loaded documents and created embeddings")
    except Exception as e:
        print(f"❌ Error initializing: {str(e)}")
        import traceback
        traceback.print_exc()

# Rest of the code remains the same...

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    query = data.get('message', '')
    
    if not query:
        return jsonify({"error": "No message provided"}), 400
    
    try:
        # Use RAG to get response with context
        response = query_with_rag(query, MODEL_NAME, OLLAMA_HOST)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        # Check if Ollama is running
        ollama_response = requests.get(f"{OLLAMA_HOST}/api/tags")
        if ollama_response.status_code == 200:
            # Check if our model is available
            models = ollama_response.json().get('models', [])
            model_available = any(m['name'].startswith(MODEL_NAME) for m in models)
            
            if not model_available:
                return jsonify({"status": "warning", "message": f"Model {MODEL_NAME} not found. Run 'docker exec ollama ollama pull {MODEL_NAME}'"})
            
            return jsonify({"status": "healthy"})
        return jsonify({"status": "error", "message": "Ollama is not responding correctly"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Could not connect to Ollama: {str(e)}"}), 500

if __name__ == '__main__':
    # Debug DNS lookup
    print("\nTesting network connectivity to Ollama:")
    try:
        import socket
        print(f"Looking up DNS for 'ollama'...")
        ollama_ip = socket.gethostbyname('ollama')
        print(f"ollama DNS resolves to: {ollama_ip}")
        
        print(f"Testing connection to ollama:11434...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        result = s.connect_ex((ollama_ip, 11434))
        if result == 0:
            print("Port 11434 is open on ollama")
        else:
            print(f"Port 11434 is not open on ollama (result: {result})")
        s.close()
        
        # Try HTTP connection
        import requests
        print(f"Making HTTP request to {OLLAMA_HOST}/api/tags...")
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        print(f"HTTP Status: {response.status_code}")
        print(f"Response: {response.text[:100]}")
    except Exception as e:
        print(f"Error testing connectivity: {str(e)}")
    
    # Initialize and start server
    initialize()
    app.run(host='0.0.0.0', port=5000)