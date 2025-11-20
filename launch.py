#!/usr/bin/env python3
"""
Launch script for the Story Types Flask application.

This script starts the Flask web server for the Story Types application.

NOTE: For easier startup with automatic virtual environment setup and dependency
installation, use the start.sh script instead:
    ./start.sh
"""

import os
import sys

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app


def main():
    """Launch the Flask application."""
    print("Starting Story Types Flask Application...")
    print("Open your web browser to http://localhost:5000")
    print("Press Ctrl+C to stop the server")

    try:
        app.run(debug=True, host="0.0.0.0", port=5000)
    except KeyboardInterrupt:
        print("\nShutting down the server...")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
