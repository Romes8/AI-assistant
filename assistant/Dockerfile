FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for unstructured and PDF processing
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    tesseract-ocr \
    poppler-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data for unstructured
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"

# Copy the rest of the application
COPY . .

# Expose the API port
EXPOSE 5000

# Start the application
CMD ["python", "app.py"]