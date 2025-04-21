import sys
import os
import random
import string
from datetime import datetime, timedelta
import json
from typing import List
from passlib.context import CryptContext
import logging
from sqlalchemy.orm import Session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.db.session import engine, SessionLocal
from app.models.user import User, UserRole
from app.models.access_log import AccessLog
from app.models.alert import Alert, AlertStatus, AlertSeverity
from app.core.security import get_password_hash

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def generate_random_email():
    """Generate a random email address."""
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"user_{random_string}@example.com"

def generate_sample_users(db: Session) -> list[User]:
    """Generate sample users with different roles."""
    try:
        users = []
        
        # Check if admin exists
        admin = db.query(User).filter(User.email == settings.FIRST_SUPERUSER).first()
        if not admin:
            admin = User(
                email=settings.FIRST_SUPERUSER,
                hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
                full_name="Admin User",
                role="ADMIN",
                is_active=True
            )
            db.add(admin)
            users.append(admin)
        
        # Generate additional users with random roles
        roles = ["ANALYST", "VIEWER"]
        for i in range(9):  # Generate 9 additional users
            email = generate_random_email()
            while db.query(User).filter(User.email == email).first():
                email = generate_random_email()  # Generate new email if this one exists
                
            user = User(
                email=email,
                hashed_password=get_password_hash(f"password{i+1}"),
                full_name=f"User {i+1}",
                role=random.choice(roles),
                is_active=True
            )
            db.add(user)
            users.append(user)
        
        db.commit()
        logger.info(f"Generated {len(users)} users")
        return users
    except Exception as e:
        logger.error(f"Error generating sample users: {e}")
        db.rollback()
        raise

def generate_sample_access_logs(db: Session, users: list[User]) -> list[AccessLog]:
    """Generate sample access logs."""
    try:
        access_logs = []
        resource_types = ["file", "database", "api", "network", "system"]
        actions = ["read", "write", "delete", "execute", "modify"]
        locations = ["US-EAST", "US-WEST", "EU-CENTRAL", "ASIA-PACIFIC"]
        
        # Generate logs for the past 30 days
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=30)
        
        for _ in range(100):  # Generate 100 access logs
            user = random.choice(users)
            timestamp = start_time + timedelta(
                seconds=random.randint(0, int((end_time - start_time).total_seconds()))
            )
            
            log = AccessLog(
                user_id=user.id,
                timestamp=timestamp,
                resource_type=random.choice(resource_types),
                resource_name=f"resource_{random.randint(1, 20)}",
                action=random.choice(actions),
                location=random.choice(locations),
                success=random.choice([True, True, True, False]),  # Bias towards successful access
                ip_address=f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
                user_agent=f"Mozilla/5.0 (Platform {random.randint(1, 5)})",
                anomaly_score=random.uniform(0, 1),
                access_metadata={
                    "session_id": f"sess_{random.randint(1000, 9999)}",
                    "device_type": random.choice(["desktop", "mobile", "tablet"]),
                    "browser": random.choice(["Chrome", "Firefox", "Safari"])
                }
            )
            db.add(log)
            access_logs.append(log)
        
        db.commit()
        logger.info(f"Generated {len(access_logs)} access logs")
        return access_logs
    except Exception as e:
        logger.error(f"Error generating access logs: {e}")
        db.rollback()
        raise

def generate_sample_alerts(db: Session, access_logs: list[AccessLog]) -> list[Alert]:
    """Generate sample alerts based on access logs."""
    try:
        alerts = []
        analysts = [user for user in db.query(User).all() if user.role == "ANALYST"]
        
        # Generate alerts for suspicious access patterns
        for log in access_logs:
            # Generate alerts for failed access attempts
            if not log.success:
                alert = Alert(
                    alert_type="Failed Access",
                    severity="HIGH",
                    status="NEW",
                    description=f"Failed access attempt detected from {log.location} with IP {log.ip_address}",
                    source_log_id=log.id,
                    assigned_to_id=random.choice(analysts).id if analysts else None,
                    alert_metadata={
                        "anomaly_score": log.anomaly_score,
                        "resource_type": log.resource_type,
                        "action": log.action
                    }
                )
                db.add(alert)
                alerts.append(alert)
            
            # Generate alerts for high anomaly scores
            elif log.anomaly_score > 0.8:
                alert = Alert(
                    alert_type="Anomalous Behavior",
                    severity="MEDIUM",
                    status="NEW",
                    description=f"High anomaly score detected for access from {log.location}",
                    source_log_id=log.id,
                    assigned_to_id=random.choice(analysts).id if analysts else None,
                    alert_metadata={
                        "anomaly_score": log.anomaly_score,
                        "resource_type": log.resource_type,
                        "action": log.action
                    }
                )
                db.add(alert)
                alerts.append(alert)
            
            # Generate alerts for sensitive resource access
            elif log.resource_type in ["database", "system"] and log.action in ["write", "delete"]:
                alert = Alert(
                    alert_type="Sensitive Resource Access",
                    severity="LOW",
                    status="NEW",
                    description=f"Sensitive {log.resource_type} {log.action} operation detected from {log.location}",
                    source_log_id=log.id,
                    assigned_to_id=random.choice(analysts).id if analysts else None,
                    alert_metadata={
                        "anomaly_score": log.anomaly_score,
                        "resource_type": log.resource_type,
                        "action": log.action
                    }
                )
                db.add(alert)
                alerts.append(alert)
        
        db.commit()
        logger.info(f"Generated {len(alerts)} alerts")
        return alerts
    except Exception as e:
        logger.error(f"Error generating alerts: {e}")
        db.rollback()
        raise

def main():
    """Main function to generate all sample data."""
    logger.info("Starting sample data generation...")
    db = SessionLocal()
    try:
        users = generate_sample_users(db)
        access_logs = generate_sample_access_logs(db, users)
        alerts = generate_sample_alerts(db, access_logs)
        logger.info("Sample data generation completed successfully")
    except Exception as e:
        logger.error(f"Error generating sample data: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main() 