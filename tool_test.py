import asyncio
import os
import sys
from mcp import StdioServerParameters, ClientSession
from mcp.client.stdio import stdio_client
from llama_index.core.tools import FunctionTool

async def setup_agent():
    # 1. Setup paths
    python_exe = sys.executable 
    base_dir = os.path.dirname(os.path.abspath(__file__))
    server_path = os.path.join(base_dir, "mcp_server.py")

    server_params = StdioServerParameters(
        command=python_exe,
        args=[server_path],
        env=None
    )

    print(f"Connecting to MCP server at: {server_path}")
    
    try:
        # 2. Start the stdio subprocess
        async with stdio_client(server_params) as (read, write):
            # 3. Create and Initialize the Session
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("Connection established!")

                # 4. Fetch tools directly from the MCP session
                # This avoids the LlamaIndex 'TaskGroup' crash
                response = await session.list_tools()
                mcp_tools = response.tools
                
                if not mcp_tools:
                    print("Connected, but no tools found on server.")
                    return

                print(f"\nSuccessfully fetched {len(mcp_tools)} tool(s):")
                
                # 5. Convert MCP tools to LlamaIndex tools manually
                llama_tools = []
                for tool in mcp_tools:
                    print(f" - [Found] {tool.name}: {tool.description}")
                    
                    # Create a wrapper function for the tool
                    async def tool_wrapper(arguments, tool_name=tool.name):
                        result = await session.call_tool(tool_name, arguments)
                        return result.content

                    # Wrap it in LlamaIndex's FunctionTool format
                    llama_tools.append(
                        FunctionTool.from_defaults(
                            async_fn=tool_wrapper,
                            name=tool.name,
                            description=tool.description
                        )
                    )

                print("\nTools are ready for an agent!")
                # You could start your agent loop here...
                
    except Exception as e:
        print(f"\n[Error] Failed to connect:")
        # This helps see the 'real' error inside the TaskGroup
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(setup_agent())