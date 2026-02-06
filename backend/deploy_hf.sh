#!/bin/bash

# Script to prepare backend for Hugging Face Spaces deployment

echo "Preparing backend for Hugging Face Spaces deployment..."

# Check if we're in the backend directory
if [ ! -f "requirements.txt" ] || [ ! -f "src/main.py" ]; then
    echo "Error: This script must be run from the backend directory"
    exit 1
fi

# Create/update the space configuration
cat > space.yaml << 'EOF'
runtime:
  huggingface: 3.0
  cuda: null
  language: en

sdk: docker
EOF

echo "Created/updated space.yaml configuration"

# Create/update the Hugging Face Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port (Hugging Face Spaces will set the PORT environment variable)
EXPOSE 8000

# Command to run the application
CMD ["sh", "-c", "python app.py"]
EOF

echo "Created/updated Dockerfile for Hugging Face Spaces"

# Create/update the main application entry point for Hugging Face
cat > app.py << 'EOF'
"""
Hugging Face Space Application Entry Point
This file serves as the entry point for running the Todo API backend on Hugging Face Spaces.
"""
import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

# Import the main application
from src.main import app as main_app

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the main FastAPI app for Hugging Face
hf_app = FastAPI(title="Todo API - Hugging Face Space", version="1.0.0")

# Add CORS middleware to allow requests from Hugging Face
hf_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hugging Face Spaces may have dynamic origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@hf_app.get("/")
def redirect_to_docs():
    """Redirect root to API documentation"""
    return RedirectResponse(url="/docs")

@hf_app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "huggingface-space-api"}

# Mount the main API application
hf_app.mount("/", main_app)

# For Hugging Face Spaces, we'll use this as the main app
app = hf_app

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting server on port {port}")
    uvicorn.run(hf_app, host="0.0.0.0", port=port)
EOF

echo "Created/updated app.py for Hugging Face Spaces"

echo ""
echo "Deployment preparation complete!"
echo ""
echo "To deploy to Hugging Face Spaces:"
echo "1. Create a new Space with the 'Docker' SDK"
echo "2. Connect your repository"
echo "3. Set the following environment variables in your Space settings:"
echo "   - DATABASE_URL: Database connection string"
echo "   - OPENAI_API_KEY: Your OpenAI API key (optional if not using AI features)"
echo "4. The Space will automatically build and deploy using the Dockerfile"
echo ""
echo "Your backend is now configured for Hugging Face Spaces deployment."