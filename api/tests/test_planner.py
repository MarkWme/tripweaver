from app.planner import Planner


def sample_index():
    return {
        "destinations": [
            {"city":"Valencia","country":"Spain","avg_temp_c_feb":"17","has_beach":"yes","has_old_town":"yes","flight_hours_from_LON":"1.9"},
            {"city":"Marrakesh","country":"Morocco","avg_temp_c_feb":"20","has_beach":"no","has_old_town":"yes","flight_hours_from_LON":"3.5"},
            {"city":"Nice","country":"France","avg_temp_c_feb":"12","has_beach":"yes","has_old_town":"yes","flight_hours_from_LON":"2.1"},
        ]
    }


def test_plan_happy_path():
    p = Planner(sample_index())
    q = {"origin":"LON","when":"next week","prefs":["warm","beach","old town"],"max_flight_hours":2}
    res = p.plan(q)
    assert "candidates" in res
    assert len(res["candidates"]) >= 1
    assert res["candidates"][0]["city"] == "Valencia"
