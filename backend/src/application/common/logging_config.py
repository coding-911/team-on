import os
import logging.config
from typing import Dict, Any

def configure_logging(env: str = "development") -> None:
    """환경별 로깅 설정"""
    config = get_logging_config(env)
    logging.config.dictConfig(config)

def get_logging_config(env: str) -> Dict[str, Any]:
    """환경별 로깅 설정 반환"""
    log_level = "DEBUG" if env == "development" else "INFO"
    
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            },
            "detailed": {
                "format": (
                    "%(asctime)s [%(levelname)s] %(name)s: %(message)s "
                    "error_id=%(error_id)s error_code=%(error_code)s "
                    "%(extra_fields)s"
                )
            }
        },
        "filters": {
            "error_context": {
                "()": "application.common.logging_filters.ErrorContextFilter"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": log_level,
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": os.path.join("logs", "errors.log"),
                "formatter": "detailed",
                "filters": ["error_context"],
                "level": "ERROR",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 10
            }
        },
        "loggers": {
            "": {  # 루트 로거
                "handlers": ["console"],
                "level": log_level,
            },
            "application": {
                "handlers": ["console", "error_file"],
                "level": log_level,
                "propagate": False
            }
        }
    }
    
    # 운영 환경 특화 설정
    if env == "production":
        # Sentry 핸들러 추가
        config["handlers"]["sentry"] = {
            "class": "raven.handlers.logging.SentryHandler",
            "level": "ERROR",
            "dsn": os.getenv("SENTRY_DSN", "")
        }
        config["loggers"]["application"]["handlers"].append("sentry")
        
        # JSON 포맷 로그 핸들러 추가
        config["formatters"]["json"] = {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "fmt": "%(asctime)s %(name)s %(levelname)s %(message)s"
        }
        config["handlers"]["json_file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join("logs", "application.json"),
            "formatter": "json",
            "level": "INFO",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 10
        }
        config["loggers"]["application"]["handlers"].append("json_file")
    
    return config 