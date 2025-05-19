
from mcp.server.fastmcp import FastMCP
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize FastMCP server
mcp = FastMCP(
    name="School List",
    port=3501,
    on_duplicate_tools="error" # Set duplicate handling
    )

# MCP tool to fetch school data
@mcp.tool()
async def get_schools() -> dict:
    """This tool fetches school data from the schools API."""
    async with httpx.AsyncClient() as client:
        print("calling api")
        # school_list_api_endpoint = os.getenv("SCHOOL_LIST_API_ENDPOINT")
        school_list_api_endpoint = os.getenv("SCHOOL_LIST_API_ENDPOINT", "http://school-list-api:3100/schools")
        response = await client.get(f"{school_list_api_endpoint}")
        # response = await client.get("http://localhost:3100/schools")
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_school_rag(query: str) -> dict:
    """
    This tool executes the RAG pipeline and gets relevant text which will be sent to LLM.
    Use this tool for any school related query around cost, course curriculum, accomodation, location, admission etc
    """
    payload = {"query": query}
    print(f"Sending POST with payload: {payload}")
    async with httpx.AsyncClient() as client_rag:
        # school_rag_api_endpoint = os.getenv("SCHOOL_RAG_API_ENDPOINT")
        school_rag_api_endpoint = os.getenv("SCHOOL_RAG_API_ENDPOINT", "http://school-rag-api:3200/chat")
        print(f"POST to: {school_rag_api_endpoint}")
        try:
            response = await client_rag.post(
                url=school_rag_api_endpoint,
                json=payload,
                timeout=10.0
            )
            print(f"Received status: {response.status_code}, response: {response.json()}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code} - {e}")
            raise
        except httpx.RequestError as e:
            print(f"Request error: {e}")
            raise


if __name__ == "__main__":
    # mcp.run(transport="streamable-http")
    mcp.run(transport="sse")
