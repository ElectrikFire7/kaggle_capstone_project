"""
File: Agents/legal_compliance_agent/__init__.py
Purpose: Package initialization file for the legal_compliance_agent module.
         This file makes the legal_compliance_agent directory a Python package and
         imports the main agent module to make it accessible when the package is imported.

This allows other modules to import the legal_compliance_agent using:
from Agents.legal_compliance_agent import agent
or
from Agents.legal_compliance_agent.agent import legal_compliance_agent
"""

# Import the agent module from the current package
from . import agent  # Imports agent.py from the same directory
