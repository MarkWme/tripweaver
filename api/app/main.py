from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
from .models import PlanRequest, PlanResponse
from .planner import Planner
from .disk_monitor import disk_monitor

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
    """Enhanced health check including disk monitoring for CVE-2025-6297 mitigation."""
    basic_health = {"status": "ok"}
    
    try:
        # Include disk health status
        disk_health = disk_monitor.get_health_status()
        basic_health.update({
            "disk_health": disk_health,
            "security_monitoring": {
                "cve_mitigation": "CVE-2025-6297",
                "monitoring_active": True
            }
        })
    except Exception as e:
        basic_health["disk_health_error"] = str(e)
    
    return basic_health

@app.get("/security/disk-status")
def get_disk_status():
    """Get detailed disk usage statistics for security monitoring."""
    try:
        return disk_monitor.get_health_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get disk status: {str(e)}")

@app.get("/security/temp-dirs")
def get_temp_directory_status():
    """Get temporary directory statistics to detect potential dpkg attacks."""
    try:
        return {
            "temp_directories": disk_monitor.check_temp_directories(),
            "cve_mitigation": "CVE-2025-6297"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to check temp directories: {str(e)}")

@app.post("/security/cleanup")
def cleanup_temp_files(max_age_hours: int = 24, dry_run: bool = True):
    """Clean up old temporary files (requires admin access in production)."""
    try:
        result = disk_monitor.cleanup_temp_files(max_age_hours=max_age_hours, dry_run=dry_run)
        return {
            "cleanup_result": result,
            "cve_mitigation": "CVE-2025-6297"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cleanup failed: {str(e)}")

