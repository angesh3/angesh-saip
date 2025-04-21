from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class AccessLogBase(BaseModel):
    resource_type: str
    resource_id: str
    action: str
    source_ip: str
    location: Dict[str, Any]
    access_metadata: Optional[Dict[str, Any]] = None

class AccessLogCreate(AccessLogBase):
    user_id: int

class AccessLogUpdate(BaseModel):
    anomaly_score: Optional[float] = None
    access_metadata: Optional[Dict[str, Any]] = None

class AccessLogInDB(AccessLogBase):
    id: int
    user_id: int
    timestamp: datetime
    anomaly_score: Optional[float] = None

    class Config:
        from_attributes = True

class AccessLogResponse(AccessLogInDB):
    pass 