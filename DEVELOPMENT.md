
# TeamOn 개발 환경 설정 가이드

## 필수 요구사항

- Docker & Docker Compose
- Python 3.9+
- Node.js 16+
- Poetry (Python 패키지 관리자)
- Git

## 초기 설정

### 1. 저장소 클론
```bash
git clone https://github.com/your-org/teamon.git
cd teamon
```

### 2. 환경 변수 설정

`.env` 파일은 민감한 정보를 포함하므로 Git에 커밋하지 않습니다.  
환경별 예제 파일을 사용하여 다음과 같이 생성하세요:

#### 개발 환경 (`backend/.env.dev`)
```env
DATABASE_URL=postgresql://teamon:CHANGEME@postgres:5432/teamon_db
REDIS_URL=redis://:CHANGEME@redis:6379/0
JWT_SECRET_KEY=CHANGEME_JWT_SECRET
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
SENTRY_DSN=your_sentry_dsn_here
ENVIRONMENT=development
LOG_LEVEL=DEBUG
API_V1_PREFIX=/api/v1
CORS_ORIGINS=["http://localhost:3000"]
ELASTICSEARCH_URL=http://elasticsearch:9200
```

#### 테스트 환경 (`backend/.env.test`) 및 운영 환경 (`backend/.env.prod`)도 동일한 구조로 생성하되 실제 비밀 키는 보안 저장소를 사용합니다.

### 3. .gitignore 설정

`.env*` 파일은 반드시 `.gitignore`에 포함합니다:
```bash
# .gitignore
.env*
```

### 4. 비밀값 보안 가이드

- 운영 환경: AWS Secrets Manager, HashiCorp Vault 등 사용 권장
- CI/CD: GitHub Secrets에 등록
- 로컬 개발: `.env.dev` 사용

### 5. 비밀값 생성 명령어 예시
```bash
openssl rand -hex 32         # JWT 시크릿 키
openssl rand -base64 32      # DB 비밀번호
openssl rand -base64 24      # Redis 비밀번호
```

### 6. 환경 변수 로딩 스크립트 권한 부여
```bash
chmod +x backend/scripts/load_env.sh
```

### 7. 백엔드 설정
```bash
cd backend
poetry install  # 의존성 설치
```

### 8. 프론트엔드 설정
```bash
cd frontend
npm install  # 의존성 설치
```

## 개발 환경 실행

### Docker Compose로 전체 서비스 실행
```bash
docker-compose up -d  # 모든 서비스를 백그라운드로 실행
```

실행되는 서비스:
- Backend API (FastAPI): http://localhost:7000
- Frontend (React): http://localhost:3000
- PostgreSQL: localhost:5432
- Redis: localhost:6379
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001
- Elasticsearch: http://localhost:9200
- Kibana: http://localhost:5601

### 로그 확인
```bash
docker-compose logs -f  # 전체 서비스 로그
docker-compose logs -f backend  # 백엔드 로그만
docker-compose logs -f frontend  # 프론트엔드 로그만
```

### 개별 서비스 재시작
```bash
docker-compose restart backend  # 백엔드 재시작
docker-compose restart frontend  # 프론트엔드 재시작
```

## 개발 도구

### 1. API 문서
- Swagger UI: http://localhost:7000/docs
- ReDoc: http://localhost:7000/redoc

### 2. 모니터링
- Grafana: http://localhost:3001
  - 기본 계정: admin/admin
- Prometheus: http://localhost:9090
- Kibana: http://localhost:5601

### 3. 데이터베이스
```bash
# PostgreSQL CLI 접속
docker-compose exec postgres psql -U teamon -d teamon_db
```

## 테스트 실행

### 백엔드 테스트
```bash
cd backend
poetry run pytest  # 전체 테스트 실행
poetry run pytest tests/unit  # 단위 테스트만 실행
poetry run pytest tests/integration  # 통합 테스트만 실행
```

### 린팅 및 포맷팅
```bash
cd backend
poetry run flake8  # 린팅
poetry run black .  # 코드 포맷팅
```

## 문제 해결

### 1. 컨테이너 상태 확인
```bash
docker-compose ps  # 실행 중인 컨테이너 상태 확인
```

### 2. 데이터베이스 초기화
```bash
docker-compose down -v  # 볼륨 삭제
docker-compose up -d postgres  # PostgreSQL 재시작
```

### 3. 전체 환경 초기화
```bash
docker-compose down -v  # 모든 컨테이너와 볼륨 삭제
docker-compose up -d  # 처음부터 다시 시작
```

## 유용한 명령어

### 1. 마이그레이션
```bash
cd backend
poetry run alembic upgrade head  # 최신 마이그레이션 적용
poetry run alembic revision --autogenerate -m "migration message"  # 새 마이그레이션 생성
```

### 2. 캐시 초기화
```bash
docker-compose restart redis  # Redis 캐시 초기화
```

### 3. 로그 분석
```bash
docker-compose exec elasticsearch curl -X GET "localhost:9200/_cat/indices?v"  # 엘라스틱서치 인덱스 확인
```

## CI/CD

GitHub Actions를 통해 다음 작업이 자동으로 실행됩니다:
- PR 생성 시: 테스트 및 린팅 검사
- main 브랜치 푸시 시: Docker 이미지 빌드 및 레지스트리 업로드

## 참고 사항

- 개발 환경에서는 디버그 모드가 활성화되어 있습니다.
- 실제 프로덕션 환경에서는 반드시 보안 설정을 변경해야 합니다.
- 모든 비밀값은 `.env` 파일에서 관리되며, 이 파일들은 Git에 커밋하지 않습니다. 
