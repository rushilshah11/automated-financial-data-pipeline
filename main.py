"""
Top-level ASGI application for the project.

This module exposes a FastAPI instance named `app` which tests and
deployment targets import. The application uses an async lifespan
context to initialize database tables before serving requests.

Routes:
 - /auth/* are mounted from `app.routers.auth`
 - /protected demonstrates a route protected by auth dependency

Keep side-effects (like DB creation) inside the lifespan so test imports
don't run expensive or blocking actions at import time.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware 
from app.util.init_db import create_tables  # async create_tables called by lifespan
from fastapi.security import HTTPBearer
from app.routers.auth import auth_router
from app.routers.subscription import subscription_router
from app.util.protect_route import get_current_user
from app.db.schemas.user_schema import UserOutput
from app.core.logging_config import configure_logging
import logging
from time import time

# Configure logging as early as possible so import-time logs are captured
configure_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run once on startup and once on shutdown.

    We use this to create DB tables asynchronously before the app starts.
    Tests that import `app` will not trigger table creation until the
    TestClient enters the lifespan context.
    """
    # create tables (uses SQLAlchemy metadata.create_all under the hood)
    await create_tables()
    yield
    # (optional) add graceful shutdown logic here


# The FastAPI instance must be named `app` so tests and uvicorn can import it.
app = FastAPI(
    lifespan=lifespan,
    version="1.0",
    swagger_ui_oauth2_redirect_url=None,
)


# Simple request logging middleware – logs method, path, status and duration.
@app.middleware("http")
async def log_requests(request, call_next):
    start = time()
    logger.info("Incoming request: %s %s", request.method, request.url.path)
    response = await call_next(request)
    duration_ms = int((time() - start) * 1000)
    logger.info("Completed %s %s -> %s (%sms)", request.method, request.url.path, response.status_code, duration_ms)
    return response

# --- NEW CORS CONFIGURATION ---
# Allow all origins (for development/Render deployment flexibility).
# Replace "*" with your actual frontend domain once you have it.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://rushils-finance-dispatch.onrender.com"], # Allows requests from all origins
    allow_credentials=True,
    allow_methods=["*"], # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"], # Allows all headers (including Authorization)
)
# --- END CORS CONFIGURATION ---

security = HTTPBearer()

# Mount the auth router under /auth (register, login)
app.include_router(router=auth_router, tags=["auth"], prefix="/auth")
app.include_router(router=subscription_router, tags=["subscriptions"], prefix="/subscriptions")

@app.get("/")
async def root():
    return {"message": "Welcome to the Automated Financial Data Pipeline API. Access docs at /docs."}

@app.get("/health")
async def health_check():
    """Simple healthcheck used during development.

    Returns a tiny JSON payload so orchestration layers can probe liveness.
    """
    return {"status": "running..."}


@app.get("/protected")
async def read_protected(current_user: UserOutput = Depends(get_current_user)):
    """Example protected route that requires a valid JWT.

    The `get_current_user` dependency decodes the Authorization header and
    returns a `UserOutput`. The route simply returns that value under
    the "data" key for demonstration.
    """
    return {"data": current_user}