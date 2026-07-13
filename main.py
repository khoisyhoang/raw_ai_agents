from openai import OpenAI
from dotenv import load_dotenv
from tools import tools, weird_add, fake_weather_api
import json
import gradio as gr
from rich import print

load_dotenv()

client = OpenAI()
chat_message = [
            {"role": "system", "content": "You are a helpful assistant."},
        ]
def chat(message: str):
    
    chat_message.append({"role": "user", "content": message}) 
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=chat_message,
        tools=tools,
    )
    
    if response.choices[0].finish_reason == "tool_calls":
        tool_calls = response.choices[0].message.tool_calls
        # chat_message.append(response.choices[0].message) # pydantic
        
        chat_message.append(response.choices[0].message.model_dump()) # convert back to dict
        
        print("Tool calls:", response.choices[0].message)
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            print("tool args:", tool_args)
            
            if tool_name == "weird_add":
                a = tool_args["a"]
                b = tool_args["b"]
                result = weird_add(a, b)
                print(f"The result of adding {a} and {b} is: {result}")
                chat_message.append({"role": "tool", "content": f"Tool call executed. Result: {result}", "tool_call_id": tool_call.id})
                
            elif tool_name == "fake_weather_api":
                location = tool_args["location"]
                weather_report = fake_weather_api(location)
                print(weather_report)
                chat_message.append({"role": "tool", "content": f"Tool call executed. Result: {weather_report}", "tool_call_id": tool_call.id})
                
        print("Chat message after tool calls:", chat_message) 
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=chat_message,
            tools=tools,
        )
        
    return response.choices[0].message.content
# chat("What is the sum of 3 and 4? and weather in new jersey?")  # This will call weird_add
demo = gr.Interface(
    fn=chat,
    inputs=gr.Textbox(label="Enter your message"),
    outputs=gr.Textbox(label="Response"),
    title="Chat with Tools",
    description="This is a simple chat interface that uses OpenAI's API to respond to user messages and can call custom tools.",
)   

demo.launch()

