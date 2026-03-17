# VetDict Docker Deployment Guide

## Overview

VetDict can be deployed using Docker with multiple deployment options:

- **Development**: Single container with hot reload
- **Production**: Multi-stage optimized build with nginx reverse proxy
- **Full Stack**: With PostgreSQL and Redis support

## Prerequisites

- Docker >= 20.10
- Docker Compose >= 2.0
- 4GB+ RAM
- 2GB+ disk space

## Quick Start (Development)

```bash
# Clone repository
git clone <repo-url>
cd vetdict

# Build image
docker build -t vetdict:latest .

# Run container
docker run -p 8000:8000 -p 3000:3000 \
    -e ENVIRONMENT=development \
    vetdict:latest

# Open browser
# API: http://localhost:8000
# Web: http://localhost:3000
# Swagger: http://localhost:8000/docs
```

## Docker Compose Setup

### Development Mode (Default)

```bash
# Copy environment file
cp .env.example .env

# Start services
docker-compose up -d

# View logs
docker-compose logs -f vetdict

# Stop services
docker-compose down
```

### With Database and Cache

```bash
# Start with all profiles
docker-compose --profile database --profile cache up -d

# Access services
# API: http://localhost:8000
# Web: http://localhost:3000
# Database: localhost:5432
# Redis: localhost:6379
```

### Production Mode with Nginx

```bash
# Generate SSL certificates (self-signed for testing)
mkdir -p ssl
openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes

# Update environment
echo "ENVIRONMENT=production" >> .env

# Start with nginx
docker-compose --profile nginx up -d

# Access via https
# https://localhost
```

## Production Build

```bash
# Build optimized image
docker build -f Dockerfile.prod -t vetdict:prod .

# Run with resource limits
docker run -d \
    --name vetdict-prod \
    -p 8000:8000 \
    -p 3000:3000 \
    -e ENVIRONMENT=production \
    --memory="2g" \
    --cpus="2" \
    --restart=unless-stopped \
    vetdict:prod

# Health check
docker ps
# or
curl http://localhost:8000/api/health
```

## Environment Variables

Common configurations in `.env`:

```env
ENVIRONMENT=production
API_PORT=8000
WEB_PORT=3000
DEBUG=false
LOG_LEVEL=INFO
```

See `.env.example` for complete options.

## Docker Commands

```bash
# Build image
docker build -t vetdict:latest .

# Run container
docker run -p 8000:8000 -p 3000:3000 vetdict:latest

# View logs
docker logs <container-id>

# Execute command in container
docker exec <container-id> bash

# Stop container
docker stop <container-id>

# Remove container
docker rm <container-id>

# View images
docker images | grep vetdict

# Remove image
docker rmi vetdict:latest
```

## Docker Compose Commands

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f vetdict

# Execute command
docker-compose exec vetdict python3 -c "print('hello')"

# Stop services
docker-compose down

# Remove volumes
docker-compose down -v

# Rebuild images
docker-compose up -d --build
```

## Health Checks

```bash
# API health check
curl http://localhost:8000/api/health

# Web server check
curl http://localhost:3000

# Docker container health
docker ps
# Look for STATUS column (healthy/unhealthy)
```

## Performance Optimization

### Memory Management
```bash
docker run --memory="1g" --memory-swap="2g" vetdict:latest
```

### CPU Allocation
```bash
docker run --cpus="2.0" vetdict:latest
```

### Volume Optimization
```bash
# Use named volumes for persistence
docker volume create vetdict-data
docker run -v vetdict-data:/app/data vetdict:latest
```

## Troubleshooting

### Container won't start
```bash
# Check logs
docker logs <container-id>

# Run interactively
docker run -it vetdict:latest bash
```

### Port already in use
```bash
# Change port mapping
docker run -p 8001:8000 -p 3001:3000 vetdict:latest

# Or kill existing process
docker-compose down
```

### High memory usage
```bash
# Monitor container
docker stats

# Reduce workers
docker run -e WORKERS=2 vetdict:latest
```

## Security Best Practices

1. **Use non-root user**: ✓ (Configured in Dockerfile)
2. **Health checks**: ✓ (Configured)
3. **Resource limits**: Configure via docker-compose
4. **Environment variables**: Use `.env` file, never commit credentials
5. **SSL/TLS**: Use nginx profile for HTTPS
6. **Network isolation**: Default bridge network, can use custom networks

## Deployment Examples

### AWS ECS
```bash
# Push to ECR
aws ecr get-login-password | docker login --username AWS --password-stdin <ecr-url>
docker tag vetdict:latest <ecr-url>/vetdict:latest
docker push <ecr-url>/vetdict:latest

# Update ECS service to use new image
```

### Docker Swarm
```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml vetdict

# View services
docker service ls
```

### Kubernetes
```bash
# Convert Docker Compose to Kubernetes manifests
kompose convert -f docker-compose.yml -o k8s/

# Apply to cluster
kubectl apply -f k8s/
```

## Monitoring and Logging

```bash
# View real-time logs
docker-compose logs -f vetdict

# Save logs to file
docker-compose logs vetdict > logs.txt

# Filter logs
docker-compose logs | grep "ERROR"

# Monitor stats
watch docker stats --no-stream
```

## Cleanup

```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Full cleanup
docker system prune -a
```

## Support

For issues or questions:
1. Check logs: `docker-compose logs vetdict`
2. Test API: `curl http://localhost:8000/api/health`
3. Check file permissions in container
4. Ensure ports are available
5. Verify environment variables are set
