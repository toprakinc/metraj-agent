import os
from dotenv import load_dotenv
from measure import list_layers, measure_layer
from anthropic import Anthropic

# Read the API key from the .env file
load_dotenv()
print("Key loaded:", os.getenv("ANTHROPIC_API_KEY") is not None)
# Tool "ID cards": Claude reads these to decide which tool to call
# Tool "ID cards": Claude reads these to decide which tool to call
tools = [
    {
        "name": "list_layers",
        "description": "List all layer names used in a DXF drawing. Call this first to find which layer holds the elements the user asks about (walls, doors, columns...).",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to the DXF file, e.g. sample_plan.dxf",
                }
            },
            "required": ["path"],
        },
    },
    {
        "name": "measure_layer",
        "description": "Measure the total length of all lines and polylines on one layer of a DXF drawing. Returns a number in drawing units (meters in the sample file). Use it after you know the exact layer name from list_layers.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to the DXF file, e.g. sample_plan.dxf",
                },
                "layer": {
                    "type": "string",
                    "description": "Exact layer name, e.g. DUVAR",
                },
            },
            "required": ["path", "layer"],
        },
    },
]


# Read the tool name Claude asked for and run the matching Python function
def run_tool(name, tool_input):
    if name == "list_layers":
        result = list_layers(tool_input["path"])
    elif name == "measure_layer":
        result = measure_layer(tool_input["path"], tool_input["layer"])
    else:
        return "Unknown tool: " + name

    # Claude can only receive text, so turn the result into a string
    return str(result)


# Create the client (it reads ANTHROPIC_API_KEY from the environment)
client = Anthropic()

question = "What is the total wall length in sample_plan.dxf?"
# The conversation history: Claude only remembers what is in this list
messages = [{"role": "user", "content": question}]

while True:
    # Send the whole history plus the tool cards to Claude
    response = client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=1000,
        tools=tools,
        messages=messages,
    )
    # Save Claude's answer (including thinking and tool requests) to the history
    messages.append({"role": "assistant", "content": response.content})

    # If Claude did not ask for a tool, it is done
    if response.stop_reason != "tool_use":
        break

    # Run every tool Claude asked for and collect the results
    tool_results = []
    for block in response.content:
        if block.type == "tool_use":
            print("Calling tool:", block.name, block.input)
            result = run_tool(block.name, block.input)
            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                }
            )

    # Send the results back as the user's next message
    messages.append({"role": "user", "content": tool_results})

# Print Claude's final answer
for block in response.content:
    if block.type == "text":
        print(block.text)
