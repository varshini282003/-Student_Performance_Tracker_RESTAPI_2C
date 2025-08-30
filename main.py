from fastapi import FastAPI
from database.session import Base, engine
from routers import students

app = FastAPI(title="Student Performance Tracker")

# Create tables on startup for SQLite (Alembic migrations can replace this later)
Base.metadata.create_all(bind=engine)

# Register router for /students paths
app.include_router(students.router, prefix="/students", tags=["students"])
