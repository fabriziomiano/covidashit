FROM node:22-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend ./
RUN npm run build

FROM python:3.12-slim AS runtime
LABEL maintainer="fabriziomiano@gmail.com"
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FRONTEND_DIST=/covidashit/frontend/dist
WORKDIR /covidashit
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY backend ./backend
COPY covidashit ./covidashit
COPY settings ./settings
COPY config.py setup.py wsgi.py ./
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist
CMD ["sh", "-c", "uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT:-5050}"]
