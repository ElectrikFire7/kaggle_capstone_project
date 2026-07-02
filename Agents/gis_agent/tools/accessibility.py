"""
File: Agents/gis_agent/tools/accessibility.py
Purpose: Scores the accessibility of a location based on road network data.
         Evaluates proximity to main roads, number of connecting roads, road quality,
         and nearby public transport stops to produce a 0–100 accessibility score.
"""


def score_accessibility(road_data: dict) -> dict:
    """
    Calculates an accessibility score (0–100) for a location based on its road network.

    Evaluates four factors:
    - Proximity to the nearest main road (0–30 points)
    - Number of connecting roads within the search area (0–20 points)
    - Quality of the best road type nearby (0–25 points)
    - Road network density and variety (0–25 points)

    Args:
        road_data: Output from the get_nearby_roads tool, containing:
            - roads: List of nearby roads with type and distance
            - main_road_count: Number of main roads found
            - nearest_main_road: Details of the closest main road
            - distance_to_nearest_main_road: Distance in meters
            - road_type_summary: Count of roads by type

    Returns:
        A dictionary containing:
            - accessibility_score: Overall score from 0 to 100
            - rating: "Excellent" / "Good" / "Fair" / "Poor"
            - factors: Breakdown of scoring by category
            - analysis: Human-readable analysis of accessibility
    """
    if "error" in road_data:
        return {
            "accessibility_score": 0,
            "rating": "Unknown",
            "factors": {},
            "analysis": f"Could not assess accessibility: {road_data['error']}",
        }

    factors = {}
    total_score = 0

    # ---- Factor 1: Proximity to nearest main road (0–30 points) ----
    dist_main = road_data.get("distance_to_nearest_main_road")
    if dist_main is not None:
        if dist_main < 50:
            proximity_score = 30
            proximity_desc = f"Directly on a main road ({dist_main:.0f}m away)"
        elif dist_main < 100:
            proximity_score = 25
            proximity_desc = f"Very close to a main road ({dist_main:.0f}m)"
        elif dist_main < 200:
            proximity_score = 20
            proximity_desc = f"Near a main road ({dist_main:.0f}m)"
        elif dist_main < 350:
            proximity_score = 14
            proximity_desc = f"Moderate distance from main road ({dist_main:.0f}m)"
        elif dist_main < 500:
            proximity_score = 8
            proximity_desc = f"Far from main road ({dist_main:.0f}m)"
        else:
            proximity_score = 3
            proximity_desc = f"Very far from main roads ({dist_main:.0f}m)"
    else:
        proximity_score = 0
        proximity_desc = "No main roads found in the search area"

    factors["proximity_to_main_road"] = {
        "score": proximity_score,
        "max": 30,
        "description": proximity_desc,
    }
    total_score += proximity_score

    # ---- Factor 2: Connecting roads (0–20 points) ----
    road_count = road_data.get("road_count", 0)
    if road_count >= 10:
        connecting_score = 20
        connecting_desc = f"Excellent connectivity — {road_count} roads in the area"
    elif road_count >= 6:
        connecting_score = 15
        connecting_desc = f"Good connectivity — {road_count} roads in the area"
    elif road_count >= 3:
        connecting_score = 10
        connecting_desc = f"Moderate connectivity — {road_count} roads in the area"
    elif road_count >= 1:
        connecting_score = 5
        connecting_desc = f"Limited connectivity — only {road_count} road(s) in the area"
    else:
        connecting_score = 0
        connecting_desc = "No roads found nearby"

    factors["connecting_roads"] = {
        "score": connecting_score,
        "max": 20,
        "description": connecting_desc,
    }
    total_score += connecting_score

    # ---- Factor 3: Road type quality (0–25 points) ----
    nearest_main = road_data.get("nearest_main_road")
    if nearest_main:
        road_type = nearest_main.get("road_type", "")
        if road_type in ("motorway", "trunk"):
            quality_score = 25
            quality_desc = f"Major arterial road ({road_type}) nearby"
        elif road_type == "primary":
            quality_score = 22
            quality_desc = "Primary road nearby — high traffic capacity"
        elif road_type == "secondary":
            quality_score = 17
            quality_desc = "Secondary road nearby — good traffic flow"
        elif road_type == "tertiary":
            quality_score = 12
            quality_desc = "Tertiary road nearby — local through-traffic"
        else:
            quality_score = 5
            quality_desc = f"Only minor roads ({road_type}) nearby"
    else:
        # Check if any roads at all
        roads = road_data.get("roads", [])
        if roads:
            quality_score = 3
            quality_desc = "Only residential/service roads nearby"
        else:
            quality_score = 0
            quality_desc = "No classified roads found"

    factors["road_type_quality"] = {
        "score": quality_score,
        "max": 25,
        "description": quality_desc,
    }
    total_score += quality_score

    # ---- Factor 4: Road network density and variety (0–25 points) ----
    type_summary = road_data.get("road_type_summary", {})
    unique_types = len(type_summary)
    main_road_count = road_data.get("main_road_count", 0)

    density_score = 0
    # Points for variety of road types (0–10)
    density_score += min(unique_types * 2, 10)
    # Points for number of main roads (0–15)
    density_score += min(main_road_count * 3, 15)

    if density_score >= 20:
        density_desc = f"Rich road network — {unique_types} road types, {main_road_count} main roads"
    elif density_score >= 12:
        density_desc = f"Moderate road network — {unique_types} road types, {main_road_count} main roads"
    else:
        density_desc = f"Sparse road network — {unique_types} road types, {main_road_count} main roads"

    factors["network_density"] = {
        "score": density_score,
        "max": 25,
        "description": density_desc,
    }
    total_score += density_score

    # ---- Overall rating ----
    if total_score >= 80:
        rating = "Excellent"
    elif total_score >= 60:
        rating = "Good"
    elif total_score >= 40:
        rating = "Fair"
    else:
        rating = "Poor"

    # Build analysis text
    analysis = f"Accessibility is {rating.lower()} (score: {total_score}/100). "
    if nearest_main:
        analysis += f"The nearest main road is '{nearest_main.get('name', 'Unnamed')}' "
        analysis += f"({nearest_main.get('road_type', '')}) at {dist_main:.0f}m. "
    analysis += f"There are {road_count} roads within the search area "
    analysis += f"including {main_road_count} main road(s)."

    return {
        "accessibility_score": total_score,
        "rating": rating,
        "factors": factors,
        "analysis": analysis,
    }
