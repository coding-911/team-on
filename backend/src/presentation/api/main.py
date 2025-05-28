from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from presentation.api.error_handlers import setup_error_handlers

def create_app() -> FastAPI:
    app = FastAPI(
        title="TeamOn API",
        description="TeamOn Productivity Platform API",
        version="1.0.0"
    )

    # CORS 설정
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 프로덕션에서는 실제 도메인으로 변경
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 신뢰할 수 있는 호스트 설정
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"]  # 프로덕션에서는 실제 도메인으로 변경
    )

    # 에러 핸들러 설정
    setup_error_handlers(app)

    # 헬스체크
    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    # API 버전 v1 라우터
    # from presentation.api.v1.auth import router as auth_router
    # from presentation.api.v1.users import router as users_router
    # app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
    # app.include_router(users_router, prefix="/api/v1/users", tags=["Users"])

    return app

app = create_app() 