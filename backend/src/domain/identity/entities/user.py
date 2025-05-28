from typing import Optional
from uuid import UUID
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import IdentityBaseEntity

class User(IdentityBaseEntity):
    """사용자 엔티티"""
    __tablename__ = "user"

    emp_no: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False, 
                                    comment="USER / TEAM_MANAGER / ORG_ADMIN / SYS_ADMIN")
    company_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("company.id"), nullable=True)

    # Relationships
    company = relationship("Company", back_populates="users")
    company_users = relationship("CompanyUser", back_populates="user")
    auth_tokens = relationship("AuthTokenLog", back_populates="user")
    role_logs = relationship("UserRoleLog", back_populates="user") 