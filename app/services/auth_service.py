"""Authentication service: register, login, JWT token management."""

from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext
from app.config import settings
from app.database.connection import get_db_connection

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plain-text password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: int, username: str) -> str:
    """Create a JWT access token."""
    payload = {
        "sub": str(user_id),
        "username": username,
        "exp": datetime.now(timezone.utc)
        + timedelta(hours=settings.JWT_EXPIRATION_HOURS),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    """Decode and verify a JWT token. Returns payload or None if invalid."""
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.PyJWTError:
        return None


def register_user(username: str, email: str, password: str) -> dict:
    """Register a new user. Returns user info or error."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            # Check if username or email already exists
            cur.execute(
                "SELECT id FROM users WHERE username = %s OR email = %s",
                (username, email),
            )
            if cur.fetchone():
                return {"success": False, "error": "Username or email already exists"}

            password_hash = hash_password(password)
            cur.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s) RETURNING id, username, email, created_at",
                (username, email, password_hash),
            )
            user = dict(cur.fetchone())
            conn.commit()
            return {"success": True, "user": user}
    finally:
        conn.close()


def authenticate_user(username: str, password: str) -> dict:
    """Authenticate a user. Returns token + user info or error."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, username, email, password_hash FROM users WHERE username = %s",
                (username,),
            )
            row = cur.fetchone()
            if not row:
                return {"success": False, "error": "Invalid username or password"}

            if not verify_password(password, row["password_hash"]):
                return {"success": False, "error": "Invalid username or password"}

            token = create_access_token(row["id"], row["username"])
            return {
                "success": True,
                "token": token,
                "user": {
                    "id": row["id"],
                    "username": row["username"],
                    "email": row["email"],
                },
            }
    finally:
        conn.close()


def get_current_user(token: str) -> dict | None:
    """Extract and validate current user from a Bearer token."""
    payload = decode_access_token(token)
    if payload is None:
        return None
    return {"user_id": int(payload["sub"]), "username": payload["username"]}





def hash_password(password: str) -> str:
    """Hash a plain-text password."""
    print(f"DEBUG: password length = {len(password)}, value = {password}")
    return pwd_context.hash(password)


