"""
File: Agents/report_agent/tools/report_writer.py
Purpose: Generates a styled HTML report file combining full detailed outputs from all
         sub-agents (Electricity, Water, GIS, Legal) with visual summary elements
         (colored badges, score bars, stat cards, cost highlighters).
         Writes the report to the output/ directory.
"""

import os
import re
import pathlib
from datetime import datetime


def write_report(
    electricity_details: str,
    gis_details: str,
    legal_details: str,
    water_details: str,
    business_type: str,
    area_sqft: float,
    address: str,
    electricity_cost_range: str,
    electricity_usage_level: str,
    electricity_appliances: str,
    accessibility_score: int,
    accessibility_rating: str,
    visibility_score: int,
    visibility_rating: str,
    competition_level: str,
    competitors_count: int,
    required_licenses: str,
    zoning_status: str,
    compliance_risk_level: str,
    reputation_status: str,
    water_cost_range: str,
    water_usage_level: str,
    water_consumption_kl: float,
    water_consumers: str,
    overall_recommendation: str,
) -> dict:
    """
    Generates a styled HTML report and writes it to the output/ directory.

    Args:
        electricity_details: Full text output from the Electricity Summarizer Agent.
        gis_details: Full text output from the GIS Agent.
        legal_details: Full text output from the Legal Compliance Agent.
        water_details: Full text output from the Water Resource Agent.
        business_type: Type of business (e.g., "restaurant", "bakery").
        area_sqft: Area of the commercial space in square feet.
        address: The address or locality analyzed.
        electricity_cost_range: Monthly electricity cost range string.
        electricity_usage_level: One of "Low", "Medium", or "High".
        electricity_appliances: Comma-separated list of top electricity consumers.
        accessibility_score: Accessibility score out of 100.
        accessibility_rating: One of "Excellent", "Good", "Fair", or "Poor".
        visibility_score: Visibility score out of 100.
        visibility_rating: One of "High", "Medium", or "Low".
        competition_level: One of "High", "Medium", "Low", or "Not Analyzed".
        competitors_count: Number of competitors found nearby.
        required_licenses: Comma-separated list of required licenses/permits.
        zoning_status: One of "Suitable", "Restricted", or "Unknown".
        compliance_risk_level: One of "Low", "Medium", or "High".
        reputation_status: One of "Clean", "Minor Concerns", or "Major Concerns".
        water_cost_range: Monthly water cost range string.
        water_usage_level: One of "Low", "Medium", or "High".
        water_consumption_kl: Monthly water consumption in kiloliters.
        water_consumers: Comma-separated list of top water consumers.
        overall_recommendation: Full overall recommendation text.

    Returns:
        A dictionary with status, file_path, and message.
    """
    project_root = pathlib.Path(__file__).parent.parent.parent.parent
    output_dir = project_root / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report_{timestamp}.html"
    file_path = output_dir / filename

    tag_colors = _get_tag_colors()

    html_content = _build_html(
        electricity_details=electricity_details,
        gis_details=gis_details,
        legal_details=legal_details,
        water_details=water_details,
        business_type=business_type,
        area_sqft=area_sqft,
        address=address,
        electricity_cost_range=electricity_cost_range,
        electricity_usage_level=electricity_usage_level,
        electricity_appliances=electricity_appliances,
        accessibility_score=accessibility_score,
        accessibility_rating=accessibility_rating,
        visibility_score=visibility_score,
        visibility_rating=visibility_rating,
        competition_level=competition_level,
        competitors_count=competitors_count,
        required_licenses=required_licenses,
        zoning_status=zoning_status,
        compliance_risk_level=compliance_risk_level,
        reputation_status=reputation_status,
        water_cost_range=water_cost_range,
        water_usage_level=water_usage_level,
        water_consumption_kl=water_consumption_kl,
        water_consumers=water_consumers,
        overall_recommendation=overall_recommendation,
        tag_colors=tag_colors,
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
        "Low": {"bg": "#d4edda", "text": "#155724", "border": "#c3e6cb"},
        "Medium": {"bg": "#fff3cd", "text": "#856404", "border": "#ffeeba"},
        "High": {"bg": "#f8d7da", "text": "#721c24", "border": "#f5c6cb"},
        "Excellent": {"bg": "#d4edda", "text": "#155724", "border": "#c3e6cb"},
        "Good": {"bg": "#d1ecf1", "text": "#0c5460", "border": "#bee5eb"},
        "Fair": {"bg": "#fff3cd", "text": "#856404", "border": "#ffeeba"},
        "Poor": {"bg": "#f8d7da", "text": "#721c24", "border": "#f5c6cb"},
        "Suitable": {"bg": "#d4edda", "text": "#155724", "border": "#c3e6cb"},
        "Restricted": {"bg": "#f8d7da", "text": "#721c24", "border": "#f5c6cb"},
        "Unknown": {"bg": "#e2e3e5", "text": "#383d41", "border": "#d6d8db"},
        "Clean": {"bg": "#d4edda", "text": "#155724", "border": "#c3e6cb"},
        "Minor Concerns": {"bg": "#fff3cd", "text": "#856404", "border": "#ffeeba"},
        "Major Concerns": {"bg": "#f8d7da", "text": "#721c24", "border": "#f5c6cb"},
        "Not Analyzed": {"bg": "#e2e3e5", "text": "#383d41", "border": "#d6d8db"},
        "Not Available": {"bg": "#e2e3e5", "text": "#383d41", "border": "#d6d8db"},
    }


def _get_tag_html(label: str, value: str, tag_colors: dict) -> str:
    """Generates an HTML badge span with appropriate color styling."""
    colors = tag_colors.get(value, {"bg": "#e2e3e5", "text": "#383d41", "border": "#d6d8db"})
    return (
        f'<span class="tag" style="background-color:{colors["bg"]};'
        f'color:{colors["text"]};border:1px solid {colors["border"]}">'
        f"{label}: {value}</span>"
    )


def _get_badge_html(text: str, color_bg: str, color_text: str, color_border: str) -> str:
    """Generates a simple badge for appliances/consumers/licenses."""
    return (
        f'<span class="badge" style="background-color:{color_bg};'
        f'color:{color_text};border:1px solid {color_border}">'
        f"{text}</span>"
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


def _convert_inline_markdown(text: str) -> str:
    """
    Converts inline markdown syntax to HTML within a line of text.
    Handles bold, italic, inline code, and cleans up leftover markers.
    """
    # Inline code: `code` -> <code>code</code> (do this first to protect contents)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    # Bold: **text** -> <strong>text</strong>
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    # Italic: *text* -> <em>text</em> (single asterisks, not inside words)
    text = re.sub(r"(?<!\w)\*([^*]+)\*(?!\w)", r"<em>\1</em>", text)
    # Clean up any stray asterisks that weren't matched (e.g., unbalanced)
    text = re.sub(r"\*{2,}", "", text)
    return text


def _is_table_separator(line: str) -> bool:
    """Checks if a line is a markdown table separator (e.g., |---|---|)."""
    return bool(re.match(r"^\|[\s\-:]+(\|[\s\-:]+)+\|?$", line.strip()))


def _parse_table_rows(lines: list, start_idx: int) -> tuple:
    """
    Parses consecutive markdown table lines starting from start_idx.
    Returns (html_string, number_of_lines_consumed).
    """
    table_lines = []
    idx = start_idx
    while idx < len(lines):
        stripped = lines[idx].strip()
        if stripped.startswith("|") or _is_table_separator(stripped):
            table_lines.append(stripped)
            idx += 1
        else:
            break

    if not table_lines:
        return "", 0

    html = '<div class="table-wrapper"><table class="detail-table">'
    is_first_data_row = True

    for tline in table_lines:
        if _is_table_separator(tline):
            continue
        # Split cells by pipe, strip edges
        cells = [c.strip() for c in tline.split("|")]
        # Remove empty first/last from leading/trailing pipes
        if cells and cells[0] == "":
            cells = cells[1:]
        if cells and cells[-1] == "":
            cells = cells[:-1]

        if is_first_data_row:
            html += "<thead><tr>"
            for cell in cells:
                html += f"<th>{_convert_inline_markdown(cell)}</th>"
            html += "</tr></thead><tbody>"
            is_first_data_row = False
        else:
            html += "<tr>"
            for cell in cells:
                html += f"<td>{_convert_inline_markdown(cell)}</td>"
            html += "</tr>"

    html += "</tbody></table></div>"
    return html, idx - start_idx


def _text_to_html(text: str) -> str:
    """
    Converts raw agent text output to styled HTML, preserving structure.
    Handles markdown headings, bold, italic, inline code, tables,
    bullet points, numbered lists, key-value pairs, and paragraphs.
    """
    if not text:
        return "<p>No data available.</p>"

    lines = text.strip().split("\n")
    html_parts = []
    in_list = False
    list_type = None  # "ul" or "ol"
    i = 0

    while i < len(lines):
        stripped = lines[i].strip()

        # Skip empty lines — close any open list and add spacing
        if not stripped:
            if in_list:
                html_parts.append(f"</{list_type}>")
                in_list = False
                list_type = None
            html_parts.append('<div class="spacer"></div>')
            i += 1
            continue

        # ---- Markdown tables ----
        if stripped.startswith("|"):
            if in_list:
                html_parts.append(f"</{list_type}>")
                in_list = False
                list_type = None
            table_html, consumed = _parse_table_rows(lines, i)
            if table_html:
                html_parts.append(table_html)
                i += consumed
                continue

        # ---- Headings ----
        is_heading = False

        # Markdown headings: ####, ###, ##, #
        heading_match = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading_match:
            if in_list:
                html_parts.append(f"</{list_type}>")
                in_list = False
                list_type = None
            level = len(heading_match.group(1))
            content = _convert_inline_markdown(heading_match.group(2))
            # Map markdown levels to h3-h6, capping at h6
            tag_level = min(level + 2, 6)
            html_parts.append(f'<h{tag_level} class="detail-heading">{content}</h{tag_level}>')
            is_heading = True

        # ALL CAPS section headings (not key:value)
        if not is_heading and stripped.isupper() and len(stripped) > 3 and ":" not in stripped:
            if in_list:
                html_parts.append(f"</{list_type}>")
                in_list = False
                list_type = None
            html_parts.append(f'<h4 class="detail-heading">{stripped.title()}</h4>')
            is_heading = True

        # Numbered section headings like "1. Accessibility Analysis"
        if not is_heading and re.match(r"^\d+\.\s+[A-Z]", stripped) and len(stripped) > 5:
            # Check it's not a short single-word item (those are list items)
            words_after_num = re.sub(r"^\d+\.\s*", "", stripped).split()
            if len(words_after_num) > 1:
                if in_list:
                    html_parts.append(f"</{list_type}>")
                    in_list = False
                    list_type = None
                html_parts.append(f'<h4 class="detail-heading">{_convert_inline_markdown(stripped)}</h4>')
                is_heading = True

        # Key: Value headings (like "BWSSB TARIFF CATEGORY: Non Domestic")
        if not is_heading and ":" in stripped:
            key_part = stripped.split(":")[0].strip()
            # Only treat as KV heading if key is ALL CAPS and longer than 3 chars
            if key_part.isupper() and len(key_part) > 3:
                if in_list:
                    html_parts.append(f"</{list_type}>")
                    in_list = False
                    list_type = None
                key, _, value = stripped.partition(":")
                html_parts.append(
                    f'<div class="detail-kv">'
                    f'<span class="detail-key">{_convert_inline_markdown(key.strip())}:</span> '
                    f'<span class="detail-value">{_convert_inline_markdown(value.strip())}</span>'
                    f'</div>'
                )
                is_heading = True

        if is_heading:
            i += 1
            continue

        # ---- Bullet points ----
        if stripped.startswith("- ") or stripped.startswith("* "):
            if not in_list or list_type != "ul":
                if in_list:
                    html_parts.append(f"</{list_type}>")
                html_parts.append('<ul class="detail-list">')
                in_list = True
                list_type = "ul"
            content = _convert_inline_markdown(stripped[2:].strip())
            html_parts.append(f"<li>{content}</li>")
            i += 1
            continue

        # ---- Numbered list items ----
        if re.match(r"^\d+[\.\)]\s", stripped):
            if not in_list or list_type != "ol":
                if in_list:
                    html_parts.append(f"</{list_type}>")
                html_parts.append('<ol class="detail-list">')
                in_list = True
                list_type = "ol"
            content = re.sub(r"^\d+[\.\)]\s*", "", stripped)
            content = _convert_inline_markdown(content)
            html_parts.append(f"<li>{content}</li>")
            i += 1
            continue

        # ---- Regular paragraph ----
        if in_list:
            html_parts.append(f"</{list_type}>")
            in_list = False
            list_type = None
        html_parts.append(f'<p class="detail-text">{_convert_inline_markdown(stripped)}</p>')
        i += 1

    # Close any remaining open list
    if in_list:
        html_parts.append(f"</{list_type}>")

    return "\n".join(html_parts)


def _build_badges(items_csv: str, color_bg: str, color_text: str, color_border: str) -> str:
    """Builds a row of badges from a comma-separated string."""
    badges = ""
    for item in items_csv.split(","):
        item = item.strip()
        if item:
            badges += _get_badge_html(item, color_bg, color_text, color_border)
    return badges


def _build_html(
    electricity_details: str,
    gis_details: str,
    legal_details: str,
    water_details: str,
    business_type: str,
    area_sqft: float,
    address: str,
    electricity_cost_range: str,
    electricity_usage_level: str,
    electricity_appliances: str,
    accessibility_score: int,
    accessibility_rating: str,
    visibility_score: int,
    visibility_rating: str,
    competition_level: str,
    competitors_count: int,
    required_licenses: str,
    zoning_status: str,
    compliance_risk_level: str,
    reputation_status: str,
    water_cost_range: str,
    water_usage_level: str,
    water_consumption_kl: float,
    water_consumers: str,
    overall_recommendation: str,
    tag_colors: dict,
) -> str:
    """Builds the complete HTML report string."""

    display_date = datetime.now().strftime("%d %B %Y, %I:%M %p")

    # Tags bar
    tags_html = (
        _get_tag_html("Electricity", electricity_usage_level, tag_colors)
        + _get_tag_html("Water", water_usage_level, tag_colors)
        + _get_tag_html("Accessibility", accessibility_rating, tag_colors)
        + _get_tag_html("Visibility", visibility_rating, tag_colors)
        + _get_tag_html("Competition", competition_level, tag_colors)
        + _get_tag_html("Compliance Risk", compliance_risk_level, tag_colors)
        + _get_tag_html("Zoning", zoning_status, tag_colors)
        + _get_tag_html("Reputation", reputation_status, tag_colors)
    )

    # Convert full text to HTML
    electricity_html = _text_to_html(electricity_details)
    water_html = _text_to_html(water_details)
    gis_html = _text_to_html(gis_details)
    legal_html = _text_to_html(legal_details)
    recommendation_html = _text_to_html(overall_recommendation)

    # Build badges
    appliance_badges = _build_badges(
        electricity_appliances, "#fff3e0", "#e65100", "#ffcc80"
    )
    water_consumer_badges = _build_badges(
        water_consumers, "#e3f2fd", "#0d47a1", "#90caf9"
    )
    license_badges = _build_badges(
        required_licenses, "#f3e5f5", "#4a148c", "#ce93d8"
    )

    # Score bars
    score_bars_html = (
        _get_score_bar_html("Accessibility", accessibility_score, accessibility_rating)
        + _get_score_bar_html("Visibility", visibility_score, visibility_rating)
    )

    # License count
    license_count = len([l for l in required_licenses.split(",") if l.strip()])

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
            line-height: 1.7;
            padding: 24px;
        }}

        .report-container {{
            max-width: 900px;
            margin: 0 auto;
        }}

        /* ---- Header ---- */
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

        /* ---- Tags Bar ---- */
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

        /* ---- Report Body ---- */
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
            font-size: 20px;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 18px;
            display: flex;
            align-items: center;
            gap: 8px;
            padding-bottom: 10px;
            border-bottom: 2px solid #f0f0f0;
        }}

        .section h2 .icon {{
            font-size: 22px;
        }}

        /* ---- Detail Content Styles ---- */
        .detail-content {{
            margin-bottom: 20px;
        }}

        .detail-heading {{
            font-size: 16px;
            font-weight: 700;
            color: #2c3e50;
            margin: 18px 0 8px 0;
        }}

        .detail-text {{
            font-size: 14px;
            color: #4a4a4a;
            margin-bottom: 8px;
            line-height: 1.7;
        }}

        .detail-kv {{
            font-size: 14px;
            margin-bottom: 6px;
            padding: 6px 0;
        }}

        .detail-key {{
            font-weight: 700;
            color: #2c3e50;
        }}

        .detail-value {{
            color: #4a4a4a;
        }}

        .detail-list {{
            padding-left: 20px;
            margin: 8px 0;
        }}

        .detail-list li {{
            font-size: 14px;
            color: #4a4a4a;
            margin-bottom: 4px;
            line-height: 1.6;
        }}

        .spacer {{
            height: 8px;
        }}

        .table-wrapper {{
            overflow-x: auto;
            margin: 12px 0;
        }}

        .detail-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }}

        .detail-table th {{
            background: #f1f3f5;
            font-weight: 700;
            color: #2c3e50;
            padding: 10px 14px;
            text-align: left;
            border-bottom: 2px solid #dee2e6;
        }}

        .detail-table td {{
            padding: 8px 14px;
            border-bottom: 1px solid #f0f0f0;
            color: #4a4a4a;
        }}

        .detail-table tbody tr:hover {{
            background: #f8f9fa;
        }}

        code {{
            background: #f1f3f5;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 12px;
            font-family: 'SF Mono', Monaco, Consolas, monospace;
            color: #e74c3c;
        }}

        /* ---- Visual Elements ---- */
        .cost-highlight {{
            background: #f8f9fa;
            border-left: 4px solid #3498db;
            padding: 16px 20px;
            border-radius: 0 8px 8px 0;
            margin: 20px 0;
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

        .badges-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 12px 0;
        }}

        .badges-label {{
            font-size: 13px;
            color: #636e72;
            margin-bottom: 6px;
            font-weight: 600;
        }}

        .badge {{
            display: inline-block;
            padding: 5px 14px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 600;
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
            min-width: 130px;
            text-align: right;
        }}

        .stat-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin: 16px 0;
        }}

        .stat-card {{
            background: #f8f9fa;
            padding: 16px;
            border-radius: 8px;
            text-align: center;
            border-left: 4px solid #6c5ce7;
        }}

        .stat-card .stat-value {{
            font-size: 24px;
            font-weight: 700;
            color: #2c3e50;
        }}

        .stat-card .stat-label {{
            font-size: 12px;
            color: #636e72;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .recommendation-box {{
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            border: 1px solid #dee2e6;
            padding: 24px;
            border-radius: 8px;
            margin-top: 8px;
        }}

        .recommendation-box .detail-text,
        .recommendation-box .detail-heading,
        .recommendation-box .detail-list li {{
            color: #2d3436;
        }}

        /* ---- Divider ---- */
        .visual-divider {{
            border-top: 2px dashed #e9ecef;
            margin: 20px 0;
        }}

        /* ---- Footer ---- */
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
            .stat-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="report-container">

        <!-- HEADER -->
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

        <!-- TAGS BAR -->
        <div class="tags-section">
            <span class="tags-label">Key Findings</span>
            {tags_html}
        </div>

        <div class="report-body">

            <!-- ELECTRICITY SECTION -->
            <div class="section">
                <h2><span class="icon">&#9889;</span> Electricity Cost Estimate</h2>
                <div class="detail-content">
                    {electricity_html}
                </div>
                <div class="visual-divider"></div>
                <div class="cost-highlight">
                    <div class="cost-label">Estimated Monthly Electricity Cost</div>
                    <div class="cost-value">&#8377;{electricity_cost_range}</div>
                </div>
                <div class="badges-label">Top Electricity Consumers</div>
                <div class="badges-row">
                    {appliance_badges}
                </div>
            </div>

            <!-- WATER SECTION -->
            <div class="section">
                <h2><span class="icon">&#128167;</span> Water Resource Estimate</h2>
                <div class="detail-content">
                    {water_html}
                </div>
                <div class="visual-divider"></div>
                <div class="cost-highlight" style="border-left-color:#0984e3;">
                    <div class="cost-label">Estimated Monthly Water Cost</div>
                    <div class="cost-value">&#8377;{water_cost_range}</div>
                </div>
                <div class="stat-grid">
                    <div class="stat-card" style="border-left-color:#0984e3;">
                        <div class="stat-value">{water_consumption_kl}</div>
                        <div class="stat-label">Monthly Kiloliters</div>
                    </div>
                    <div class="stat-card" style="border-left-color:#0984e3;">
                        <div class="stat-value">{water_usage_level}</div>
                        <div class="stat-label">Usage Level</div>
                    </div>
                </div>
                <div class="badges-label">Top Water Consumers</div>
                <div class="badges-row">
                    {water_consumer_badges}
                </div>
            </div>

            <!-- LOCATION INTELLIGENCE SECTION -->
            <div class="section">
                <h2><span class="icon">&#128205;</span> Location Intelligence</h2>
                <div class="detail-content">
                    {gis_html}
                </div>
                <div class="visual-divider"></div>
                {score_bars_html}
                <div class="stat-grid">
                    <div class="stat-card" style="border-left-color:#e17055;">
                        <div class="stat-value">{competitors_count}</div>
                        <div class="stat-label">Competitors Nearby</div>
                    </div>
                    <div class="stat-card" style="border-left-color:#e17055;">
                        <div class="stat-value">{competition_level}</div>
                        <div class="stat-label">Competition Level</div>
                    </div>
                </div>
            </div>

            <!-- LEGAL COMPLIANCE SECTION -->
            <div class="section">
                <h2><span class="icon">&#9878;</span> Legal Compliance</h2>
                <div class="detail-content">
                    {legal_html}
                </div>
                <div class="visual-divider"></div>
                <div class="stat-grid">
                    <div class="stat-card">
                        <div class="stat-value">{zoning_status}</div>
                        <div class="stat-label">Zoning Status</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{compliance_risk_level}</div>
                        <div class="stat-label">Compliance Risk</div>
                    </div>
                    <div class="stat-card" style="border-left-color:#e17055;">
                        <div class="stat-value">{reputation_status}</div>
                        <div class="stat-label">Location Reputation</div>
                    </div>
                    <div class="stat-card" style="border-left-color:#e17055;">
                        <div class="stat-value">{license_count}</div>
                        <div class="stat-label">Licenses Required</div>
                    </div>
                </div>
                <div class="badges-label">Required Licenses &amp; Permits</div>
                <div class="badges-row">
                    {license_badges}
                </div>
            </div>

            <!-- OVERALL RECOMMENDATION -->
            <div class="section">
                <h2><span class="icon">&#9989;</span> Overall Recommendation</h2>
                <div class="recommendation-box">
                    {recommendation_html}
                </div>
            </div>

        </div>

        <!-- FOOTER -->
        <div class="report-footer">
            Capstone Project &mdash; Commercial Space Analysis &mdash; Bangalore, India
        </div>

    </div>
</body>
</html>"""
