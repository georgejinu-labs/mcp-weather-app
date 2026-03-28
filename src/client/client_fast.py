import asyncio
from fastmcp import Client

async def main():
    url = "http://localhost:8000/mcp/"
    async with Client(url) as client:
        if client.is_connected():
            print("Connected to the server successfully!")

            tools = await client.list_tools()
            print(f"Available tools: {tools}")

            for tool in tools:
                print(f"Tool: {tool.name}, Description: {tool.description}")

            weather = await client.call_tool("get_weather", {"city": "London"})
            print(f"Weather: {weather}")

            forecast = await client.call_tool("get_forecast", {"city": "London"})
            print(f"Forecast: {forecast}")


if __name__ == "__main__":
    asyncio.run(main())
