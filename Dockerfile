FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /usr/bin/psql /usr/bin/psql
COPY --from=builder /usr/lib/x86_64-linux-gnu/libpq* /usr/lib/x86_64-linux-gnu/
COPY --from=builder /root/.local /root/.local

ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=DirectLain.settings

COPY . .

RUN python manage.py collectstatic --noinput

# Create startup script for environment validation
RUN echo '#!/bin/bash\nset -e\n\necho "Checking required environment variables..."\n\nREQUIRED_VARS=("DB_NAME" "DB_USER" "DB_PASSWORD" "DB_HOST" "SECRET_KEY")\nfor var in "${REQUIRED_VARS[@]}"; do\n  if [ -z "$(eval echo $"$var")" ]; then\n    echo "ERROR: Required environment variable $var is not set"\n    exit 1\n  fi\ndone\n\necho "Running database migrations..."\npython manage.py migrate\n\necho "Starting gunicorn..."\nexec python -m gunicorn DirectLain.wsgi:application --bind 0.0.0.0:8000 --workers 4 --timeout 120\n' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health/', timeout=5)"

CMD ["/app/entrypoint.sh"]
