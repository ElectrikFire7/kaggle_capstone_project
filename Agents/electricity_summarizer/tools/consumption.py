"""
File: Agents/electricity_summarizer/tools/consumption.py
Purpose: Converts daily electricity load estimates into monthly consumption figures.
         Uses the formula: units = load_kw × hours × utilization_factor
         and scales to monthly totals (30 days).
"""


def calculate_consumption(
    daily_units_low: float,
    daily_units_high: float,
    operating_hours: float = 10.0,
    utilization_factor: float = 0.75,
) -> dict:
    """
    Converts daily electricity load estimates to daily and monthly unit consumption.

    Takes the raw daily kWh range from the load estimator and adjusts it using
    operating hours and a utilization factor to produce realistic consumption figures.

    Args:
        daily_units_low: Lower bound of estimated daily consumption in kWh.
        daily_units_high: Upper bound of estimated daily consumption in kWh.
        operating_hours: Number of hours the business operates per day (default: 10).
        utilization_factor: Fraction of time equipment runs at full load (0.0-1.0, default: 0.75).

    Returns:
        A dictionary containing:
            - daily_units_low: Adjusted lower daily consumption in kWh
            - daily_units_high: Adjusted upper daily consumption in kWh
            - monthly_units_low: Lower monthly consumption in kWh (30 days)
            - monthly_units_high: Upper monthly consumption in kWh (30 days)
            - operating_hours: Hours used in calculation
            - utilization_factor: Utilization factor used
    """
    # Apply utilization factor to adjust raw estimates
    adjusted_low = round(daily_units_low * utilization_factor, 2)
    adjusted_high = round(daily_units_high * utilization_factor, 2)

    # Scale to monthly (30 days)
    monthly_low = round(adjusted_low * 30, 2)
    monthly_high = round(adjusted_high * 30, 2)

    return {
        "daily_units_low": adjusted_low,
        "daily_units_high": adjusted_high,
        "monthly_units_low": monthly_low,
        "monthly_units_high": monthly_high,
        "operating_hours": operating_hours,
        "utilization_factor": utilization_factor,
    }
