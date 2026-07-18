# StadiumSenseAI — Single container, Flask + gunicorn
# Serves both the REST API and the static frontend HTML

FROM python:3.11-slim

# Non-root user for security
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

WORKDIR /app

# Install dependencies first (leverages Docker layer cache)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Hand ownership to non-root user
RUN chown -R appuser:appgroup /app
USER appuser

WORKDIR /app/backend

# PORT is injected by Render at runtime (default 8080)
ENV PORT=8080
EXPOSE 8080

# Production: gunicorn WSGI server — 2 workers, binds to $PORT
CMD gunicorn --workers 2 --bind 0.0.0.0:$PORT --timeout 60 --access-logfile - --error-logfile - app:app
