import autogen
import json
import logging

# Configure logging
logging.basicConfig(filename="logs/validator.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

validator = autogen.AssistantAgent(
    name="Validator",
    system_message="Validates the JSON output to ensure it follows the correct format.",
)

@validator.register_for_execution()
def validate_json(json_file_path):
    """Validates the JSON file structure to ensure it is correctly formatted."""
    try:
        logging.info(f"Validating JSON file: {json_file_path}")

        with open(json_file_path, "r") as file:
            data = json.load(file)

        # Basic validation check
        if not isinstance(data, dict):
            logging.error(f"Invalid JSON structure: Expected dictionary but got {type(data)}")
            return "❌ Error: JSON file does not contain a valid dictionary."

        logging.info("JSON validation successful.")
        return "✅ JSON validation successful."

    except FileNotFoundError:
        logging.error(f"JSON file not found: {json_file_path}")
        return f"❌ Error: JSON file not found: {json_file_path}"
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON format: {str(e)}")
        return f"❌ Error: Invalid JSON format: {str(e)}"
    except Exception as e:
        logging.exception("Unexpected error during JSON validation.")
        return f"❌ Error: An unexpected error occurred during JSON validation: {str(e)}"
