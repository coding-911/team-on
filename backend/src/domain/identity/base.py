from datetime import datetime
from typing import Optional
from uuid import UUID
from sqlalchemy import String, CHAR
from sqlalchemy.orm import Mapped, mapped_column

from domain.common.base import Base, IdMixin, TimestampMixin, AuditMixin

class IdentityStatusMixin:
    """상태 관리를 위한 Mixin - CHAR(1) 타입 사용"""
    use_yn: Mapped[str] = mapped_column(CHAR(1), default='Y', nullable=False)
    delete_yn: Mapped[str] = mapped_column(CHAR(1), default='N', nullable=False)

class IdentityBaseEntity(Base, IdMixin, IdentityStatusMixin, TimestampMixin, AuditMixin):
    """Identity 도메인의 기본 엔티티"""
    __abstract__ = True

    def mark_deleted(self, deleted_by: UUID) -> None:
        """엔티티를 삭제 처리합니다."""
        self.delete_yn = 'Y'
        self.use_yn = 'N'
        self.deleted_at = datetime.utcnow()
        self.deleted_by = deleted_by
        self.updated_at = datetime.utcnow()
        self.updated_by = deleted_by

class OrganizationBaseEntity(IdentityBaseEntity):
    """조직 관련 엔티티의 기본 클래스"""
    __abstract__ = True

    name: Mapped[str] = mapped_column(String(100), nullable=False) 