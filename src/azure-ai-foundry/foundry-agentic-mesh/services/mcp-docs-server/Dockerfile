FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
# Optional: static OpenAPI files for reference
COPY openapi.yaml ./openapi.yaml
COPY openapi.json ./openapi.json

ENV PORT=8080
EXPOSE 8080

CMD ["uvicorn", "src.server_http:app", "--host", "0.0.0.0", "--port", "8080"]
