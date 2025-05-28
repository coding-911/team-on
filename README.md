# TeamOn

TeamOn은 현대적인 팀 협업 플랫폼입니다. 업무 관리, 회의 관리, 리워드 시스템을 통합하여 제공합니다.

## 주요 기능

- 👥 사용자 및 조직 관리
  - 조직 구조 관리
  - 권한 및 역할 관리
  - 프로필 및 설정
  
- 📋 업무 관리 및 추적
  - 태스크 생성 및 할당
  - 진행 상황 추적
  - 마일스톤 관리
  
- 🎯 회의 관리 및 녹음/요약
  - 회의 일정 관리
  - 실시간 회의록
  - AI 기반 회의 요약
  
- 🌟 리워드 및 게이미피케이션
  - 업적 시스템
  - 포인트 및 배지
  - 리더보드

- 📊 실시간 모니터링 및 분석
  - 대시보드
  - 리포트 생성
  - 데이터 시각화

- 🔔 실시간 알림
  - 이메일 알림
  - 푸시 알림
  - 인앱 알림

## 시스템 아키텍처

```
TeamOn/
├── backend/           # FastAPI 백엔드
├── frontend/          # React 프론트엔드
├── infrastructure/    # 인프라 코드 (Terraform)
└── k8s/              # Kubernetes 매니페스트
```

## 기술 스택

### 백엔드
- FastAPI (Python 3.10)
- PostgreSQL 14
- Redis 6
- Elasticsearch 8

### 프론트엔드
- React 18
- TypeScript 5
- Material-UI 5

### 인프라
- Docker & Docker Compose
- Kubernetes
- GitHub Actions
- Prometheus & Grafana
- ELK Stack

## 시작하기

1. 저장소 클론:
```bash
git clone https://github.com/coding-911/team-on.git
cd team-on
```

2. 개발 환경 설정:
자세한 내용은 [개발 환경 설정 가이드](DEVELOPMENT.md)를 참조하세요.

3. 빠른 시작:
```bash
# 환경 변수 설정
cp backend/.env.example backend/.env

# Docker Compose로 실행
docker-compose up -d
```

## 문서

- [개발 환경 설정](DEVELOPMENT.md)
- [백엔드 아키텍처](backend/README.md)
- [API 문서](http://localhost:8000/docs)
- [배포 가이드](docs/DEPLOYMENT.md)

## 기여하기

1. 이슈 생성 또는 기존 이슈 선택
2. Feature 브랜치 생성
3. 변경사항 커밋
4. Pull Request 생성

자세한 내용은 [기여 가이드](CONTRIBUTING.md)를 참조하세요.

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.


