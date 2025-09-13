from pydantic import BaseModel
from typing import List, Optional, Any

class PlanRequest(BaseModel):
    origin: str
    when: str
    prefs: List[str]
    max_flight_hours: float

class ItineraryDay(BaseModel):
    day: int
    summary: str

class Candidate(BaseModel):
    city: str
    country: str
    score: float
    why: List[str]
    itinerary: List[ItineraryDay]

class PlanResponse(BaseModel):
    query: Any
    candidates: List[Candidate]
    generated_at: str

