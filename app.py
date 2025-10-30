from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

app = FastAPI(title="Vitals REST API")

# Path to your JSON file
VITALS_FILE = "vitals.json"

# Define a data model
class Vitals(BaseModel):
    Temperature: str | None = None
    PulseRate: str | None = None
    RespirationRate: str | None = None
    OxygenSaturation: str | None = None
    PerfusionIndex: str | None = None


# ------------------ ROUTES ------------------

@app.get("/")
def home():
    return {"message": "Welcome to the Vitals REST API!"}


@app.get("/vitals")
def get_vitals():
    """Return the stored vitals.json data"""
    if not os.path.exists(VITALS_FILE):
        raise HTTPException(status_code=404, detail="Vitals file not found")
    with open(VITALS_FILE, "r") as f:
        data = json.load(f)
    return data


@app.post("/vitals")
def post_vitals(vitals: Vitals):
    """Upload new vitals data"""
    data = vitals.dict(exclude_none=True)
    with open(VITALS_FILE, "w") as f:
        json.dump(data, f, indent=4)
    return {"status": "success", "message": "Vitals saved successfully!"}
