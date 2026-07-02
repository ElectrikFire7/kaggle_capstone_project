"""
File: Agents/electricity_summarizer/agent.py
Purpose: Defines the Electricity Summarizer Agent that estimates electricity consumption
         and monthly cost for commercial spaces in Bangalore. Uses BESCOM tariff data,
         location-based adjustments, and business-specific consumption benchmarks.

This agent uses Google ADK skills for progressive disclosure and tool orchestration:
1. Loads the electricity_estimation skill from the skills directory
2. Wraps individual tools (tariff, load_estimator, consumption, billing, location)
   into a SkillToolset for the agent to use
3. The agent follows the skill instructions to perform the estimation flow
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
from Agents.electricity_summarizer.tools.tariff import get_tariff
from Agents.electricity_summarizer.tools.load_estimator import estimate_load
from Agents.electricity_summarizer.tools.consumption import calculate_consumption
from Agents.electricity_summarizer.tools.billing import calculate_bill
from Agents.electricity_summarizer.tools.location import get_location_adjustment

# ---- Load the Electricity Estimation Skill ----
# The skill provides structured instructions for the agent to follow
# when performing an electricity estimation (progressive disclosure: L1 → L2 → L3)
skill_path = pathlib.Path(__file__).parent / "skills" / "electricity-estimation"
electricity_estimation_skill = load_skill_from_dir(skill_path)

# Create a SkillToolset that bundles the skill with the functional tools
# This allows the agent to access both the skill instructions and the tools
electricity_toolset = SkillToolset(
    skills=[electricity_estimation_skill],
)

# Create the Electricity Summarizer Agent instance
electricity_summarizer_agent = LlmAgent(
    # Agent identifier - unique name for this agent in the system
    name="electricity_summarizer_agent",

    # AI model to use - Gemini 2.0 Flash for fast, capable estimation
    model="gemini-flash-latest",

    # Load detailed instructions from external text file
    # Instructions tell the agent how to use the skill and tools together
    instruction=load_instructions_file(os.path.join(os.path.dirname(__file__), "instructions.txt")),

    # Load agent description from external text file
    # Provides a brief summary of this agent's electricity estimation role
    description=load_instructions_file(os.path.join(os.path.dirname(__file__), "description.txt")),

    # Tools available to this agent:
    # 1. SkillToolset with the electricity_estimation skill for structured guidance
    # 2. Individual functional tools for tariff lookup, load estimation, etc.
    tools=[
        electricity_toolset,
        get_tariff,
        estimate_load,
        calculate_consumption,
        calculate_bill,
        get_location_adjustment,
    ],
)
