import pytest
from uuid import UUID
from datetime import datetime
from domain.common.exceptions import (
    DomainException,
    EntityNotFoundException,
    ValidationException,
    BusinessRuleException
)

def test_domain_exception_basic():
    """기본 도메인 예외 테스트"""
    message = "테스트 에러 메시지"
    exc = DomainException(message)
    
    assert str(exc) == message
    assert exc.message == message
    
    # to_dict 테스트
    data = exc.to_dict()
    assert data["type"] == "DomainException"
    assert data["message"] == message

def test_entity_not_found_exception():
    """엔티티 찾기 실패 예외 테스트"""
    # UUID 사용 케이스
    entity_id = UUID("12345678-1234-5678-1234-567812345678")
    exc = EntityNotFoundException("User", entity_id)
    assert "User(ID: " in str(exc)
    assert str(entity_id) in str(exc)
    
    # 문자열 ID 사용 케이스
    exc = EntityNotFoundException("Team", "TEAM-001")
    assert "Team(ID: TEAM-001)" in str(exc)
    
    # 추가 정보 포함 케이스
    additional_info = {"last_seen": "2024-03-01"}
    exc = EntityNotFoundException("User", "user123", additional_info)
    data = exc.to_dict()
    assert data["entity_type"] == "User"
    assert data["entity_id"] == "user123"
    assert data["additional_info"] == additional_info

def test_validation_exception():
    """유효성 검사 예외 테스트"""
    # 기본 케이스
    exc = ValidationException("email", "올바른 이메일 형식이 아닙니다")
    assert "email" in str(exc)
    assert "올바른 이메일 형식이 아닙니다" in str(exc)
    
    # 값 포함 케이스
    exc = ValidationException("age", "나이는 0보다 커야 합니다", -5)
    assert "age(-5)" in str(exc)
    
    # 직렬화 불가능한 값 처리
    complex_value = datetime.now()
    exc = ValidationException("date", "잘못된 날짜", complex_value)
    data = exc.to_dict()
    assert isinstance(data["value"], str)
    
    # 추가 정보 포함
    additional_info = {"allowed_range": "1-100"}
    exc = ValidationException("count", "범위 초과", 150, additional_info)
    data = exc.to_dict()
    assert data["field"] == "count"
    assert data["value"] == 150
    assert data["additional_info"] == additional_info

def test_business_rule_exception():
    """비즈니스 규칙 예외 테스트"""
    # 기본 케이스
    exc = BusinessRuleException(
        "MaxTasksPerUser",
        "사용자당 최대 태스크 수 초과"
    )
    assert "MaxTasksPerUser" in str(exc)
    
    # 컨텍스트 포함 케이스
    context = {"current": 11, "max": 10}
    exc = BusinessRuleException(
        "MaxTasksPerUser",
        "사용자당 최대 태스크 수 초과",
        context
    )
    data = exc.to_dict()
    assert data["rule"] == "MaxTasksPerUser"
    assert data["context"] == context
    
    # 컨텍스트 추가 테스트
    exc.add_context("user_id", "user123")
    data = exc.to_dict()
    assert data["context"]["user_id"] == "user123"
    
    # 직렬화 불가능한 컨텍스트 값 처리
    exc.add_context("created_at", datetime.now())
    data = exc.to_dict()
    assert isinstance(data["context"]["created_at"], str)

def test_exception_inheritance():
    """예외 상속 관계 테스트"""
    assert issubclass(EntityNotFoundException, DomainException)
    assert issubclass(ValidationException, DomainException)
    assert issubclass(BusinessRuleException, DomainException)
    
    exc = EntityNotFoundException("User", "123")
    assert isinstance(exc, DomainException)
    assert isinstance(exc, Exception) 