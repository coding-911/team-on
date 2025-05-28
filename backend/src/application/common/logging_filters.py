import logging
from typing import Dict, Any

class ErrorContextFilter(logging.Filter):
    """에러 컨텍스트 정보를 로그 레코드에 추가하는 필터"""
    
    def filter(self, record: logging.LogRecord) -> bool:
        """로그 레코드에 에러 컨텍스트 정보 추가"""
        extra = getattr(record, "extra", {})
        
        # 기본값 설정
        record.error_id = extra.get("error_id", "-")
        record.error_code = extra.get("error_code", "-")
        
        # 추가 필드를 문자열로 변환
        extra_fields = []
        for key, value in extra.items():
            if key not in ["error_id", "error_code"]:
                extra_fields.append(f"{key}={value}")
        record.extra_fields = " ".join(extra_fields)
        
        return True 