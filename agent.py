import os
from dotenv import load_dotenv
from measure import list_layers, measure_layer

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


print(run_tool("list_layers", {"path": "sample_plan.dxf"}))
print(run_tool("measure_layer", {"path": "sample_plan.dxf", "layer": "DUVAR"}))
print(run_tool("count_columns", {"path": "sample_plan.dxf"}))
print(len(tools))
