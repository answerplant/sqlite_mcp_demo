# SQLite MCP Demo in Python

Quick demo to show how an MCP allows an LLM-based chatbot to query a SQLite database.
This uses qwen3.5:0.8b as the agent model.

1. Install Ollama
2. Pull the model

``` sh
ollama pull qwen3.5:0.8b
```

Set up your virtual environment, then start the server and client.

``` sh
python .\mcp_server.py 
python .\mcp_client.py 
```

TODO: Standardise and expand logging