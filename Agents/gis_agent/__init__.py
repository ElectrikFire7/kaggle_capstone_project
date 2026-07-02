"""
File: Agents/gis_agent/__init__.py
Purpose: Package initialization file for the gis_agent module.
         This file makes the gis_agent directory a Python package and
         imports the main agent module to make it accessible when the package is imported.

This allows other modules to import the gis_agent using:
from Agents.gis_agent import agent
or
from Agents.gis_agent.agent import gis_agent
"""

# Import the agent module from the current package
# This makes the gis_agent definition available when the package is imported
from . import agent  # Imports agent.py from the same directory
