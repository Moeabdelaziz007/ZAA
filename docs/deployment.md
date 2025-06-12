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
- Rate limiting 