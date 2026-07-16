FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY .env.example .

# Guest list / events mounted or injected via env in production
ENV SERVERLESS=true
ENV DEFAULT_COMMUNITY=The Inlets
ENV VERIFY_RETELL_SIGNATURES=true
ENV PORT=8080

EXPOSE 8080

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]
