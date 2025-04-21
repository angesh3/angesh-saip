from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from ..models.access_log import AccessLog
from ..schemas.access_log import AccessLogCreate, AccessLogUpdate

def get_access_log(db: Session, log_id: int) -> Optional[AccessLog]:
    return db.query(AccessLog).filter(AccessLog.id == log_id).first()

def get_access_logs(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = None,
    resource_type: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    min_anomaly_score: Optional[float] = None
) -> List[AccessLog]:
    query = db.query(AccessLog)
    
    if user_id:
        query = query.filter(AccessLog.user_id == user_id)
    if resource_type:
        query = query.filter(AccessLog.resource_type == resource_type)
    if start_time:
        query = query.filter(AccessLog.timestamp >= start_time)
    if end_time:
        query = query.filter(AccessLog.timestamp <= end_time)
    if min_anomaly_score is not None:
        query = query.filter(AccessLog.anomaly_score >= min_anomaly_score)
    
    return query.order_by(AccessLog.timestamp.desc()).offset(skip).limit(limit).all()

def create_access_log(db: Session, log: AccessLogCreate) -> AccessLog:
    db_log = AccessLog(**log.model_dump())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def update_access_log(
    db: Session, log_id: int, log: AccessLogUpdate
) -> Optional[AccessLog]:
    db_log = get_access_log(db, log_id)
    if not db_log:
        return None
    
    update_data = log.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_log, field, value)
    
    db.commit()
    db.refresh(db_log)
    return db_log

def get_user_access_patterns(
    db: Session,
    user_id: int,
    days: int = 30
) -> Dict[str, Any]:
    start_time = datetime.utcnow() - timedelta(days=days)
    logs = db.query(AccessLog).filter(
        AccessLog.user_id == user_id,
        AccessLog.timestamp >= start_time
    ).all()
    
    patterns = {
        "total_accesses": len(logs),
        "resource_types": {},
        "actions": {},
        "time_distribution": {},
        "locations": {},
        "anomaly_scores": []
    }
    
    for log in logs:
        # Resource type distribution
        patterns["resource_types"][log.resource_type] = patterns["resource_types"].get(log.resource_type, 0) + 1
        
        # Action distribution
        patterns["actions"][log.action] = patterns["actions"].get(log.action, 0) + 1
        
        # Time distribution (by hour)
        hour = log.timestamp.hour
        patterns["time_distribution"][hour] = patterns["time_distribution"].get(hour, 0) + 1
        
        # Location distribution
        location_key = f"{log.location.get('country', 'unknown')}-{log.location.get('city', 'unknown')}"
        patterns["locations"][location_key] = patterns["locations"].get(location_key, 0) + 1
        
        # Anomaly scores
        if log.anomaly_score is not None:
            patterns["anomaly_scores"].append(log.anomaly_score)
    
    return patterns 