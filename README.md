# DirectLine - Help Desk Ticket Management System

A modern, containerized Django help desk application for managing support tickets and communication between users and support staff.

## Overview

DirectLine is a web-based help desk platform built with Django 5.2, PostgreSQL, and Docker. It enables users to submit support requests (calls), receive real-time assistance through messages, and provides admins with a centralized dashboard to manage all tickets and communications.

**Live Demo:** Deploy on Render using the instructions below.

## Features

- **User Authentication** — Secure login/signup with role-based access control
- **Ticket Management** — Create, view, update, and delete support tickets (calls)
- **Real-time Messaging** — Exchange messages between users and support staff within tickets
- **Role-Based Access** — User and Admin roles with different permissions
- **Admin Dashboard** — View and manage all tickets and messages
- **Production Ready** — Docker containerization, healthchecks, environment validation
- **Monitoring** — Built-in `/health/` endpoint for uptime monitoring

## Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Backend | Django | 5.2.5 |
| Database | PostgreSQL | 16 (Alpine) |
| Server | Gunicorn | 23.0.0 |
| Container | Docker | Latest |
| Orchestration | Docker Compose | Latest |

## Project Structure

```
DirectLine/
├── DirectLain/                 # Django project settings
│   ├── settings.py             # Configuration (env-based)
│   ├── urls.py                 # URL routing
│   ├── wsgi.py                 # WSGI application
│   └── asgi.py                 # ASGI application
├── main_app/                   # Django app
│   ├── models.py               # Call, Message, User models
│   ├── views.py                # View logic + healthcheck
│   ├── urls.py                 # App URL routes
│   ├── forms.py                # Django forms
│   ├── migrations/             # Database migrations
│   ├── templates/              # HTML templates
│   │   ├── Calls/              # Ticket templates
│   │   ├── Messages/           # Message templates
│   │   └── registration/       # Auth templates
│   └── static/                 # CSS, JS, images
├── Dockerfile                  # Multi-stage Docker build
├── docker-compose.yml          # Local dev environment
├── .dockerignore                # Build optimization
├── .env.example                # Environment template
├── requirements.txt            # Python dependencies
├── manage.py                   # Django CLI
├── SETUP_AND_DEPLOY.md        # Deployment guide
└── README.md                   # This file
```

## Quick Start

### Prerequisites

- Docker & Docker Compose installed
- Python 3.12+ (for local development)
- PostgreSQL 16+ (or use Docker)

### Local Development

1. **Clone and navigate:**
   ```bash
   cd DirectLine/DirectLain
   ```

2. **Copy environment template:**
   ```bash
   cp .env.example .env
   ```

3. **Start services:**
   ```bash
   docker compose up
   ```

4. **Create admin user:**
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

5. **Access the app:**
   - Application: http://localhost:8000
   - Healthcheck: http://localhost:8000/health/
   - Admin panel: http://localhost:8000/admin (login with superuser)

### Environment Variables

Required variables (see `.env.example` for full list):

```env
DEBUG=False
SECRET_KEY=your-50-character-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

DB_ENGINE=django.db.backends.postgresql
DB_NAME=directline
DB_USER=directline_user
DB_PASSWORD=secure_password
DB_HOST=db
DB_PORT=5432
```

## Features & Endpoints

### User Features

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Redirect to calls list |
| `/auth/signup/` | GET, POST | User registration |
| `/auth/login/` | GET, POST | User login |
| `/auth/logout/` | GET | User logout |
| `/calls/` | GET | List user's tickets |
| `/calls/new/` | GET, POST | Create new ticket |
| `/calls/<id>/` | GET | View ticket details & messages |
| `/calls/<id>/delete/` | POST | Delete ticket (owner/admin only) |
| `/messages/` | GET | List user's messages |
| `/messages/new/<call_id>/` | GET, POST | Add message to ticket |
| `/messages/<id>/update/` | GET, POST | Edit message (author/admin only) |
| `/messages/<id>/delete/` | POST | Delete message (author/admin only) |
| `/health/` | GET | Healthcheck (returns JSON) |

### Admin Features

- View all tickets across all users
- View all messages from all users
- Update ticket status
- Delete tickets/messages from any user

## API Response Examples

### Healthcheck Endpoint

```bash
curl http://localhost:8000/health/
```

**Success (200):**
```json
{
  "status": "healthy",
  "service": "directline-api",
  "database": "connected"
}
```

**Failure (503):**
```json
{
  "status": "unhealthy",
  "service": "directline-api",
  "error": "Connection refused"
}
```

## Deployment

### Docker Hub + Render

1. **Push to Docker Hub:**
   ```bash
   docker tag directlain-web:latest YOUR_USERNAME/directline:latest
   docker push YOUR_USERNAME/directline:latest
   ```

2. **Deploy on Render:**
   - See [SETUP_AND_DEPLOY.md](SETUP_AND_DEPLOY.md) for step-by-step instructions
   - Render auto-runs migrations on startup
   - App accessible at: `https://your-app.onrender.com`

### Manual Docker Deployment (VPS/EC2)

```bash
docker pull YOUR_USERNAME/directline:latest
docker run -d \
  --name directline \
  -p 8000:80 \
  -e DB_HOST=postgres.example.com \
  -e DB_NAME=directline \
  -e DB_USER=admin \
  -e DB_PASSWORD=secure_pass \
  -e SECRET_KEY=your-secret-key \
  YOUR_USERNAME/directline:latest
```

## Development

### Running Tests

```bash
docker compose exec web python manage.py test main_app
```

### Database Migrations

```bash
# Create migration
docker compose exec web python manage.py makemigrations

# Apply migration
docker compose exec web python manage.py migrate

# Rollback (fake)
docker compose exec web python manage.py migrate main_app 0001 --fake
```

### Django Shell

```bash
docker compose exec web python manage.py shell
```

### Static Files

```bash
# Collect static files
docker compose exec web python manage.py collectstatic --noinput
```

## Monitoring & Logs

### View Logs

```bash
# All services
docker compose logs -f

# Web service only
docker compose logs -f web

# Database only
docker compose logs -f db
```

### Healthcheck Status

```bash
docker compose ps
```

Look for "healthy" status in the `STATUS` column.

### Docker Stats

```bash
docker stats
```

## Troubleshooting

### Database Connection Error

```bash
docker compose logs web
```

Check `DB_HOST`, `DB_USER`, `DB_PASSWORD`, and ensure database is running.

### Port Already in Use

Change port in `docker-compose.yml`:
```yaml
web:
  ports:
    - "8001:8000"  # Changed from 8000
```

### Static Files Not Loading

```bash
docker compose exec web python manage.py collectstatic --noinput --clear
```

### Container Keeps Restarting

1. Check logs: `docker compose logs web`
2. Verify all required environment variables are set
3. Check database connection: `docker compose logs db`

## Security Considerations

- **SECRET_KEY** — Change in production (generate 50+ char random string)
- **DEBUG** — Always set to `False` in production
- **ALLOWED_HOSTS** — Set to your domain in production
- **Database Password** — Use strong, unique password
- **HTTPS** — Render auto-enables HTTPS; ensure SSL_REDIRECT is enabled
- **CSRF Protection** — Enabled by default in Django

## Performance Optimization

- **Gunicorn Workers** — 4 workers configured for standard load
- **Database Indexing** — PostgreSQL indexes on commonly queried fields
- **Caching** — Layer caching in Docker multi-stage builds
- **Static Files** — Pre-collected and served by reverse proxy

## Contributing

Contributions welcome! Fork, create a feature branch, and submit a pull request.

```bash
git checkout -b feature/your-feature
git commit -m "Add your feature"
git push origin feature/your-feature
```

## License

MIT License — See LICENSE file for details.

## Author

**Hassan Abbas** — [GitHub](https://github.com/HassanAbbas107)

## Support

For issues, questions, or suggestions:
- Open an issue on [GitHub Issues](https://github.com/HassanAbbas107/DirectLine/issues)
- Email: [your-email@example.com]
- Documentation: See [SETUP_AND_DEPLOY.md](SETUP_AND_DEPLOY.md)

## Changelog

### v1.1.0 (Current)
- Add Docker containerization with multi-stage builds
- Add healthcheck endpoint and monitoring
- Add environment validation on startup
- Add Gunicorn for production WSGI server
- Add comprehensive deployment documentation

### v1.0.0
- Initial Django project setup
- User authentication and role-based access
- Ticket (Call) and Message models
- CRUD operations for tickets and messages

## References

- [Django Documentation](https://docs.djangoproject.com/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Gunicorn Documentation](https://gunicorn.org/)
- [Render Deployment](https://render.com/docs)

---

**Last Updated:** July 2026  
**Status:** Production Ready ✅
