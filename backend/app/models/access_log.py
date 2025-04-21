from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

class AccessLog(Base):
    __tablename__ = "accesslog"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("user.id"))
    resource_type = Column(String)  # e.g., "file", "database", "api"
    resource_name = Column(String)
    action = Column(String)  # e.g., "read", "write", "execute"
    location = Column(String)
    success = Column(Boolean, default=True)
    ip_address = Column(String)
    user_agent = Column(String)
    anomaly_score = Column(Float, default=0.0)
    access_metadata = Column(JSON)  # Additional context-specific data
    
    # Relationships
    user = relationship("User", back_populates="access_logs")
    alerts = relationship("Alert", back_populates="source_log") 