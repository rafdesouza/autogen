import autogen
import os
import glob
import json
import logging
from agents.user_proxy import user_proxy
from agents.file_reader import file_reader
from agents.categorizer import categorizer
from agents.json_formatter import json_formatter
from agents.validator import validator
from llm_config import llm_config
import sys
import ast

# Configure logging
logging.basicConfig(filename="logs/main.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Add console logging for error messages
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(console_formatter)
logging.getLogger("").addHandler(console_handler)

# Define input and output file paths
INPUT_FILE = "data/input_assets.txt"
OUTPUT_PATTERN = "data/categorized_output_*.json"

# Create GroupChat with all agents
groupchat = autogen.GroupChat(
    agents=[user_proxy, file_reader, categorizer, json_formatter, validator], 
    messages=[], 
    max_round=12
)

# Manager to coordinate the conversation
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# Start the process
if __name__ == "__main__":
    logging.info("Starting the asset categorization process.")

    # Ensure input file exists
    if not os.path.exists(INPUT_FILE):
        logging.error(f"File not found: {INPUT_FILE}")
        print(f"\n❌ Error: {INPUT_FILE} not found. Please create it before running the script.\n")
        sys.exit(1)

    print(f"\n📥 Using input file: {INPUT_FILE}")

    # 1️⃣ Trigger File Reader Agent
    extracted_data = file_reader.function_map.get("extract_data", lambda: "❌ Error: Function not found")()

    # ✅ Print extracted data for debugging
    logging.info(f"Extracted Data: {extracted_data}")
    print(f"\n🔍 Extracted Data:\n{extracted_data}\n")

    # 🔹 FIX: Correctly validate and parse extracted_data
    if isinstance(extracted_data, str):
        if extracted_data.startswith("❌"):
            logging.error("Extracted data contains an error message.")
            print("\n❌ Error: Extracted data contains an error. Exiting...\n")
            sys.exit(1)
        else:
            try:
                extracted_data = ast.literal_eval(extracted_data)
            except Exception as e:
                logging.error("Failed to parse extracted_data string into a list.", exc_info=True)
                print("\n❌ Error: Could not parse extracted data into the correct format. Exiting...\n")
                sys.exit(1)

    if not isinstance(extracted_data, list) or len(extracted_data) == 0:
        logging.error(f"Unexpected data type for extracted data: {type(extracted_data)}")
        print("\n❌ Error: Extracted data is empty or not in the correct format. Exiting...\n")
        sys.exit(1)

    print("\n📂 File extracted successfully.")

    # 2️⃣ Trigger Categorizer Agent (Force Execution)
    if "categorize_assets" in categorizer.function_map:
        categorized_data = categorizer.function_map["categorize_assets"](extracted_data)
        logging.info(f"Categorized Data: {categorized_data}")
    else:
        logging.error("Categorization function not found.")
        print("\n❌ Error: Categorization function not found. Exiting...\n")
        sys.exit(1)

    # If categorized_data is a string, convert it to a dictionary
    if isinstance(categorized_data, str):
        try:
            categorized_data = ast.literal_eval(categorized_data)
        except Exception as e:
            logging.error("Failed to parse categorized_data string into a dictionary.", exc_info=True)
            print("\n❌ Error: Could not parse categorized data into the correct format. Exiting...\n")
            sys.exit(1)

    # ✅ Ensure categorized_data is a dictionary
    if not isinstance(categorized_data, dict):
        logging.error(f"Categorization failed. Expected dictionary but got {type(categorized_data)}")
        print(f"\n❌ Error: Categorization failed. Expected dictionary but got {type(categorized_data)}.\nCategorized data:\n{categorized_data}\nExiting...\n")
        sys.exit(1)

    print("\n🔍 Categorization completed.")

    # 3️⃣ Trigger JSON Formatter Agent (Save JSON)
    json_file = json_formatter.function_map["format_to_json"](categorized_data)
    if json_file.startswith("❌"):
        logging.error("JSON formatting failed.")
        print(f"\n❌ Error: {json_file}\n")
        sys.exit(1)

    print(f"\n✅ JSON saved: {json_file}")

    # 4️⃣ Validate JSON Output
    if "validate_json" in validator.function_map:
        validation_result = validator.function_map["validate_json"](json_file)
        print(f"\n🔍 JSON Validation: {validation_result}")
        logging.info(f"JSON Validation Result: {validation_result}")
    else:
        logging.error("Validation function not found in function_map.")
        print("\n❌ Error: Validation function not found. Skipping validation step.\n")

    sys.exit(0)  # Force script exit
