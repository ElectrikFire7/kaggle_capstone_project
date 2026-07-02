"""
File: Agents/gis_agent/tools/visibility.py
Purpose: Scores the visibility of a commercial location based on road frontage,
         foot traffic potential, and proximity to landmarks. Uses Overpass API to
         detect nearby landmarks (bus stops, metro stations, malls, parks, junctions).
"""

import requests
import math

# Overpass API endpoint
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# Landmark types and their visibility weight (higher = more foot traffic / visibility)
LANDMARK_WEIGHTS = {
    # Public transport — high foot traffic generators
    "bus_stop": 8,
    "bus_station": 10,
    "station": 10,        # metro/train station
    "subway_entrance": 9,

    # Shopping / commercial — draw crowds
    "mall": 9,
    "supermarket": 7,
    "marketplace": 8,

    # Education — regular foot traffic
    "school": 6,
    "college": 7,
    "university": 8,

    # Healthcare — steady footfall
    "hospital": 7,
    "clinic": 5,

    # Leisure / social — foot traffic
    "park": 5,
    "cinema": 6,
    "place_of_worship": 5,

    # Other
    "bank": 4,
    "atm": 3,
    "fuel": 3,
    "parking": 3,
}

# Road types and their foot traffic potential scores
ROAD_FOOT_TRAFFIC = {
    "primary": 28,
    "trunk": 25,
    "secondary": 22,
    "tertiary": 16,
    "residential": 8,
    "service": 4,
    "living_street": 10,
    "pedestrian": 20,
}


def _haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates distance between two points in meters using the Haversine formula."""
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _fetch_landmarks(latitude: float, longitude: float, radius_meters: int = 500) -> list:
    """
    Queries Overpass API for landmarks (amenities, shops, public transport) near a point.

    Returns a list of landmark dicts with name, type, and distance.
    """
    query = f"""
    [out:json][timeout:25];
    (
      node(around:{radius_meters},{latitude},{longitude})["amenity"];
      node(around:{radius_meters},{latitude},{longitude})["shop"];
      node(around:{radius_meters},{latitude},{longitude})["public_transport"];
      node(around:{radius_meters},{latitude},{longitude})["railway"="station"];
      node(around:{radius_meters},{latitude},{longitude})["highway"="bus_stop"];
    );
    out body;
    """

    try:
        response = requests.post(OVERPASS_URL, data={"data": query}, timeout=30)
        response.raise_for_status()
        data = response.json()
    except Exception:
        return []

    landmarks = []
    for element in data.get("elements", []):
        if element["type"] != "node":
            continue

        tags = element.get("tags", {})
        name = tags.get("name", "Unnamed")

        # Determine the landmark type
        landmark_type = (
            tags.get("amenity")
            or tags.get("shop")
            or tags.get("public_transport")
            or tags.get("railway")
            or tags.get("highway")
            or "unknown"
        )

        distance = _haversine_distance(latitude, longitude, element["lat"], element["lon"])

        landmarks.append({
            "name": name,
            "type": landmark_type,
            "distance_meters": round(distance, 1),
            "lat": element["lat"],
            "lon": element["lon"],
        })

    # Sort by distance
    landmarks.sort(key=lambda l: l["distance_meters"])
    return landmarks


def score_visibility(latitude: float, longitude: float, road_data: dict) -> dict:
    """
    Calculates a visibility score (0–100) for a commercial location.

    Evaluates three factors:
    - Road frontage quality (0–40 points): How visible the location is from nearby roads
    - Foot traffic potential (0–30 points): Expected pedestrian/vehicle flow based on road types
    - Landmark proximity (0–30 points): Nearness to foot-traffic generators (bus stops, malls, etc.)

    Args:
        latitude: Latitude of the location.
        longitude: Longitude of the location.
        road_data: Output from the get_nearby_roads tool.

    Returns:
        A dictionary containing:
            - visibility_score: Overall score from 0 to 100
            - rating: "High" / "Medium" / "Low"
            - factors: Breakdown of scoring by category
            - nearby_landmarks: List of significant nearby landmarks
            - analysis: Human-readable visibility analysis
    """
    if "error" in road_data:
        return {
            "visibility_score": 0,
            "rating": "Unknown",
            "factors": {},
            "nearby_landmarks": [],
            "analysis": f"Could not assess visibility: {road_data['error']}",
        }

    factors = {}
    total_score = 0

    # ---- Factor 1: Road frontage quality (0–40 points) ----
    roads = road_data.get("roads", [])
    nearest_main = road_data.get("nearest_main_road")

    if nearest_main:
        dist = nearest_main["distance_meters"]
        road_type = nearest_main.get("road_type", "")

        # Base points by road type
        base = {"primary": 40, "trunk": 38, "secondary": 32, "tertiary": 24}.get(road_type, 10)

        # Distance penalty: full score if <30m, decreasing after
        if dist < 30:
            frontage_score = base
        elif dist < 100:
            frontage_score = int(base * 0.75)
        elif dist < 200:
            frontage_score = int(base * 0.50)
        elif dist < 400:
            frontage_score = int(base * 0.30)
        else:
            frontage_score = int(base * 0.15)

        frontage_desc = (
            f"{'Direct frontage on' if dist < 30 else 'Near'} "
            f"{road_type} road '{nearest_main.get('name', 'Unnamed')}' ({dist:.0f}m)"
        )
    else:
        frontage_score = 2 if roads else 0
        frontage_desc = "No main road frontage"

    frontage_score = min(frontage_score, 40)
    factors["road_frontage"] = {"score": frontage_score, "max": 40, "description": frontage_desc}
    total_score += frontage_score

    # ---- Factor 2: Foot traffic potential (0–30 points) ----
    # Based on the best road type within close range (< 100m)
    close_roads = [r for r in roads if r["distance_meters"] < 100]
    if close_roads:
        best_traffic = max(
            ROAD_FOOT_TRAFFIC.get(r["road_type"], 0) for r in close_roads
        )
        traffic_score = min(best_traffic, 30)
        traffic_desc = f"{len(close_roads)} road(s) within 100m — good vehicle/foot traffic exposure"
    else:
        nearby_roads = [r for r in roads if r["distance_meters"] < 300]
        if nearby_roads:
            best_traffic = max(
                ROAD_FOOT_TRAFFIC.get(r["road_type"], 0) for r in nearby_roads
            )
            traffic_score = min(int(best_traffic * 0.5), 30)
            traffic_desc = f"Roads within 300m but none within 100m — limited direct traffic exposure"
        else:
            traffic_score = 0
            traffic_desc = "No significant road traffic exposure"

    factors["foot_traffic"] = {"score": traffic_score, "max": 30, "description": traffic_desc}
    total_score += traffic_score

    # ---- Factor 3: Landmark proximity (0–30 points) ----
    landmarks = _fetch_landmarks(latitude, longitude, radius_meters=500)

    landmark_score = 0
    significant_landmarks = []

    for lm in landmarks[:30]:  # Cap processing
        ltype = lm["type"]
        weight = LANDMARK_WEIGHTS.get(ltype, 1)
        dist = lm["distance_meters"]

        # Distance-weighted contribution
        if dist < 100:
            contribution = weight * 1.0
        elif dist < 250:
            contribution = weight * 0.6
        elif dist < 500:
            contribution = weight * 0.3
        else:
            contribution = 0

        landmark_score += contribution

        if weight >= 5 and lm["name"] != "Unnamed":
            significant_landmarks.append({
                "name": lm["name"],
                "type": ltype,
                "distance_meters": lm["distance_meters"],
            })

    # Normalize to 0–30 range
    landmark_score = min(int(landmark_score), 30)

    if landmark_score >= 20:
        landmark_desc = f"{len(significant_landmarks)} key landmarks nearby — strong foot traffic generators"
    elif landmark_score >= 10:
        landmark_desc = f"Some landmarks nearby — moderate foot traffic potential"
    else:
        landmark_desc = "Few landmarks nearby — limited organic foot traffic"

    factors["landmark_proximity"] = {"score": landmark_score, "max": 30, "description": landmark_desc}
    total_score += landmark_score

    # ---- Overall rating ----
    total_score = min(total_score, 100)
    if total_score >= 70:
        rating = "High"
    elif total_score >= 40:
        rating = "Medium"
    else:
        rating = "Low"

    # Build analysis
    analysis = f"Visibility is {rating.lower()} (score: {total_score}/100). "
    if nearest_main:
        analysis += f"The location is {nearest_main['distance_meters']:.0f}m from "
        analysis += f"'{nearest_main.get('name', 'a main road')}' ({nearest_main.get('road_type', '')}). "
    if significant_landmarks:
        top = significant_landmarks[:3]
        names = ", ".join(f"{l['name']} ({l['distance_meters']:.0f}m)" for l in top)
        analysis += f"Key nearby landmarks: {names}."

    return {
        "visibility_score": total_score,
        "rating": rating,
        "factors": factors,
        "nearby_landmarks": significant_landmarks[:10],
        "analysis": analysis,
    }
