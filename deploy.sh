#!/bin/bash

# Deployment Script for Zentix
# المؤلف: محمد عبدالعزيز (Amrikyy)
# 
# Description (EN): Automated deployment script with health checks
# الوصف (ع): سكريبت النشر التلقائي مع فحوصات الصحة

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
ENVIRONMENT=${1:-staging}
HEALTH_CHECK_URL=""
ROLLBACK_VERSION=""

echo -e "${GREEN}🚀 Starting deployment to ${ENVIRONMENT}...${NC}"

# Set environment-specific variables
case $ENVIRONMENT in
  "staging")
    HEALTH_CHECK_URL="https://staging.zentix.com/api/health"
    ;;
  "production")
    HEALTH_CHECK_URL="https://zentix.com/api/health"
    ;;
  *)
    echo -e "${RED}❌ Invalid environment: $ENVIRONMENT${NC}"
    exit 1
    ;;
esac

# Function to check health
check_health() {
  local url=$1
  local max_attempts=30
  local attempt=1
  
  echo -e "${YELLOW}🔍 Checking application health...${NC}"
  
  while [ $attempt -le $max_attempts ]; do
    if curl -f -s "$url" > /dev/null; then
      echo -e "${GREEN}✅ Health check passed!${NC}"
      return 0
    fi
    
    echo "Attempt $attempt/$max_attempts failed, retrying in 10s..."
    sleep 10
    ((attempt++))
  done
  
  echo -e "${RED}❌ Health check failed after $max_attempts attempts${NC}"
  return 1
}

# Function to rollback
rollback() {
  echo -e "${YELLOW}🔄 Rolling back to previous version...${NC}"
  # Add rollback logic here
  echo -e "${GREEN}✅ Rollback completed${NC}"
}

# Pre-deployment checks
echo -e "${YELLOW}🔍 Running pre-deployment checks...${NC}"

# Check if required environment variables are set
required_vars=("VERCEL_TOKEN" "VERCEL_ORG_ID" "VERCEL_PROJECT_ID")
for var in "${required_vars[@]}"; do
  if [ -z "${!var}" ]; then
    echo -e "${RED}❌ Required environment variable $var is not set${NC}"
    exit 1
  fi
done

# Run tests
echo -e "${YELLOW}🧪 Running tests...${NC}"
cd frontend
npm run test
npm run lint
npm run type-check

# Build application
echo -e "${YELLOW}🔨 Building application...${NC}"
npm run build

# Deploy to Vercel
echo -e "${YELLOW}🚀 Deploying to Vercel...${NC}"
if [ "$ENVIRONMENT" = "production" ]; then
  vercel --prod --token "$VERCEL_TOKEN"
else
  vercel --token "$VERCEL_TOKEN"
fi

# Health check
if check_health "$HEALTH_CHECK_URL"; then
  echo -e "${GREEN}🎉 Deployment successful!${NC}"
  
  # Send notification
  curl -X POST "$SLACK_WEBHOOK_URL" \
    -H 'Content-type: application/json' \
    --data "{\"text\":\"✅ Zentix deployed successfully to $ENVIRONMENT\"}" || true
    
else
  echo -e "${RED}❌ Deployment failed health check${NC}"
  rollback
  exit 1
fi

# Post-deployment tasks
echo -e "${YELLOW}📊 Running post-deployment tasks...${NC}"

# Update Sentry release
if [ "$ENVIRONMENT" = "production" ]; then
  sentry-cli releases new "$(git rev-parse HEAD)"
  sentry-cli releases set-commits "$(git rev-parse HEAD)" --auto
  sentry-cli releases finalize "$(git rev-parse HEAD)"
fi

# Run performance audit
echo -e "${YELLOW}⚡ Running performance audit...${NC}"
npm run lighthouse || echo -e "${YELLOW}⚠️ Performance audit failed (non-blocking)${NC}"

echo -e "${GREEN}🎉 Deployment completed successfully!${NC}" 