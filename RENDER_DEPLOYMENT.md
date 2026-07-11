# Docker Hub + Render Deployment Guide

## Prerequisites

1. **Docker Hub Account** — Sign up at https://hub.docker.com if you don't have one
2. **Render Account** — Sign up at https://render.com (free tier available)
3. **GitHub Repo** — Push this project to GitHub (optional, but recommended for Render auto-deploy)

## Step 1: Push Image to Docker Hub

```bash
# Log in to Docker Hub
docker login

# Tag your image with your Docker Hub username
docker tag directlain-web:latest YOUR_USERNAME/directline:latest

# Push to Docker Hub
docker push YOUR_USERNAME/directline:latest
```

Replace `YOUR_USERNAME` with your actual Docker Hub username.

## Step 2: Create PostgreSQL on Render

1. Go to https://render.com/dashboard
2. Click **New +** → **PostgreSQL**
3. Fill in:
   - Name: `directline-db`
   - Database: `directline`
   - User: `directline_user`
   - Leave password to auto-generate
4. Click **Create Database**
5. Copy the **Internal Database URL** — you'll need this

## Step 3: Deploy Web Service on Render

1. Go to https://render.com/dashboard
2. Click **New +** → **Web Service**
3. Select **Deploy existing image** (if pushing manually) or connect your GitHub repo
4. Fill in:
   - **Name**: `directline-web`
   - **Image URL**: `docker.io/YOUR_USERNAME/directline:latest`
   - **Region**: Choose closest to you
   - **Plan**: Free (or Starter for production)

5. Under **Environment**, add:
   ```
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=directline
   DB_USER=directline_user
   DB_PASSWORD=[paste from Render PostgreSQL password]
   DB_HOST=[paste from Render PostgreSQL Internal URL, extract host only]
   DB_PORT=5432
   DEBUG=False
   ALLOWED_HOSTS=YOUR_RENDER_URL.onrender.com
   SECRET_KEY=[generate a random 50-char string]
   ```

6. Click **Create Web Service**
7. Render will auto-deploy and run migrations

## Step 4: Access Your App

Once deployed, Render gives you a URL like `https://directline-web.onrender.com`. Visit it to access your help desk app.

## Ongoing Updates

After making code changes:
```bash
docker build -t YOUR_USERNAME/directline:latest .
docker push YOUR_USERNAME/directline:latest
```

Then click **Manual Deploy** on the Render dashboard, or set up GitHub auto-deployment.
