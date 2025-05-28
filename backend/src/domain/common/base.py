from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    """모든 엔티티의 기본이 되는 베이스 클래스"""
    pass

class IdMixin:
    """UUID 기본키를 제공하는 Mixin"""
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

class StatusMixin:
    """상태 관리를 위한 Mixin"""
    use_yn: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    delete_yn: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

class TimestampMixin:
    """타임스탬프 필드를 제공하는 Mixin"""
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=datetime.utcnow,
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

class AuditMixin:
    """감사 추적을 위한 Mixin"""
    created_by: Mapped[Optional[UUID]] = mapped_column(nullable=True)
    updated_by: Mapped[Optional[UUID]] = mapped_column(nullable=True)
    deleted_by: Mapped[Optional[UUID]] = mapped_column(nullable=True)

class SoftDeleteMixin:
    """소프트 삭제 기능을 제공하는 Mixin"""
    
    def soft_delete(self, deleted_by: UUID) -> None:
        """엔티티를 소프트 삭제 처리합니다."""
        self.delete_yn = True
        self.deleted_at = datetime.utcnow()
        self.deleted_by = deleted_by

    @property
    def is_deleted(self) -> bool:
        """엔티티가 삭제되었는지 확인합니다."""
        return self.delete_yn

    @property
    def is_active(self) -> bool:
        """엔티티가 활성 상태인지 확인합니다."""
        return self.use_yn and not self.delete_yn

class BaseEntity(Base, IdMixin, StatusMixin, TimestampMixin, AuditMixin, SoftDeleteMixin):
    """실제 엔티티들이 상속받을 베이스 엔티티 클래스"""
    __abstract__ = True  # 이 클래스는 테이블로 생성되지 않음

    def update_audit_fields(self, updated_by: UUID) -> None:
        """감사 필드를 업데이트합니다."""
        self.updated_at = datetime.utcnow()
        self.updated_by = updated_by 