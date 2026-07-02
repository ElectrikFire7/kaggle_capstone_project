"""
File: Agents/orchestrator/agent.py
Purpose: Defines the top-level Orchestrator Agent that runs the full commercial space
         analysis pipeline as a sequential workflow using Google ADK's SequentialAgent.

         The pipeline executes three stages in order:
         1. Prompt Splitter — Parses the free-form user query and extracts structured fields
         2. Parallel Research Agent — Runs Electricity Summarizer and GIS Agent concurrently
         3. Report Agent — Generates a styled HTML report from the combined findings

         Each stage's output is passed as context to the next stage automatically.
"""

# Import required system modules for path manipulation
import os  # Operating system interface for file paths
import sys  # System-specific parameters and functions

# Import the SequentialAgent class from Google ADK (Agent Development Kit)
# SequentialAgent runs sub-agents one after another, passing context between them
from google.adk.agents import SequentialAgent  # Workflow agent for sequential execution

# Add the project root directory to Python path so we can import agent modules
# This allows importing from the Agents directory two levels up from current file
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Import utility function to load instruction files from text files
from utils.file_loader import load_instructions_file  # Helper to read instruction text files

# Import the three sub-agents that form the sequential pipeline
from Agents.prompt_splitter.agent import prompt_splitter_agent
from Agents.parallel_research_agent.agent import parallel_research_agent
from Agents.report_agent.agent import report_agent

# Create the Orchestrator Agent instance
root_agent = SequentialAgent(
    # Agent identifier - unique name for this agent in the system
    name="orchestrator_agent",

    # Sub-agents executed in order:
    # 1. prompt_splitter_agent — parses user input into structured sub-prompts
    # 2. parallel_research_agent — runs electricity + GIS analysis in parallel
    # 3. report_agent — generates the final HTML report
    sub_agents=[
        prompt_splitter_agent,
        parallel_research_agent,
        report_agent,
    ],

    # Load agent description from external text file
    description=load_instructions_file(os.path.join(os.path.dirname(__file__), "description.txt")),
)
