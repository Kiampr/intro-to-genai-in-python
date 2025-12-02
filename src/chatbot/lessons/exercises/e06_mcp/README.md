# Exercise 6: Model Context Protocol

In this exercise, you will equip the [chatbot](chatbot.py) to 3rd party tools hosted on Model Context Protocol (MCP) servers.

## Motivation

Giving agents access to tools augments their capabilities with new data sources and the ability to take actions. Self-defined tools limit this to the systems under our control or those with public APIs. What if we need to enable interaction with a black-box?

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/docs/getting-started/intro) solves this by standardizing the way tools are exposed for LLM use. Using it, a 3rd party can wrap proprietary functionality in tools that can be consumed by clients without knowledge of the internals - only the required arguments and type of the expected result.

## How do I do it?

The exercise code already instantiates an MCP client in the constructor

```python
def __init__(self):
    mcp_config = {}
    mcp_client = MCPClient(mcp_config)
    mcp_tools = mcp_client.get_tools()
```

then creates a LangChain agent equipped with the resulting tools

```python
    self._graph = create_agent(model=LLM(), tools=mcp_tools)
```

Your task is to fill in the configuration to connect to public MCP servers on the internet (using `streamable_http` transport). Be conscious that tools allow an LLM to execute code defined externally, which could be exploited for malicious purposes. Therefore, only use MCP servers from reputable vendors and take proactive steps to minimize the attack surface (e.g. hosting the app in a container or VM with limited privileges). 

Some examples suitable for this exercise:

* Microsoft Learn MCP: `https://learn.microsoft.com/api/mcp`
* Time utilities MCP: `https://time.mcp.inevitable.fyi/mcp`

## Under the hood

Instead of diving into the detailed structure of the MCP protocol, it is sufficient to discuss the high-level overview of the commnication pattern.

An MCP server can be hosted locally, on a private intranet or the public internet. A client connects to the endpoint (host and port) and sends a tool call request via a HTTP message. This can contain authentication information in the headers, while the body indicates the desired tool and the corresponding values for its arguments. The server executes the tool and returns the result as a HTTP reply. Any logging messages produced during tool execution also need to be communicated to the client via HTTP.

## Further reading

MCP clients and server implementations make use of asynchronous programming. This allows input-output-bound operations to execute concurrently without blocking the execution loop. This aspect is abstracted away in the exercise code via the `MCPClient` wrapper. Knowledge and experience with [`async`](https://realpython.com/async-io-python/) is, nonetheless, essential for production-grade applications.

🏠 [Overview](/README.md) | ◀️ [Previous exercise](/src/chatbot/lessons/exercises/e05_tool_calling/README.md) | ✅ [Solution](/src/chatbot/lessons/solutions/s06_mcp/README.md) | ▶️ [Next exercise](/src/chatbot/lessons/exercises/e07_rag/README.md)
---|---|---|---
