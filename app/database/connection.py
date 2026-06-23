"""Database connection management using psycopg2."""

import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from app.config import settings


def get_db_connection():
    """Create and return a new database connection."""
    conn = psycopg2.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        dbname=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        cursor_factory=RealDictCursor,
    )
    return conn


def init_db():
    """Initialize the database by creating all required tables."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            # Create the database if it doesn't exist
            cur.execute(
                sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"),
                [settings.DB_NAME],
            )
            if cur.fetchone() is None:
                # Cannot create DB within a transaction block
                conn.autocommit = True
                cur.execute(
                    sql.SQL("CREATE DATABASE {}").format(
                        sql.Identifier(settings.DB_NAME)
                    )
                )
                conn.autocommit = False

        # Create tables
        from app.database.models import create_tables

        create_tables(conn)
    finally:
        conn.close()
