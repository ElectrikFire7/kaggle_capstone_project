"""
File: Agents/prompt_splitter/__init__.py
Purpose: Package initialization file for the prompt_splitter agent module.
         This file makes the prompt_splitter directory a Python package and
         imports the main agent module to make it accessible when the package is imported.

This allows other modules to import the prompt_splitter_agent using:
from Agents.prompt_splitter import agent
or
from Agents.prompt_splitter.agent import prompt_splitter_agent
"""

# Import the agent module from the current package
# This makes the prompt_splitter_agent definition available when the package is imported
from . import agent  # Imports agent.py from the same directory
