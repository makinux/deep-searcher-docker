FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim

WORKDIR /app

ENV UV_CACHE_DIR=/tmp/uv-cache \
    DEEPSEARCHER_MOUNT_DIR=/app/mounted_data

RUN mkdir -p "$UV_CACHE_DIR" /app/data /app/logs "$DEEPSEARCHER_MOUNT_DIR"

COPY pyproject.toml uv.lock LICENSE README.md ./
COPY deepsearcher/ ./deepsearcher/

RUN uv sync
RUN uv pip install "deepsearcher[ollama]"

COPY . .

VOLUME ["/app/data", "/app/logs", "/app/mounted_data"]

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/docs || exit 1

CMD ["uv", "run", "python", "main.py", "--enable-cors", "true"]
