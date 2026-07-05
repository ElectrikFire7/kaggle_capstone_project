"""
File: Agents/water_resource_agent/tools/water_tariff.py
Purpose: Reads official BWSSB (Bangalore Water Supply and Sewerage Board) data from
         the bundled JSON file and returns tariff category, rates, and consumption
         statistics for a given business type.
"""

import json
import os
import pathlib


# BWSSB tariff rates per kiloliter (KL) for different categories
# Source: BWSSB official tariff schedule for non-domestic/commercial connections
BWSSB_TARIFF_RATES = {
    "Non Domestic": {
        "0-25": 48.0,       # 0-25 KL per month
        "25-50": 72.0,      # 25-50 KL per month
        "50-75": 96.0,      # 50-75 KL per month
        "75-100": 108.0,    # 75-100 KL per month
        "100+": 132.0,      # Above 100 KL per month
        "sewerage_pct": 50, # Sewerage charge as % of water bill
    },
    "Industries, BIAL, and others": {
        "0-25": 60.0,
        "25-50": 84.0,
        "50-75": 108.0,
        "75-100": 120.0,
        "100+": 144.0,
        "sewerage_pct": 50,
    },
    "Partial Non Domestic": {
        "0-25": 36.0,
        "25-50": 54.0,
        "50-75": 72.0,
        "75-100": 84.0,
        "100+": 108.0,
        "sewerage_pct": 50,
    },
}

# Mapping of business types to BWSSB consumption categories
BUSINESS_CATEGORY_MAP = {
    "restaurant": "Non Domestic",
    "cafe": "Non Domestic",
    "bakery": "Non Domestic",
    "hotel": "Non Domestic",
    "salon": "Non Domestic",
    "spa": "Non Domestic",
    "gym": "Non Domestic",
    "clinic": "Non Domestic",
    "hospital": "Industries, BIAL, and others",
    "office": "Non Domestic",
    "retail shop": "Non Domestic",
    "grocery store": "Non Domestic",
    "warehouse": "Industries, BIAL, and others",
    "factory": "Industries, BIAL, and others",
    "laundry": "Industries, BIAL, and others",
    "car wash": "Industries, BIAL, and others",
}


def get_water_tariff(business_type: str) -> dict:
    """
    Retrieves BWSSB tariff information for a given business type using official data.

    Args:
        business_type: Type of business (e.g., "restaurant", "bakery", "gym").

    Returns:
        A dictionary containing:
            - category: BWSSB consumption category name
            - tariff_slabs: Dict of rate per KL for each consumption slab
            - sewerage_charge_pct: Sewerage charge as percentage of water bill
            - revenue_yield_per_ml: Revenue yield per ML from official data
            - total_connections: Total connections in this category
            - total_consumption_ml: Total consumption in ML for this category
            - water_accounted_pct: Percentage of total water accounted
            - demand_lakhs: Demand in lakhs for this category
    """
    # Load official BWSSB data from bundled JSON file
    data_path = pathlib.Path(__file__).parent.parent / "data" / "BWSSB Consumption Categories Number of Connections and Revenue.json"

    try:
        with open(data_path, "r", encoding="utf-8") as f:
            bwssb_data = json.load(f)
    except Exception as e:
        return {"error": f"Failed to load BWSSB data: {str(e)}"}

    # Determine the BWSSB category for this business type
    business_lower = business_type.lower().strip()
    category = BUSINESS_CATEGORY_MAP.get(business_lower, "Non Domestic")

    # Find the matching record from official data
    official_record = None
    for record in bwssb_data.get("records", []):
        if record[1] == category:
            official_record = record
            break

    if official_record is None:
        return {
            "error": f"No BWSSB data found for category: {category}",
            "category": category,
        }

    # Get tariff rates for this category
    tariff_info = BWSSB_TARIFF_RATES.get(category, BWSSB_TARIFF_RATES["Non Domestic"])

    return {
        "category": category,
        "tariff_slabs": {
            "0_to_25_kl": tariff_info["0-25"],
            "25_to_50_kl": tariff_info["25-50"],
            "50_to_75_kl": tariff_info["50-75"],
            "75_to_100_kl": tariff_info["75-100"],
            "above_100_kl": tariff_info["100+"],
        },
        "sewerage_charge_pct": tariff_info["sewerage_pct"],
        "revenue_yield_per_ml": official_record[7],
        "total_connections": official_record[2],
        "total_consumption_ml": official_record[3],
        "water_accounted_pct": official_record[4],
        "demand_lakhs": official_record[5],
    }
