from uuid import UUID
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import IdentityBaseEntity

class CompanyUser(IdentityBaseEntity):
    """회사-사용자 매핑 엔티티"""
    __tablename__ = "company_user"

    company_id: Mapped[UUID] = mapped_column(ForeignKey("company.id"), nullable=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"), nullable=False)
    emp_no: Mapped[str] = mapped_column(String(50), nullable=False)
    department_id: Mapped[UUID] = mapped_column(ForeignKey("department.id"), nullable=True)
    team_id: Mapped[UUID] = mapped_column(ForeignKey("team.id"), nullable=True)
    responsibility_id: Mapped[UUID] = mapped_column(ForeignKey("responsibility.id"), nullable=True)
    position_id: Mapped[UUID] = mapped_column(ForeignKey("position.id"), nullable=True)

    # Relationships
    company = relationship("Company", back_populates="company_users")
    user = relationship("User", back_populates="company_users")
    department = relationship("Department", back_populates="company_departments")
    team = relationship("Team", back_populates="company_teams")
    responsibility = relationship("Responsibility", back_populates="company_responsibilities")
    position = relationship("Position", back_populates="company_positions")

class CompanyDepartment(IdentityBaseEntity):
    """회사-부서 매핑 엔티티"""
    __tablename__ = "company_department"

    company_id: Mapped[UUID] = mapped_column(ForeignKey("company.id"), nullable=False)
    department_id: Mapped[UUID] = mapped_column(ForeignKey("department.id"), nullable=False)

    # Relationships
    company = relationship("Company", back_populates="company_departments")
    department = relationship("Department", back_populates="company_departments")

class CompanyTeam(IdentityBaseEntity):
    """회사-팀 매핑 엔티티"""
    __tablename__ = "company_team"

    company_id: Mapped[UUID] = mapped_column(ForeignKey("company.id"), nullable=False)
    team_id: Mapped[UUID] = mapped_column(ForeignKey("team.id"), nullable=False)

    # Relationships
    company = relationship("Company", back_populates="company_teams")
    team = relationship("Team", back_populates="company_teams")

class CompanyPosition(IdentityBaseEntity):
    """회사-직위 매핑 엔티티"""
    __tablename__ = "company_position"

    company_id: Mapped[UUID] = mapped_column(ForeignKey("company.id"), nullable=False)
    position_id: Mapped[UUID] = mapped_column(ForeignKey("position.id"), nullable=False)

    # Relationships
    company = relationship("Company", back_populates="company_positions")
    position = relationship("Position", back_populates="company_positions")

class CompanyResponsibility(IdentityBaseEntity):
    """회사-직책 매핑 엔티티"""
    __tablename__ = "company_responsibility"

    company_id: Mapped[UUID] = mapped_column(ForeignKey("company.id"), nullable=False)
    responsibility_id: Mapped[UUID] = mapped_column(ForeignKey("responsibility.id"), nullable=False)

    # Relationships
    company = relationship("Company", back_populates="company_responsibilities")
    responsibility = relationship("Responsibility", back_populates="company_responsibilities") 