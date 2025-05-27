FROM python:3.9-slim

WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Poetry 설치
RUN pip install poetry

# Poetry 가상환경 비활성화 (Docker에서는 불필요)
RUN poetry config virtualenvs.create false

# 프로젝트 의존성 파일 복사
COPY pyproject.toml poetry.lock ./

# 의존성 설치
RUN poetry install --no-dev --no-interaction --no-ansi

# 소스코드 복사
COPY . .

# 포트 설정
EXPOSE 7000

# 실행 명령
CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7000"] 