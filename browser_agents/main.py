from langchain_openai import ChatOpenAI
from typing import TypedDict
from typing import Annotated
from operator import add
from langgraph.graph import StateGraph
from langgraph.graph import START, END
import asyncio
from dotenv import load_dotenv
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode,tools_condition
from langchain_mcp_adapters.client import MultiServerMCPClient
from rich import print
from langchain_core.messages import HumanMessage

load_dotenv()
llm = ChatOpenAI(
    model="gpt-4.1",
    temperature=0
)



# for i in browser_tools:
#     print(i.name)
#     print(i.description)
    
class State(TypedDict):
    messages: Annotated[list, add]

async def get_tools():
    client = MultiServerMCPClient({
        "playwright": {
            "transport": "stdio",
            "command": "npx",
            "args": ["-y", "@playwright/mcp@latest", "--isolated"],
        }
    })
    return await client.get_tools()


async def chatbot(state: State):
    browser_llm = llm.bind_tools(browser_tools)
    llm_response = await browser_llm.ainvoke(state["messages"])
    print("contentt: ", llm_response.content)
    print("tool calls: ", llm_response.tool_calls)
    print("this is our message lol: ", state["messages"])
    return {
        "messages": [llm_response]
    }
    
@tool
async def search_web(query: str) -> str:
    """
    Search the web for information based on a query.
    """
    return f"Searching for {query} on the web..."

tools = [search_web]
llm_w_tooks = llm.bind_tools(tools)

browser_tools = asyncio.run(get_tools())

agent = StateGraph(State)
agent.add_node("chatbot", chatbot)
agent.add_node("tools", ToolNode(browser_tools))

agent.add_edge(START, "chatbot")
agent.add_conditional_edges(
    "chatbot",
    tools_condition,
    {
        "tools": "tools",
        END: END
    }
)
agent.add_edge("tools", "chatbot")
agent.add_edge("chatbot", END)
graph = agent.compile()



async def main():
    res = await graph.ainvoke({"messages": [
        HumanMessage(content="Hello! I want to know the latest news about https://cintrifusecapital.com/.")
    ]})
    print(res)
    return res

asyncio.run(main())

png = graph.get_graph().draw_mermaid_png()

with open("graph.png", "wb") as f:
    f.write(png)