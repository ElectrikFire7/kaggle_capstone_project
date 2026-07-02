"""
File: Agents/report_agent/tools/report_writer.py
Purpose: Generates a styled HTML report file combining electricity cost estimates and
         GIS location intelligence findings for a commercial space in Bangalore.
         Writes the report to the output/ directory with colored tags for key metrics.
"""

import os
import pathlib
from datetime import datetime


def write_report(
    business_type: str,
    area_sqft: float,
    address: str,
    electricity_summary: str,
    electricity_cost_range: str,
    electricity_usage_level: str,
    major_consumers: str,
    accessibility_score: int,
    accessibility_rating: str,
    visibility_score: int,
    visibility_rating: str,
    competition_level: str,
    competitors_count: int,
    gis_summary: str,
    overall_recommendation: str,
) -> dict:
    """
    Generates a styled HTML report and writes it to the output/ directory.

    Args:
        business_type: Type of business (e.g., "restaurant", "bakery").
        area_sqft: Area of the commercial space in square feet.
        address: The address or locality analyzed.
        electricity_summary: Concise paragraph summarizing electricity cost findings.
        electricity_cost_range: Monthly cost range string (e.g., "12,500 - 22,000").
        electricity_usage_level: One of "Low", "Medium", or "High".
        major_consumers: Comma-separated list of top electricity consumers.
        accessibility_score: Accessibility score out of 100.
        accessibility_rating: One of "Excellent", "Good", "Fair", or "Poor".
        visibility_score: Visibility score out of 100.
        visibility_rating: One of "High", "Medium", or "Low".
        competition_level: One of "High", "Medium", "Low", or "Not Analyzed".
        competitors_count: Number of competitors found.
        gis_summary: Concise paragraph summarizing location intelligence findings.
        overall_recommendation: Brief overall assessment combining both perspectives.

    Returns:
        A dictionary containing:
            - status: "success" or "error"
            - file_path: Absolute path to the generated HTML file
            - message: Confirmation message
    """
    # Resolve output directory relative to project root
    project_root = pathlib.Path(__file__).parent.parent.parent.parent
    output_dir = project_root / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report_{timestamp}.html"
    file_path = output_dir / filename

    # Build tag color mappings
    tag_colors = _get_tag_colors()

    # Build the HTML content
    html_content = _build_html(
        business_type=business_type,
        area_sqft=area_sqft,
        address=address,
        electricity_summary=electricity_summary,
        electricity_cost_range=electricity_cost_range,
        electricity_usage_level=electricity_usage_level,
        major_consumers=major_consumers,
        accessibility_score=accessibility_score,
        accessibility_rating=accessibility_rating,
        visibility_score=visibility_score,
        visibility_rating=visibility_rating,
        competition_level=competition_level,
        competitors_count=competitors_count,
        gis_summary=gis_summary,
        overall_recommendation=overall_recommendation,
        tag_colors=tag_colors,
        timestamp=timestamp,
    )

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        return {
            "status": "success",
            "file_path": str(file_path.resolve()),
            "message": f"Report saved to {file_path.resolve()}",
        }
    except Exception as e:
        return {
            "status": "error",
            "file_path": "",
            "message": f"Failed to write report: {str(e)}",
        }


def _get_tag_colors() -> dict:
    """Returns color mappings for different rating/level values."""
    return {
        # Electricity usage level
        "Low": {"bg": "#d4edda", "text": "#155724", "border": "#c3e6cb"},
        "Medium": {"bg": "#fff3cd", "text": "#856404", "border": "#ffeeba"},
        "High": {"bg": "#f8d7da", "text": "#721c24", "border": "#f5c6cb"},
        # Accessibility rating
        "Excellent": {"bg": "#d4edda", "text": "#155724", "border": "#c3e6cb"},
        "Good": {"bg": "#d1ecf1", "text": "#0c5460", "border": "#bee5eb"},
        "Fair": {"bg": "#fff3cd", "text": "#856404", "border": "#ffeeba"},
        "Poor": {"bg": "#f8d7da", "text": "#721c24", "border": "#f5c6cb"},
        # Visibility rating (reuses some colors)
        # "High", "Medium", "Low" already defined above
        # Competition level (reuses some colors)
        "Not Analyzed": {"bg": "#e2e3e5", "text": "#383d41", "border": "#d6d8db"},
        "Not Available": {"bg": "#e2e3e5", "text": "#383d41", "border": "#d6d8db"},
    }


def _get_tag_html(label: str, value: str, tag_colors: dict) -> str:
    """Generates an HTML tag span with appropriate color styling."""
    colors = tag_colors.get(value, {"bg": "#e2e3e5", "text": "#383d41", "border": "#d6d8db"})
    return (
        f'<span class="tag" style="background-color:{colors["bg"]};'
        f'color:{colors["text"]};border:1px solid {colors["border"]}">'
        f"{label}: {value}</span>"
    )


def _get_score_bar_html(label: str, score: int, rating: str) -> str:
    """Generates an HTML progress bar for a score out of 100."""
    if score >= 75:
        bar_color = "#28a745"
    elif score >= 50:
        bar_color = "#ffc107"
    elif score >= 25:
        bar_color = "#fd7e14"
    else:
        bar_color = "#dc3545"

    return f"""
    <div class="score-row">
        <div class="score-label">{label}</div>
        <div class="score-bar-container">
            <div class="score-bar" style="width:{score}%;background-color:{bar_color}"></div>
        </div>
        <div class="score-value">{score}/100 ({rating})</div>
    </div>
    """


def _build_html(
    business_type: str,
    area_sqft: float,
    address: str,
    electricity_summary: str,
    electricity_cost_range: str,
    electricity_usage_level: str,
    major_consumers: str,
    accessibility_score: int,
    accessibility_rating: str,
    visibility_score: int,
    visibility_rating: str,
    competition_level: str,
    competitors_count: int,
    gis_summary: str,
    overall_recommendation: str,
    tag_colors: dict,
    timestamp: str,
) -> str:
    """Builds the complete HTML report string."""

    # Build consumer list items
    consumers_list = ""
    for consumer in major_consumers.split(","):
        consumer = consumer.strip()
        if consumer:
            consumers_list += f"<li>{consumer}</li>\n"

    # Build tags section
    tags_html = (
        _get_tag_html("Electricity Usage", electricity_usage_level, tag_colors)
        + _get_tag_html("Accessibility", accessibility_rating, tag_colors)
        + _get_tag_html("Visibility", visibility_rating, tag_colors)
        + _get_tag_html("Competition", competition_level, tag_colors)
    )

    # Build score bars
    score_bars_html = (
        _get_score_bar_html("Accessibility", accessibility_score, accessibility_rating)
        + _get_score_bar_html("Visibility", visibility_score, visibility_rating)
    )

    # Format display date
    display_date = datetime.now().strftime("%d %B %Y, %I:%M %p")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Commercial Space Report - {business_type.title()} at {address}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, sans-serif;
            background-color: #f5f6fa;
            color: #2d3436;
            line-height: 1.6;
            padding: 24px;
        }}

        .report-container {{
            max-width: 860px;
            margin: 0 auto;
        }}

        .report-header {{
            background: linear-gradient(135deg, #2c3e50, #3498db);
            color: #ffffff;
            padding: 32px;
            border-radius: 12px 12px 0 0;
        }}

        .report-header h1 {{
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 8px;
        }}

        .report-header .subtitle {{
            font-size: 14px;
            opacity: 0.85;
        }}

        .business-info {{
            display: flex;
            gap: 24px;
            margin-top: 16px;
            flex-wrap: wrap;
        }}

        .business-info .info-item {{
            background: rgba(255, 255, 255, 0.15);
            padding: 8px 16px;
            border-radius: 6px;
            font-size: 14px;
        }}

        .info-item .info-label {{
            font-weight: 600;
            text-transform: uppercase;
            font-size: 10px;
            letter-spacing: 0.5px;
            display: block;
            opacity: 0.8;
        }}

        .tags-section {{
            background: #ffffff;
            padding: 20px 32px;
            border-left: 1px solid #e0e0e0;
            border-right: 1px solid #e0e0e0;
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            align-items: center;
        }}

        .tags-section .tags-label {{
            font-size: 13px;
            font-weight: 600;
            color: #636e72;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-right: 8px;
        }}

        .tag {{
            display: inline-block;
            padding: 5px 14px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
        }}

        .report-body {{
            background: #ffffff;
            border-left: 1px solid #e0e0e0;
            border-right: 1px solid #e0e0e0;
        }}

        .section {{
            padding: 28px 32px;
            border-bottom: 1px solid #f0f0f0;
        }}

        .section:last-child {{
            border-bottom: none;
        }}

        .section h2 {{
            font-size: 18px;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .section h2 .icon {{
            font-size: 20px;
        }}

        .section p {{
            font-size: 15px;
            color: #4a4a4a;
            margin-bottom: 12px;
        }}

        .cost-highlight {{
            background: #f8f9fa;
            border-left: 4px solid #3498db;
            padding: 16px 20px;
            border-radius: 0 8px 8px 0;
            margin: 16px 0;
        }}

        .cost-highlight .cost-value {{
            font-size: 22px;
            font-weight: 700;
            color: #2c3e50;
        }}

        .cost-highlight .cost-label {{
            font-size: 13px;
            color: #636e72;
        }}

        .consumers-list {{
            list-style: none;
            padding: 0;
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 8px;
        }}

        .consumers-list li {{
            background: #edf2f7;
            padding: 6px 14px;
            border-radius: 6px;
            font-size: 13px;
            color: #4a5568;
        }}

        .score-row {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
        }}

        .score-label {{
            font-size: 14px;
            font-weight: 600;
            color: #4a4a4a;
            min-width: 110px;
        }}

        .score-bar-container {{
            flex: 1;
            height: 10px;
            background: #e9ecef;
            border-radius: 5px;
            overflow: hidden;
        }}

        .score-bar {{
            height: 100%;
            border-radius: 5px;
            transition: width 0.3s ease;
        }}

        .score-value {{
            font-size: 13px;
            color: #636e72;
            min-width: 120px;
            text-align: right;
        }}

        .competition-box {{
            display: flex;
            gap: 20px;
            margin-top: 12px;
            flex-wrap: wrap;
        }}

        .competition-stat {{
            background: #f8f9fa;
            padding: 14px 20px;
            border-radius: 8px;
            text-align: center;
            min-width: 140px;
        }}

        .competition-stat .stat-value {{
            font-size: 24px;
            font-weight: 700;
            color: #2c3e50;
        }}

        .competition-stat .stat-label {{
            font-size: 12px;
            color: #636e72;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .recommendation-box {{
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            border: 1px solid #dee2e6;
            padding: 20px 24px;
            border-radius: 8px;
            margin-top: 8px;
        }}

        .recommendation-box p {{
            font-size: 15px;
            color: #2d3436;
            font-weight: 500;
            margin: 0;
        }}

        .report-footer {{
            background: #f8f9fa;
            padding: 16px 32px;
            border-radius: 0 0 12px 12px;
            border: 1px solid #e0e0e0;
            border-top: none;
            text-align: center;
            font-size: 12px;
            color: #b2bec3;
        }}

        @media (max-width: 600px) {{
            body {{
                padding: 12px;
            }}
            .report-header {{
                padding: 20px;
            }}
            .section {{
                padding: 20px;
            }}
            .business-info {{
                flex-direction: column;
                gap: 8px;
            }}
            .score-row {{
                flex-direction: column;
                align-items: flex-start;
                gap: 4px;
            }}
            .score-value {{
                text-align: left;
            }}
        }}
    </style>
</head>
<body>
    <div class="report-container">

        <div class="report-header">
            <h1>Commercial Space Analysis Report</h1>
            <p class="subtitle">Bangalore, India &mdash; Generated on {display_date}</p>
            <div class="business-info">
                <div class="info-item">
                    <span class="info-label">Business Type</span>
                    {business_type.title()}
                </div>
                <div class="info-item">
                    <span class="info-label">Area</span>
                    {int(area_sqft):,} sq ft
                </div>
                <div class="info-item">
                    <span class="info-label">Location</span>
                    {address}
                </div>
            </div>
        </div>

        <div class="tags-section">
            <span class="tags-label">Key Findings</span>
            {tags_html}
        </div>

        <div class="report-body">

            <div class="section">
                <h2><span class="icon">&#9889;</span> Electricity Cost Estimate</h2>
                <p>{electricity_summary}</p>
                <div class="cost-highlight">
                    <div class="cost-label">Estimated Monthly Cost</div>
                    <div class="cost-value">&#8377;{electricity_cost_range}</div>
                </div>
                <p style="font-size:13px;color:#636e72;margin-bottom:4px;">Top Electricity Consumers:</p>
                <ul class="consumers-list">
                    {consumers_list}
                </ul>
            </div>

            <div class="section">
                <h2><span class="icon">&#128205;</span> Location Intelligence</h2>
                <p>{gis_summary}</p>
                {score_bars_html}
            </div>

            <div class="section">
                <h2><span class="icon">&#127970;</span> Competition Overview</h2>
                <div class="competition-box">
                    <div class="competition-stat">
                        <div class="stat-value">{competitors_count}</div>
                        <div class="stat-label">Competitors Nearby</div>
                    </div>
                    <div class="competition-stat">
                        <div class="stat-value">{competition_level}</div>
                        <div class="stat-label">Competition Level</div>
                    </div>
                </div>
            </div>

            <div class="section">
                <h2><span class="icon">&#9989;</span> Overall Recommendation</h2>
                <div class="recommendation-box">
                    <p>{overall_recommendation}</p>
                </div>
            </div>

        </div>

        <div class="report-footer">
            Capstone Project &mdash; Commercial Space Analysis &mdash; Bangalore, India
        </div>

    </div>
</body>
</html>"""
