from mcp.server.fastmcp import FastMCP
from app.tools.registry import calculate, get_utc_time

mcp = FastMCP("ai-voice-agent-tools")

@mcp.tool()
def calculator(expression: str) -> dict:
    """Safely evaluate a basic arithmetic expression."""
    return calculate(expression)

@mcp.tool()
def utc_time() -> dict:
    """Return current UTC time."""
    return get_utc_time()

if __name__ == "__main__":
    mcp.run(transport="stdio")
