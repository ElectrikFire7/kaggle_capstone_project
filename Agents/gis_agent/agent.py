"""
File: Agents/gis_agent/agent.py
Purpose: Defines the GIS Agent that performs spatial analysis of commercial locations
         in Bangalore. Geocodes addresses, analyzes road networks, scores accessibility
         and visibility, and detects nearby competition using OpenStreetMap data.

This agent uses Google ADK skills for progressive disclosure and tool orchestration:
1. Loads the spatial_analysis skill from the skills directory
2. Wraps individual tools (geocoder, road_network, accessibility, visibility, competition)
   into a SkillToolset for the agent to use
3. The agent follows the skill instructions to perform the spatial analysis flow
"""

# Import required system modules for path manipulation
import os  # Operating system interface for file paths
import sys  # System-specific parameters and functions
import pathlib  # Object-oriented path handling

# Import the main LlmAgent class from Google ADK (Agent Development Kit)
from google.adk.agents import LlmAgent  # Core agent class for creating LLM-based agents

# Import ADK skill loading utilities
from google.adk.skills import load_skill_from_dir  # Loads a skill definition from a directory
from google.adk.tools.skill_toolset import SkillToolset  # Wraps skills into agent-usable toolsets

# Add the project root directory to Python path so we can import utility modules
# This allows importing from the utils directory two levels up from current file
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Import utility function to load instruction files from text files
from utils.file_loader import load_instructions_file  # Helper to read instruction text files

# Import the individual tools that the agent will use
from gis_agent.tools.geocoder import geocode_address
from gis_agent.tools.road_network import get_nearby_roads
from gis_agent.tools.accessibility import score_accessibility
from gis_agent.tools.visibility import score_visibility
from gis_agent.tools.competition import find_competition

# ---- Load the Spatial Analysis Skill ----
# The skill provides structured instructions for the agent to follow
# when performing a spatial analysis (progressive disclosure: L1 → L2 → L3)
skill_path = pathlib.Path(__file__).parent / "skills" / "spatial-analysis"
spatial_analysis_skill = load_skill_from_dir(skill_path)

# Create a SkillToolset that bundles the skill with the functional tools
# This allows the agent to access both the skill instructions and the tools
gis_toolset = SkillToolset(
    skills=[spatial_analysis_skill],
)

# Create the GIS Agent instance
gis_agent = LlmAgent(
    # Agent identifier - unique name for this agent in the system
    name="gis_agent",

    # AI model to use - Gemini 2.0 Flash for fast spatial analysis
    model="gemini-flash-latest",

    # Load detailed instructions from external text file
    # Instructions tell the agent how to use the skill and tools together
    instruction=load_instructions_file(os.path.join(os.path.dirname(__file__), "instructions.txt")),

    # Load agent description from external text file
    # Provides a brief summary of this agent's spatial analysis role
    description=load_instructions_file(os.path.join(os.path.dirname(__file__), "description.txt")),

    # Tools available to this agent:
    # 1. SkillToolset with the spatial_analysis skill for structured guidance
    # 2. Individual functional tools for geocoding, road analysis, scoring, etc.
    tools=[
        gis_toolset,
        geocode_address,
        get_nearby_roads,
        score_accessibility,
        score_visibility,
        find_competition,
    ],
)
