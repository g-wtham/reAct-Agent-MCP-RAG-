import asyncio
from fastmcp import Client

client = Client("http://127.0.0.1:8000/mcp")

async def main(prompt_text: str):
    """Connects to the server and calls the 'retrieve_answer' tool."""
    async with client:
        print(f"Connected to MCP Server: {await client.ping()}")
        
        # 3. Call the tool defined in your server
        print(f"Calling tool 'retrieve_answer' with prompt: '{prompt_text}'")
        
        result = await client.call_tool("retrieve_answer", {"prompt": prompt_text})
        
        print("\n--- Tool Response ---")
        print(result)

if __name__ == '__main__':
    query = "Projects done by person!?"
    asyncio.run(main(query))