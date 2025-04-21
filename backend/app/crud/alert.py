from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, timedelta
from ..models.alert import Alert, AlertStatus, AlertSeverity
from ..schemas.alert import AlertCreate, AlertUpdate

def get_alert(db: Session, alert_id: int) -> Optional[Alert]:
    return db.query(Alert).filter(Alert.id == alert_id).first()

def get_alerts(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: Optional[AlertStatus] = None,
    severity: Optional[AlertSeverity] = None,
    assigned_to_id: Optional[int] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None
) -> List[Alert]:
    query = db.query(Alert)
    
    if status:
        query = query.filter(Alert.status == status)
    if severity:
        query = query.filter(Alert.severity == severity)
    if assigned_to_id:
        query = query.filter(Alert.assigned_to_id == assigned_to_id)
    if start_time:
        query = query.filter(Alert.timestamp >= start_time)
    if end_time:
        query = query.filter(Alert.timestamp <= end_time)
    
    return query.order_by(Alert.timestamp.desc()).offset(skip).limit(limit).all()

def create_alert(db: Session, alert: AlertCreate) -> Alert:
    db_alert = Alert(**alert.model_dump())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

def update_alert(
    db: Session, alert_id: int, alert: AlertUpdate
) -> Optional[Alert]:
    db_alert = get_alert(db, alert_id)
    if not db_alert:
        return None
    
    update_data = alert.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_alert, field, value)
    
    db.commit()
    db.refresh(db_alert)
    return db_alert

def get_alert_statistics(
    db: Session,
    days: int = 30
) -> dict:
    start_time = datetime.utcnow() - timedelta(days=days)
    alerts = db.query(Alert).filter(Alert.timestamp >= start_time).all()
    
    stats = {
        "total_alerts": len(alerts),
        "by_status": {},
        "by_severity": {},
        "resolution_time": [],
        "alerts_by_day": {}
    }
    
    for alert in alerts:
        # Status distribution
        stats["by_status"][alert.status] = stats["by_status"].get(alert.status, 0) + 1
        
        # Severity distribution
        stats["by_severity"][alert.severity] = stats["by_severity"].get(alert.severity, 0) + 1
        
        # Resolution time (for resolved alerts)
        if alert.status == AlertStatus.RESOLVED and alert.investigation_notes:
            resolution_time = (datetime.utcnow() - alert.timestamp).total_seconds() / 3600  # in hours
            stats["resolution_time"].append(resolution_time)
        
        # Alerts by day
        day = alert.timestamp.date().isoformat()
        stats["alerts_by_day"][day] = stats["alerts_by_day"].get(day, 0) + 1
    
    # Calculate average resolution time
    if stats["resolution_time"]:
        stats["avg_resolution_time"] = sum(stats["resolution_time"]) / len(stats["resolution_time"])
    else:
        stats["avg_resolution_time"] = 0
    
    return stats 