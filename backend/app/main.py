from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .core.database import get_db
from .core.init_db import init_db
from .api.api import api_router
from .core.config import settings

app = FastAPI(
    title="Secure Access Insights Platform",
    description="API for monitoring and analyzing secure access patterns",
    version="1.0.0"
)

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://frontend:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    # Initialize database and create admin user
    db = next(get_db())
    init_db(db)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Secure Access Insights Platform API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    } 