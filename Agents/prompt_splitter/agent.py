"""
File: Agents/prompt_splitter/agent.py
Purpose: Defines the Prompt Splitter Agent that parses free-form user queries about
         commercial spaces in Bangalore and generates structured sub-prompts for the
         Electricity Summarizer Agent and GIS Agent. This agent acts as the entry point
         before the ParallelResearchAgent, ensuring each sub-agent receives a tailored
         prompt with exactly the inputs it needs.

This is a pure LLM agent with no tools — it relies on the LLM's language understanding
to extract business_type, area_sqft, and address from conversational input and reformat
them into structured sub-prompts.
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

# Create the Prompt Splitter Agent instance
prompt_splitter_agent = LlmAgent(
    # Agent identifier - unique name for this agent in the system
    name="prompt_splitter_agent",

    # AI model to use - Gemini 2.0 Flash for fast prompt parsing and reformatting
    model="gemini-2.0-flash",

    # Load detailed instructions from external text file
    # Instructions tell the agent how to parse user queries and generate sub-prompts
    instruction=load_instructions_file("Agents/prompt_splitter/instructions.txt"),

    # Load agent description from external text file
    # Provides a brief summary of this agent's prompt splitting role
    description=load_instructions_file("Agents/prompt_splitter/description.txt"),
)
