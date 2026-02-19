import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import settings
from database import engine, Base
from middleware import RequestLoggingMiddleware
from routers import users, todos, students, logs, dashboard

# Ensure all models are registered before create_all
import models  # noqa: F401

Base.metadata.create_all(bind=engine)

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting")
    yield
    logger.info("Application shutting down")


app = FastAPI(
    title=settings.APP_NAME,
    description="Professional backend for school management.",
    version="1.0",
    lifespan=lifespan,
)

# CORS
origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Auto-log every request to logs table
app.add_middleware(RequestLoggingMiddleware)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


app.include_router(users.router)
app.include_router(todos.router)
app.include_router(students.router)
app.include_router(logs.router)
app.include_router(dashboard.router)


@app.get("/")
def home():
    return {"msg": "API is running", "docs": "/docs"}


@app.get("/health")
def health():
    """Health check for load balancers and monitoring."""
    return {"status": "ok"}
