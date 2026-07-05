"""
File: Agents/legal_compliance_agent/agent.py
Purpose: Defines the Legal Compliance Agent that uses Google Search to research legal
         requirements, zoning regulations, licensing needs, and location reputation
         for a commercial business in Bangalore. It leverages the ADK-provided
         google_search tool to gather real-time legal and reputation information.
"""

# Import required system modules for path manipulation
import os  # Operating system interface for file paths
import sys  # System-specific parameters and functions

# Import the main LlmAgent class from Google ADK (Agent Development Kit)
from google.adk.agents import LlmAgent  # Core agent class for creating LLM-based agents

# Import the ADK-provided Google Search tool
from google.adk.tools import google_search  # Built-in Google Search tool

# Add the project root directory to Python path so we can import utility modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Import utility function to load instruction files from text files
from utils.file_loader import load_instructions_file  # Helper to read instruction text files

# Create the Legal Compliance Agent instance
legal_compliance_agent = LlmAgent(
    # Agent identifier - unique name for this agent in the system
    name="legal_compliance_agent",

    # AI model to use - Gemini Flash for fast search-based research
    model="gemini-flash-latest",

    # Load detailed instructions from external text file
    # Instructions tell the agent what to search for and how to structure findings
    instruction=load_instructions_file(os.path.join(os.path.dirname(__file__), "instructions.txt")),

    # Load agent description from external text file
    description=load_instructions_file(os.path.join(os.path.dirname(__file__), "description.txt")),

    # Tools available to this agent:
    # google_search is the ADK-provided built-in tool for web search
    tools=[
        google_search,
    ],
)
