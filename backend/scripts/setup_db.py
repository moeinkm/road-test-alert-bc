#!/usr/bin/env python3
"""
Database setup script that creates the database and user if they don't exist.
This script reads from environment variables and sets up the database for local development.
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

def create_database_and_user():
    """Create database and user if they don't exist."""
    
    # Parse database URL to get components
    db_url = settings.DATABASE_URL
    logger.info(f"Setting up database from URL: {db_url}")
    
    # Extract database name from URL
    db_name = settings.DATABASE_NAME
    db_user = settings.DATABASE_USER
    db_password = settings.DATABASE_PASSWORD
    
    logger.info(f"Database: {db_name}")
    logger.info(f"User: {db_user}")
    
    # Connect to default postgres database to create our database
    # Remove the database name from the URL to connect to default 'postgres' database
    default_db_url = db_url.replace(f"/{db_name}", "/postgres")
    
    try:
        # Connect to default postgres database with autocommit for database creation
        engine = create_engine(default_db_url)
        
        # First, check user and database existence
        with engine.connect() as conn:
            # Check if user exists
            logger.info("Checking if user exists...")
            result = conn.execute(text("SELECT 1 FROM pg_roles WHERE rolname = :user"), {"user": db_user})
            user_exists = result.fetchone() is not None
            
            if not user_exists:
                logger.info(f"Creating user '{db_user}'...")
                conn.execute(text(f"CREATE USER {db_user} WITH PASSWORD '{db_password}'"))
                conn.execute(text(f"ALTER USER {db_user} CREATEDB"))
                logger.info(f"✅ User '{db_user}' created successfully")
            else:
                logger.info(f"✅ User '{db_user}' already exists")
            
            # Check if database exists
            logger.info("Checking if database exists...")
            result = conn.execute(text("SELECT 1 FROM pg_database WHERE datname = :db"), {"db": db_name})
            db_exists = result.fetchone() is not None
            
            if not db_exists:
                logger.info(f"Creating database '{db_name}'...")
                # Use autocommit connection for database creation
                with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as autocommit_conn:
                    autocommit_conn.execute(text(f"CREATE DATABASE {db_name} OWNER {db_user}"))
                logger.info(f"✅ Database '{db_name}' created successfully")
            else:
                logger.info(f"✅ Database '{db_name}' already exists")
            
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
    
    # Test connection to the new database
    try:
        logger.info("Testing connection to the new database...")
        test_engine = create_engine(db_url)
        with test_engine.connect() as conn:
            result = conn.execute(text("SELECT current_database(), current_user"))
            db, user = result.fetchone()
            logger.info(f"✅ Successfully connected to database '{db}' as user '{user}'")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to connect to new database: {e}")
        return False

def main():
    """Main function to set up the database."""
    logger.info("🚀 Starting database setup...")
    
    success = create_database_and_user()
    
    if success:
        logger.info("🎉 Database setup completed successfully!")
        logger.info("💡 You can now run migrations and seed the database")
    else:
        logger.error("❌ Database setup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
