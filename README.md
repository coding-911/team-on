# TeamOn

TeamOn은 현대적인 팀 협업 플랫폼입니다. 업무 관리, 회의 관리, 리워드 시스템을 통합하여 제공합니다.

## 주요 기능

- 👥 사용자 및 조직 관리
- 📋 업무 관리 및 추적
- 🎯 회의 관리 및 녹음/요약
- 🌟 리워드 및 게이미피케이션
- 📊 실시간 모니터링 및 분석
- 🔔 실시간 알림

## 기술 스택

### 백엔드
- FastAPI (Python 3.9)
- PostgreSQL
- Redis
- Elasticsearch

### 프론트엔드
- React
- TypeScript
- Material-UI

### 인프라
- Docker & Docker Compose
- Kubernetes
- GitHub Actions
- Prometheus & Grafana
- ELK Stack

## 시작하기

자세한 개발 환경 설정 및 실행 방법은 [DEVELOPMENT.md](DEVELOPMENT.md)를 참조하세요.

### 빠른 시작
```bash
# 저장소 클론
git clone https://github.com/coding-911/team-on.git
cd teamon

# 환경 변수 설정
cp backend/.env.example backend/.env.dev

# Docker Compose로 실행
docker-compose up -d
```

## 문서

- [개발 가이드](DEVELOPMENT.md)
- [API 문서](http://localhost:7000/docs)
- [아키텍처 문서](docs/ARCHITECTURE.md)
- [배포 가이드](docs/DEPLOYMENT.md)


