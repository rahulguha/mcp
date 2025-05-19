import asyncio
import os

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
import pprint

load_dotenv()

llm = ChatOpenAI()


async def main():


    url = os.getenv("SSE_SERVER_ENDPOINT")
    client = MultiServerMCPClient(
        {
            # "school-list": {
            #     "command": "uv",
            #     "args":["run", "/Users/rahul/code/llm-projects/mcp/servers/school_server/stdio/school_list_stdio.py"],
            #     "transport": "stdio",
            # },
            "school-server-sse": {
                "url":url, 
                # "url": "http://localhost:3501/sse",
                # "transport": "streamable_http",
                "transport": "sse",
                
            }
        })
    # tools = []
    tools = await client.get_tools()
    pprint.pprint ( tools, indent=3)
    agent = create_react_agent(llm, tools)
    result = await agent.ainvoke(
        {"messages": "Tell me about research opportunities for aersopace engineering"}
    )

    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())