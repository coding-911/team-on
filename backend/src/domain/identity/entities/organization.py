from uuid import UUID
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import OrganizationBaseEntity

class Department(OrganizationBaseEntity):
    """부서 엔티티
    
    Attributes:
        id (UUID): 기본 키 (IdMixin에서 상속)
        name (str): 부서명 (OrganizationBaseEntity에서 상속)
    """
    __tablename__ = "department"

    # Relationships
    company_departments = relationship("CompanyDepartment", back_populates="department")

class Team(OrganizationBaseEntity):
    """팀 엔티티
    
    Attributes:
        id (UUID): 기본 키 (IdMixin에서 상속)
        name (str): 팀명 (OrganizationBaseEntity에서 상속)
    """
    __tablename__ = "team"

    # Relationships
    company_teams = relationship("CompanyTeam", back_populates="team")

class Position(OrganizationBaseEntity):
    """직위 엔티티
    
    Attributes:
        id (UUID): 기본 키 (IdMixin에서 상속)
        name (str): 직위명 (OrganizationBaseEntity에서 상속)
    """
    __tablename__ = "position"

    # Relationships
    company_positions = relationship("CompanyPosition", back_populates="position")

class Responsibility(OrganizationBaseEntity):
    """직책 엔티티
    
    Attributes:
        id (UUID): 기본 키 (IdMixin에서 상속)
        name (str): 직책명 (OrganizationBaseEntity에서 상속)
    """
    __tablename__ = "responsibility"

    # Relationships
    company_responsibilities = relationship("CompanyResponsibility", back_populates="responsibility") 