#!/usr/bin/env python3
"""
Startup script for ArXiv Research Hub Backend API
"""
import uvicorn
import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(__file__))

if __name__ == "__main__":
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except OSError as e:
        print(f"Error: Port 8000 may already be in use. {e}")
        sys.exit(1)
    except ImportError as e:
        print(f"Error: Failed to import application. {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)