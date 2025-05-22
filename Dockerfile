# Use Python + uv baked in
FROM ghcr.io/astral-sh/uv:alpine

# 1. Copy only lock & manifest to leverage layer caching
WORKDIR /app
COPY pyproject.toml uv.lock ./

# 2. Sync dependencies into a fresh venv
RUN uv sync --locked --compile-bytecode

# 3. Copy app code
COPY app.py ./

# 4. Expose and run
EXPOSE 8000
CMD ["uv", "run", "gunicorn", "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", "app:app"]