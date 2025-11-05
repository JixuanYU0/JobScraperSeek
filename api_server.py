"""API Server entry point for Seek Job Scraper."""

import uvicorn
import argparse
from pathlib import Path


def main():
    """Run the FastAPI server."""
    parser = argparse.ArgumentParser(description="Seek Job Scraper API Server")
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind to (default: 8000)"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of worker processes (default: 1)"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Seek Job Scraper API Server")
    print("=" * 60)
    print(f"Server starting on http://{args.host}:{args.port}")
    print(f"API Documentation: http://{args.host}:{args.port}/api/docs")
    print(f"ReDoc: http://{args.host}:{args.port}/api/redoc")
    print("=" * 60)

    uvicorn.run(
        "src.api.app:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        workers=args.workers if not args.reload else 1,  # reload doesn't work with multiple workers
        log_level="info"
    )


if __name__ == "__main__":
    main()
