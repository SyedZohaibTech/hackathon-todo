# Todo Application - Backend

This is the backend for the Todo application with AI assistant functionality.

## Deploying to Railway

### Prerequisites
- Railway account (sign up at [railway.app](https://railway.app))
- Railway CLI installed (optional): `npm i -g @railway/cli`

### Deployment Steps

1. **Prepare your Railway project**
   ```bash
   cd backend
   railway login
   ```

2. **Create a new Railway project**
   ```bash
   railway init
   ```

3. **Set environment variables**
   You'll need to set the following environment variables in Railway:
   - `DATABASE_URL`: PostgreSQL database URL (you can provision one through Railway)
   - `OPENAI_API_KEY`: Your OpenAI API key (required for AI agent functionality)
   - `MCP_SERVER_URL`: URL for the MCP server (typically `http://localhost:8001` locally, but will be different in production)

4. **Deploy**
   ```bash
   railway up
   ```

   Or if you're linking to an existing project:
   ```bash
   railway link <project-id>
   railway up
   ```

5. **Alternative: Deploy directly from GitHub**
   - Connect your GitHub repository to Railway
   - Enable automatic deployments
   - Railway will automatically use the `Dockerfile` and `railway.json` configurations

### Configuration Details

- The application listens on the port specified by the `PORT` environment variable (provided by Railway)
- The Dockerfile builds the Python environment and runs the FastAPI application
- The `railway.json` file specifies build and deployment configurations

## Deploying to Hugging Face Spaces

### Prerequisites
- Hugging Face account (sign up at [huggingface.co](https://huggingface.co))

### Deployment Steps

1. **Prepare your Hugging Face Space**
   Run the deployment preparation script:
   ```bash
   cd backend
   ./deploy_hf.sh
   ```

2. **Create a new Hugging Face Space**
   - Go to your Hugging Face Spaces dashboard
   - Click "Create new Space"
   - Choose "Docker" as the SDK
   - Select "CPU" hardware (sufficient for this application)
   - Set "Public" visibility (or Private as needed)

3. **Connect your repository**
   - Choose "From a repository on the internet"
   - Enter the URL to your GitHub repository containing this backend
   - Or fork this repository to your Hugging Face account first

4. **Set environment variables**
   In your Space settings, go to "Files and secrets" and add:
   - `DATABASE_URL`: Database connection string (e.g., `sqlite:///./todo.db` or PostgreSQL URL)
   - `OPENAI_API_KEY`: Your OpenAI API key (required for AI agent functionality)
   - `MCP_SERVER_URL`: URL of the MCP server (for AI agent communication)

5. **Wait for deployment**
   - The Space will automatically build using the Dockerfile
   - Monitor the build logs in the "Logs" tab
   - Once complete, your backend will be accessible at the Space URL

### Configuration Details

- The application listens on the port specified by the `PORT` environment variable (set by Hugging Face)
- The Dockerfile builds the Python environment and runs the FastAPI application
- The `space.yaml` file configures the Hugging Face Space environment

## Environment Variables

Required environment variables:
- `DATABASE_URL` - Database connection string (SQLite file path or PostgreSQL URL)
- `OPENAI_API_KEY` - API key for OpenAI (for AI agent functionality)
- `MCP_SERVER_URL` - URL of the MCP server (for AI agent communication)

## Services Architecture

The backend consists of:
- Main API server (port determined by `PORT` env var)
- MCP (Model Context Protocol) server for AI agent communication

## Connecting Frontend

Once deployed, update your frontend's environment variables:
- For Railway: Set `NEXT_PUBLIC_API_URL` to your Railway backend URL
  Example: `NEXT_PUBLIC_API_URL=https://your-app-production.up.railway.app`
- For Hugging Face: Set `NEXT_PUBLIC_API_URL` to your Hugging Face Space backend URL
  Example: `NEXT_PUBLIC_API_URL=https://your-username-todo-backend.hf.space`

## Troubleshooting

- For Railway: Check Railway logs with `railway logs`
- For Hugging Face: Check Space logs in the dashboard "Logs" tab
- Ensure your database is properly configured
- Verify environment variables are set correctly
- Check that CORS settings allow requests from your frontend domain