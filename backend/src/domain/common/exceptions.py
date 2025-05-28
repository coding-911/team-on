# File: backend/src/domain/common/exceptions.py
from typing import Any, Dict, Optional, Union
from uuid import UUID
import json
from datetime import datetime

class DomainException(Exception):
    """도메인 계층의 기본 예외 클래스"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """예외 정보를 직렬화 가능한 딕셔너리로 변환"""
        return {
            "type": self.__class__.__name__,
            "message": self.message
        }

    def _ensure_serializable(self, value: Any) -> Any:
        """값이 JSON 직렬화 가능하도록 변환"""
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

class EntityNotFoundException(DomainException):
    """엔티티를 찾을 수 없을 때 발생하는 예외"""
    def __init__(
        self,
        entity_type: str,
        entity_id: Optional[Union[UUID, str, int]] = None,
        additional_info: Optional[Dict[str, Any]] = None
    ):
        self.entity_type = entity_type
        self.entity_id = str(entity_id) if entity_id is not None else None
        self.additional_info = self._ensure_serializable(additional_info or {})
        
        message = f"{entity_type}을(를) 찾을 수 없습니다."
        if entity_id:
            message = f"{entity_type}(ID: {self.entity_id})을(를) 찾을 수 없습니다."
        
        super().__init__(message)

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "additional_info": self.additional_info
        })
        return data

class ValidationException(DomainException):
    """도메인 유효성 검사 실패 시 발생하는 예외"""
    def __init__(
        self,
        field: str,
        message: str,
        value: Any = None,
        additional_info: Optional[Dict[str, Any]] = None
    ):
        self.field = field
        self.invalid_value = self._ensure_serializable(value)
        self.additional_info = self._ensure_serializable(additional_info or {})
        
        message_with_value = f"유효성 검사 실패: {field} - {message}"
        if value is not None:
            message_with_value = f"유효성 검사 실패: {field}({self.invalid_value}) - {message}"
        
        super().__init__(message_with_value)

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "field": self.field,
            "value": self.invalid_value,
            "additional_info": self.additional_info
        })
        return data

class BusinessRuleException(DomainException):
    """비즈니스 규칙 위반 시 발생하는 예외"""
    def __init__(
        self,
        rule: str,
        detail: str,
        context: Optional[Dict[str, Any]] = None
    ):
        self.rule = rule
        self.detail = detail
        self.context = self._ensure_serializable(context or {})
        
        message = f"비즈니스 규칙 위반 ({rule}): {detail}"
        super().__init__(message)

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "rule": self.rule,
            "detail": self.detail,
            "context": self.context
        })
        return data

    def add_context(self, key: str, value: Any) -> None:
        """예외 컨텍스트에 추가 정보를 더합니다."""
        self.context[key] = self._ensure_serializable(value)