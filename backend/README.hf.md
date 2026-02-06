# Todo Application - Backend for Hugging Face Spaces

This is the backend for the Todo application with AI assistant functionality, configured for deployment on Hugging Face Spaces.

## About

This backend provides:
- REST API endpoints for task management
- User authentication and authorization
- AI integration through OpenAI
- MCP (Model Context Protocol) server for AI agent communication

## Deploying to Hugging Face Spaces

### Prerequisites

- Hugging Face account (sign up at [huggingface.co](https://huggingface.co))
- Git repository connected to your Hugging Face Space

### Deployment Steps

1. **Fork this repository to your Hugging Face account**

2. **Configure the Space**
   - Go to your Hugging Face Spaces dashboard
   - Create a new Space with the "Docker" SDK
   - Select "GPU" or "CPU" based on your needs (CPU is sufficient for this application)
   - Link your repository

3. **Set Environment Variables**

   In your Space settings, go to "Files and secrets" and add the following environment variables:

   - `DATABASE_URL`: Database connection string (SQLite file path or PostgreSQL URL)
   - `OPENAI_API_KEY`: Your OpenAI API key (required for AI agent functionality)
   - `MCP_SERVER_URL`: URL for the MCP server (typically the same as the main app URL)

4. **Space Configuration**

   The space is configured using:
   - `Dockerfile.hf`: Docker configuration optimized for Hugging Face Spaces
   - `space.yaml`: Hugging Face Spaces configuration
   - `app.py`: Main application entry point for Hugging Face

5. **Application Architecture**

   The application runs both:
   - Main API server (port determined by `PORT` env var)
   - MCP (Model Context Protocol) server for AI agent communication (on separate port)

## Environment Variables

Required environment variables to set in Hugging Face Spaces:
- `DATABASE_URL` - Database connection string (e.g., `sqlite:///./todo.db` or PostgreSQL URL)
- `OPENAI_API_KEY` - API key for OpenAI (for AI agent functionality)
- `MCP_SERVER_URL` - URL of the MCP server (for AI agent communication)

## Services Architecture

The backend consists of:
- Main API server (port determined by `PORT` env var)
- MCP (Model Context Protocol) server for AI agent communication

## Connecting Frontend

Once deployed, update your frontend's environment variables:
- Set `NEXT_PUBLIC_API_URL` to your Hugging Face Space backend URL
- Example: `NEXT_PUBLIC_API_URL=https://your-username-todo-backend.hf.space`

## Troubleshooting

- Check Space logs in the Hugging Face dashboard
- Ensure your database is properly configured
- Verify environment variables are set correctly
- Check that CORS settings allow requests from your frontend domain