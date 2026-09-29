# 🚀 Production Deployment Guide

This guide details best practices for deploying **ComicCraft** into production environments using Docker containers, Linux virtual machines (systemd + Nginx), or cloud PaaS platforms.

---

## 1. Option A: Containerized Deployment via Docker (Recommended)

### Dockerfile
A production-ready `Dockerfile` is included in the project root:
```dockerfile
FROM python:3.12-slim

# Prevent Python from writing .pyc and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies (fonts, build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Ensure storage directories exist with proper permissions
RUN mkdir -p static/panels static/exports static/fonts static/css static/img

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Building & Running with Docker
```bash
# Build Docker image
docker build -t comiccraft:latest .

# Run container with persistent volume for exports
docker run -d \
  --name comiccraft-app \
  -p 8000:8000 \
  -e GEMINI_API_KEY="your_api_key_here" \
  -v comiccraft_exports:/app/static/exports \
  comiccraft:latest
```

### Running with Docker Compose
```bash
docker compose up -d
```

---

## 2. Option B: Linux Server Deployment (Ubuntu / Debian + Systemd)

### 1. Create a Systemd Service File
Create `/etc/systemd/system/comiccraft.service`:
```ini
[Unit]
Description=ComicCraft AI Comic Creator Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/comiccraft
Environment="PATH=/var/www/comiccraft/venv/bin"
EnvironmentFile=/var/www/comiccraft/.env
ExecStart=/var/www/comiccraft/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 4
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable comiccraft
sudo systemctl start comiccraft
```

---

## 3. Nginx Reverse Proxy Configuration
Create `/etc/nginx/sites-available/comiccraft`:
```nginx
server {
    listen 80;
    server_name comiccraft.yourdomain.com;

    client_max_body_size 50M;

    # Static assets direct serving for maximum throughput
    location /static/ {
        alias /var/www/comiccraft/static/;
        expires 7d;
        add_header Cache-Control "public, no-transform";
    }

    # Proxy application requests to Uvicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 60s;
    }
}
```
Enable the site and obtain SSL via Let's Encrypt:
```bash
sudo ln -s /etc/nginx/sites-available/comiccraft /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
sudo certbot --nginx -d comiccraft.yourdomain.com
```

---

## 4. Option C: Cloud Platform Deployment (Render, Railway, Fly.io)
- **Render**: Connect your GitHub repository, choose **Web Service**, set Runtime to **Python 3**, Build Command: `pip install -r requirements.txt`, Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`. Add `GEMINI_API_KEY` in Environment Variables.
- **Railway**: Connect repo; Railway automatically detects the Python project or Dockerfile and provisions an accessible HTTPS domain.
- **Fly.io**: Run `fly launch` and `fly deploy`.
