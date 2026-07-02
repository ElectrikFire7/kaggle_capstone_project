"""
File: Agents/parallel_research_agent/__init__.py
Purpose: Package initialization file for the parallel_research_agent module.
         This file makes the parallel_research_agent directory a Python package and
         imports the main agent module to make it accessible when the package is imported.

This allows other modules to import the parallel_research_agent using:
from Agents.parallel_research_agent import agent
or
from Agents.parallel_research_agent.agent import parallel_research_agent
"""

# Import the agent module from the current package
# This makes the parallel_research_agent definition available when the package is imported
from . import agent  # Imports agent.py from the same directory
