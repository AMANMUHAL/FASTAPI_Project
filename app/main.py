from fastapi import FastAPI , Path, HTTPException , Query
from app.routes import router as patient_router

app = FastAPI(title="Patient Management API")

app.include_router(patient_router)

@app.get("/")
def hello():
    return {"message": "Patient management API is running."}
