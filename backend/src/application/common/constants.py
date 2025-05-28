from enum import IntEnum
from typing import Dict, Any

class ResponseCode(IntEnum):
    """응답 코드 및 메시지 Enum
    
    각 코드는 4자리 숫자이며, 관련 메시지를 포함합니다.
    """
    def __new__(cls, value: int, message: str = "") -> "ResponseCode":
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.message = message
        return obj

    def format_message(self, **kwargs: Dict[str, Any]) -> str:
        """메시지에 동적 값을 포맷팅하여 반환"""
        return self.message.format(**kwargs) if kwargs else self.message

    # Success
    SUCCESS = (1000, "요청이 성공적으로 처리되었습니다.")

    # Common Errors (1xxx)
    NOT_FOUND = (1001, "요청한 리소스를 찾을 수 없습니다.")            # 기본(0) - 찾기 실패(1)
    VALIDATION_ERROR = (1403, "입력값이 유효하지 않습니다.")           # 데이터 검증(4) - 유효하지 않은 값(3)
    BUSINESS_RULE_VIOLATION = (1607, "비즈니스 규칙 위반이 발생했습니다.")  # 비즈니스 로직(6) - 규칙 위반(7)

    # Auth Domain (2xxx)
    AUTH_INVALID_TOKEN = (2303, "유효하지 않은 인증 토큰입니다.")       # 권한/인증(3) - 유효하지 않은 값(3)
    AUTH_INVALID_CREDENTIALS = (2304, "아이디 또는 비밀번호가 올바르지 않습니다.") # 권한/인증(3) - 권한/인증(4)
    AUTH_TOKEN_EXPIRED = (2305, "인증 토큰이 만료되었습니다.")         # 권한/인증(3) - 제한/초과(5)
    AUTH_REFRESH_TOKEN_EXPIRED = (2305, "리프레시 토큰이 만료되었습니다. 다시 로그인해주세요.") # 권한/인증(3) - 제한/초과(5)

    # Task Domain (3xxx)
    TASK_NOT_FOUND = (3001, "해당 태스크를 찾을 수 없습니다.")         # 기본(0) - 찾기 실패(1)
    TASK_INVALID_STATUS = (3203, "유효하지 않은 태스크 상태입니다.")    # 상태(2) - 유효하지 않은 값(3)
    REPORT_GENERATION_FAILED = (3106, "보고서 생성에 실패했습니다.")    # 문서(1) - 외부 서비스 실패(6)
    TASK_ALREADY_ASSIGNED = (3602, "이미 할당된 태스크입니다.")        # 비즈니스 로직(6) - 중복(2)
    TASK_DUE_DATE_PASSED = (3605, "태스크의 마감 기한이 지났습니다.")   # 비즈니스 로직(6) - 제한/초과(5)
    REWARD_INSUFFICIENT_POINTS = (3605, "보상 지급을 위한 포인트가 부족합니다.") # 비즈니스 로직(6) - 제한/초과(5)

    # User/Org Domain (4xxx)
    USER_NOT_FOUND = (4001, "해당 사용자를 찾을 수 없습니다.")         # 기본(0) - 찾기 실패(1)
    USER_ALREADY_EXISTS = (4002, "이미 존재하는 사용자입니다.")        # 기본(0) - 중복(2)
    USER_INACTIVE = (4203, "비활성화된 사용자입니다.")                # 상태(2) - 유효하지 않은 상태(3)
    COMPANY_NOT_FOUND = (4601, "해당 회사를 찾을 수 없습니다.")        # 비즈니스 로직(6) - 찾기 실패(1)
    COMPANY_ALREADY_EXISTS = (4602, "이미 존재하는 회사입니다.")       # 비즈니스 로직(6) - 중복(2)
    DEPARTMENT_NOT_FOUND = (4601, "해당 부서를 찾을 수 없습니다.")     # 비즈니스 로직(6) - 찾기 실패(1)
    TEAM_NOT_FOUND = (4601, "해당 팀을 찾을 수 없습니다.")            # 비즈니스 로직(6) - 찾기 실패(1)

    # Attendance Domain (5xxx)
    ATTENDANCE_ALREADY_CHECKED = (5002, "이미 출근/퇴근 체크가 완료되었습니다.")   # 기본(0) - 중복(2)
    ATTENDANCE_INVALID_TIME = (5403, "유효하지 않은 출퇴근 시간입니다.")      # 데이터 검증(4) - 유효하지 않은 값(3)
    ATTENDANCE_LOCATION_REQUIRED = (5403, "출퇴근 위치 정보가 필요합니다.")   # 데이터 검증(4) - 유효하지 않은 값(3)
    WORKING_HOURS_EXCEEDED = (5605, "일일 최대 근무시간을 초과했습니다.")     # 비즈니스 로직(6) - 제한/초과(5)

    # File Domain (6xxx)
    FILE_NOT_FOUND = (6001, "파일을 찾을 수 없습니다.")               # 기본(0) - 찾기 실패(1)
    FILE_UPLOAD_FAILED = (6006, "파일 업로드에 실패했습니다.")         # 기본(0) - 외부 서비스 실패(6)
    EXPORT_FAILED = (6106, "파일 내보내기에 실패했습니다.")            # 문서(1) - 외부 서비스 실패(6)
    FILE_TYPE_NOT_ALLOWED = (6403, "허용되지 않는 파일 형식입니다.")    # 데이터 검증(4) - 유효하지 않은 값(3)
    FILE_SIZE_EXCEEDED = (6405, "파일 크기가 허용된 최대 크기를 초과했습니다.") # 데이터 검증(4) - 제한/초과(5)

    # Notification Domain (7xxx)
    PUSH_TOKEN_INVALID = (7503, "유효하지 않은 푸시 토큰입니다.")       # 외부 연동(5) - 유효하지 않은 값(3)
    NOTIFICATION_SEND_FAILED = (7506, "알림 전송에 실패했습니다.")      # 외부 연동(5) - 외부 서비스 실패(6)
    EMAIL_SEND_FAILED = (7506, "이메일 전송에 실패했습니다.")          # 외부 연동(5) - 외부 서비스 실패(6)

    # System Domain (9xxx)
    SERVICE_UNAVAILABLE = (9706, "서비스를 일시적으로 사용할 수 없습니다.")     # 시스템/인프라(7) - 외부 서비스 실패(6)
    INTERNAL_SERVER_ERROR = (9708, "내부 서버 오류가 발생했습니다.")           # 시스템/인프라(7) - 시스템 오류(8)
    DATABASE_ERROR = (9708, "데이터베이스 오류가 발생했습니다.")              # 시스템/인프라(7) - 시스템 오류(8)
    REDIS_ERROR = (9708, "캐시 서버 오류가 발생했습니다.")                   # 시스템/인프라(7) - 시스템 오류(8)
    EXTERNAL_SERVICE_ERROR = (9506, "외부 서비스 연동 중 오류가 발생했습니다.") # 외부 연동(5) - 외부 서비스 실패(6) 