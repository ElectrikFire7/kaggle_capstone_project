"""
File: Agents/electricity_summarizer/__init__.py
Purpose: Package initialization file for the electricity_summarizer agent module.
         This file makes the electricity_summarizer directory a Python package and
         imports the main agent module to make it accessible when the package is imported.

This allows other modules to import the electricity_summarizer_agent using:
from Agents.electricity_summarizer import agent
or
from Agents.electricity_summarizer.agent import electricity_summarizer_agent
"""

# Import the agent module from the current package
# This makes the electricity_summarizer_agent definition available when the package is imported
from . import agent  # Imports agent.py from the same directory
