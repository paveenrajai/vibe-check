# syntax=docker/dockerfile:1
FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY packages ./packages
COPY apps/mcp ./apps/mcp

RUN uv sync --frozen --no-dev

ENV VIBE_CHECK_DATA_DIR=/data
ENV VIBE_CHECK_TRANSPORT=http
ENV VIBE_CHECK_HOST=0.0.0.0
ENV VIBE_CHECK_PORT=3100

RUN mkdir -p /data
VOLUME ["/data"]
EXPOSE 3100

CMD ["uv", "run", "vibe-check"]
