"""
File: Agents/gis_agent/tools/geocoder.py
Purpose: Translates a human-readable address into geographic coordinates (latitude, longitude)
         using the OpenStreetMap Nominatim API. Returns structured location data including
         the resolved address, place type, and bounding box.
"""

import requests
import time

# Nominatim API endpoint
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

# Required by Nominatim usage policy — identifies our application
USER_AGENT = "CapstoneProjectGISAgent/1.0 (student-project)"

# Rate limiting: track last request time to enforce 1 req/sec policy
_last_request_time = 0.0


def geocode_address(address: str) -> dict:
    """
    Converts a natural language address into geographic coordinates using OpenStreetMap Nominatim.

    Takes a human-readable address string (e.g., "100 Feet Road, Indiranagar, Bangalore")
    and returns its latitude, longitude, and other location metadata.

    Args:
        address: A natural language address string. Can be a full address,
            a landmark name, or a locality (e.g., "MG Road, Bangalore",
            "Koramangala 4th Block, Bengaluru").

    Returns:
        A dictionary containing:
            - latitude: Latitude of the location (float)
            - longitude: Longitude of the location (float)
            - display_name: Full resolved address string from OSM
            - place_type: Type of place (e.g., "building", "road", "neighbourhood")
            - osm_type: OSM object type ("node", "way", "relation")
            - bounding_box: [south_lat, north_lat, west_lon, east_lon]
            - address_details: Parsed address components (road, suburb, city, etc.)
        Or a dict with "error" key if geocoding fails.
    """
    global _last_request_time

    # Enforce rate limit (1 request per second as per Nominatim policy)
    elapsed = time.time() - _last_request_time
    if elapsed < 1.0:
        time.sleep(1.0 - elapsed)

    params = {
        "q": address,
        "format": "json",
        "limit": 1,
        "addressdetails": 1,
    }

    headers = {
        "User-Agent": USER_AGENT,
    }

    try:
        response = requests.get(NOMINATIM_URL, params=params, headers=headers, timeout=10)
        _last_request_time = time.time()

        response.raise_for_status()
        results = response.json()

        if not results:
            return {
                "error": f"No results found for address: '{address}'",
                "suggestion": "Try a more specific address or include the city name (e.g., 'MG Road, Bangalore')",
            }

        result = results[0]

        return {
            "latitude": float(result["lat"]),
            "longitude": float(result["lon"]),
            "display_name": result.get("display_name", ""),
            "place_type": result.get("type", "unknown"),
            "osm_type": result.get("osm_type", "unknown"),
            "bounding_box": [float(x) for x in result.get("boundingbox", [])],
            "address_details": result.get("address", {}),
        }

    except requests.exceptions.Timeout:
        return {"error": "Nominatim API request timed out. Please try again."}
    except requests.exceptions.RequestException as e:
        return {"error": f"Geocoding request failed: {str(e)}"}
    except (ValueError, KeyError) as e:
        return {"error": f"Failed to parse geocoding response: {str(e)}"}
