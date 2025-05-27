from typing import List
from pydantic import BaseSettings, AnyHttpUrl, validator
from enum import Enum

class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"

class Settings(BaseSettings):
    # API 설정
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False
    ENVIRONMENT: EnvironmentType = EnvironmentType.DEVELOPMENT
    
    # 보안 설정
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    PASSWORD_HASH_ALGORITHM: str = "bcrypt"
    PASSWORD_SALT_ROUNDS: int = 12
    
    # 데이터베이스 설정
    DATABASE_URL: str
    DATABASE_MAX_CONNECTIONS: int = 20
    DATABASE_POOL_SIZE: int = 5
    
    # Redis 설정
    REDIS_URL: str
    REDIS_MAX_CONNECTIONS: int = 10
    
    # CORS 설정
    CORS_ORIGINS: List[str]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    # 모니터링 설정
    SENTRY_DSN: str = ""
    ENABLE_METRICS: bool = True
    PROMETHEUS_METRICS_PATH: str = "/metrics"
    
    # Elasticsearch 설정
    ELASTICSEARCH_URL: str
    ELASTICSEARCH_USERNAME: str = ""
    ELASTICSEARCH_PASSWORD: str = ""
    ELASTICSEARCH_VERIFY_CERTS: bool = True
    
    # 파일 업로드 설정
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_UPLOAD_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "pdf"]
    UPLOAD_DIRECTORY: str = "/app/uploads"
    
    # 기능 플래그
    ENABLE_NOTIFICATIONS: bool = True
    ENABLE_AUDIO_PROCESSING: bool = True
    
    # 레이트 리미팅
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 60

    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    @validator("JWT_SECRET_KEY", pre=True)
    def validate_jwt_secret(cls, v: str) -> str:
        if len(v) < 32:
            raise ValueError("JWT_SECRET_KEY must be at least 32 characters long")
        return v

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

# 설정 인스턴스 생성
settings = Settings()

# 환경별 설정 로드
def get_settings():
    return settings 