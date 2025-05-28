# 로깅 가이드

## 1. 로그 구조

### 1.1 기본 로그 포맷
```
[error_id] message
```

### 1.2 구조화된 로그 데이터
```python
{
    "timestamp": "2024-01-20T12:34:56.789Z",
    "level": "ERROR",
    "error_id": "550e8400-e29b-41d4-a716-446655440000",
    "message": "에러 메시지",
    "error_code": "NOT_FOUND",
    "additional_info": {
        "resource_id": "123",
        "resource_type": "Team"
    }
}
```

## 2. 로그 레벨 사용 가이드

### 2.1 ERROR
- 시스템 운영에 심각한 영향을 미치는 오류
- 즉각적인 대응이 필요한 상황
- 예: 데이터베이스 연결 실패, 중요 API 호출 실패

### 2.2 WARNING
- 잠재적 문제가 될 수 있는 상황
- 당장의 대응은 필요없으나 주의가 필요
- 예: 재시도 성공, 디스크 공간 부족 경고

### 2.3 INFO
- 중요한 비즈니스 이벤트
- 시스템 상태 변경
- 예: 사용자 로그인, 중요 프로세스 시작/종료

### 2.4 DEBUG
- 개발 및 문제 해결을 위한 상세 정보
- 운영 환경에서는 기본적으로 비활성화
- 예: API 요청/응답 상세 내용, 변수값 추적

## 3. 로깅 모범 사례

### 3.1 컨텍스트 정보 포함
```python
logger.error(
    "데이터베이스 쿼리 실패",
    extra={
        "error_id": error_id,
        "query_type": "SELECT",
        "table": "teams",
        "duration_ms": 1234
    }
)
```

### 3.2 구조화된 로깅
```python
# 잘못된 예
logger.error(f"팀({team_id})을 찾을 수 없습니다")

# 좋은 예
logger.error(
    "팀을 찾을 수 없습니다",
    extra={
        "team_id": team_id,
        "error_id": error_id
    }
)
```

### 3.3 민감 정보 처리
```python
# 잘못된 예
logger.error(f"로그인 실패: {user_email}, 비밀번호: {password}")

# 좋은 예
logger.error(
    "로그인 실패",
    extra={
        "user_email_hash": hash_email(user_email),
        "error_id": error_id
    }
)
```

## 4. 로그 수집 및 분석

### 4.1 로그 집계
- ELK 스택 활용
- error_id 기반 연관 로그 추적
- 구조화된 필드 기반 쿼리

### 4.2 모니터링 및 알림
- 중요 에러 발생 시 알림 설정
- 에러 발생 패턴 분석
- 임계치 기반 경고

### 4.3 로그 보관
- 로그 레벨별 보관 기간 설정
- 로그 압축 및 아카이빙
- 규정 준수 고려 