# 예외 처리 시스템 사용 가이드

## 1. 기본 사용법

### 1.1 예외 발생
```python
from application.common import ApplicationException, ResponseCode

raise ApplicationException(
    code=ResponseCode.NOT_FOUND,
    message="리소스를 찾을 수 없습니다",
    additional_info={"resource_id": "123"}
)
```

### 1.2 예외 처리
```python
try:
    process_something()
except ApplicationException as e:
    logger.error(f"처리 실패: {e.error_id}")
    return JSONResponse(
        status_code=e.status_code,
        content=e.to_response_dict()
    )
```

## 2. 계층별 사용 예시

### 2.1 도메인 계층
```python
from application.common import BusinessRuleViolationException

class Team:
    def add_member(self, member):
        if len(self.members) >= self.max_members:
            raise BusinessRuleViolationException(
                message="팀 최대 인원을 초과했습니다",
                rule="max_team_members",
                context={
                    "team_id": self.id,
                    "current_count": len(self.members),
                    "max_count": self.max_members
                }
            )
```

### 2.2 애플리케이션 계층
```python
from application.common import ResourceNotFoundException

class TeamService:
    def get_team(self, team_id: str):
        team = self.team_repository.find_by_id(team_id)
        if not team:
            raise ResourceNotFoundException(
                message="팀을 찾을 수 없습니다",
                resource_type="Team",
                resource_id=team_id
            )
        return team
```

### 2.3 프레젠테이션 계층
```python
from fastapi import APIRouter, Depends
from application.common import ValidationFailedException

router = APIRouter()

@router.post("/teams/{team_id}/members")
async def add_team_member(
    team_id: str,
    member_data: dict
):
    if not member_data.get('email'):
        raise ValidationFailedException(
            message="이메일은 필수 항목입니다",
            field="email",
            value=member_data.get('email')
        )
```

## 3. 로깅 활용

### 3.1 기본 로깅
```python
# 예외 발생 시 자동으로 로깅됨
# [error_id] message
# 추가 컨텍스트 정보도 함께 기록
```

### 3.2 커스텀 로깅
```python
try:
    process_something()
except ApplicationException as e:
    logger.error(
        f"커스텀 에러 처리: {e.message}",
        extra={
            "error_id": e.error_id,
            "custom_field": "custom_value"
        }
    )
```

## 4. 모범 사례

### 4.1 예외 계층 선택
- 가능한 한 구체적인 예외 사용
- 적절한 컨텍스트 정보 포함
- 사용자 친화적 메시지 작성

### 4.2 로깅 최적화
- 적절한 로그 레벨 사용
- 필요한 컨텍스트만 포함
- 민감 정보 제외

### 4.3 성능 고려사항
- 스택 트레이스 최소화
- 로그 볼륨 관리
- 예외 처리 비용 고려 