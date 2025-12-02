# Solution 6: Model Context Protocol

In the solution, we connect the [chatbot](chatbot.py) to two public Model Context Protocol (MCP) servers.

They are configured by specifying the URL and transport as `streamable_http`:

```python
mcp_config = {
    "microsoft_learn" : {
        "url": "https://learn.microsoft.com/api/mcp",
        "transport": "streamable_http",
    },
    "time_tools": {
        "url": "https://time.mcp.inevitable.fyi/mcp",
        "transport": "streamable_http",
        }
}
```

## Verification

If the connection to the MCP servers is successful, the available tools will be listed in a log message at chatbot creation.

Ask questions about Microsoft software or time conversions and verify that the tools get called by observing the status updates.

🏠 [Overview](/README.md) | ◀️ [Back to exercise](/src/chatbot/lessons/exercises/e06_mcp/README.md) | ▶️ [Next exercise](/src/chatbot/lessons/exercises/e07_rag/README.md)
---|---|---
