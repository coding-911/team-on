# TeamOn Backend

TeamOn 백엔드는 도메인 주도 설계(DDD) 원칙을 따르는 FastAPI 기반의 RESTful API 서버입니다.

## 아키텍처

계층형 아키텍처를 사용하여 관심사를 분리하고 있습니다:

```
backend/
├── src/
│   ├── domain/         # 도메인 계층: 비즈니스 로직과 규칙
│   │   ├── common/     # 공통 도메인 예외, 인터페이스 등
│   │   ├── user/       # 사용자 도메인
│   │   ├── task/       # 태스크 도메인
│   │   └── reward/     # 리워드 도메인
│   │
│   ├── application/    # 애플리케이션 계층: 유스케이스 구현
│   │   ├── common/     # 공통 응답 형식, 예외 처리 등
│   │   ├── user/       # 사용자 관련 서비스
│   │   ├── task/       # 태스크 관련 서비스
│   │   └── reward/     # 리워드 관련 서비스
│   │
│   └── presentation/   # 프레젠테이션 계층: API 엔드포인트
│       ├── api/        # FastAPI 라우터, 미들웨어
│       └── schemas/    # 요청/응답 스키마
│
├── tests/             # 테스트 코드
├── alembic/           # 데이터베이스 마이그레이션
└── scripts/           # 유틸리티 스크립트
```

## 주요 컴포넌트

### 1. 도메인 계층
- 비즈니스 엔티티와 값 객체 정의
- 도메인 예외 처리
- 도메인 이벤트 처리
- 리포지토리 인터페이스 정의

### 2. 애플리케이션 계층
- 유스케이스 구현
- 트랜잭션 관리
- 도메인 객체 조합
- 외부 서비스 통합

### 3. 프레젠테이션 계층
- REST API 엔드포인트
- 요청 유효성 검사
- 응답 직렬화
- 인증/인가 처리

## 주요 기능

### 에러 처리
- [에러 코드 체계](src/application/common/README.md)
- 계층별 예외 처리
- 일관된 에러 응답 형식

### 인증/인가
- JWT 기반 인증
- RBAC(Role-Based Access Control)
- OAuth2 지원

### 데이터 접근
- SQLAlchemy ORM
- Redis 캐싱
- Elasticsearch 검색

### API 문서
- OpenAPI (Swagger) 문서
- ReDoc 지원
- [API 가이드](docs/api/README.md)

## 코드 품질

### 테스트
- 단위 테스트 (pytest)
- 통합 테스트
- E2E 테스트

### 코드 스타일
- Black 포맷터
- Flake8 린터
- MyPy 타입 체커

### 모니터링
- Prometheus 메트릭
- 구조화된 로깅
- Sentry 에러 추적

## 참고 문서

- [프로젝트 설정 가이드](../DEVELOPMENT.md)
- [API 문서](http://localhost:8000/docs)
- [아키텍처 결정 기록](docs/adr/README.md)

## 주요 문서

- [에러 코드 체계](src/application/common/README.md)
- [API 문서](docs/api/README.md)
- [개발 가이드](docs/development.md)

## 개발 환경 설정

[개발 환경 설정 내용...] 