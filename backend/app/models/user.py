from sqlalchemy import Column, Integer, String, Boolean, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from enum import Enum
from app.db.base_class import Base

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    ANALYST = "ANALYST"
    VIEWER = "VIEWER"

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    role = Column(SQLAlchemyEnum(UserRole))  # Using the enum for role
    is_active = Column(Boolean, default=True)
    
    # Relationships
    access_logs = relationship("AccessLog", back_populates="user")
    assigned_alerts = relationship("Alert", back_populates="assigned_to") 