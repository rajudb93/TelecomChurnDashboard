# Docker Setup Guide - Telecom Churn Dashboard

## Overview
This guide provides instructions for building and running the Telecom Churn Intelligence Platform in Docker containers.

---

## Prerequisites

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/) (v20.10+)
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/) (v2.0+)
- Environment variables file (`.env`) with your configuration

---

## Quick Start

### 1. **Clone & Setup Environment**

```bash
# Copy the environment template
cp .env.example .env

# Edit .env with your Snowflake and email credentials
# Use your favorite editor (VSCode, nano, vim, etc.)
```

### 2. **Build the Docker Image**

#### Option A: Using Docker Compose (Recommended)
```bash
docker-compose build
```

#### Option B: Using Docker CLI directly
```bash
docker build -t telecom-churn-dashboard:latest .
```

#### With custom tag and version
```bash
docker build -t telecom-churn-dashboard:v1.0 .
```

### 3. **Run the Container**

#### Option A: Using Docker Compose (Recommended)
```bash
docker-compose up -d
```

The application will be available at: **http://localhost:8501**

#### Option B: Using Docker CLI directly
```bash
docker run -d \
  -p 8501:8501 \
  --name telecom-dashboard \
  --env-file .env \
  -v $(pwd)/data:/app/data:ro \
  -v $(pwd)/models:/app/models:ro \
  telecom-churn-dashboard:latest
```

---

## Common Commands

### View Logs
```bash
# Using Docker Compose
docker-compose logs -f

# Using Docker CLI
docker logs -f telecom-dashboard
```

### Stop the Container
```bash
# Using Docker Compose
docker-compose down

# Using Docker CLI
docker stop telecom-dashboard
docker rm telecom-dashboard
```

### Access Container Shell
```bash
# Using Docker Compose
docker-compose exec telecom-churn-dashboard /bin/bash

# Using Docker CLI
docker exec -it telecom-dashboard /bin/bash
```

### Check Container Health
```bash
docker ps
# Look for the STATUS column - should show "healthy"

# Detailed health check
docker inspect --format='{{.State.Health.Status}}' telecom-dashboard
```

---

## Environment Configuration

### Snowflake Configuration
Update your `.env` file with:
```
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=xy12345.us-east-1
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=ANALYTICS_DB
SNOWFLAKE_SCHEMA=PUBLIC
```

### Email Configuration (Gmail)
For Gmail SMTP, follow these steps:
1. Enable 2-Factor Authentication on your Gmail account
2. Generate an [App Password](https://support.google.com/accounts/answer/185833)
3. Update `.env`:
```
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
RECIPIENT_EMAIL=target@example.com
```

---

## Dockerfile Architecture

### Multi-Stage Build
The Dockerfile uses a two-stage build for optimization:

1. **Builder Stage**: Compiles wheels for faster installation
2. **Runtime Stage**: Minimal image with only runtime dependencies

### Key Features
- ✅ **Multi-stage build**: Reduces final image size
- ✅ **Non-root user**: Runs as `streamlit_user` (UID: 1000)
- ✅ **Health checks**: Monitors container health
- ✅ **Optimized dependencies**: Only includes necessary system libraries
- ✅ **Volume support**: Persistent data storage
- ✅ **Security best practices**: Minimal attack surface

### Base Image
- **Python 3.11-slim**: Lightweight and secure

### System Dependencies
- `libgeos-c1`: Geographic libraries for geopandas
- `libproj25`: Projection libraries for geographic data

---

## Advanced Usage

### Building for Specific Platform
```bash
# Build for ARM64 (Apple Silicon, ARM servers)
docker build --platform linux/arm64 -t telecom-churn-dashboard:latest .

# Build for AMD64 (standard Intel/AMD)
docker build --platform linux/amd64 -t telecom-churn-dashboard:latest .
```

### Build with Build Arguments
```bash
docker build \
  --build-arg PYTHON_VERSION=3.11 \
  -t telecom-churn-dashboard:custom .
```

### Push to Docker Registry

#### Docker Hub
```bash
# Login to Docker Hub
docker login

# Tag the image
docker tag telecom-churn-dashboard:latest yourusername/telecom-churn-dashboard:latest

# Push the image
docker push yourusername/telecom-churn-dashboard:latest
```

#### Azure Container Registry (ACR)
```bash
# Login to ACR
az acr login --name myregistry

# Tag the image
docker tag telecom-churn-dashboard:latest myregistry.azurecr.io/telecom-churn-dashboard:latest

# Push the image
docker push myregistry.azurecr.io/telecom-churn-dashboard:latest
```

---

## Performance Optimization

### Image Size
```bash
# Check image size
docker images telecom-churn-dashboard

# Expected: ~800MB - 1GB (with all dependencies)
```

### Volume Mounts
- **Read-only data**: Mount `data/` directory as read-only
- **Persistent models**: Mount `models/` directory for trained models
- **Temporary files**: `temp/` directory is created inside container

---

## Troubleshooting

### Port Already in Use
```bash
# If port 8501 is already in use, map to a different port:
docker run -d -p 8502:8501 telecom-churn-dashboard:latest
# Access at http://localhost:8502
```

### Snowflake Connection Issues
```bash
# Check environment variables
docker exec telecom-dashboard env | grep SNOWFLAKE

# Test Snowflake connection inside container
docker exec telecom-dashboard python -c "import snowflake.connector; print('Snowflake OK')"
```

### Out of Memory
```bash
# Allocate more memory to Docker and run with memory limit
docker run -d -p 8501:8501 -m 2g telecom-churn-dashboard:latest
```

### Permission Denied Errors
The container runs as non-root user `streamlit_user`. Ensure:
- `.env` file has proper read permissions
- `data/` directory is readable
- `models/` directory is readable

---

## Security Best Practices

1. **Environment Variables**: Never commit `.env` to git
2. **Non-root User**: Container runs as `streamlit_user`
3. **Read-only Data**: Mount data directories as read-only
4. **Secret Management**: Use Docker Secrets or external vault for production
5. **Image Scanning**: Scan for vulnerabilities:
   ```bash
   docker scan telecom-churn-dashboard:latest
   ```

---

## Docker Compose Networking

Multiple services can communicate:
```yaml
# Add database or API service to docker-compose.yml
services:
  api:
    image: my-api:latest
  dashboard:
    depends_on:
      - api
```

Services communicate via service name: `http://api:5000`

---

## Production Deployment

### Health Check Verification
```bash
# Container should show "healthy" status
docker ps -a
# STATUS column should display: "Up X minutes (healthy)"
```

### Resource Limits
```bash
docker run -d \
  -p 8501:8501 \
  --memory=2g \
  --cpus=2 \
  --restart=unless-stopped \
  telecom-churn-dashboard:latest
```

### Logging
```bash
# View structured logs
docker logs --timestamps telecom-dashboard

# Save logs to file
docker logs telecom-dashboard > logs.txt 2>&1
```

---

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Streamlit Deployment Guide](https://docs.streamlit.io/deploy/tutorials/docker)
- [Best Practices for Writing Dockerfiles](https://docs.docker.com/develop/dev-best-practices/)
- [Docker Security](https://docs.docker.com/engine/security/)

---

## Support

For issues with Docker setup:
1. Check logs: `docker-compose logs`
2. Verify `.env` configuration
3. Ensure Snowflake credentials are correct
4. Verify network connectivity

---

**Last Updated**: May 2026
**Version**: 1.0
