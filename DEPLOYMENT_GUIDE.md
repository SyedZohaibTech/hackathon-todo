# Deployment Guide: Frontend (Vercel) + Backend (Railway)

This guide explains how to deploy both the frontend and backend of the Todo application with AI assistant functionality.

## Architecture Overview

- **Frontend**: Next.js application hosted on Vercel
- **Backend**: FastAPI application hosted on Railway
- **Database**: PostgreSQL (can be provisioned through Railway)

## Deployment Order

1. Deploy the backend first
2. Update frontend environment variables with backend URL
3. Deploy the frontend

## Backend Deployment (Railway)

### Step 1: Prepare for Railway Deployment

The backend is already configured for Railway deployment with:
- `Dockerfile` for containerization
- `railway.json` for configuration
- Environment variable support for port and database

### Step 2: Deploy to Railway

1. Sign up at [railway.app](https://railway.app)

2. Install Railway CLI (optional):
   ```bash
   npm i -g @railway/cli
   ```

3. Login to Railway:
   ```bash
   railway login
   ```

4. Create a new project:
   ```bash
   cd backend
   railway init
   ```

5. Provision a PostgreSQL database:
   - In the Railway dashboard, go to your project
   - Click "New" → "Database" → "Provision PostgreSQL"
   - Or via CLI: `railway add postgresql`

6. Set environment variables in Railway:
   - `OPENAI_API_KEY`: Your OpenAI API key (required for AI functionality)
   - `MCP_SERVER_URL`: Will be the same as your main backend URL

7. Deploy:
   ```bash
   railway up
   ```

8. Take note of your backend URL (e.g., `https://your-app-production.up.railway.app`)

### Step 3: Verify Backend Deployment

After deployment, verify that:
- The API is accessible at your Railway URL
- The `/health` endpoint returns `{"status": "healthy"}`
- The `/docs` endpoint shows the API documentation
- The `/api/v1/chat/process_real` endpoint is available

## Frontend Deployment (Vercel)

### Step 1: Prepare for Vercel Deployment

The frontend is already configured for Vercel deployment.

### Step 2: Deploy to Vercel

1. Sign up at [vercel.com](https://vercel.com)

2. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

3. Login to Vercel:
   ```bash
   vercel login
   ```

4. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

5. Set the backend API URL environment variable:
   ```bash
   vercel env add NEXT_PUBLIC_API_URL production
   ```
   Enter your Railway backend URL when prompted (e.g., `https://your-app-production.up.railway.app`)

6. Deploy:
   ```bash
   vercel --prod
   ```

## Configuration Settings

### Backend Environment Variables (Railway)
- `DATABASE_URL`: PostgreSQL connection string (automatically set when provisioning DB)
- `OPENAI_API_KEY`: OpenAI API key for AI agent functionality
- `MCP_SERVER_URL`: URL of the MCP server (typically same as main backend URL)

### Frontend Environment Variables (Vercel)
- `NEXT_PUBLIC_API_URL`: URL of your deployed backend

## Testing the Deployment

1. Visit your deployed frontend URL
2. Register a new account
3. Log in
4. Navigate to the AI Assistant page
5. Try entering: "Add meeting with team tomorrow at 10 am"
6. Verify that the AI processes the request and creates the task

## Troubleshooting

### Common Issues:

1. **CORS errors**: Make sure your backend allows requests from your Vercel domain
2. **Database connection**: Verify that the PostgreSQL database is properly provisioned and connected
3. **Environment variables**: Double-check that all required environment variables are set correctly
4. **API connectivity**: Ensure the frontend can reach the backend API endpoints

### Debugging Steps:

1. Check Railway logs: `railway logs`
2. Check Vercel logs through the dashboard
3. Verify environment variables in both platforms
4. Test API endpoints directly using curl or Postman
5. Check browser developer tools for network errors

## Scaling Considerations

- For production use, consider upgrading your Railway plan for better performance
- Monitor API usage for OpenAI costs
- Consider implementing rate limiting for API endpoints
- Set up monitoring and alerting for both frontend and backend

## Maintenance

- Regularly update dependencies in both frontend and backend
- Monitor application logs for errors
- Backup your database regularly
- Plan for scaling as user base grows