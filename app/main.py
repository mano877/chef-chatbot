"""FastAPI application entry point for the Chef Chatbot API."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.connection import init_db
from app.routers import auth, chat, users, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: initialize database on startup."""
    try:
        init_db()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"⚠️ Database initialization error: {e}")
        print("⚠️ The API will start, but database features may not work.")
    yield


app = FastAPI(
    title="Chef Chatbot API",
    description="AI Chef Assistant powered by LangChain + Ollama — Chef Zoya 🧑‍🍳",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware — allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(users.router)
