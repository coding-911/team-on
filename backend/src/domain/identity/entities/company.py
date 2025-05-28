from datetime import datetime
from typing import Optional, List
from uuid import UUID
from sqlalchemy import String, ForeignKey, Text, CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import IdentityBaseEntity

class Company(IdentityBaseEntity):
    """회사 엔티티"""
    __tablename__ = "company"

    business_registration_number: Mapped[str] = mapped_column(String(20), nullable=False, unique=True, 
                                                            comment="사업자등록번호")
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="기업명")
    eng_name: Mapped[str] = mapped_column(String(100), nullable=False, comment="영문 기업명")
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    ceo_name: Mapped[str] = mapped_column(String(100), nullable=False, comment="대표자 성명")
    homepage_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="회사 홈페이지")

    # Relationships
    users = relationship("User", back_populates="company")
    company_users = relationship("CompanyUser", back_populates="company")
    company_departments = relationship("CompanyDepartment", back_populates="company")
    company_teams = relationship("CompanyTeam", back_populates="company")
    company_positions = relationship("CompanyPosition", back_populates="company")
    company_responsibilities = relationship("CompanyResponsibility", back_populates="company")
    registration_requests = relationship("CompanyRegistrationRequest", back_populates="approved_company")
    subscriptions = relationship("CompanySubscription", back_populates="company")

class CompanyRegistrationRequest(IdentityBaseEntity):
    """회사 등록 요청 엔티티"""
    __tablename__ = "company_registration_request"

    business_registration_number: Mapped[str] = mapped_column(String(20), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    eng_name: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    ceo_name: Mapped[str] = mapped_column(String(100), nullable=False)
    homepage_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, 
                                      comment="PENDING / APPROVED / REJECTED")
    
    requested_by: Mapped[UUID] = mapped_column(ForeignKey("user.id"), nullable=False)
    approved_by: Mapped[Optional[UUID]] = mapped_column(ForeignKey("user.id"), nullable=True)
    approved_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    rejected_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    reject_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    approved_company_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("company.id"), nullable=True)

    # Relationships
    requester = relationship("User", foreign_keys=[requested_by], back_populates="requested_registrations")
    approver = relationship("User", foreign_keys=[approved_by])
    approved_company = relationship("Company", back_populates="registration_requests") 