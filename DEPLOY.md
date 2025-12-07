# Deployment Guide

This guide covers deploying Crawley to free hosting platforms.

## Railway (Recommended - Free Tier Available)

Railway offers a free tier with $5 credit per month, perfect for testing deployments.

### Prerequisites

- GitHub account
- Railway account (sign up at https://railway.app)

### Deployment Steps

1. **Fork/Clone the repository** (if not already done)

2. **Connect to Railway:**
   - Go to https://railway.app
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `crowley` repository

3. **Deploy Redis Service:**
   - In Railway dashboard, click "New" → "Database" → "Add Redis"
   - Railway will automatically provision a Redis instance
   - Note the Redis connection details (host, port, password)

4. **Deploy Crawler Service:**
   - Click "New" → "GitHub Repo" → Select your `crowley` repo
   - Railway will detect the Dockerfile and build automatically
   - Add environment variables:
     - `REDIS_HOST`: Your Redis host (from step 3)
     - `REDIS_PORT`: Your Redis port (usually 6379)
     - `REDIS_PASSWORD`: Your Redis password (if set)
     - `PORT`: Railway will auto-set this (default: 5000)
   - Railway will automatically expose the web UI on a public URL

5. **Access the Web UI:**
   - Railway provides a public URL for your service (e.g., `https://your-app.railway.app`)
   - Open the URL in your browser to access the web interface
   - The web UI allows you to run crawls with all options
   - Click "View Redis Data" to access Redis UI (if deployed separately)

### Accessing the Web UI

Once deployed, Railway will provide a public URL `https://mr-crowley-production.up.railway.app/`. Simply open this URL in your browser to access the web interface where you can:

- Enter crawl parameters (URL, level, user-agent, etc.)
- Start crawls with a click
- View real-time crawl logs
- Access Redis data (if Redis UI is configured)

No CLI needed - everything works through the web interface!

## Alternative: Render

Render also offers a free tier suitable for Docker deployments.

### Deployment Steps

1. **Sign up at https://render.com**

2. **Create a Redis Instance:**
   - New → Redis
   - Choose free tier
   - Note connection details

3. **Create a Web Service:**
   - New → Web Service
   - Connect your GitHub repo
   - Build Command: `docker build -t crawley .`
   - Start Command: `sleep infinity`
   - Add environment variables for Redis

4. **Access via Render Shell:**
   - Use Render's shell feature to run crawler commands

## Alternative: Fly.io

Fly.io offers a generous free tier with good Docker support.

### Deployment Steps

1. **Install Fly CLI:**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Create fly.toml:**
   ```bash
   fly launch
   ```

3. **Deploy:**
   ```bash
   fly deploy
   ```

4. **Run commands:**
   ```bash
   fly ssh console -C "python crawler.py https://crawlme.monzo.com/ --use-storage --level 2"
   ```

## Environment Variables

All platforms require these environment variables when using Redis:

- `REDIS_HOST`: Redis server hostname
- `REDIS_PORT`: Redis server port (default: 6379)
- `REDIS_PASSWORD`: Redis password (if required)

## Notes

- Free tiers have resource limits (CPU, memory, bandwidth)
- Services may sleep after inactivity (Render free tier)
- Consider upgrading for production use
- Always use `--level` flag to limit crawl depth in free tier environments

