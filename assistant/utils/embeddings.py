import os
from langchain_community.document_loaders import (
    DirectoryLoader,
    PyPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
    BSHTMLLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

# Configure embeddings
CHROMA_HOST = os.getenv("CHROMA_HOST", "http://localhost:8000")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Debug env variables
print(f"CHROMA_HOST: {CHROMA_HOST}")
print(f"OLLAMA_HOST: {OLLAMA_HOST}")

COLLECTION_NAME = "personal_assistant"
PERSIST_DIRECTORY = "/tmp/chroma"

def document_loader(data_dir):
    """Load documents from various file types"""
    print(f"Loading documents from directory: {data_dir}")
    
    # Debug info
    if not os.path.exists(data_dir):
        print(f"Warning: Directory does not exist: {data_dir}")
        os.makedirs(data_dir, exist_ok=True)
        print(f"Created directory: {data_dir}")
    
    files = os.listdir(data_dir)
    print(f"Files in directory: {files}")
    
    documents = []
    
    # Load markdown files
    try:
        md_loader = DirectoryLoader(
            data_dir, 
            glob="**/*.md", 
            loader_cls=UnstructuredMarkdownLoader
        )
        md_docs = md_loader.load()
        print(f"Loaded {len(md_docs)} markdown documents")
        documents.extend(md_docs)
    except Exception as e:
        print(f"Error loading markdown: {str(e)}")
    
    # Load PDFs
    try:
        pdf_loader = DirectoryLoader(
            data_dir,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader
        )
        pdf_docs = pdf_loader.load()
        print(f"Loaded {len(pdf_docs)} PDF documents")
        documents.extend(pdf_docs)
    except Exception as e:
        print(f"Error loading PDFs: {str(e)}")
    
    # Load text files
    try:
        text_loader = DirectoryLoader(
            data_dir,
            glob="**/*.txt",
            loader_cls=TextLoader
        )
        text_docs = text_loader.load()
        print(f"Loaded {len(text_docs)} text documents")
        documents.extend(text_docs)
    except Exception as e:
        print(f"Error loading text files: {str(e)}")
    
    # Load HTML files
    try:
        html_loader = DirectoryLoader(
            data_dir,
            glob="**/*.html",
            loader_cls=BSHTMLLoader
        )
        html_docs = html_loader.load()
        print(f"Loaded {len(html_docs)} HTML documents")
        documents.extend(html_docs)
    except Exception as e:
        print(f"Error loading HTML: {str(e)}")
    
    print(f"Loaded {len(documents)} documents in total")
    
    # If no documents were found, create a sample document
    if len(documents) == 0:
        print("No documents found. Creating a sample document.")
        sample_file = os.path.join(data_dir, "sample.txt")
        with open(sample_file, "w") as f:
            f.write("This is a sample document for the LLM assistant.")
        
        # Load the sample document
        try:
            text_loader = TextLoader(sample_file)
            sample_doc = text_loader.load()
            documents.extend(sample_doc)
            print(f"Created and loaded sample document. Now have {len(documents)} documents.")
        except Exception as e:
            print(f"Error loading sample document: {str(e)}")
    
    return documents

def create_embeddings(documents):
    """Create embeddings and store in vector database"""
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(documents)
    
    print(f"Split documents into {len(splits)} chunks")
    print(f"Using Ollama at: {OLLAMA_HOST}")
    
    # Create embeddings using Ollama
    try:
        embeddings = OllamaEmbeddings(
            base_url=OLLAMA_HOST,  # This should be using the correct host from env
            model="llama3.2:3b"
        )
        
        print("Embedding function created successfully")
        
        # Store in Chroma
        print(f"Creating Chroma vectorstore with collection: {COLLECTION_NAME}")
        vectorstore = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
            persist_directory=PERSIST_DIRECTORY
        )
        
        print(f"Adding {len(splits)} document chunks to vectorstore")
        # Add documents to the vectorstore
        vectorstore.add_documents(splits)
        vectorstore.persist()
        print("Vectorstore created and persisted successfully")
        
        return vectorstore
    except Exception as e:
        print(f"Error creating embeddings: {str(e)}")
        import traceback
        traceback.print_exc()
        raise

def get_vectorstore():
    """Get the vector store for querying"""
    print(f"Getting vectorstore with Ollama at: {OLLAMA_HOST}")
    embeddings = OllamaEmbeddings(
        base_url=OLLAMA_HOST,
        model="llama3.2:3b"
    )
    
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )