"""
File: Agents/electricity_summarizer/tools/billing.py
Purpose: Calculates the monthly electricity bill using BESCOM slab-based tariffs.
         Takes monthly consumption units, connected load, and tariff details to
         produce a complete bill breakdown with energy cost, fixed charges, and taxes.
"""


def calculate_bill(
    monthly_units: float,
    load_kw: float,
    per_unit_cost: float,
    fixed_charge_per_kw: float,
    tax_percent: float,
    slabs: list = None,
) -> dict:
    """
    Calculates a detailed monthly electricity bill based on BESCOM tariff structure.

    If slab details are provided, uses slab-based calculation for accurate billing.
    Otherwise, falls back to a flat per-unit rate.

    Args:
        monthly_units: Total monthly electricity consumption in kWh.
        load_kw: Connected/sanctioned load in kW.
        per_unit_cost: Flat per-unit cost in INR (used if slabs not provided).
        fixed_charge_per_kw: Fixed demand charge per kW per month in INR.
        tax_percent: Tax percentage to apply on the total.
        slabs: Optional list of tariff slabs, each with min_units, max_units, per_unit_cost.

    Returns:
        A dictionary containing:
            - energy_cost: Cost of energy consumed in INR
            - fixed_cost: Fixed demand charges in INR
            - subtotal: Energy cost + fixed cost
            - tax: Tax amount in INR
            - total: Final bill amount in INR
            - breakdown: Slab-wise breakdown (if slabs provided)
    """
    # Calculate energy cost
    if slabs and len(slabs) > 0:
        energy_cost, breakdown = _calculate_slab_cost(monthly_units, slabs)
    else:
        energy_cost = round(monthly_units * per_unit_cost, 2)
        breakdown = [{"units": monthly_units, "rate": per_unit_cost, "cost": energy_cost}]

    # Calculate fixed demand charges
    fixed_cost = round(load_kw * fixed_charge_per_kw, 2)

    # Subtotal before tax
    subtotal = round(energy_cost + fixed_cost, 2)

    # Calculate tax
    tax = round(subtotal * (tax_percent / 100), 2)

    # Total bill
    total = round(subtotal + tax, 2)

    return {
        "energy_cost": energy_cost,
        "fixed_cost": fixed_cost,
        "subtotal": subtotal,
        "tax": tax,
        "total": total,
        "breakdown": breakdown,
    }


def _calculate_slab_cost(units: float, slabs: list) -> tuple:
    """
    Calculates energy cost using slab-based pricing.

    Args:
        units: Total units consumed.
        slabs: List of slab dicts with min_units, max_units, per_unit_cost.

    Returns:
        Tuple of (total_cost, breakdown_list).
    """
    remaining = units
    total_cost = 0.0
    breakdown = []

    for slab in slabs:
        if remaining <= 0:
            break

        slab_min = slab["min_units"]
        slab_max = slab.get("max_units")  # None means unlimited
        rate = slab["per_unit_cost"]

        if slab_max is not None:
            slab_range = slab_max - slab_min + 1
            slab_units = min(remaining, slab_range)
        else:
            slab_units = remaining

        cost = round(slab_units * rate, 2)
        total_cost += cost
        remaining -= slab_units

        breakdown.append({
            "slab": f"{slab_min}-{slab_max if slab_max else '∞'}",
            "units": round(slab_units, 2),
            "rate": rate,
            "cost": cost,
        })

    return round(total_cost, 2), breakdown
