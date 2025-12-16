#!/bin/bash
set -e

PROJECT=weather-app
AWS_REGION=us-east-1
ACCOUNT_ID=123456789012

ECR_BASE="$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"

echo "Logging into ECR..."
aws ecr get-login-password --region $AWS_REGION \
| docker login --username AWS --password-stdin $ECR_BASE

echo "Building ingestion image..."
docker build -t $PROJECT-ingestion ./ingestion
docker tag $PROJECT-ingestion:latest $ECR_BASE/$PROJECT-ingestion:latest
docker push $ECR_BASE/$PROJECT-ingestion:latest

echo "Building aggregation image..."
docker build -t $PROJECT-aggregation ./aggregation
docker tag $PROJECT-aggregation:latest $ECR_BASE/$PROJECT-aggregation:latest
docker push $ECR_BASE/$PROJECT-aggregation:latest

echo "Building API image..."
docker build -t $PROJECT-api ./api
docker tag $PROJECT-api:latest $ECR_BASE/$PROJECT-api:latest
docker push $ECR_BASE/$PROJECT-api:latest

echo "All images pushed to ECR"

echo "Deployment completed successfully"