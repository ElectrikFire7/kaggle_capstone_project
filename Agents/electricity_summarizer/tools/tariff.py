"""
File: Agents/electricity_summarizer/tools/tariff.py
Purpose: Returns BESCOM tariff values for a given consumer type by reading
         from the tariffs.json data file. Supports slab-based pricing for
         commercial, industrial, IT/ITES, and residential-converted categories.
"""

import json
import os
import pathlib


def get_tariff(consumer_type: str) -> dict:
    """
    Retrieves BESCOM electricity tariff details for a given consumer type.

    Args:
        consumer_type: The type of consumer. One of:
            - "commercial" (shops, restaurants, salons, offices)
            - "industrial" (small scale industries, manufacturing)
            - "it_ites" (IT and ITES companies)
            - "residential_converted" (residential premises used commercially)

    Returns:
        A dictionary containing:
            - per_unit_cost: Weighted average cost per unit in INR
            - fixed_charge_per_kw: Fixed demand charge per kW per month in INR
            - tax_percent: Applicable tax percentage
            - fac_surcharge_percent: FAC surcharge percentage
            - slabs: Detailed slab-wise per-unit rates
            - description: Tariff category description
    """
    # Resolve the path to tariffs.json relative to this file
    data_path = pathlib.Path(__file__).parent.parent / "data" / "tariffs.json"

    with open(data_path, "r", encoding="utf-8") as f:
        tariffs = json.load(f)

    # Normalize consumer_type to lowercase for matching
    consumer_type_key = consumer_type.strip().lower().replace(" ", "_")

    if consumer_type_key not in tariffs:
        available = list(tariffs.keys())
        return {
            "error": f"Unknown consumer type: '{consumer_type}'. Available types: {available}",
            "available_types": available,
        }

    tariff_data = tariffs[consumer_type_key]

    # Calculate a representative per-unit cost (average of first slab for simplicity)
    # The agent can use the full slab data for precise billing
    avg_cost = tariff_data["slabs"][0]["per_unit_cost"]

    return {
        "per_unit_cost": avg_cost,
        "fixed_charge_per_kw": tariff_data["fixed_charge_per_kw"],
        "tax_percent": tariff_data["tax_percent"],
        "fac_surcharge_percent": tariff_data["fac_surcharge_percent"],
        "slabs": tariff_data["slabs"],
        "description": tariff_data["description"],
    }
