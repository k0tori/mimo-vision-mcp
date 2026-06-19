"""Allow running as python -m mimo_vision_mcp."""

import asyncio

from mimo_vision_mcp.server import main

if __name__ == "__main__":
    asyncio.run(main())
