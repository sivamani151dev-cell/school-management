from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.database import engine, Base
from app.routers import auth, students, teachers, attendance, grades, fees
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="School Management System",
    description="A complete school management backend API",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(students.router)
app.include_router(teachers.router)
app.include_router(attendance.router)
app.include_router(grades.router)
app.include_router(fees.router)

@app.get("/")
def root():
    return RedirectResponse(url="/docs")