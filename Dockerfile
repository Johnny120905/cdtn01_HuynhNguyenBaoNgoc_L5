# ==============================================================================
# File: Dockerfile
# Dự án: Hệ thống Smart CRM – Mekong Mobile (Luồng 05: Kho linh kiện thay thế)
# Chi nhánh: Quận 1 (L5-WH-890)
# Mục đích: Đóng gói toàn bộ Backend FastAPI + Frontend SPA Dark 3D + Seed Data
# ==============================================================================

FROM python:3.11-slim

LABEL maintainer="Huynh Nguyen Bao Ngoc <2374802010339>"
LABEL project="Smart CRM - Mekong Mobile (Flow 05: Spare Parts Inventory)"
LABEL version="1.0"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    API_PORT=8000 \
    DB_NAME=mekong_mobile_l5 \
    DEFAULT_CENTER_ID=L5-WH-890

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY seeds/ ./seeds/
COPY data/ ./data/
COPY tests/ ./tests/
COPY pytest.ini .
COPY .env.example .

RUN mkdir -p /app/data /app/seeds

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Tự động nạp dữ liệu mẫu khi khởi động và chạy máy chủ Uvicorn
CMD ["sh", "-c", "python seeds/seed.py || true; uvicorn src.app:app --host 0.0.0.0 --port ${PORT:-8000}"]
