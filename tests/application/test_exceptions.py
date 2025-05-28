import json
import logging
import pytest
from uuid import UUID

from application.common.constants import ResponseCode
from application.common.exceptions import (
    ApplicationException,
    ResourceNotFoundException,
    ValidationFailedException,
    BusinessRuleViolationException
)

def test_error_id_and_logging(caplog):
    """에러 ID 생성 및 로깅 테스트"""
    with caplog.at_level(logging.ERROR):
        test_message = "에러 ID 테스트"
        exc = ApplicationException(
            code=ResponseCode.INTERNAL_SERVER_ERROR,
            message=test_message
        )

        # 1. 에러 ID 검증
        assert exc.error_id is not None
        assert isinstance(exc.error_id, str)
        assert len(exc.error_id) == 36  # UUID 길이

        # 2. 로그 기록 검증
        assert len(caplog.records) == 1
        log_record = caplog.records[0]
        
        # 3. 로그 레벨 검증
        assert log_record.levelno == logging.ERROR
        
        # 4. 로그 메시지 포맷 검증
        assert f"[{exc.error_id}]" in log_record.message
        assert test_message in log_record.message
        
        # 5. LogRecord extra 필드 검증
        assert hasattr(log_record, "error_code")
        assert hasattr(log_record, "error_id")
        assert hasattr(log_record, "error_message")
        assert hasattr(log_record, "additional_info")
        
        assert log_record.error_id == exc.error_id
        assert log_record.error_code == str(exc.code)
        assert log_record.error_message == test_message

def test_application_exception_response():
    """ApplicationException의 HTTP 응답 변환 테스트"""
    additional_info = {
        "test_key": "test_value",
        "nested": {"key": "value"}
    }
    
    exc = ApplicationException(
        code=ResponseCode.INTERNAL_SERVER_ERROR,
        message="테스트 메시지",
        additional_info=additional_info
    )
    
    response = exc.to_response_dict()
    
    assert response["code"] == ResponseCode.INTERNAL_SERVER_ERROR
    assert response["message"] == "테스트 메시지"
    assert response["data"] == additional_info
    assert "error_id" in response
    assert isinstance(response["error_id"], str)

def test_empty_additional_info():
    """추가 정보가 없는 경우 테스트"""
    exc = ApplicationException(
        code=ResponseCode.INTERNAL_SERVER_ERROR,
        message="테스트 메시지"
    )
    
    assert exc.additional_info == {}
    response = exc.to_response_dict()
    assert response["data"] == {}

# ... 기존 다른 테스트 케이스들 ... 