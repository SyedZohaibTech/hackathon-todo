from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database.database import create_db_and_tables

# Create the FastAPI app
app = FastAPI(title="Todo API", version="1.0.0")

# Add CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    """Create database tables on startup"""
    create_db_and_tables()


# Include API routers
from .api.v1 import tasks, auth, users
app.include_router(tasks.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API!"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}


# Simple console application for basic task management
def console_app():
    """Simple console application for basic task management"""
    print("Welcome to the Todo Console App!")
    print("This is a simple console interface for managing tasks.")

    # Create tables if they don't exist
    create_db_and_tables()

    while True:
        print("\nOptions:")
        print("1. Exit")
        print("Choose an option: ", end="")

        try:
            choice = input().strip()

            if choice == "1":
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    import uvicorn
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "console":
        console_app()
    elif len(sys.argv) > 1 and sys.argv[1] == "docs":
        print("Documentation would be generated here")
    else:
        # Run the web server by default
        uvicorn.run(app, host="0.0.0.0", port=8000)