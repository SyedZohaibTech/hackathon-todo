import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

"""
Backend application entry point
References: Task T202, Spec §X
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Import routes using absolute imports
# from backend.routes.auth import router as auth_router
from routes.auth import router as auth_router
from routes.tasks import router as tasks_router

load_dotenv()

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(tasks_router)

@app.get("/")
def root():
    return {"message": "Todo API Running"}

# This allows running the file directly with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)