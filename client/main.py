import asyncio
import os


from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI()

stdio_server_params = StdioServerParameters(
    command="uv",
    args=["run", "/Users/rahul/code/llm-projects/mcp/servers/school_server/stdio/school_list_stdio.py"],
)

async def main():
    async with stdio_client(stdio_server_params) as (read,write):    
        async with ClientSession(read_stream=read, write_stream=write) as session:
            await session.initialize()
            print("session initialized")
            tools = await load_mcp_tools(session)
            print(tools)
            agent = create_react_agent(llm,tools)

            result = await agent.ainvoke({"messages": [HumanMessage(content="get me list of schools that teach aerospace engineering")]})
            print(result["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())
