import autogen
import json
import datetime
from llm_config import llm_config

# Generate timestamped filename
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_FILE = f"data/categorized_output_{timestamp}.json"

json_formatter = autogen.AssistantAgent(
    name="JSON_formatter",
    system_message="Formats categorized data into JSON and saves it.",
    llm_config=llm_config
)

@json_formatter.register_for_execution()
def format_to_json(categorized_data):
    """Converts categorized asset data into structured JSON and saves it to a timestamped file."""

    # Ensure categorized_data is a dictionary
    if not isinstance(categorized_data, dict):
        try:
            categorized_data = json.loads(categorized_data)  # Try parsing if received as a string
        except json.JSONDecodeError:
            return "❌ Error: Categorized data is not a valid dictionary."

    try:
        json_output = json.dumps(categorized_data, indent=4)

        with open(OUTPUT_FILE, "w") as f:
            f.write(json_output)

        print(f"\n✅ JSON saved successfully: {OUTPUT_FILE}")
        return OUTPUT_FILE
    except Exception as e:
        return f"❌ Error: Failed to save JSON. {str(e)}"
