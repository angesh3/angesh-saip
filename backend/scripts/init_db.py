import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User, UserRole

def init_db() -> None:
    try:
        # Drop all tables first to ensure a clean slate
        Base.metadata.drop_all(bind=engine)
        print("Dropped all existing tables.")
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        print("Created all database tables successfully.")
        
        db = SessionLocal()
        try:
            # Create superuser
            superuser = User(
                email=settings.FIRST_SUPERUSER,
                hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
                full_name=settings.FIRST_SUPERUSER_FULLNAME,
                role=UserRole.ADMIN,
                is_active=True
            )
            db.add(superuser)
            db.commit()
            print(f"Created superuser: {settings.FIRST_SUPERUSER}")
            
        except Exception as e:
            db.rollback()
            print(f"Error creating superuser: {str(e)}")
            raise
        finally:
            db.close()
            
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        raise

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialization completed.") 