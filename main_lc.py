from openai import OpenAI
from dotenv import load_dotenv
from tools import tools, weird_add, fake_weather_api
import json
import gradio as gr
from rich import print
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser


load_dotenv()

chat_history = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="What is the sum of 3 and 4? and weather in new jersey?"),
    AIMessage(content="The sum of 3 and 4 is 7. The weather in New Jersey is sunny.")
]

chat_message = ChatPromptTemplate.from_messages([
    MessagesPlaceholder("chat_history"),
    ("human", "{input}")
])

test_mess = "What is the weather in France? and 1 + 200?"
messages = chat_message.invoke({"input": test_mess, "chat_history": chat_history})
chat_history.append(HumanMessage(content=test_mess))

parser = StrOutputParser()
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
llm_w_tools = llm.bind_tools([weird_add, fake_weather_api])

response = llm_w_tools.invoke(messages)
chat_history.append(response)

if len(response.tool_calls) > 0:
    tool_calls = response.tool_calls
    for tool_call in tool_calls:

        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        
        if tool_name == "weird_add":
            a = tool_args["a"]
            b = tool_args["b"]
            res = weird_add.invoke({"a": a, "b": b})
            chat_history.append(ToolMessage(content=f"The result of adding {a} and {b} is: {res}", tool_call_id=tool_call["id"]))
            
        elif tool_name == "fake_weather_api":
            location = tool_args["location"]
            weather_report = fake_weather_api.invoke({"location": location})
            chat_history.append(ToolMessage(content=f"Tool call executed. Result: {weather_report}", tool_call_id=tool_call["id"]))

response = llm_w_tools.invoke(chat_history)

print("messages gau gau:", chat_history)
print("response gau gau:", response)