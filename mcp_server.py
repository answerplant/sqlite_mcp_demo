"""
Demo SQLite MCP in Python
https://github.com/arjunprabhulal/mcp-llama3-client/blob/main/mcp_flight_client.py

https://www.reddit.com/r/AI_Agents/comments/1jd9gzv/learn_mcp_by_building_an_sqlite_ai_agent/
https://github.com/prayanks/mcp-sqlite-server/blob/main/sqlite_sdio_mcp_server.py
https://gofastmcp.com/getting-started/welcome
"""

import sqlite3
from setup import setup_db
from mcp.server.fastmcp import FastMCP

setup_db("answer", "capabilities")
from loguru import logger

mcp = FastMCP("SQL Agent Server")


@mcp.tool()
def query_data(sql: str) -> str:
    """Execute SQL queries safely."""
    logger.info(
        f"Executing SQL query: {sql}"
    )
    conn = sqlite3.connect(
        "./answer.db"
    )
    try:
        result = conn.execute(
            sql
        ).fetchall()
        conn.commit()
        return "\n".join(
            str(row) for row in result
        )
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        conn.close()


if __name__ == "__main__":
    print("Starting server...")
    mcp.run(transport="stdio")
