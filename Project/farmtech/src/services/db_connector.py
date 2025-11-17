# src/services/db_connector.py
import sqlite3
import logging
import threading
import os # <-- NEW
import psycopg2 # <-- NEW
from typing import Optional, Any, List, Dict
from urllib.parse import urlparse # <-- NEW

# --- NEW: Cloud Database Logic ---
# Render (and other hosts) provides the DB connection string in an env variable
DATABASE_URL = os.environ.get('DATABASE_URL')
IS_PRODUCTION = DATABASE_URL is not None

# Fallback to local file if not in production
DB_NAME = "local_farm_data.db"

db_local = threading.local()

class DBConnector:
    @staticmethod
    def get_db() -> Any:
        """
        Gets the database connection for the current thread.
        Uses PostgreSQL in production, SQLite locally.
        """
        conn = getattr(db_local, 'connection', None)
        if conn is None:
            try:
                if IS_PRODUCTION:
                    # --- PRODUCTION: Connect to PostgreSQL ---
                    conn = db_local.connection = psycopg2.connect(DATABASE_URL)
                    logging.info("DBConnector: Connected to production PostgreSQL.")
                else:
                    # --- LOCAL: Connect to SQLite ---
                    conn = db_local.connection = sqlite3.connect(DB_NAME, check_same_thread=False)
                    conn.row_factory = sqlite3.Row
                    logging.info("DBConnector: Connected to local SQLite.")
            except Exception as e:
                logging.error(f"Database connection error: {e}")
                raise e
        return conn

    @staticmethod
    def execute_query(query: str, params: tuple = (), one: bool = False) -> Optional[Any]:
        """
        Executes a SELECT query.
        Returns dict (if one=True) or list of dicts (if one=False).
        """
        try:
            conn = DBConnector.get_db()
            cursor = conn.cursor()
            
            if IS_PRODUCTION:
                # PostgreSQL uses %s placeholders
                query = query.replace("?", "%s")
                
            cursor.execute(query, params)
            
            if IS_PRODUCTION:
                # --- NEW: PostgreSQL cursor needs column names ---
                columns = [col[0] for col in cursor.description]
                if one:
                    row = cursor.fetchone()
                    return dict(zip(columns, row)) if row else None
                else:
                    rows = cursor.fetchall()
                    return [dict(zip(columns, row)) for row in rows]
            else:
                # --- SQLite (old logic) ---
                if one:
                    row = cursor.fetchone()
                    return dict(row) if row else None
                else:
                    rows = cursor.fetchall()
                    return [dict(row) for row in rows]
            
        except Exception as e:
            logging.error(f"Error executing query: {e}")
            return None if one else []

    @staticmethod
    def execute_commit(query: str, params: tuple = ()) -> bool:
        """Executes an INSERT/UPDATE/DELETE query and commits."""
        try:
            conn = DBConnector.get_db()
            cursor = conn.cursor()
            
            if IS_PRODUCTION:
                # PostgreSQL uses %s placeholders
                query = query.replace("?", "%s")

            cursor.execute(query, params)
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            logging.error(f"Error executing commit: {e}")
            conn.rollback() # Rollback on failure
            return False

    @staticmethod
    def close_db(e=None):
        conn = getattr(db_local, 'connection', None)
        if conn is not None:
            conn.close()
            db_local.connection = None