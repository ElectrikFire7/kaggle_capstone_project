"""
File: Agents/gis_agent/tools/road_network.py
Purpose: Queries the Overpass API to find roads near a given point and classifies them
         by type (primary, secondary, tertiary, residential). Calculates distances
         using the Haversine formula and returns structured road network data.
"""

import requests
import math

# Overpass API endpoint
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# Road classification hierarchy (higher = more important)
ROAD_HIERARCHY = {
    "motorway": 7,
    "trunk": 6,
    "primary": 5,
    "secondary": 4,
    "tertiary": 3,
    "unclassified": 2,
    "residential": 1,
    "service": 0,
    "living_street": 0,
    "pedestrian": 0,
}

# Roads considered "main" for accessibility/visibility purposes
MAIN_ROAD_TYPES = {"motorway", "trunk", "primary", "secondary", "tertiary"}


def _haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculates the great-circle distance between two points on Earth using the Haversine formula.

    Args:
        lat1, lon1: Coordinates of the first point (degrees).
        lat2, lon2: Coordinates of the second point (degrees).

    Returns:
        Distance in meters.
    """
    R = 6371000  # Earth's radius in meters

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def _closest_point_on_way(lat: float, lon: float, nodes: list) -> float:
    """
    Finds the minimum distance from a point to a polyline (way) defined by a list of nodes.

    Args:
        lat, lon: Coordinates of the query point.
        nodes: List of dicts with 'lat' and 'lon' keys.

    Returns:
        Minimum distance in meters.
    """
    min_dist = float("inf")
    for node in nodes:
        dist = _haversine_distance(lat, lon, node["lat"], node["lon"])
        if dist < min_dist:
            min_dist = dist
    return round(min_dist, 1)


def get_nearby_roads(latitude: float, longitude: float, radius_meters: int = 500) -> dict:
    """
    Fetches and classifies roads near a given point using the Overpass API.

    Queries OpenStreetMap for all roads within the specified radius, classifies them
    by type (primary, secondary, tertiary, residential), and calculates the distance
    from the query point to each road.

    Args:
        latitude: Latitude of the point to query around.
        longitude: Longitude of the point to query around.
        radius_meters: Search radius in meters (default: 500).

    Returns:
        A dictionary containing:
            - roads: List of nearby roads, each with name, road_type, distance_meters,
              lanes, surface, and classification_rank
            - road_count: Total number of roads found
            - main_road_count: Number of main roads (primary/secondary/tertiary+)
            - nearest_main_road: Details of the closest main road
            - distance_to_nearest_main_road: Distance to the nearest main road in meters
            - road_type_summary: Count of roads by type
        Or a dict with "error" key if the query fails.
    """
    # Build Overpass QL query for roads within radius
    query = f"""
    [out:json][timeout:25];
    (
      way(around:{radius_meters},{latitude},{longitude})["highway"];
    );
    out body;
    >;
    out skel qt;
    """

    try:
        response = requests.post(OVERPASS_URL, data={"data": query}, timeout=30)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout:
        return {"error": "Overpass API request timed out. Try a smaller radius or try again later."}
    except requests.exceptions.RequestException as e:
        return {"error": f"Overpass API request failed: {str(e)}"}
    except ValueError as e:
        return {"error": f"Failed to parse Overpass response: {str(e)}"}

    # Separate nodes and ways from the response
    nodes_by_id = {}
    ways = []

    for element in data.get("elements", []):
        if element["type"] == "node":
            nodes_by_id[element["id"]] = {"lat": element["lat"], "lon": element["lon"]}
        elif element["type"] == "way":
            tags = element.get("tags", {})
            highway_type = tags.get("highway", "")
            if highway_type in ROAD_HIERARCHY:
                ways.append({
                    "id": element["id"],
                    "tags": tags,
                    "highway_type": highway_type,
                    "node_ids": element.get("nodes", []),
                })

    # Process each way: resolve nodes and calculate distances
    roads = []
    for way in ways:
        # Resolve node coordinates for this way
        way_nodes = []
        for nid in way["node_ids"]:
            if nid in nodes_by_id:
                way_nodes.append(nodes_by_id[nid])

        if not way_nodes:
            continue

        distance = _closest_point_on_way(latitude, longitude, way_nodes)
        tags = way["tags"]

        roads.append({
            "name": tags.get("name", "Unnamed Road"),
            "road_type": way["highway_type"],
            "distance_meters": distance,
            "lanes": tags.get("lanes", "unknown"),
            "surface": tags.get("surface", "unknown"),
            "classification_rank": ROAD_HIERARCHY.get(way["highway_type"], 0),
            "is_main_road": way["highway_type"] in MAIN_ROAD_TYPES,
        })

    # Sort by distance
    roads.sort(key=lambda r: r["distance_meters"])

    # Find nearest main road
    main_roads = [r for r in roads if r["is_main_road"]]
    nearest_main = main_roads[0] if main_roads else None

    # Road type summary
    type_summary = {}
    for r in roads:
        rtype = r["road_type"]
        type_summary[rtype] = type_summary.get(rtype, 0) + 1

    return {
        "roads": roads[:20],  # Cap at 20 to keep response manageable
        "road_count": len(roads),
        "main_road_count": len(main_roads),
        "nearest_main_road": nearest_main,
        "distance_to_nearest_main_road": nearest_main["distance_meters"] if nearest_main else None,
        "road_type_summary": type_summary,
    }
