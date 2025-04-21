from typing import Any, List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ...crud import access_log as access_log_crud
from ...schemas.access_log import AccessLogCreate, AccessLogResponse
from ..deps import get_db, get_current_active_user, get_current_analyst_user

router = APIRouter()

@router.get("/", response_model=List[AccessLogResponse])
def read_access_logs(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = None,
    resource_type: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    min_anomaly_score: Optional[float] = None,
    current_user: Any = Depends(get_current_active_user)
) -> Any:
    """
    Retrieve access logs with optional filtering.
    """
    logs = access_log_crud.get_access_logs(
        db,
        skip=skip,
        limit=limit,
        user_id=user_id,
        resource_type=resource_type,
        start_time=start_time,
        end_time=end_time,
        min_anomaly_score=min_anomaly_score
    )
    return logs

@router.post("/", response_model=AccessLogResponse)
def create_access_log(
    *,
    db: Session = Depends(get_db),
    log_in: AccessLogCreate,
    current_user: Any = Depends(get_current_active_user)
) -> Any:
    """
    Create new access log entry.
    """
    log = access_log_crud.create_access_log(db, log_in)
    return log

@router.get("/{log_id}", response_model=AccessLogResponse)
def read_access_log(
    *,
    db: Session = Depends(get_db),
    log_id: int,
    current_user: Any = Depends(get_current_active_user)
) -> Any:
    """
    Get a specific access log by id.
    """
    log = access_log_crud.get_access_log(db, log_id)
    if not log:
        raise HTTPException(
            status_code=404,
            detail="Access log not found"
        )
    return log

@router.get("/user/{user_id}/patterns", response_model=dict)
def read_user_access_patterns(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    days: int = Query(30, ge=1, le=365),
    current_user: Any = Depends(get_current_analyst_user)
) -> Any:
    """
    Get access patterns for a specific user.
    Only accessible by analysts and admins.
    """
    patterns = access_log_crud.get_user_access_patterns(db, user_id, days)
    return patterns

@router.get("/analytics/summary", response_model=dict)
def get_access_log_analytics(
    *,
    db: Session = Depends(get_db),
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    current_user: Any = Depends(get_current_analyst_user)
) -> Any:
    """
    Get summary analytics for access logs.
    Only accessible by analysts and admins.
    """
    logs = access_log_crud.get_access_logs(
        db,
        start_time=start_time,
        end_time=end_time
    )
    
    analytics = {
        "total_logs": len(logs),
        "unique_users": len(set(log.user_id for log in logs)),
        "resource_types": {},
        "actions": {},
        "anomaly_score_distribution": {
            "low": 0,    # 0-0.3
            "medium": 0, # 0.3-0.7
            "high": 0    # 0.7-1.0
        }
    }
    
    for log in logs:
        # Resource type distribution
        analytics["resource_types"][log.resource_type] = analytics["resource_types"].get(log.resource_type, 0) + 1
        
        # Action distribution
        analytics["actions"][log.action] = analytics["actions"].get(log.action, 0) + 1
        
        # Anomaly score distribution
        if log.anomaly_score is not None:
            if log.anomaly_score < 0.3:
                analytics["anomaly_score_distribution"]["low"] += 1
            elif log.anomaly_score < 0.7:
                analytics["anomaly_score_distribution"]["medium"] += 1
            else:
                analytics["anomaly_score_distribution"]["high"] += 1
    
    return analytics 