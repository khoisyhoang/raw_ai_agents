from langchain_core.tools import Tool, tool

@tool
def weird_add(a: int, b: int) -> int:
    """
    Add two integers.

    Args:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        int: The sum of the two integers.
    """
    return a + 2 * b

@tool
def fake_weather_api(location: str) -> str:
    """
    Fake weather API that returns a hardcoded weather report for a given location.

    Args:
        location (str): The location for which to get the weather report.

    Returns:
        str: The weather report for the given location.
    """
    return f"The weather in {location} is sunny and warm."

tools = [
    {
        "type": "function",
        "function": {
            "name": "weird_add",
            "description": "Add two integers with a twist.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "integer",
                        "description": "The first integer."
                    },
                    "b": {
                        "type": "integer",
                        "description": "The second integer."
                    }
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fake_weather_api",
            "description": "Fake weather API that returns a hardcoded weather report for a given location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The location for which to get the weather report."
                    }
                },
                "required": ["location"]
            }
        }
    }
]