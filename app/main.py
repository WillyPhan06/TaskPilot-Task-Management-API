from fastapi import FastAPI
from app.routers import tasks
from app.routers import users
from app.core.config import settings
from contextlib import asynccontextmanager
from app.db.session import engine
from app.models.base import Base
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Database tables created (if not already).")

    # Yield control to the app (this is when the API runs)
    yield

    # Shutdown actions (optional)
    await engine.dispose()
    print("🛑 Database connection closed.")


# Create FastAPI instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    lifespan=lifespan
)

# Routers
app.include_router(tasks.router)
app.include_router(users.router)

origins = [
    "http://localhost:3000",  # your frontend
    "https://myfrontend.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           # restrict to these domains
    allow_credentials=True,
    allow_methods=["*"],             # GET, POST, etc.
    allow_headers=["*"],             # Authorization headers, etc.
)

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response: Response = await call_next(request)
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Permissions-Policy"] = "geolocation=(), camera=()"
        return response

app.add_middleware(SecurityHeadersMiddleware)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"detail": "Too many requests"})

@app.get("/tasks")
@limiter.limit("5/minute")  # max 5 requests per minute per IP
async def get_tasks(request: Request):
    return [{"task": "Test task"}]

# Root route
@app.get("/")
def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} API! Greetings from {settings.AUTHOR}!"}

# Health check route
@app.get("/health")
def health_check():
    return {"status": "ok"}
