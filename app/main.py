from fastapi import FastAPI
from app.routers import tasks
from app.routers import users
from app.core.config import settings



# Create FastAPI instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION
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
