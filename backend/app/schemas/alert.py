from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from ..models.alert import AlertStatus, AlertSeverity

class AlertBase(BaseModel):
    access_log_id: int
    severity: AlertSeverity
    description: str
    alert_metadata: Optional[Dict[str, Any]] = None

class AlertCreate(AlertBase):
    pass

class AlertUpdate(BaseModel):
    assigned_to_id: Optional[int] = None
    status: Optional[AlertStatus] = None
    investigation_notes: Optional[str] = None
    resolution_notes: Optional[str] = None
    alert_metadata: Optional[Dict[str, Any]] = None

class AlertInDB(AlertBase):
    id: int
    timestamp: datetime
    assigned_to_id: Optional[int] = None
    status: AlertStatus
    investigation_notes: Optional[str] = None
    resolution_notes: Optional[str] = None

    class Config:
        from_attributes = True

class AlertResponse(AlertInDB):
    pass 