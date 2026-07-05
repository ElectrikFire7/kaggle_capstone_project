"""
File: Agents/water_resource_agent/tools/water_estimator.py
Purpose: Estimates monthly water consumption and cost for a commercial space in
         Bangalore based on business type and area. Uses industry benchmarks for
         water usage per square foot and BWSSB tariff slab calculations.
"""

import json
import pathlib


# Water consumption benchmarks in liters per square foot per day
# Based on industry standards for commercial establishments
WATER_BENCHMARKS = {
    "restaurant": {
        "liters_per_sqft_per_day": 1.8,
        "major_consumers": ["kitchen operations", "dishwashing", "restrooms", "floor cleaning", "food preparation"],
    },
    "cafe": {
        "liters_per_sqft_per_day": 1.2,
        "major_consumers": ["beverage preparation", "dishwashing", "restrooms", "cleaning"],
    },
    "bakery": {
        "liters_per_sqft_per_day": 1.4,
        "major_consumers": ["dough preparation", "equipment cleaning", "restrooms", "floor cleaning"],
    },
    "hotel": {
        "liters_per_sqft_per_day": 2.5,
        "major_consumers": ["guest rooms", "laundry", "kitchen", "restrooms", "swimming pool", "landscaping"],
    },
    "salon": {
        "liters_per_sqft_per_day": 1.6,
        "major_consumers": ["hair washing", "spa treatments", "restrooms", "cleaning", "sterilization"],
    },
    "spa": {
        "liters_per_sqft_per_day": 2.2,
        "major_consumers": ["spa pools", "steam rooms", "showers", "laundry", "cleaning"],
    },
    "gym": {
        "liters_per_sqft_per_day": 1.0,
        "major_consumers": ["showers", "restrooms", "drinking water", "cleaning", "laundry"],
    },
    "clinic": {
        "liters_per_sqft_per_day": 0.8,
        "major_consumers": ["sterilization", "restrooms", "cleaning", "patient care"],
    },
    "hospital": {
        "liters_per_sqft_per_day": 2.0,
        "major_consumers": ["patient care", "sterilization", "laundry", "kitchen", "cooling systems", "restrooms"],
    },
    "office": {
        "liters_per_sqft_per_day": 0.4,
        "major_consumers": ["restrooms", "pantry", "cleaning", "cooling systems"],
    },
    "retail shop": {
        "liters_per_sqft_per_day": 0.3,
        "major_consumers": ["restrooms", "cleaning", "drinking water"],
    },
    "grocery store": {
        "liters_per_sqft_per_day": 0.5,
        "major_consumers": ["produce washing", "restrooms", "cleaning", "refrigeration"],
    },
    "warehouse": {
        "liters_per_sqft_per_day": 0.15,
        "major_consumers": ["restrooms", "cleaning", "fire suppression systems"],
    },
    "laundry": {
        "liters_per_sqft_per_day": 3.0,
        "major_consumers": ["washing machines", "rinsing", "steam pressing", "restrooms"],
    },
    "car wash": {
        "liters_per_sqft_per_day": 4.0,
        "major_consumers": ["vehicle washing", "rinsing", "pressure cleaning", "water recycling systems"],
    },
}

# Default benchmark for unknown business types
DEFAULT_BENCHMARK = {
    "liters_per_sqft_per_day": 0.6,
    "major_consumers": ["restrooms", "cleaning", "drinking water", "general operations"],
}

# BWSSB tariff slabs for Non Domestic category (INR per KL)
TARIFF_SLABS = [
    (25, 48.0),
    (50, 72.0),
    (75, 96.0),
    (100, 108.0),
    (float("inf"), 132.0),
]

SEWERAGE_CHARGE_PCT = 50  # Sewerage charge as % of water bill


def estimate_water_usage(business_type: str, area_sqft: float) -> dict:
    """
    Estimates monthly water consumption and cost for a commercial space.

    Args:
        business_type: Type of business (e.g., "restaurant", "bakery", "gym").
        area_sqft: Area of the commercial space in square feet.

    Returns:
        A dictionary containing:
            - monthly_consumption_kl: Estimated monthly water consumption in kiloliters
            - monthly_cost_low: Lower bound of monthly cost estimate in INR
            - monthly_cost_high: Upper bound of monthly cost estimate in INR
            - water_usage_level: One of "Low", "Medium", or "High"
            - major_consumers: List of major water consumers for this business type
            - daily_consumption_liters: Estimated daily water consumption in liters
            - benchmark_liters_per_sqft: Water benchmark used (liters/sqft/day)
    """
    try:
        area_sqft = float(area_sqft)
    except (ValueError, TypeError):
        return {"error": f"Invalid area value: {area_sqft}"}

    # Get benchmark for business type
    business_lower = business_type.lower().strip()
    benchmark = WATER_BENCHMARKS.get(business_lower, DEFAULT_BENCHMARK)

    liters_per_sqft = benchmark["liters_per_sqft_per_day"]
    major_consumers = benchmark["major_consumers"]

    # Calculate daily consumption in liters
    daily_liters = area_sqft * liters_per_sqft

    # Calculate monthly consumption in kiloliters (30 days, 1 KL = 1000 liters)
    monthly_kl = (daily_liters * 30) / 1000

    # Apply variation factor for low/high estimates (+-20%)
    monthly_kl_low = monthly_kl * 0.8
    monthly_kl_high = monthly_kl * 1.2

    # Calculate cost using BWSSB slab-based tariff
    cost_low = _calculate_slab_cost(monthly_kl_low)
    cost_high = _calculate_slab_cost(monthly_kl_high)

    # Add sewerage charges
    cost_low_total = cost_low * (1 + SEWERAGE_CHARGE_PCT / 100)
    cost_high_total = cost_high * (1 + SEWERAGE_CHARGE_PCT / 100)

    # Determine usage level
    if monthly_kl < 15:
        usage_level = "Low"
    elif monthly_kl <= 50:
        usage_level = "Medium"
    else:
        usage_level = "High"

    return {
        "monthly_consumption_kl": round(monthly_kl, 1),
        "monthly_cost_low": round(cost_low_total),
        "monthly_cost_high": round(cost_high_total),
        "water_usage_level": usage_level,
        "major_consumers": major_consumers,
        "daily_consumption_liters": round(daily_liters, 1),
        "benchmark_liters_per_sqft": liters_per_sqft,
    }


def _calculate_slab_cost(consumption_kl: float) -> float:
    """
    Calculates water bill using BWSSB slab-based tariff structure.

    Args:
        consumption_kl: Monthly water consumption in kiloliters.

    Returns:
        Total water charge in INR (before sewerage).
    """
    total_cost = 0.0
    remaining = consumption_kl
    prev_limit = 0

    for slab_limit, rate in TARIFF_SLABS:
        slab_width = slab_limit - prev_limit
        if remaining <= 0:
            break
        consumed_in_slab = min(remaining, slab_width)
        total_cost += consumed_in_slab * rate
        remaining -= consumed_in_slab
        prev_limit = slab_limit

    return total_cost
