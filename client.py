from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent  
from langchain_groq import ChatGroq

from dotenv import load_dotenv
load_dotenv()

import asyncio
import os


async def main():
    client = MultiServerMCPClient(
        {
            "mathServer": {
                "command": "python",
                "args": ["mathServer.py"],
                "transport": "stdio",
            },
            "weatherServer": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable-http",  
            }
        }
    )

    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    tools = await client.get_tools()

   
    model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

    agent = create_agent(
        model=model,
        tools=tools
    )

 
    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what is 3 + 5?"}]}
    )

    print("Math response:", math_response["messages"][-1].content)

    weather_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what is the weather in California?"}]}
    )

    print("Weather response:", weather_response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())