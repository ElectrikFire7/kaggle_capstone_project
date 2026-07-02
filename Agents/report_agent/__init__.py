"""
File: Agents/report_agent/__init__.py
Purpose: Package initialization file for the report_agent module.
         This file makes the report_agent directory a Python package and
         imports the main agent module to make it accessible when the package is imported.

This allows other modules to import the report_agent using:
from Agents.report_agent import agent
or
from Agents.report_agent.agent import report_agent
"""

# Import the agent module from the current package
# This makes the report_agent definition available when the package is imported
from . import agent  # Imports agent.py from the same directory
