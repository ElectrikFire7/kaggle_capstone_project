"""
File: Agents/report_agent/agent.py
Purpose: Defines the Report Agent that takes the combined outputs from the Electricity
         Summarizer Agent and GIS Agent and generates a styled HTML report file in the
         output/ directory. The report presents findings in a structured layout with
         colored tags for key metrics like cost level, accessibility, visibility, and
         competition.

This agent uses a single tool (write_report) to generate the HTML file. The LLM's role
is to parse the sub-agent outputs, extract structured fields, and call the tool with
the correct parameters.
"""

# Import required system modules for path manipulation
import os  # Operating system interface for file paths
import sys  # System-specific parameters and functions

# Import the main LlmAgent class from Google ADK (Agent Development Kit)
from google.adk.agents import LlmAgent  # Core agent class for creating LLM-based agents

# Add the project root directory to Python path so we can import utility modules
# This allows importing from the utils directory two levels up from current file
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Import utility function to load instruction files from text files
from utils.file_loader import load_instructions_file  # Helper to read instruction text files

# Import the report writing tool
from .tools.report_writer import write_report

# Create the Report Agent instance
report_agent = LlmAgent(
    # Agent identifier - unique name for this agent in the system
    name="report_agent",

    # AI model to use - Gemini 2.0 Flash for fast output parsing and tool invocation
    model="gemini-flash-latest",

    # Load detailed instructions from external text file
    # Instructions tell the agent how to parse sub-agent outputs and call write_report
    instruction=load_instructions_file(os.path.join(os.path.dirname(__file__), "instructions.txt")),

    # Load agent description from external text file
    # Provides a brief summary of this agent's report generation role
    description=load_instructions_file(os.path.join(os.path.dirname(__file__), "description.txt")),

    # Tools available to this agent:
    # write_report generates the styled HTML file in the output/ directory
    tools=[
        write_report,
    ],
)
