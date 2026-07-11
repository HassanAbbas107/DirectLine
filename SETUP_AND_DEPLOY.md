# DirectLine Deployment & Setup Guide

## Local Development

1. **Copy environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Start with Docker Compose:**
   ```bash
   docker compose up
   ```
   App runs on `http://localhost:8000`
   Healthcheck: `http://localhost:8000/health/`

3. **Create superuser (admin):**
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

## Docker Hub Setup

1. **Create a Docker Hub account** at https://hub.docker.com

2. **Add GitHub Secrets** to your repo (Settings → Secrets and variables → Actions):
   - `DOCKER_HUB_USERNAME` — your Docker Hub username
   - `DOCKER_HUB_PASSWORD` — your Docker Hub personal access token (not your password)

3. **GitHub Actions will auto-build and push** on every push to `main` branch

4. **View builds:** https://github.com/HassanAbbas107/DirectLine/actions

## Render Deployment

1. **Connect GitHub repo** to Render (https://render.com)

2. **Create PostgreSQL database:**
   - Dashboard → New → PostgreSQL
   - Copy the internal database URL

3. **Deploy web service:**
   - Dashboard → New → Web Service
   - Source: Connect GitHub repo
   - Build command: `python manage.py migrate`
   - Start command: `python -m gunicorn DirectLain.wsgi:application --bind 0.0.0.0:8000`
   - Environment variables:
     ```
     DB_ENGINE=django.db.backends.postgresql
     DB_NAME=directline
     DB_USER=<from PostgreSQL>
     DB_PASSWORD=<from PostgreSQL>
     DB_HOST=<internal-url-from-PostgreSQL>
     DEBUG=False
     SECRET_KEY=<generate-random-string>
     ALLOWED_HOSTS=<your-render-domain>
     ```

4. **Access your app:** `https://your-app.onrender.com`

## Monitoring

- **Healthcheck endpoint:** `GET /health/` — returns JSON status and database connection status
- **Docker healthcheck:** Auto-checks every 30 seconds, restarts container if unhealthy
- **Logs:** `docker compose logs web` or view in Render dashboard

## Updating Code

1. **Make code changes** and commit:
   ```bash
   git add .
   git commit -m "Your message"
   git push origin main
   ```

2. **GitHub Actions automatically:**
   - Builds Docker image
   - Runs tests (if configured)
   - Pushes to Docker Hub

3. **Render automatically:**
   - Pulls new image from Docker Hub
   - Restarts container
   - Runs migrations

## Required Environment Variables

- `DB_NAME` — PostgreSQL database name
- `DB_USER` — PostgreSQL username
- `DB_PASSWORD` — PostgreSQL password
- `DB_HOST` — PostgreSQL host (db for docker-compose, Render internal URL for production)
- `SECRET_KEY` — Django secret key (generate a 50+ character random string)
- `DEBUG` — Set to False in production
- `ALLOWED_HOSTS` — Comma-separated list of allowed domains

## Troubleshooting

**Container keeps restarting:**
```bash
docker compose logs web
```
Check for missing environment variables or database connection issues.

**Database migration fails:**
```bash
docker compose exec web python manage.py migrate --fake-initial
```

**Healthcheck fails:**
```bash
curl http://localhost:8000/health/
```
If returns 503, database is not connected.
