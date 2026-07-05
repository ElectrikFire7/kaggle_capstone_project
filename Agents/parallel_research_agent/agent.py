"""
File: Agents/parallel_research_agent/agent.py
Purpose: Defines the Parallel Research Agent that runs the Electricity Summarizer Agent
         and GIS Agent concurrently using Google ADK's ParallelAgent. Given a commercial
         space query (business type, area, address in Bangalore), it dispatches both
         analyses in parallel and returns combined results — electricity cost estimates
         and spatial location intelligence.

This agent uses Google ADK's ParallelAgent workflow agent:
1. Takes the two existing LlmAgent sub-agents as sub_agents
2. Runs them simultaneously when invoked
3. Merges their outputs into a unified research report
"""

# Import required system modules for path manipulation
import os  # Operating system interface for file paths
import sys  # System-specific parameters and functions

# Import the ParallelAgent class from Google ADK (Agent Development Kit)
# ParallelAgent is a workflow agent that runs multiple sub-agents concurrently
from google.adk.agents import ParallelAgent  # Workflow agent for parallel execution

# Add the project root directory to Python path so we can import agent modules
# This allows importing from the Agents directory two levels up from current file
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Import utility function to load instruction files from text files
from utils.file_loader import load_instructions_file  # Helper to read instruction text files

# Import the four sub-agents that will run in parallel
from electricity_summarizer.agent import electricity_summarizer_agent
from gis_agent.agent import gis_agent
from legal_compliance_agent.agent import legal_compliance_agent
from water_resource_agent.agent import water_resource_agent

# Create the Parallel Research Agent instance
parallel_research_agent = ParallelAgent(
    # Agent identifier - unique name for this agent in the system
    name="parallel_research_agent",

    # Sub-agents that will be executed in parallel
    # All four agents receive the same user query and run concurrently
    sub_agents=[
        electricity_summarizer_agent,
        gis_agent,
        legal_compliance_agent,
        water_resource_agent,
    ],

    # Load agent description from external text file
    # Provides a brief summary of this agent's parallel research role
    description=load_instructions_file(os.path.join(os.path.dirname(__file__), "description.txt")),
)
