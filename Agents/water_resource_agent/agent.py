"""
File: Agents/water_resource_agent/agent.py
Purpose: Defines the Water Resource Agent that estimates monthly water consumption
         and operational cost for a commercial space in Bangalore using official
         BWSSB data. It uses two tools: one to retrieve tariff information from
         the bundled BWSSB dataset, and another to estimate consumption and cost
         based on business type and area benchmarks.
"""

# Import required system modules for path manipulation
import os  # Operating system interface for file paths
import sys  # System-specific parameters and functions

# Import the main LlmAgent class from Google ADK (Agent Development Kit)
from google.adk.agents import LlmAgent  # Core agent class for creating LLM-based agents

# Add the project root directory to Python path so we can import utility modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Import utility function to load instruction files from text files
from utils.file_loader import load_instructions_file  # Helper to read instruction text files

# Import the water resource tools
from .tools.water_tariff import get_water_tariff
from .tools.water_estimator import estimate_water_usage

# Create the Water Resource Agent instance
water_resource_agent = LlmAgent(
    # Agent identifier - unique name for this agent in the system
    name="water_resource_agent",

    # AI model to use - Gemini Flash for fast tariff lookup and estimation
    model="gemini-flash-latest",

    # Load detailed instructions from external text file
    # Instructions tell the agent how to use tariff and estimator tools
    instruction=load_instructions_file(os.path.join(os.path.dirname(__file__), "instructions.txt")),

    # Load agent description from external text file
    description=load_instructions_file(os.path.join(os.path.dirname(__file__), "description.txt")),

    # Tools available to this agent:
    # get_water_tariff retrieves BWSSB tariff data from official dataset
    # estimate_water_usage calculates consumption and cost based on benchmarks
    tools=[
        get_water_tariff,
        estimate_water_usage,
    ],
)
