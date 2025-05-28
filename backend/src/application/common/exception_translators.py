from typing import Dict, Any, Type, Optional

from domain.common.exceptions import (
    DomainException,
    EntityNotFoundException,
    ValidationException,
    BusinessRuleException
)
from application.common.constants import ResponseCode
from application.common.exceptions import (
    ApplicationException,
    ResourceNotFoundException,
    ValidationFailedException,
    BusinessRuleViolationException
)

class ExceptionTranslator:
    """도메인 예외를 애플리케이션 예외로 변환"""

    @classmethod
    def translate(cls, domain_exc: Exception) -> ApplicationException:
        """도메인 예외를 애플리케이션 예외로 변환"""
        if isinstance(domain_exc, EntityNotFoundException):
            return cls._translate_entity_not_found(domain_exc)
        elif isinstance(domain_exc, ValidationException):
            return cls._translate_validation_exception(domain_exc)
        elif isinstance(domain_exc, BusinessRuleException):
            return cls._translate_business_rule_exception(domain_exc)
        elif hasattr(domain_exc, "to_dict"):
            return cls._translate_unknown_domain_exception(domain_exc)
        else:
            return ApplicationException(
                code=ResponseCode.INTERNAL_SERVER_ERROR,
                message=str(domain_exc)
            )

    @classmethod
    def _translate_entity_not_found(
        cls,
        exc: EntityNotFoundException
    ) -> ResourceNotFoundException:
        """엔티티 찾기 실패 예외 변환"""
        return ResourceNotFoundException(
            message=str(exc),
            resource_type=exc.entity_type,
            resource_id=exc.entity_id,
            additional_info=exc.additional_info
        )

    @classmethod
    def _translate_validation_exception(
        cls,
        exc: ValidationException
    ) -> ValidationFailedException:
        """유효성 검사 예외 변환"""
        return ValidationFailedException(
            message=str(exc),
            field=exc.field,
            value=exc.invalid_value,
            additional_info=exc.additional_info
        )

    @classmethod
    def _translate_business_rule_exception(
        cls,
        exc: BusinessRuleException
    ) -> BusinessRuleViolationException:
        """비즈니스 규칙 예외 변환"""
        return BusinessRuleViolationException(
            message=str(exc),
            rule=exc.rule,
            context=exc.context
        )

    @classmethod
    def _translate_unknown_domain_exception(
        cls,
        exc: Any
    ) -> ApplicationException:
        """알 수 없는 도메인 예외 변환"""
        exc_dict = exc.to_dict()
        message = exc_dict.pop("message", str(exc))
        
        return ApplicationException(
            code=ResponseCode.INTERNAL_SERVER_ERROR,
            message=message,
            additional_info=exc_dict
        ) 