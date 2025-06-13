# Deployment Guide

## Prerequisites
- Docker and Docker Compose installed
- SSL certificates (for HTTPS)

## Production Deployment

1. Clone the repository:
```bash
git clone https://github.com/yourusername/zentix-clean.git
cd zentix-clean
```

2. Create SSL directory and add certificates:
```bash
mkdir ssl
# Add your SSL certificates to the ssl directory
# - ssl/cert.pem
# - ssl/key.pem
```

3. Build and start the containers:
```bash
docker-compose up -d --build
```

The application will be available at:
- Frontend: http://localhost
- Backend API: http://localhost/api
- API Documentation: http://localhost/api/docs

## Performance Optimizations

The project includes several performance optimizations:

### 1. Nginx Configuration
- Gzip and Brotli compression
- Static file caching
- API response caching
- Security headers
- Load balancing

### 2. Frontend Optimizations
- Static file optimization
- Image optimization
- Code splitting
- Caching headers
- Compression

### 3. Backend Optimizations
- Response compression
- Caching middleware
- Performance monitoring
- Database connection pooling

## Monitoring

The application includes built-in monitoring:

### 1. Performance Metrics
- Request processing time
- Response sizes
- Cache hit rates
- Error rates

### 2. Health Checks
- API health endpoint: `/api/health`
- Database connection status
- Service dependencies status

## Scaling

The application is designed to scale horizontally:

### 1. Frontend
- Stateless design
- CDN-ready static assets
- Load balancer compatible

### 2. Backend
- Stateless API design
- Database connection pooling
- Cache-friendly architecture

### 3. Database
- Connection pooling
- Indexed queries
- Optimized schema

## Environment Variables

### Frontend
```env
NEXT_PUBLIC_API_URL=http://localhost/api
NODE_ENV=production
```

### Backend
```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/zentix
ENVIRONMENT=production
```

### Database
```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=zentix
```

## Deploying to Vercel

The `vercel.json` file in the repository configures the Next.js frontend.
It sets `frontend` as the root directory, specifies the build command and
output folder, and rewrites `/api` requests to the backend URL. Environment
variables can be defined in this file or through the Vercel dashboard. The
most important one is `NEXT_PUBLIC_API_URL` which should point to the public
address of the backend API.

### Required Environment Variables
- `VERCEL_TOKEN` - authentication token for the `vercel` CLI
- `VERCEL_ORG_ID` - your Vercel organization ID
- `VERCEL_PROJECT_ID` - the project ID used by Vercel

### Vercel CLI Commands
1. Install the CLI:
   ```bash
   npm install -g vercel
   ```
2. Log in to your account:
   ```bash
   vercel login
   ```
3. Create a preview deployment:
   ```bash
   vercel
   ```
4. Deploy to production from the `frontend` directory:
   ```bash
   vercel --prod
   ```

### Backend Handling
 codex/update-deployment-docs-with-vercel-details
Host the backend separately (Docker, VPS, or any cloud provider) and expose
its public URL. Configure `NEXT_PUBLIC_API_URL` in the Vercel dashboard or in
`vercel.json` so the frontend can reach the API.

The backend is deployed separately (Docker, VPS, or any cloud provider).
Set `NEXT_PUBLIC_API_URL` in the Vercel dashboard to point to the public
backend URL.

### Configuration File
This repository provides a `vercel.json` file that defines the project
settings and the `frontend` root. It also configures the build and output
directories and exposes environment variables required by the Next.js
application:

- `NEXT_PUBLIC_API_URL` – URL of the backend API
- `NEXT_PUBLIC_JWT_STORAGE_KEY` – key used to store the authentication token

Requests to `/api/*` are rewritten to the backend so the frontend can call the
API without hard‑coding the server address.
 main

## Maintenance

### Logs
View logs for all services:
```bash
docker-compose logs -f
```

View logs for specific service:
```bash
docker-compose logs -f [service_name]
```

### Updates
To update the application:
1. Pull latest changes
2. Rebuild containers
```bash
git pull
docker-compose up -d --build
```

### Backup
Database backup:
```bash
docker-compose exec db pg_dump -U postgres zentix > backup.sql
```

Database restore:
```bash
cat backup.sql | docker-compose exec -T db psql -U postgres zentix
```

## Troubleshooting

### Common Issues

1. **Port Conflicts**
   - Check if ports 80 and 443 are available
   - Modify ports in docker-compose.yml if needed

2. **Database Connection**
   - Verify database credentials
   - Check database logs for errors

3. **SSL Issues**
   - Ensure SSL certificates are valid
   - Check certificate permissions

4. **Memory Issues**
   - Monitor container memory usage
   - Adjust container limits if needed

### Debugging

1. **Container Status**
```bash
docker-compose ps
```

2. **Container Logs**
```bash
docker-compose logs [service_name]
```

3. **Container Shell**
```bash
docker-compose exec [service_name] sh
```

## Security

### SSL/TLS
- Use valid SSL certificates
- Enable HTTPS only
- Configure secure headers

### Database
- Use strong passwords
- Regular backups
- Access control

### Application
- Regular updates
- Security headers
- Input validation
 codex/search-and-clean-affected-files
- Rate limiting 
- Rate limiting

 main
## Kubernetes Deployment

A Kubernetes configuration is provided in `k8s/deployment.yml`. Apply it with:

```bash
kubectl apply -f k8s/deployment.yml
```

 codex/search-and-clean-affected-files
This configuration runs a single replica of each component in the `zentix` namespace. Update image tags and resources as needed.


The file defines deployments and services for the frontend and backend in the `zentix` namespace. Update image tags and resources as needed.
 main
