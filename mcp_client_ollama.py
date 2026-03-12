import nest_asyncio
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec

nest_asyncio.apply()

from llama_index.llms.ollama import Ollama
from llama_index.core import Settings

llm = Ollama(model="llama3.2", request_timeout=120.0)
Settings.llm = llm

mcp_client = BasicMCPClient("http://127.0.0.1:8000/stdio")
mcp_tools = McpToolSpec(client=mcp_client)

# https://www.youtube.com/watch?v=C64rVY1eN8k
# https://github.com/patchy631/ai-engineering-hub/blob/main/llamaindex-mcp/ollama_client.ipynb

tools = await mcp_tools.to_tool_list_async()