from typing import Dict, Any, Optional
from datetime import datetime
from uuid import UUID, uuid4
from fastapi import status
import logging
import json

from application.common.constants import ResponseCode

logger = logging.getLogger(__name__)

class StructuredLogger:
    """구조화된 로깅을 위한 래퍼 클래스"""
    
    @staticmethod
    def error(logger: logging.Logger, message: str, **kwargs):
        """구조화된 에러 로그를 기록합니다."""
        # 기본 로그 메시지에 추가 정보를 JSON 형식으로 포함
        structured_message = {
            "message": message,
            **kwargs
        }
        logger.error(json.dumps(structured_message))

class ApplicationException(Exception):
    """애플리케이션 계층의 기본 예외 클래스
    
    모든 비즈니스 예외의 기본이 되는 클래스입니다.
    error_id를 통한 추적성과 구조화된 로깅을 제공합니다.
    """
    
    def __init__(
        self,
        code: ResponseCode,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        additional_info: Optional[Dict[str, Any]] = None,
        error_id: Optional[str] = None
    ):
        self.code = code
        self.message = message
        self.detail = message
        self.status_code = status_code
        self.additional_info = self._ensure_serializable(additional_info) if additional_info is not None else {}
        self.error_id = error_id or str(uuid4())
        
        self._log_error()
        super().__init__(message)
    
    def _log_error(self):
        """예외 발생 시 로그를 기록합니다.
        
        Python logging 시스템의 extra 매개변수를 사용하여
        LogRecord에 추가 필드를 포함시킵니다.
        """
        logger.error(
            f"[{self.error_id}] {self.message}",
            extra={
                "error_code": str(self.code),
                "error_id": self.error_id,
                "error_message": self.message,
                "additional_info": str(self.additional_info)
            }
        )
    
    def to_response_dict(self) -> Dict[str, Any]:
        """HTTP 응답으로 변환할 수 있는 딕셔너리를 반환합니다."""
        return {
            "code": self.code,
            "message": self.message,
            "data": self.additional_info if self.additional_info else None,
            "error_id": self.error_id
        }
    
    def _ensure_serializable(self, value: Any) -> Any:
        """값이 JSON 직렬화 가능하도록 변환합니다."""
        if isinstance(value, (str, int, float, bool, type(None))):
            return value
        elif isinstance(value, (datetime, UUID)):
            return str(value)
        elif isinstance(value, dict):
            return {k: self._ensure_serializable(v) for k, v in value.items()}
        elif isinstance(value, (list, tuple)):
            return [self._ensure_serializable(item) for item in value]
        else:
            return str(value)

class ResourceNotFoundException(ApplicationException):
    """리소스를 찾을 수 없을 때 발생하는 예외"""
    
    def __init__(
        self,
        message: str,
        resource_type: str = None,
        resource_id: Optional[str] = None,
        additional_info: Optional[Dict[str, Any]] = None
    ):
        if resource_type is None:
            resource_type = "Resource"
        
        super().__init__(
            code=ResponseCode.NOT_FOUND,
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            additional_info={
                "entity_type": resource_type,
                "resource_id": resource_id,
                **(additional_info or {})
            }
        )

class ValidationFailedException(ApplicationException):
    """입력값 유효성 검사 실패 시 발생하는 예외"""
    
    def __init__(
        self,
        message: str,
        field: str,
        value: Any = None,
        additional_info: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            code=ResponseCode.VALIDATION_ERROR,
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            additional_info={
                "field": field,
                "value": self._ensure_serializable(value),
                "additional_info": additional_info or {}
            }
        )

class BusinessRuleViolationException(ApplicationException):
    """비즈니스 규칙 위반 시 발생하는 예외"""
    
    def __init__(
        self,
        message: str,
        rule: str,
        context: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            code=ResponseCode.BUSINESS_RULE_VIOLATION,
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            additional_info={
                "rule": rule,
                "context": self._ensure_serializable(context or {})
            }
        )

class AuthenticationException(ApplicationException):
    """인증 실패 시 발생하는 예외의 기본 클래스"""
    
    def __init__(
        self,
        code: ResponseCode,
        message: str,
        additional_info: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            code=code,
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            additional_info=additional_info
        )

class InvalidCredentialsException(AuthenticationException):
    """잘못된 인증 정보로 인한 인증 실패"""
    
    def __init__(
        self,
        additional_info: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            code=ResponseCode.AUTH_INVALID_CREDENTIALS,
            message=ResponseCode.AUTH_INVALID_CREDENTIALS.message,
            additional_info=additional_info
        )

class TokenExpiredException(AuthenticationException):
    """토큰 만료로 인한 인증 실패"""
    
    def __init__(
        self,
        token_type: str = "access",
        additional_info: Optional[Dict[str, Any]] = None
    ):
        code = (ResponseCode.AUTH_REFRESH_TOKEN_EXPIRED 
                if token_type == "refresh" 
                else ResponseCode.AUTH_TOKEN_EXPIRED)
        super().__init__(
            code=code,
            message=code.message,
            additional_info={
                "token_type": token_type,
                **(additional_info or {})
            }
        )

class InvalidTokenException(AuthenticationException):
    """유효하지 않은 토큰으로 인한 인증 실패"""
    
    def __init__(
        self,
        reason: str,
        additional_info: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            code=ResponseCode.AUTH_INVALID_TOKEN,
            message=ResponseCode.AUTH_INVALID_TOKEN.message,
            additional_info={
                "reason": reason,
                **(additional_info or {})
            }
        )

class AuthorizationException(ApplicationException):
    """권한 부족으로 인한 접근 거부 시 발생하는 예외"""
    
    def __init__(
        self,
        message: str,
        required_permissions: Optional[list] = None,
        additional_info: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            code=ResponseCode.AUTH_INVALID_TOKEN,
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            additional_info={
                "required_permissions": required_permissions,
                **(additional_info or {})
            }
        ) 