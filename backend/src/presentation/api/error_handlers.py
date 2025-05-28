import logging
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError as PydanticValidationError

from domain.common.exceptions import DomainException
from application.common.exceptions import ApplicationException
from application.common.exception_translators import ExceptionTranslator
from application.common.constants import ResponseCode

logger = logging.getLogger(__name__)

def setup_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(ApplicationException)
    async def application_exception_handler(
        request: Request,
        exc: ApplicationException
    ) -> JSONResponse:
        response_code = ResponseCode(exc.code)
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": exc.code,
                "message": response_code.format_message(**exc.additional_info) if exc.additional_info else response_code.message,
                "data": exc.additional_info if exc.additional_info else None
            }
        )

    @app.exception_handler(DomainException)
    async def domain_exception_handler(
        request: Request,
        exc: DomainException
    ) -> JSONResponse:
        app_exc = ExceptionTranslator.translate(exc)
        response_code = ResponseCode(app_exc.code)
        return JSONResponse(
            status_code=app_exc.status_code,
            content={
                "code": app_exc.code,
                "message": response_code.format_message(**app_exc.additional_info) if app_exc.additional_info else response_code.message,
                "data": app_exc.additional_info if app_exc.additional_info else None
            }
        )

    @app.exception_handler(PydanticValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: PydanticValidationError
    ) -> JSONResponse:
        errors = [
            {
                "field": ".".join(str(loc) for loc in error["loc"]),
                "message": error["msg"]
            }
            for error in exc.errors()
        ]
        
        logger.warning(
            "Validation error",
            extra={
                "path": request.url.path,
                "errors": errors
            }
        )
        
        return JSONResponse(
            status_code=422,
            content={
                "code": ResponseCode.VALIDATION_ERROR,
                "message": ResponseCode.VALIDATION_ERROR.message,
                "data": {"errors": errors}
            }
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(
        request: Request,
        exc: SQLAlchemyError
    ) -> JSONResponse:
        logger.error(
            "Database error",
            exc_info=exc,
            extra={
                "path": request.url.path,
                "error": str(exc)
            }
        )
        
        return JSONResponse(
            status_code=500,
            content={
                "code": ResponseCode.DATABASE_ERROR,
                "message": ResponseCode.DATABASE_ERROR.message,
                "data": {
                    "error": str(exc) if app.debug else None
                }
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request,
        exc: Exception
    ) -> JSONResponse:
        logger.error(
            "Unhandled exception",
            exc_info=exc,
            extra={
                "path": request.url.path,
                "error": str(exc)
            }
        )
        
        return JSONResponse(
            status_code=500,
            content={
                "code": ResponseCode.INTERNAL_SERVER_ERROR,
                "message": ResponseCode.INTERNAL_SERVER_ERROR.message,
                "data": {
                    "error": str(exc) if app.debug else None
                }
            }
        ) 