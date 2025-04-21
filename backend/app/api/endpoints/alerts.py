from typing import Any, List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ...crud import alert as alert_crud
from ...schemas.alert import AlertCreate, AlertUpdate, AlertResponse
from ..deps import get_db, get_current_active_user, get_current_analyst_user

router = APIRouter()

@router.get("/", response_model=List[AlertResponse])
def read_alerts(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    severity: Optional[str] = None,
    assigned_to_id: Optional[int] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    current_user: Any = Depends(get_current_active_user)
) -> Any:
    """
    Retrieve alerts with optional filtering.
    """
    alerts = alert_crud.get_alerts(
        db,
        skip=skip,
        limit=limit,
        status=status,
        severity=severity,
        assigned_to_id=assigned_to_id,
        start_time=start_time,
        end_time=end_time
    )
    return alerts

@router.post("/", response_model=AlertResponse)
def create_alert(
    *,
    db: Session = Depends(get_db),
    alert_in: AlertCreate,
    current_user: Any = Depends(get_current_analyst_user)
) -> Any:
    """
    Create new alert. Only accessible by analysts and admins.
    """
    alert = alert_crud.create_alert(db, alert_in)
    return alert

@router.get("/{alert_id}", response_model=AlertResponse)
def read_alert(
    *,
    db: Session = Depends(get_db),
    alert_id: int,
    current_user: Any = Depends(get_current_active_user)
) -> Any:
    """
    Get a specific alert by id.
    """
    alert = alert_crud.get_alert(db, alert_id)
    if not alert:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )
    return alert

@router.put("/{alert_id}", response_model=AlertResponse)
def update_alert(
    *,
    db: Session = Depends(get_db),
    alert_id: int,
    alert_in: AlertUpdate,
    current_user: Any = Depends(get_current_analyst_user)
) -> Any:
    """
    Update an alert. Only accessible by analysts and admins.
    """
    alert = alert_crud.get_alert(db, alert_id)
    if not alert:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )
    alert = alert_crud.update_alert(db, alert_id, alert_in)
    return alert

@router.get("/analytics/summary", response_model=dict)
def get_alert_analytics(
    *,
    db: Session = Depends(get_db),
    days: int = Query(30, ge=1, le=365),
    current_user: Any = Depends(get_current_analyst_user)
) -> Any:
    """
    Get summary analytics for alerts.
    Only accessible by analysts and admins.
    """
    stats = alert_crud.get_alert_statistics(db, days)
    return stats

@router.get("/analytics/trends", response_model=dict)
def get_alert_trends(
    *,
    db: Session = Depends(get_db),
    days: int = Query(30, ge=1, le=365),
    current_user: Any = Depends(get_current_analyst_user)
) -> Any:
    """
    Get alert trends over time.
    Only accessible by analysts and admins.
    """
    stats = alert_crud.get_alert_statistics(db, days)
    
    # Calculate trends
    trends = {
        "daily_alert_counts": stats["alerts_by_day"],
        "severity_trends": {
            severity: count / stats["total_alerts"] * 100
            for severity, count in stats["by_severity"].items()
        },
        "resolution_trends": {
            "avg_resolution_time": stats["avg_resolution_time"],
            "resolution_rate": (
                stats["by_status"].get("resolved", 0) / stats["total_alerts"] * 100
                if stats["total_alerts"] > 0 else 0
            )
        }
    }
    
    return trends 