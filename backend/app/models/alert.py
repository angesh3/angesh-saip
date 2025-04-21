from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, JSON, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime
import enum

class AlertStatus(str, enum.Enum):
    NEW = "new"
    ACKNOWLEDGED = "acknowledged"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    FALSE_POSITIVE = "false_positive"

class AlertSeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Alert(Base):
    __tablename__ = "alert"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    alert_type = Column(String)
    severity = Column(String)
    status = Column(String)
    description = Column(Text)
    source_log_id = Column(Integer, ForeignKey("accesslog.id"))
    assigned_to_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    resolution_notes = Column(Text, nullable=True)
    investigation_notes = Column(String, nullable=True)
    alert_metadata = Column(JSON)  # Additional context and model explainability data
    
    # Relationships
    source_log = relationship("AccessLog", back_populates="alerts")
    assigned_to = relationship("User", back_populates="assigned_alerts") 