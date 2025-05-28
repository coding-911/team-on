import pytest
from fastapi import status
from domain.common.exceptions import (
    DomainException,
    EntityNotFoundException,
    ValidationException,
    BusinessRuleException
)
from application.common.constants import ResponseCode
from application.common.exceptions import (
    ApplicationException,
    ResourceNotFoundException,
    ValidationFailedException,
    BusinessRuleViolationException
)
from application.common.exception_translators import ExceptionTranslator

def test_entity_not_found_translation():
    """엔티티 찾기 실패 예외 변환 테스트"""
    domain_exc = EntityNotFoundException(
        "User",
        "user123",
        {"last_login": "2024-03-01"}
    )
    
    app_exc = ExceptionTranslator.translate(domain_exc)
    
    assert isinstance(app_exc, ResourceNotFoundException)
    assert app_exc.code == ResponseCode.NOT_FOUND
    assert "User" in app_exc.detail
    assert "user123" in app_exc.detail
    
    response = app_exc.to_response_dict()
    assert response["data"]["entity_type"] == "User"
    assert response["data"]["resource_id"] == "user123"
    assert response["data"]["last_login"] == "2024-03-01"

def test_validation_exception_translation():
    """유효성 검사 예외 변환 테스트"""
    domain_exc = ValidationException(
        "email",
        ResponseCode.VALIDATION_ERROR.message,
        "invalid-email",
        {"allowed_pattern": "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}$"}
    )
    
    app_exc = ExceptionTranslator.translate(domain_exc)
    
    assert isinstance(app_exc, ValidationFailedException)
    assert app_exc.code == ResponseCode.VALIDATION_ERROR
    assert "email" in app_exc.detail
    
    response = app_exc.to_response_dict()
    assert response["data"]["field"] == "email"
    assert response["data"]["value"] == "invalid-email"
    assert response["data"]["additional_info"]["allowed_pattern"] == "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}$"

def test_business_rule_exception_translation():
    """비즈니스 규칙 예외 변환 테스트"""
    domain_exc = BusinessRuleException(
        "MaxTeamMembers",
        ResponseCode.BUSINESS_RULE_VIOLATION.message,
        {"current": 11, "max": 10}
    )
    
    app_exc = ExceptionTranslator.translate(domain_exc)
    
    assert isinstance(app_exc, BusinessRuleViolationException)
    assert app_exc.code == ResponseCode.BUSINESS_RULE_VIOLATION
    assert "MaxTeamMembers" in app_exc.detail
    
    response = app_exc.to_response_dict()
    assert response["data"]["rule"] == "MaxTeamMembers"
    assert response["data"]["context"]["current"] == 11
    assert response["data"]["context"]["max"] == 10

def test_unknown_domain_exception_translation():
    """알 수 없는 도메인 예외 변환 테스트"""
    class UnknownDomainException(DomainException):
        def to_dict(self):
            data = super().to_dict()
            data.update({
                "custom_field": "custom_value"
            })
            return data

    domain_exc = UnknownDomainException("알 수 없는 에러")
    app_exc = ExceptionTranslator.translate(domain_exc)
    
    assert isinstance(app_exc, ApplicationException)
    assert app_exc.code == ResponseCode.INTERNAL_SERVER_ERROR
    assert "알 수 없는 에러" in app_exc.detail

    response = app_exc.to_response_dict()
    assert response["data"]["custom_field"] == "custom_value"

def test_non_domain_exception_translation():
    """도메인 예외가 아닌 예외 변환 테스트"""
    exc = ValueError("잘못된 값")
    app_exc = ExceptionTranslator.translate(exc)

    assert isinstance(app_exc, ApplicationException)
    assert app_exc.code == ResponseCode.INTERNAL_SERVER_ERROR
    assert str(exc) in app_exc.detail

def test_complex_value_serialization():
    """복잡한 값의 직렬화 처리 테스트"""
    from datetime import datetime
    from uuid import UUID

    now = datetime.now()
    uuid = UUID("12345678-1234-5678-1234-567812345678")
    
    domain_exc = ValidationException(
        "data",
        "복잡한 값 테스트",
        {"datetime": now, "uuid": uuid}
    )

    app_exc = ExceptionTranslator.translate(domain_exc)
    response = app_exc.to_response_dict()

    assert isinstance(response["data"]["value"]["datetime"], str)
    assert isinstance(response["data"]["value"]["uuid"], str)
    assert str(now) in response["data"]["value"]["datetime"]
    assert str(uuid) in response["data"]["value"]["uuid"] 