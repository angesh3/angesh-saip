from sqlalchemy.orm import Session
from ..models import User, UserRole
from .database import engine, Base
from .security import get_password_hash

def init_db(db: Session) -> None:
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Check if admin user exists
    admin = db.query(User).filter(User.email == "admin@example.com").first()
    if not admin:
        admin_user = User(
            email="admin@example.com",
            hashed_password=get_password_hash("password"),  # Change this in production
            full_name="System Administrator",
            role=UserRole.ADMIN,
            is_active=True
        )
        db.add(admin_user)
        db.commit() 