from fastapi import FastAPI

from app.routers import router

app = FastAPI(
    title="Hospital Appointment Management API",
    version="1.0.0",
    description=("API for managing patients, doctors, " "and hospital appointments."),
)

app.include_router(
    router,
    tags=["Hospital API"],
)
