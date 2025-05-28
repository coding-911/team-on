import pytest
from fastapi import status
from application.common.exceptions import (
    ApplicationException,
    ResourceNotFoundException,
    ValidationFailedException,
    BusinessRuleViolationException,
    AuthenticationException,
    AuthorizationException,
    InvalidCredentialsException,
    TokenExpiredException,
    InvalidTokenException
)
from application.common.constants import ResponseCode
import logging
from datetime import datetime
from uuid import UUID

def test_application_exception_basic():
    """기본 애플리케이션 예외 테스트"""
    code = ResponseCode.NOT_FOUND
    message = ResponseCode.NOT_FOUND.message
    exc = ApplicationException(code=code, message=message)
    
    assert exc.code == code
    assert exc.detail == message
    assert exc.status_code == status.HTTP_400_BAD_REQUEST
    
    # 응답 형식 테스트
    response = exc.to_response_dict()
    assert response["code"] == code
    assert response["message"] == message
    assert response["data"] is None

def test_application_exception_with_additional_info():
    """추가 정보를 포함한 애플리케이션 예외 테스트"""
    additional_info = {"key": "value"}
    exc = ApplicationException(
        code=ResponseCode.NOT_FOUND,
        message=ResponseCode.NOT_FOUND.message,
        additional_info=additional_info
    )
    
    response = exc.to_response_dict()
    assert response["data"] == additional_info

def test_resource_not_found_exception():
    """리소스 찾기 실패 예외 테스트"""
    message = ResponseCode.NOT_FOUND.message
    exc = ResourceNotFoundException(message)
    
    assert exc.code == ResponseCode.NOT_FOUND
    assert exc.detail == message
    assert exc.status_code == status.HTTP_404_NOT_FOUND
    
    # 도메인별 NOT_FOUND 테스트
    exc = ResourceNotFoundException(
        message=ResponseCode.USER_NOT_FOUND.message,
        resource_type="User",
        resource_id="user123",
        additional_info={"last_seen": "2024-03-01"}
    )
    response = exc.to_response_dict()
    assert exc.code == ResponseCode.NOT_FOUND
    assert response["data"]["entity_type"] == "User"
    assert response["data"]["resource_id"] == "user123"
    assert response["data"]["last_seen"] == "2024-03-01"

def test_validation_failed_exception():
    """입력값 유효성 검사 실패 예외 테스트"""
    field = "email"
    value = "invalid-email"
    message = ResponseCode.VALIDATION_ERROR.message
    additional_info = {"allowed_pattern": "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}$"}
    
    exc = ValidationFailedException(
        message=message,
        field=field,
        value=value,
        additional_info=additional_info
    )
    
    assert exc.code == ResponseCode.VALIDATION_ERROR
    assert exc.detail == message
    assert exc.status_code == status.HTTP_400_BAD_REQUEST
    
    response = exc.to_response_dict()
    assert response["data"]["field"] == field
    assert response["data"]["value"] == value
    assert response["data"]["additional_info"] == additional_info

def test_business_rule_violation_exception():
    """비즈니스 규칙 위반 예외 테스트"""
    rule = "MaxTeamMembers"
    message = ResponseCode.BUSINESS_RULE_VIOLATION.message
    context = {"current": 11, "max": 10}
    
    exc = BusinessRuleViolationException(
        message=message,
        rule=rule,
        context=context
    )
    
    assert exc.code == ResponseCode.BUSINESS_RULE_VIOLATION
    assert exc.detail == message
    assert exc.status_code == status.HTTP_400_BAD_REQUEST
    
    response = exc.to_response_dict()
    assert response["data"]["rule"] == rule
    assert response["data"]["context"] == context

def test_authentication_exceptions():
    """세분화된 인증 예외 테스트"""
    # 잘못된 인증 정보
    exc = InvalidCredentialsException(
        additional_info={"login_attempts": 3}
    )
    
    assert exc.code == ResponseCode.AUTH_INVALID_CREDENTIALS
    assert exc.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.additional_info["login_attempts"] == 3
    
    # 액세스 토큰 만료
    exc = TokenExpiredException(
        token_type="access",
        additional_info={"expired_at": "2024-03-01T12:00:00Z"}
    )
    
    assert exc.code == ResponseCode.AUTH_TOKEN_EXPIRED
    assert exc.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.additional_info["token_type"] == "access"
    
    # 리프레시 토큰 만료
    exc = TokenExpiredException(
        token_type="refresh",
        additional_info={"expired_at": "2024-03-01T12:00:00Z"}
    )
    
    assert exc.code == ResponseCode.AUTH_REFRESH_TOKEN_EXPIRED
    assert exc.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.additional_info["token_type"] == "refresh"
    
    # 유효하지 않은 토큰
    exc = InvalidTokenException(
        reason="signature_invalid",
        additional_info={"token_id": "token123"}
    )
    
    assert exc.code == ResponseCode.AUTH_INVALID_TOKEN
    assert exc.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.additional_info["reason"] == "signature_invalid"
    assert exc.additional_info["token_id"] == "token123"

def test_authorization_exception():
    """권한 부족 예외 테스트"""
    message = ResponseCode.AUTH_INVALID_TOKEN.message
    required_permissions = ["admin", "manager"]
    additional_info = {"current_role": "user"}
    
    exc = AuthorizationException(
        message=message,
        required_permissions=required_permissions,
        additional_info=additional_info
    )
    
    assert exc.code == ResponseCode.AUTH_INVALID_TOKEN
    assert exc.detail == message
    assert exc.status_code == status.HTTP_403_FORBIDDEN
    
    response = exc.to_response_dict()
    assert response["data"]["required_permissions"] == required_permissions
    assert response["data"]["current_role"] == "user"

def test_circular_reference_serialization():
    """순환 참조가 있는 객체의 직렬화 테스트"""
    class Node:
        def __init__(self, name: str):
            self.name = name
            self.next = None
            self.prev = None
        
        def __str__(self):
            return f"Node({self.name})"
    
    # 순환 참조 생성
    node1 = Node("A")
    node2 = Node("B")
    node1.next = node2
    node2.prev = node1
    
    exc = ApplicationException(
        code=ResponseCode.INTERNAL_SERVER_ERROR,
        message="순환 참조 테스트",
        additional_info={"node": node1}
    )
    
    response = exc.to_response_dict()
    assert isinstance(response["data"]["node"], str)
    assert "Node(A)" in response["data"]["node"]

def test_deep_nested_structure_serialization():
    """깊은 중첩 구조의 직렬화 테스트"""
    deep_structure = {
        "level1": {
            "level2": {
                "level3": {
                    "level4": {
                        "level5": {
                            "datetime": datetime.now(),
                            "uuid": UUID("12345678-1234-5678-1234-567812345678"),
                            "custom_obj": type("CustomObject", (), {"__str__": lambda x: "Custom"})()
                        }
                    }
                }
            }
        }
    }
    
    exc = ApplicationException(
        code=ResponseCode.INTERNAL_SERVER_ERROR,
        message="깊은 중첩 구조 테스트",
        additional_info={"data": deep_structure}
    )
    
    response = exc.to_response_dict()
    nested_data = response["data"]["data"]
    assert isinstance(nested_data["level1"]["level2"]["level3"]["level4"]["level5"]["datetime"], str)
    assert isinstance(nested_data["level1"]["level2"]["level3"]["level4"]["level5"]["uuid"], str)
    assert nested_data["level1"]["level2"]["level3"]["level4"]["level5"]["custom_obj"] == "Custom"

def test_error_id_and_logging(caplog):
    """에러 ID 생성 및 로깅 테스트"""
    with caplog.at_level(logging.ERROR):
        exc = ApplicationException(
            code=ResponseCode.INTERNAL_SERVER_ERROR,
            message="에러 ID 테스트"
        )
        
        # 에러 ID 검증
        assert exc.error_id is not None
        assert isinstance(exc.error_id, str)
        assert len(exc.error_id) == 36  # UUID 길이
        
        # 로그 메시지 검증
        assert len(caplog.records) == 1
        log_record = caplog.records[0]
        assert exc.error_id in log_record.message
        assert log_record.levelno == logging.ERROR

        # extra로 들어간 값들은 __dict__에서 바로 접근
        assert "error_code" in log_record.__dict__
        assert log_record.__dict__["error_code"] == str(exc.code)
        assert log_record.__dict__["error_message"] == exc.message
        assert log_record.__dict__["error_id"] == exc.error_id
