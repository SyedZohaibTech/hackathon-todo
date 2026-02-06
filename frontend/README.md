# Deploying Frontend to Vercel

## Prerequisites
- Vercel account (sign up at [vercel.com](https://vercel.com))
- Vercel CLI installed: `npm i -g vercel`

## Deployment Steps

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Set environment variables**
   Before deploying, you'll need to set the backend API URL:

   For production:
   ```bash
   vercel env add NEXT_PUBLIC_API_URL
   ```
   Then enter your Railway backend URL (e.g., `https://your-app-production.up.railway.app`)

   For development/staging:
   ```bash
   vercel env add NEXT_PUBLIC_API_URL --environment=preview
   ```
   Then enter your staging backend URL

4. **Deploy**
   ```bash
   vercel --prod
   ```

   Or for a preview deployment:
   ```bash
   vercel
   ```

5. **Connect to Git repository (recommended)**
   - Push your code to GitHub/GitLab/Bitbucket
   - Connect your repository to Vercel dashboard
   - Enable automatic deployments for every push

## Environment Variables

The frontend requires these environment variables:

- `NEXT_PUBLIC_API_URL`: The URL of your deployed backend API
  - Example: `https://sz453781it-hackathon-todo.hf.space`
  - For local development: `http://localhost:8000`
  - For production: `https://sz453781it-hackathon-todo.hf.space`

## Configuration Notes

- The Next.js application is configured to work with the API endpoints we've set up
- Authentication tokens are stored in browser's localStorage
- The AI assistant functionality connects to the backend's `/api/v1/chat/process_real` endpoint

## Connecting to Backend

Make sure your backend is deployed and accessible before deploying the frontend. The frontend will connect to:
- Authentication endpoints: `${NEXT_PUBLIC_API_URL}/api/v1/auth/`
- Task management endpoints: `${NEXT_PUBLIC_API_URL}/api/v1/tasks/`
- Chat/AI assistant endpoints: `${NEXT_PUBLIC_API_URL}/api/v1/chat/`

## Troubleshooting

- Verify that your backend API is accessible from the internet
- Check CORS settings on your backend to allow requests from your Vercel domain
- Monitor browser console for API connection errors
- Ensure environment variables are properly set in Vercel dashboard