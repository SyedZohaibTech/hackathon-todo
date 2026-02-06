"""
Hugging Face Space Application Entry Point
This file serves as the entry point for running the Todo API backend on Hugging Face Spaces.
"""
import os
import subprocess
import time
import logging
from threading import Thread
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
import uvicorn

# Import the main application
from src.main import app as main_app
from src.mcp_server.server import app as mcp_app

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
hf_app.mount("/api", main_app)
hf_app.mount("/mcp", mcp_app)


def start_servers():
    """
    Start both the main API server and MCP server in separate threads
    This is used when running the application directly
    """
    def run_main_server():
        port = int(os.environ.get("PORT", 8000))
        logger.info(f"Starting main API server on port {port}")
        uvicorn.run(main_app, host="0.0.0.0", port=port)

    def run_mcp_server():
        port = int(os.environ.get("MCP_PORT", 8001))
        logger.info(f"Starting MCP server on port {port}")
        uvicorn.run(mcp_app, host="0.0.0.0", port=port)

    # Start both servers in daemon threads
    main_thread = Thread(target=run_main_server, daemon=True)
    mcp_thread = Thread(target=run_mcp_server, daemon=True)

    main_thread.start()
    mcp_thread.start()

    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down servers...")
        main_thread.join(timeout=1)
        mcp_thread.join(timeout=1)


if __name__ == "__main__":
    # When run directly, start both servers
    start_servers()