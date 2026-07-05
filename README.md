# Commercial Space Analyzer - Bangalore

A multi-agent AI system that surveys a commercial location in Bangalore for starting or expanding a business — in minutes, not days.

Instead of manually searching for electricity tariffs, visiting the site to assess foot traffic, reading through BWSSB water rate documents, or consulting a lawyer about permits, this tool does it all at once. Provide a business type, area, and address, and four specialized AI agents run in parallel to deliver a comprehensive, styled HTML report covering electricity costs, water expenses, location intelligence, and legal compliance.

Built on [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/) with Gemini models.

---

## How to Run

### 1. Clone the repository

```bash
git clone <repo-url>
cd kaggle_capstone_project
```

### 2. Python version

Ensure Python **3.11.9** is installed on your system.

### 3. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Set up your API key

Create a `.env` file inside the `Agents/` directory:

```
GOOGLE_API_KEY=your-gemini-api-key-here
```

### 6. Navigate to the Agents directory

```bash
cd Agents
```

### 7. Launch the ADK web interface

```bash
adk web
```

### 8. Use the application

- Open the URL shown in the terminal (typically `http://localhost:8000`) in a browser
- Select **orchestrator** from the agent dropdown
- Enter a query, for example:

> I want to open a 600 sqft salon near Begur Koppa Road, next to Prestige Song of South, Bangalore

- Watch the agents work through the pipeline
- Once complete, retrieve the generated report from the `output/` folder and open the `.html` file in a browser to view the styled results

---

## Agent Pipeline

```
                          User Query
                              |
                              v
                    +-------------------+
                    |  Prompt Splitter  |
                    |    (LlmAgent)     |
                    +-------------------+
                              |
              Extracts business_type, area_sqft, address
              Generates 4 tailored sub-prompts
                              |
                              v
                 +------------------------+
                 |  Parallel Research     |
                 |    (ParallelAgent)     |
                 +------------------------+
                    |    |    |    |
         +----------+    |    |    +----------+
         |           |---+    |               |
         v           v        v               v
  +-----------+  +-----+  +----------+   +------------+
  |Electricity|  | GIS |  |  Legal   |   |   Water    |
  |Summarizer |  |Agent|  |Compliance|   |  Resource  |
  | (LlmAgent)|  |     |  |  Agent   |   |  (LlmAgent)|
  +-----------+  +-----+  +----------+   +------------+
         |          |         |              |
         +----------+---------+--------------+
                              |
                              v
                    +-------------------+
                    |   Report Agent    |
                    |    (LlmAgent)     |
                    +-------------------+
                              |
                              v
                   output/report_<ts>.html
```

**Orchestrator** (`SequentialAgent`) drives the full pipeline top to bottom.

---

## Sub-Agents

### Electricity Summarizer Agent

Estimates monthly electricity consumption and cost for a commercial space using BESCOM tariff data, business-specific load benchmarks, and location adjustments.

| Tool | Description |
|------|-------------|
| `get_tariff` | Reads BESCOM commercial tariff slabs and rates from bundled data |
| `estimate_load` | Calculates connected electrical load based on business type and area |
| `calculate_consumption` | Estimates monthly kWh consumption from load and operating hours |
| `calculate_bill` | Computes the monthly bill using BESCOM slab-based tariff structure |
| `get_location_adjustment` | Applies location-specific multipliers for different Bangalore zones |

---

### GIS Agent

Performs spatial analysis of the business location using OpenStreetMap data — evaluating road access, storefront visibility, and nearby competition.

| Tool | Description |
|------|-------------|
| `geocode_address` | Converts a natural language address to latitude/longitude coordinates via Nominatim |
| `get_nearby_roads` | Retrieves road network data within a radius to assess connectivity |
| `score_accessibility` | Scores location accessibility based on road proximity, network density, and connectivity |
| `score_visibility` | Scores storefront visibility based on road frontage, foot traffic, and landmark proximity |
| `find_competition` | Detects competing businesses of the same type within a configurable radius |

---

### Legal Compliance Agent

Researches legal requirements, zoning regulations, licensing needs, and location reputation using Google Search.

| Tool | Description |
|------|-------------|
| `google_search` | ADK built-in tool — searches for Bangalore/Karnataka-specific permits, zoning rules, and area reputation |

---

### Water Resource Agent

Estimates monthly water consumption and operational cost using official BWSSB (Bangalore Water Supply and Sewerage Board) data and business-specific benchmarks.

| Tool | Description |
|------|-------------|
| `get_water_tariff` | Reads BWSSB tariff category, slab rates, and consumption statistics from bundled official data |
| `estimate_water_usage` | Calculates monthly water consumption in kiloliters and cost using per-business-type benchmarks and BWSSB slab pricing |
