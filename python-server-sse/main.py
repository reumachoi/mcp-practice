from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Mount, Route
import uvicorn 

# Initialize FastMCP server
mcp = FastMCP("weather")

def health_check(request):
    return PlainTextResponse('OK')

app = Starlette(
    routes=[
        Route('/health', health_check, methods=["GET"]),
        Mount('/', app=mcp.sse_app()),
    ]
)

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
    """Echo a message as a resource"""
    return f"Resource echo: {message}"


@mcp.tool()
def calculate_bmi(weightKg: int, heightM: int) -> str:
    """Echo a message as a tool"""
    return f"Tool echo: {(weightKg / (heightM * heightM))}"


@mcp.prompt()
def echo_prompt(message: str) -> str:
    """Create an echo prompt"""
    return f"Please process this message: {message}"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
