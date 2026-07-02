"""
File: Agents/orchestrator/__init__.py
Purpose: Package initialization file for the orchestrator agent module.
         This file makes the orchestrator directory a Python package and
         imports the main agent module to make it accessible when the package is imported.

This allows other modules to import the orchestrator_agent using:
from Agents.orchestrator import agent
or
from Agents.orchestrator.agent import orchestrator_agent
"""

# Import the agent module from the current package
# This makes the orchestrator_agent definition available when the package is imported
from . import agent  # Imports agent.py from the same directory
