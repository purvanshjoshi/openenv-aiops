FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port 8000 for FastAPI (HF Space default routing is 7860, but OpenEnv HTTP typically allows mapping or we can bind to 0.0.0.0:8000 and Space config manages the rest, huggingface routes 7860, let's expose 8000).
# Hugging Face apps default to 7860. It's safer to expose 8000 as per openenv spec, but let's bind to 0.0.0.0:8000 which HF spaces parses. Wait! Huggingface prefers 7860. I'll configure server.py and openenv.yaml to 8000.
EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
