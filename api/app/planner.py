import json
from typing import List, Dict, Any
from datetime import datetime

DataIndex = Dict[str, Any]

class Planner:
    def __init__(self, index: DataIndex):
        self.index = index
        self.destinations = index.get("destinations", [])

    def plan(self, query: Dict[str, Any]) -> Dict[str, Any]:
        prefs = set([p.lower() for p in query.get("prefs", [])])
        max_hours = float(query.get("max_flight_hours", 24))

        candidates = []
        for d in self.destinations:
            try:
                hours = float(d.get("flight_hours_from_LON") or 999)
            except Exception:
                hours = 999
            if hours > max_hours:
                continue
            score = 0.0
            why = []
            # temp preference
            avg_temp = None
            try:
                avg_temp = float(d.get("avg_temp_c_feb") or 0)
            except Exception:
                avg_temp = 0
            if "warm" in prefs and avg_temp >= 14:
                score += 0.3
                why.append(f"avg_temp ~{avg_temp}C")
            if "beach" in prefs and str(d.get("has_beach","no")).lower().startswith("y"):
                score += 0.3
                why.append("beach=yes")
            if "old town" in prefs and str(d.get("has_old_town","no")).lower().startswith("y"):
                score += 0.2
                why.append("old_town=yes")
            # shorter flights get small boost
            score += max(0, (max_hours - hours) / max_hours) * 0.2
            why.append(f"{hours}h flight")

            if score <= 0:
                continue

            # create simple 3-day itinerary deterministic based on city name hash
            city = d.get("city")
            summary_base = str(city)
            itinerary = [
                {"day": 1, "summary": f"Arrive, {summary_base} old town walk"},
                {"day": 2, "summary": f"Beach or waterfront & local market"},
                {"day": 3, "summary": f"Day trip or museum in {summary_base}"},
            ]

            candidates.append({
                "city": d.get("city"),
                "country": d.get("country"),
                "score": round(score, 2),
                "why": why,
                "itinerary": itinerary,
            })

        # sort by score desc, then city
        candidates = sorted(candidates, key=lambda x: (-x["score"], x["city"]))[:3]

        return {
            "query": query,
            "candidates": candidates,
            "generated_at": datetime.utcnow().isoformat() + "Z",
        }
