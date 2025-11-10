from fastapi import FastAPI
from app.routers import tasks
from app.routers import users
from app.core.config import settings
from contextlib import asynccontextmanager
from app.db.session import engine
from app.models.base import Base

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

# Root route
@app.get("/")
def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} API! Greetings from {settings.AUTHOR}!"}

# Health check route
@app.get("/health")
def health_check():
    return {"status": "ok"}
