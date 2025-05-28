# TeamOn 예외 처리 시스템

## 개요
TeamOn의 예외 처리 시스템은 계층화된 아키텍처에서 일관된 에러 처리와 로깅을 제공합니다.

## 문서 구조
- [아키텍처 개요](./architecture.md)
- [사용 가이드](./usage-guide.md)
- [에러 코드 목록](./error-codes.md)
- [로깅 가이드](./logging-guide.md)

## 주요 기능
- 계층별 예외 처리
- 구조화된 로깅
- 표준화된 에러 응답
- 에러 추적 및 모니터링

## 빠른 시작
```python
from application.common import (
    ApplicationException,
    ResponseCode
)

# 예외 발생
raise ApplicationException(
    code=ResponseCode.NOT_FOUND,
    message="리소스를 찾을 수 없습니다"
)
```

자세한 사용법은 [사용 가이드](./usage-guide.md)를 참조하세요. 