"""
File: Agents/gis_agent/tools/competition.py
Purpose: Detects nearby businesses of the same or similar type using the Overpass API.
         Maps business types to OpenStreetMap amenity/shop tags and queries for POIs
         within a specified radius to assess the competition level.
"""

import requests
import math

# Overpass API endpoint
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# Mapping of business types to OSM tags for Overpass queries
# Each business type maps to a list of (tag_key, tag_value) pairs
BUSINESS_TO_OSM_TAGS = {
    "restaurant": [
        ("amenity", "restaurant"),
        ("amenity", "fast_food"),
        ("amenity", "food_court"),
    ],
    "cafe": [
        ("amenity", "cafe"),
    ],
    "salon": [
        ("shop", "hairdresser"),
        ("shop", "beauty"),
    ],
    "gym": [
        ("leisure", "fitness_centre"),
        ("leisure", "sports_centre"),
    ],
    "retail_shop": [
        ("shop", "convenience"),
        ("shop", "supermarket"),
        ("shop", "clothes"),
        ("shop", "department_store"),
    ],
    "grocery_store": [
        ("shop", "convenience"),
        ("shop", "supermarket"),
        ("shop", "greengrocer"),
    ],
    "office": [
        ("office", "company"),
        ("office", "coworking"),
        ("office", "it"),
    ],
    "clinic": [
        ("amenity", "clinic"),
        ("amenity", "doctors"),
        ("amenity", "dentist"),
    ],
    "bakery": [
        ("shop", "bakery"),
        ("shop", "pastry"),
    ],
    "pharmacy": [
        ("amenity", "pharmacy"),
        ("shop", "chemist"),
    ],
    "hotel": [
        ("tourism", "hotel"),
        ("tourism", "guest_house"),
    ],
    "bank": [
        ("amenity", "bank"),
    ],
}


def _haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates distance between two points in meters using the Haversine formula."""
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _build_overpass_query(latitude: float, longitude: float, radius_meters: int, osm_tags: list) -> str:
    """
    Builds an Overpass QL query to find POIs matching the given OSM tags within a radius.
    """
    tag_queries = []
    for tag_key, tag_value in osm_tags:
        tag_queries.append(
            f'  node(around:{radius_meters},{latitude},{longitude})["{tag_key}"="{tag_value}"];'
        )
        tag_queries.append(
            f'  way(around:{radius_meters},{latitude},{longitude})["{tag_key}"="{tag_value}"];'
        )

    union_body = "\n".join(tag_queries)

    return f"""
[out:json][timeout:25];
(
{union_body}
);
out body;
>;
out skel qt;
"""


def find_competition(
    latitude: float,
    longitude: float,
    business_type: str,
    radius_meters: int = 1000,
) -> dict:
    """
    Finds nearby businesses of the same or similar type using OpenStreetMap data.

    Queries the Overpass API for Points of Interest (POIs) matching the given
    business type within the specified radius and assesses the competition level.

    Args:
        latitude: Latitude of the target location.
        longitude: Longitude of the target location.
        business_type: Type of business to search for competitors
            (e.g., "restaurant", "salon", "gym", "retail_shop", "cafe", "clinic").
        radius_meters: Search radius in meters (default: 1000).

    Returns:
        A dictionary containing:
            - competitors_count: Total number of similar businesses found
            - competitors: List of nearby competitors with name, type, and distance
            - competition_level: "High" / "Medium" / "Low"
            - density_per_sqkm: Competitor density per square kilometer
            - closest_competitor: Details of the nearest competitor
            - analysis: Human-readable competition analysis
    """
    # Normalize business type
    biz_key = business_type.strip().lower().replace(" ", "_")

    # Find matching OSM tags
    osm_tags = None
    for key in BUSINESS_TO_OSM_TAGS:
        if biz_key == key or biz_key in key or key in biz_key:
            osm_tags = BUSINESS_TO_OSM_TAGS[key]
            break

    if osm_tags is None:
        return {
            "error": f"No OSM tag mapping for business type: '{business_type}'",
            "available_types": list(BUSINESS_TO_OSM_TAGS.keys()),
            "suggestion": "Try one of the available types, or provide a more specific business category.",
        }

    # Build and execute Overpass query
    query = _build_overpass_query(latitude, longitude, radius_meters, osm_tags)

    try:
        response = requests.post(OVERPASS_URL, data={"data": query}, timeout=30)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout:
        return {"error": "Overpass API request timed out. Try again later or reduce the radius."}
    except requests.exceptions.RequestException as e:
        return {"error": f"Overpass API request failed: {str(e)}"}
    except ValueError as e:
        return {"error": f"Failed to parse Overpass response: {str(e)}"}

    # Process results — extract POIs (nodes and ways with tags)
    competitors = []
    seen_names = set()  # Avoid duplicates from node+way results

    for element in data.get("elements", []):
        tags = element.get("tags", {})
        if not tags:
            continue  # Skip skeleton nodes (from `out skel`)

        name = tags.get("name", "Unnamed")
        comp_type = (
            tags.get("amenity")
            or tags.get("shop")
            or tags.get("leisure")
            or tags.get("office")
            or tags.get("tourism")
            or "unknown"
        )

        # Get coordinates (for nodes directly, for ways use center if available)
        if "lat" in element and "lon" in element:
            comp_lat = element["lat"]
            comp_lon = element["lon"]
        else:
            continue  # Skip ways without resolved coordinates

        distance = _haversine_distance(latitude, longitude, comp_lat, comp_lon)

        # Dedup by name + approximate location
        dedup_key = f"{name}_{round(comp_lat, 4)}_{round(comp_lon, 4)}"
        if dedup_key in seen_names:
            continue
        seen_names.add(dedup_key)

        competitors.append({
            "name": name,
            "type": comp_type,
            "distance_meters": round(distance, 1),
            "address": tags.get("addr:street", tags.get("addr:full", "")),
        })

    # Sort by distance
    competitors.sort(key=lambda c: c["distance_meters"])

    # Calculate metrics
    count = len(competitors)
    area_sqkm = math.pi * (radius_meters / 1000) ** 2
    density = round(count / area_sqkm, 1) if area_sqkm > 0 else 0

    # Competition level classification
    if count >= 9:
        level = "High"
    elif count >= 4:
        level = "Medium"
    else:
        level = "Low"

    closest = competitors[0] if competitors else None

    # Build analysis
    analysis = f"Found {count} similar {business_type} business(es) within {radius_meters}m. "
    analysis += f"Competition level is {level.lower()} ({density} per sq km). "
    if closest:
        if closest["name"] != "Unnamed":
            analysis += f"The nearest competitor is '{closest['name']}' at {closest['distance_meters']:.0f}m. "
        else:
            analysis += f"The nearest competitor is at {closest['distance_meters']:.0f}m. "
    if count == 0:
        analysis += "This could be an underserved area or a niche opportunity."

    return {
        "competitors_count": count,
        "competitors": competitors[:15],  # Cap at 15 for readability
        "competition_level": level,
        "density_per_sqkm": density,
        "closest_competitor": closest,
        "search_radius_meters": radius_meters,
        "analysis": analysis,
    }
