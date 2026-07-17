import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from models import Base
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.database_url = os.environ.get('DATABASE_URL')
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable is required")
        
        # Create engine with connection pooling
        self.engine = create_engine(
            self.database_url,
            pool_pre_ping=True,
            pool_recycle=300,
            echo=False  # Set to True for SQL debugging
        )
        
        # Create session factory
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # Create tables
        self.create_tables()
    
    def create_tables(self):
        """Create all database tables"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except SQLAlchemyError as e:
            logger.error(f"Error creating database tables: {e}")
            raise
    
    def get_session(self):
        """Get database session with context manager support"""
        return self.SessionLocal()
    
    def health_check(self):
        """Check database connectivity"""
        try:
            with self.get_session() as session:
                from sqlalchemy import text
                session.execute(text("SELECT 1"))
                return True
        except SQLAlchemyError as e:
            logger.error(f"Database health check failed: {e}")
            return False
    
    def close(self):
        """Close database connections"""
        self.engine.dispose()

# Global database manager instance
db_manager = DatabaseManager()

def get_db():
    """Dependency to get database session"""
    session = db_manager.get_session()
    try:
        yield session
    finally:
        session.close()