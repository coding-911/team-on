# 예외 처리 시스템 아키텍처

## 1. 계층 구조

### 도메인 계층
```
DomainException (도메인 계층 기본 예외)
├── EntityNotFoundException
├── ValidationException
└── BusinessRuleException
```

### 애플리케이션 계층
```
ApplicationException (애플리케이션 계층 기본 예외)
├── ResourceNotFoundException
├── ValidationFailedException
├── BusinessRuleViolationException
└── AuthenticationException
```

## 2. 주요 컴포넌트

### 2.1 기본 예외 클래스
#### DomainException
- 도메인 계층의 기본 예외 클래스
- 도메인 규칙 위반 및 유효성 검사 실패 처리
- 풍부한 컨텍스트 정보 제공
- JSON 직렬화 지원

#### ApplicationException
- 애플리케이션 계층의 기본 예외 클래스
- 에러 코드 및 HTTP 상태 코드 관리
- 사용자 친화적 메시지 처리
- 구조화된 로깅 통합

### 2.2 응답 형식
```python
{
    "code": str,           # 표준화된 에러 코드 (ResponseCode enum)
    "message": str,        # 사용자 친화적 메시지 (포맷팅된 메시지 지원)
    "data": dict | None    # 추가 컨텍스트 정보 (validation errors, debug 정보 등)
}
```

예시:
```python
# 유효성 검사 실패 응답
{
    "code": "VALIDATION_ERROR",
    "message": "입력값이 유효하지 않습니다",
    "data": {
        "errors": [
            {
                "field": "email",
                "message": "올바른 이메일 형식이 아닙니다"
            }
        ]
    }
}

# 비즈니스 규칙 위반 응답
{
    "code": "BUSINESS_RULE_VIOLATION",
    "message": "이미 완료된 작업은 수정할 수 없습니다",
    "data": {
        "task_id": "123",
        "status": "COMPLETED"
    }
}
```

### 2.3 로깅 시스템
#### 기본 로깅 구조
```python
{
    "timestamp": "2024-03-14T12:34:56.789Z",
    "level": "ERROR",
    "path": "/api/v1/tasks",
    "exception_type": "ValidationException",
    "message": "유효성 검사 실패",
    "context": {
        "field": "due_date",
        "value": "2024-13-45",
        "additional_info": {...}
    }
}
```

#### 로그 레벨 정책
- ERROR: 시스템 오류, 데이터베이스 오류
- WARNING: 유효성 검사 실패, 인증 실패
- INFO: 주요 비즈니스 이벤트
- DEBUG: 상세 디버깅 정보 (개발 환경)

#### 로깅 컨텍스트
- 요청 경로 (path)
- 예외 타입 (exception_type)
- 상세 메시지 (message)
- 추가 컨텍스트 (context)
  - 실패한 필드 정보
  - 잘못된 입력값
  - 비즈니스 규칙 관련 정보

## 3. 계층별 책임

### 3.1 도메인 계층
- 순수한 비즈니스 규칙 위반 예외 정의
- 도메인 특화 예외 클래스 구현
- 풍부한 컨텍스트 정보 제공

### 3.2 애플리케이션 계층
- 트랜잭션 관리
- 예외 변환 및 래핑
- 로깅 및 모니터링

### 3.3 프레젠테이션 계층
- 전역 예외 처리
- HTTP 상태 코드 매핑
- 클라이언트 응답 포맷팅

## 4. 주요 기능

### 4.1 예외 변환 (Exception Translation)
- ExceptionTranslator를 통한 도메인 예외의 애플리케이션 예외 변환
- 도메인 예외의 컨텍스트 정보 보존
- 표준화된 에러 코드 및 HTTP 상태 코드 매핑

예외 변환 매핑:
```
DomainException -> ApplicationException
├── EntityNotFoundException -> ResourceNotFoundException
├── ValidationException -> ValidationFailedException
└── BusinessRuleException -> BusinessRuleViolationException
```

### 4.2 예외 추적
- 고유한 error_id 생성
- 로그-응답 연계
- 디버깅 용이성

### 4.3 구조화된 로깅
- JSON 형식 로그
- 컨텍스트 데이터 포함
- 로그 레벨 최적화

### 4.4 확장성
- 새로운 예외 타입 쉽게 추가
- 커스텀 처리 로직 구현
- 외부 시스템 통합 