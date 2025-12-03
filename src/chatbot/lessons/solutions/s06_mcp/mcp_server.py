import requests
from enum import Enum
from fastmcp import FastMCP

mcp_server = FastMCP("my_mcp_tools")


class Currency(Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    NOK = "NOK"


# the tool is registered with the MCP server using the decorator
@mcp_server.tool
def convert_currency(
    amount: float, from_currency: Currency, to_currency: Currency
) -> float:
    """Converts money between currencies at today's rate."""
    url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency.value}&to={to_currency.value}"
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    data = response.json()
    answer = data["rates"][to_currency.value]
    return answer


if __name__ == "__main__":
    # start the server with stdio transport for local testing
    mcp_server.run(transport="stdio")
