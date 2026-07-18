FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY main.py .
COPY models.py .
COPY credentials.py .
COPY .env.example .

# Copy static assets and seed files
COPY static/ ./static/
COPY guest-list.example.json .
COPY vendors.seed.json .

# Create data directory for runtime files (SQLite, logs, etc.)
RUN mkdir -p /data

ENV SERVERLESS=true
ENV DEFAULT_COMMUNITY=The Inlets
ENV VERIFY_RETELL_SIGNATURES=true

EXPOSE 8080

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]
