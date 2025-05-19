
from mcp.server.fastmcp import FastMCP
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize FastMCP server
mcp = FastMCP(
    name="School List STDIO",
    instructions="""
        This server provides the list of schools available in our database.
        Call get_schools() to get the list of schools.
        """
    )

# MCP tool to fetch school data
@mcp.tool()
async def get_schools() -> dict:
    """Fetch school data from the schools API."""
    async with httpx.AsyncClient() as client:
        school_list_api_endpoint = os.getenv("SCHOOL_LIST_API_ENDPOINT")
        response = await client.get(f"{school_list_api_endpoint}")
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    mcp.run(transport="stdio")
