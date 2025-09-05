#!/usr/bin/env python3
"""
Test database setup script that creates the test database if it doesn't exist.
This script reads from environment variables and sets up the test database for pytest.
"""

import os
import sys
import logging

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, ProgrammingError
from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_test_database():
    """Create test database if it doesn't exist."""
    
    # Get test database URL
    test_db_url = settings.TEST_DATABASE_URL
    logger.info(f"Setting up test database from URL: {test_db_url}")
    
    # Extract database name from URL
    test_db_name = test_db_url.split('/')[-1]
    db_user = settings.DATABASE_USER
    db_password = settings.DATABASE_PASSWORD
    
    logger.info(f"Test Database: {test_db_name}")
    logger.info(f"User: {db_user}")
    
    # Connect to default postgres database to create our test database
    # Remove the database name from the URL to connect to default 'postgres' database
    default_db_url = test_db_url.replace(f"/{test_db_name}", "/postgres")
    
    try:
        # Connect to default postgres database with autocommit for database creation
        engine = create_engine(default_db_url)
        
        # Check if test database exists
        with engine.connect() as conn:
            logger.info("Checking if test database exists...")
            result = conn.execute(text("SELECT 1 FROM pg_database WHERE datname = :db"), {"db": test_db_name})
            db_exists = result.fetchone() is not None
            
            if not db_exists:
                logger.info(f"Creating test database '{test_db_name}'...")
                # Use autocommit connection for database creation
                with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as autocommit_conn:
                    autocommit_conn.execute(text(f"CREATE DATABASE {test_db_name} OWNER {db_user}"))
                logger.info(f"✅ Test database '{test_db_name}' created successfully")
            else:
                logger.info(f"✅ Test database '{test_db_name}' already exists")
            
            conn.commit()
            
    except OperationalError as e:
        logger.error(f"❌ Failed to connect to PostgreSQL: {e}")
        logger.info("💡 Make sure PostgreSQL is running:")
        logger.info("   - For local PostgreSQL: brew services start postgresql@16")
        logger.info("   - For Docker: docker compose up postgres")
        return False
    except ProgrammingError as e:
        logger.error(f"❌ Database operation failed: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return False
    
    # Test connection to the new test database
    try:
        logger.info("Testing connection to the test database...")
        test_engine = create_engine(test_db_url)
        with test_engine.connect() as conn:
            result = conn.execute(text("SELECT current_database(), current_user"))
            db, user = result.fetchone()
            logger.info(f"✅ Successfully connected to test database '{db}' as user '{user}'")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to connect to test database: {e}")
        return False

def main():
    """Main function to set up the test database."""
    logger.info("🚀 Starting test database setup...")
    
    success = create_test_database()
    
    if success:
        logger.info("🎉 Test database setup completed successfully!")
        logger.info("💡 You can now run pytest")
    else:
        logger.error("❌ Test database setup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
