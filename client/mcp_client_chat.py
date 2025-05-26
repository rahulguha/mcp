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
            "school-server-sse": {
                "url":url, 
                # "transport": "streamable_http",
                "transport": "sse",
                
            }
        })
    # tools = []
    tools = await client.get_tools()
    pprint.pprint ( tools, indent=3)
    agent = create_react_agent(llm, tools)
    # Chat interface
    print("Welcome to the AI Chat! Type 'exit' to quit.")
    chat_history = [] # Initialize an empty list to store chat history
    while True:
        user_message = input("You: ")
        if user_message.lower() == 'exit':
            print("Goodbye!")
            break

        # Add user message to history
        chat_history.append({"role": "user", "content": user_message})

        print("AI: Thinking...")
        try:
            # Pass the entire chat history to the agent
            result = await agent.ainvoke({"messages": chat_history})

            # Get the agent's response
            agent_response_content = result["messages"][-1].content
            print(f"AI: {agent_response_content}")

            # Add AI response to history
            chat_history.append({"role": "assistant", "content": agent_response_content})
        except Exception as e:
            print(f"Error: {e}")
            # Optionally, remove the last user message if the agent failed to respond
            chat_history.pop() if chat_history else None
    
    # result = await agent.ainvoke(
    #     {"messages": "what schools are there in list ?"}
    # )

    # print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())