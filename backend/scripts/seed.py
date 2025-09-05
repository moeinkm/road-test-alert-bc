import logging
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.db.session import SessionLocal
from app.models import User

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run():
    logger.info("🌱 Starting database seeding...")
    
    try:
        with SessionLocal() as db:
            # Check if data already exists
            existing_user = db.scalar(select(User.id).limit(1))
            
            if existing_user:
                logger.info("✅ Seed data already exists, skipping.")
                return
            
            # Create initial user
            admin_user = User(
                email="admin@example.com", 
                hashed_password="dummy_password_for_testing",  # This should be properly hashed in production
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            
            logger.info("✅ Successfully inserted initial admin user")
            
    except SQLAlchemyError as e:
        logger.error(f"❌ Database error during seeding: {e}")
        raise
    except Exception as e:
        logger.error(f"❌ Unexpected error during seeding: {e}")
        raise

if __name__ == "__main__":
    run()
