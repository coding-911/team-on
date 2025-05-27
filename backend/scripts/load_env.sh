#!/bin/bash

# 환경 변수 파일 선택
if [ "$ENVIRONMENT" = "production" ]; then
    ENV_FILE=".env.prod"
elif [ "$ENVIRONMENT" = "testing" ]; then
    ENV_FILE=".env.test"
else
    ENV_FILE=".env.dev"
fi

# 환경 변수 파일 존재 확인
if [ ! -f "$ENV_FILE" ]; then
    echo "Error: $ENV_FILE not found!"
    echo "Please create $ENV_FILE file based on .env.example"
    exit 1
fi

# 필수 환경 변수 검증
required_vars=(
    "DATABASE_URL"
    "REDIS_URL"
    "JWT_SECRET_KEY"
    "ELASTICSEARCH_URL"
)

# 환경 변수 파일 로드
set -a
source "$ENV_FILE"
set +a

# 필수 환경 변수 존재 확인
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "Error: Required environment variable $var is not set in $ENV_FILE"
        exit 1
    fi
done

# JWT 시크릿 키 길이 검증
if [ ${#JWT_SECRET_KEY} -lt 32 ]; then
    echo "Error: JWT_SECRET_KEY must be at least 32 characters long"
    exit 1
fi

echo "Successfully loaded environment variables from $ENV_FILE" 