#!/usr/bin/env python3
"""
Entry point for the Checkson application.
This file serves as a backwards compatibility layer for direct script execution.
"""

from checkson.cli.main import app

if __name__ == "__main__":
    app()
