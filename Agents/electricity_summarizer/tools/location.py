"""
File: Agents/electricity_summarizer/tools/location.py
Purpose: Provides location-based adjustment factors for electricity consumption
         estimation in Bangalore. Different areas have different usage patterns
         based on commercial density, climate micro-zones, and typical operating hours.
"""


# Bangalore location profiles with adjustment multipliers and typical operating hours
LOCATION_PROFILES = {
    # Central Business District / Prime Commercial
    "mg_road": {"multiplier": 1.25, "typical_hours": 12, "zone": "CBD", "description": "MG Road — prime commercial, heavy AC usage"},
    "brigade_road": {"multiplier": 1.25, "typical_hours": 12, "zone": "CBD", "description": "Brigade Road — premium retail and dining"},
    "commercial_street": {"multiplier": 1.20, "typical_hours": 11, "zone": "CBD", "description": "Commercial Street — dense retail corridor"},
    "church_street": {"multiplier": 1.20, "typical_hours": 12, "zone": "CBD", "description": "Church Street — F&B and retail hub"},

    # Tech Corridors
    "whitefield": {"multiplier": 1.15, "typical_hours": 10, "zone": "Tech Corridor", "description": "Whitefield — IT hub with modern infrastructure"},
    "electronic_city": {"multiplier": 1.15, "typical_hours": 10, "zone": "Tech Corridor", "description": "Electronic City — IT/ITES zone"},
    "outer_ring_road": {"multiplier": 1.15, "typical_hours": 10, "zone": "Tech Corridor", "description": "Outer Ring Road — tech and commercial corridor"},
    "marathahalli": {"multiplier": 1.10, "typical_hours": 10, "zone": "Tech Corridor", "description": "Marathahalli — mixed commercial-residential"},
    "sarjapur_road": {"multiplier": 1.10, "typical_hours": 10, "zone": "Tech Corridor", "description": "Sarjapur Road — emerging tech corridor"},

    # Established Commercial-Residential
    "koramangala": {"multiplier": 1.15, "typical_hours": 11, "zone": "Urban Commercial", "description": "Koramangala — startup and F&B hub"},
    "indiranagar": {"multiplier": 1.15, "typical_hours": 11, "zone": "Urban Commercial", "description": "Indiranagar — premium retail and dining"},
    "hsr_layout": {"multiplier": 1.10, "typical_hours": 10, "zone": "Urban Commercial", "description": "HSR Layout — mixed use with growing commercial"},
    "jayanagar": {"multiplier": 1.05, "typical_hours": 10, "zone": "Urban Commercial", "description": "Jayanagar — established residential-commercial"},
    "malleshwaram": {"multiplier": 1.05, "typical_hours": 10, "zone": "Urban Commercial", "description": "Malleshwaram — traditional commercial area"},
    "basavanagudi": {"multiplier": 1.00, "typical_hours": 10, "zone": "Urban Commercial", "description": "Basavanagudi — moderate commercial density"},
    "rajajinagar": {"multiplier": 1.05, "typical_hours": 10, "zone": "Urban Commercial", "description": "Rajajinagar — industrial-commercial mix"},

    # Suburban / Emerging
    "yelahanka": {"multiplier": 0.95, "typical_hours": 9, "zone": "Suburban", "description": "Yelahanka — growing suburban commercial"},
    "bannerghatta_road": {"multiplier": 1.00, "typical_hours": 10, "zone": "Suburban", "description": "Bannerghatta Road — mixed development corridor"},
    "kanakapura_road": {"multiplier": 0.95, "typical_hours": 9, "zone": "Suburban", "description": "Kanakapura Road — emerging suburban area"},
    "hebbal": {"multiplier": 1.05, "typical_hours": 10, "zone": "Suburban", "description": "Hebbal — north Bangalore commercial node"},
    "jp_nagar": {"multiplier": 1.05, "typical_hours": 10, "zone": "Urban Commercial", "description": "JP Nagar — residential with commercial pockets"},

    # Outskirts
    "devanahalli": {"multiplier": 0.85, "typical_hours": 9, "zone": "Outskirts", "description": "Devanahalli — airport area, lower commercial density"},
    "nelamangala": {"multiplier": 0.80, "typical_hours": 8, "zone": "Outskirts", "description": "Nelamangala — industrial outskirts"},
    "anekal": {"multiplier": 0.80, "typical_hours": 8, "zone": "Outskirts", "description": "Anekal — emerging peripheral area"},
}

# Default values for unknown locations
DEFAULT_PROFILE = {
    "multiplier": 1.0,
    "typical_hours": 10,
    "zone": "Unknown",
    "description": "Default Bangalore average — location not specifically profiled",
}


def get_location_adjustment(location: str) -> dict:
    """
    Returns location-based adjustment factors for electricity estimation in Bangalore.

    Different areas in Bangalore have varying commercial densities, climate patterns,
    and typical business operating hours, which affect electricity consumption.
    The multiplier adjusts the base consumption estimate up or down.

    Args:
        location: The area/locality name in Bangalore (e.g., "Koramangala",
            "Whitefield", "MG Road", "Electronic City").

    Returns:
        A dictionary containing:
            - multiplier: Consumption adjustment factor (1.0 = baseline)
            - typical_hours: Typical business operating hours in this area
            - zone: Zone classification (CBD, Tech Corridor, Urban, Suburban, Outskirts)
            - description: Brief description of the location's commercial character
    """
    # Normalize location string for matching
    loc_key = location.strip().lower().replace(" ", "_").replace("-", "_")

    # Try exact match first
    if loc_key in LOCATION_PROFILES:
        return LOCATION_PROFILES[loc_key]

    # Try partial match
    for key, profile in LOCATION_PROFILES.items():
        if loc_key in key or key in loc_key:
            return profile

    # Return default if no match found
    return {
        **DEFAULT_PROFILE,
        "note": f"Location '{location}' not in database. Using Bangalore average values.",
        "available_locations": list(LOCATION_PROFILES.keys()),
    }
