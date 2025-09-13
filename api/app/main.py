from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
from .models import PlanRequest, PlanResponse
from .planner import Planner

app = FastAPI(title="TripWeaver API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

INDEX_PATH = os.environ.get("INDEX_PATH") or "/app/data/index.json"

@app.on_event("startup")
def load_index():
    global planner
    try:
        with open(INDEX_PATH, "r") as f:
            index = json.load(f)
    except Exception as e:
        print("Failed to load index.json:", e)
        index = {"destinations": []}
    planner = Planner(index)

@app.post("/itinerary/plan", response_model=PlanResponse)
def plan(request: PlanRequest):
    q = request.dict()
    res = planner.plan(q)
    return res

@app.get("/healthz")
def health():
    return {"status": "ok"}

