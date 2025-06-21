from mcp.server.fastmcp import FastMCP
from urllib.request import urlopen
import json

mcp = FastMCP("Hello World")


@mcp.tool()
def add(a: int, b: int) -> int:
    """
    把兩個數字相加
    """
    return a + b


@mcp.tool()
def get_tenlong_book_list():
    """
    天瓏書局暢銷書排行榜
    """
    url = "https://api.5xcamp.us/api/books/tenlong"
    return json.load(urlopen(url))
