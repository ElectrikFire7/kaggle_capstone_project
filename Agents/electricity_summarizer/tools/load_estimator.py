"""
File: Agents/electricity_summarizer/tools/load_estimator.py
Purpose: Provides electricity consumption benchmarks for various business types.
         Contains pre-researched data for common commercial establishments in India,
         with per-square-foot consumption rates to enable area-based estimation.
"""


# Pre-researched consumption benchmarks (kWh per sq ft per day)
# Sources: CPWD energy benchmarks, BEE commercial building data, TERI research
BUSINESS_BENCHMARKS = {
    "restaurant": {
        "kwh_per_sqft_per_day_low": 0.15,
        "kwh_per_sqft_per_day_high": 0.35,
        "description": "Includes kitchen equipment, HVAC, lighting, refrigeration",
        "major_loads": ["commercial kitchen equipment", "HVAC/air conditioning", "refrigeration", "lighting"],
    },
    "salon": {
        "kwh_per_sqft_per_day_low": 0.08,
        "kwh_per_sqft_per_day_high": 0.18,
        "description": "Includes hair dryers, styling tools, HVAC, lighting",
        "major_loads": ["hair dryers and styling tools", "air conditioning", "water heater", "lighting"],
    },
    "office": {
        "kwh_per_sqft_per_day_low": 0.05,
        "kwh_per_sqft_per_day_high": 0.12,
        "description": "Includes computers, HVAC, lighting, printers",
        "major_loads": ["computers and monitors", "air conditioning", "lighting", "printers and copiers"],
    },
    "retail_shop": {
        "kwh_per_sqft_per_day_low": 0.06,
        "kwh_per_sqft_per_day_high": 0.15,
        "description": "Includes display lighting, HVAC, billing systems",
        "major_loads": ["display and accent lighting", "air conditioning", "billing/POS systems", "signage"],
    },
    "grocery_store": {
        "kwh_per_sqft_per_day_low": 0.12,
        "kwh_per_sqft_per_day_high": 0.28,
        "description": "Includes refrigeration, freezers, HVAC, lighting",
        "major_loads": ["refrigeration and freezers", "air conditioning", "lighting", "cold storage"],
    },
    "gym": {
        "kwh_per_sqft_per_day_low": 0.10,
        "kwh_per_sqft_per_day_high": 0.22,
        "description": "Includes treadmills, HVAC, lighting, water heaters",
        "major_loads": ["motorized equipment (treadmills, etc.)", "heavy HVAC", "lighting", "water heaters"],
    },
    "cafe": {
        "kwh_per_sqft_per_day_low": 0.10,
        "kwh_per_sqft_per_day_high": 0.25,
        "description": "Includes coffee machines, HVAC, refrigeration, lighting",
        "major_loads": ["coffee/espresso machines", "air conditioning", "refrigeration", "lighting"],
    },
    "clinic": {
        "kwh_per_sqft_per_day_low": 0.07,
        "kwh_per_sqft_per_day_high": 0.16,
        "description": "Includes medical equipment, HVAC, lighting, sterilizers",
        "major_loads": ["medical equipment", "air conditioning", "sterilization equipment", "lighting"],
    },
    "bakery": {
        "kwh_per_sqft_per_day_low": 0.18,
        "kwh_per_sqft_per_day_high": 0.40,
        "description": "Includes ovens, mixers, refrigeration, HVAC",
        "major_loads": ["commercial ovens", "mixers and dough equipment", "refrigeration", "air conditioning"],
    },
    "warehouse": {
        "kwh_per_sqft_per_day_low": 0.02,
        "kwh_per_sqft_per_day_high": 0.06,
        "description": "Includes lighting, ventilation, loading dock equipment",
        "major_loads": ["lighting", "ventilation fans", "loading dock equipment", "security systems"],
    },
}


def estimate_load(business_type: str, area_sqft: float) -> dict:
    """
    Estimates daily electricity consumption range for a business based on its type and area.

    Uses pre-researched benchmarks for common commercial establishments in India.
    The benchmarks are sourced from CPWD energy guidelines, BEE commercial building
    data, and TERI research reports.

    Args:
        business_type: The type of business (e.g., "restaurant", "salon", "office",
            "retail_shop", "grocery_store", "gym", "cafe", "clinic", "bakery", "warehouse").
        area_sqft: The area of the commercial space in square feet.

    Returns:
        A dictionary containing:
            - daily_units_low: Lower estimate of daily consumption in kWh
            - daily_units_high: Upper estimate of daily consumption in kWh
            - description: Description of what's included in the estimate
            - major_loads: List of major electricity consumers for this business type
            - benchmark_source: Source of the benchmark data
    """
    # Normalize business type
    biz_key = business_type.strip().lower().replace(" ", "_")

    # Try to find an exact or partial match
    matched_key = None
    for key in BUSINESS_BENCHMARKS:
        if biz_key == key or biz_key in key or key in biz_key:
            matched_key = key
            break

    if matched_key is None:
        available = list(BUSINESS_BENCHMARKS.keys())
        return {
            "error": f"No benchmark data found for business type: '{business_type}'.",
            "suggestion": "Using generic commercial estimate instead.",
            "daily_units_low": round(area_sqft * 0.07, 2),
            "daily_units_high": round(area_sqft * 0.18, 2),
            "description": "Generic commercial estimate — actual consumption may vary.",
            "major_loads": ["air conditioning", "lighting", "general equipment"],
            "benchmark_source": "generic commercial average",
            "available_types": available,
        }

    benchmark = BUSINESS_BENCHMARKS[matched_key]
    daily_low = round(area_sqft * benchmark["kwh_per_sqft_per_day_low"], 2)
    daily_high = round(area_sqft * benchmark["kwh_per_sqft_per_day_high"], 2)

    return {
        "daily_units_low": daily_low,
        "daily_units_high": daily_high,
        "description": benchmark["description"],
        "major_loads": benchmark["major_loads"],
        "benchmark_source": f"Pre-researched benchmarks for {matched_key} (CPWD/BEE/TERI)",
    }
