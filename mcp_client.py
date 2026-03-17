import asyncio
import os
import sys
from mcp import StdioServerParameters, ClientSession
from mcp.client.stdio import stdio_client
from llama_index.llms.ollama import Ollama

async def run_manual_agent():
    python_exe = sys.executable 
    server_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mcp_server.py")
    server_params = StdioServerParameters(command=python_exe, args=[server_path], env=None)
    llm = Ollama(model="qwen3.5:0.8b", request_timeout=300.0)

    print("--- Connecting to MCP Server ---")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("Connected! You are now talking to the database.")

            while True:
                user_query = input("\nWhat would you like to know? (or 'exit'): ")
                if user_query.lower() in ['exit', 'quit']: break
                prompt = f"Based on the user's request: '{user_query}', write a single SQLite query. Return ONLY the SQL code, no explanation."
                response = await llm.acomplete(prompt)
                sql = response.text.strip().replace("```sql", "").replace("```", "")
                print(f"Generated SQL: {sql}")

                try:
                    result = await session.call_tool("query_data", {"sql": sql})
                    output = "".join([c.text for c in result.content if hasattr(c, 'text')])
                    print(f"Database Result:\n{output}")
                except Exception as e:
                    print(f"Error running SQL: {e}")

if __name__ == "__main__":
    asyncio.run(run_manual_agent())