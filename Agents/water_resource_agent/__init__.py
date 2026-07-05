"""
File: Agents/water_resource_agent/__init__.py
Purpose: Package initialization file for the water_resource_agent module.
         This file makes the water_resource_agent directory a Python package and
         imports the main agent module to make it accessible when the package is imported.

This allows other modules to import the water_resource_agent using:
from Agents.water_resource_agent import agent
or
from Agents.water_resource_agent.agent import water_resource_agent
"""

# Import the agent module from the current package
from . import agent  # Imports agent.py from the same directory
