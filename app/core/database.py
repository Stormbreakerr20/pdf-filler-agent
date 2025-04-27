import os
import psycopg2
from psycopg2 import pool
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

# Connection parameters
DB_CONFIG = {
    "host": os.getenv("AZURE_PG_HOST"),
    "port": os.getenv("AZURE_PG_PORT"),
    "database": os.getenv("AZURE_PG_DATABASE"),
    "user": os.getenv("AZURE_PG_USER"),
    "password": os.getenv("AZURE_PG_PASSWORD"),
    "sslmode": os.getenv("AZURE_PG_SSLMODE", "require")
}

# Create a connection pool - Azure recommends min=1, max=10 for most apps
connection_pool = None

def init_pool(minconn=1, maxconn=10):
    """Initialize the connection pool"""
    global connection_pool
    if connection_pool is None:
        try:
            connection_pool = pool.ThreadedConnectionPool(minconn, maxconn, **DB_CONFIG)
            logger.info(f"PostgreSQL connection pool initialized with {minconn}-{maxconn} connections")
        except Exception as e:
            logger.error(f"Failed to create connection pool: {e}")
            raise

def get_connection():
    """Get a connection from the pool"""
    global connection_pool
    if connection_pool is None:
        init_pool()
    return connection_pool.getconn()

def release_connection(conn):
    """Return a connection to the pool"""
    global connection_pool
    if connection_pool is not None:
        connection_pool.putconn(conn)

def test_connection():
    """Test database connectivity"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT 1')
        cursor.close()
        return True
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False
    finally:
        if conn:
            release_connection(conn)

def create_tables():
    """Create necessary tables if they don't exist"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Create tables with indexes for better performance
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_sessions (
            id SERIAL PRIMARY KEY,
            user_id TEXT NOT NULL,
            document_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_user_sessions_user_id ON user_sessions(user_id)
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            session_id INTEGER REFERENCES user_sessions(id) ON DELETE CASCADE,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_messages_session_id ON messages(session_id)
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS form_data (
            id SERIAL PRIMARY KEY,
            session_id INTEGER REFERENCES user_sessions(id) ON DELETE CASCADE UNIQUE,
            data JSONB NOT NULL
        )
        """)
        
        conn.commit()
        logger.info("Database tables created or verified successfully")
        
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            release_connection(conn)