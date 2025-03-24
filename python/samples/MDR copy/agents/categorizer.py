import autogen
from llm_config import llm_config
import logging
import json  # Ensure we can work with JSON if needed

# Configure logging
logging.basicConfig(filename="logs/categorizer.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

categorizer = autogen.AssistantAgent(
    name="Categorizer",
    system_message="Categorizes asset data into hardware, software, and maintenance.",
    llm_config=llm_config
)

@categorizer.register_for_execution()
def categorize_assets(data):
    """Processes a plain-text list and classifies items into categories."""

    logging.info(f"Received data for categorization: {data}")
    
    if isinstance(data, str):
        try:
            data = json.loads(data)  # If mistakenly received as JSON string
        except json.JSONDecodeError:
            data = data.strip().split("\n")  # Convert plain text into a list

    if not isinstance(data, list):
        logging.error("Invalid input format. Expected a list of asset items.")
        return {"error": "Invalid input format, expected a list of asset items."}

    categories = {"hardware": [], "software": [], "maintenance": []}

    for item in data:
        item = item.strip().lower()
        if any(keyword in item for keyword in ["cpu", "ram", "hard drive"]):
            categories["hardware"].append(item)
        elif any(keyword in item for keyword in ["license", "update", "subscription", "adobe", "windows"]):
            categories["software"].append(item)
        else:
            categories["maintenance"].append(item)

    logging.info(f"Categorization result: {categories}")

    print("\n🔍 Categorization completed. Returning structured dictionary.")
    return categories  # ✅ Ensure the return type is a dictionary
