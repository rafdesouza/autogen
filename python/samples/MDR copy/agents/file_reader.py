import autogen
from llm_config import llm_config
from utils.file_utils import read_asset_file
import logging

# Configure logging
logging.basicConfig(filename="logs/file_reader.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

INPUT_FILE = "data/input_assets.txt"

file_reader = autogen.AssistantAgent(
    name="File_reader",
    system_message="Reads asset data from input_assets.txt and extracts information.",
    llm_config=llm_config
)

@file_reader.register_for_execution()
def extract_data():
    """Reads asset data from the predefined input file and returns a list of items."""
    try:
        logging.info(f"Attempting to read file: {INPUT_FILE}")
        
        with open(INPUT_FILE, "r") as file:
            data = [line.strip() for line in file.readlines() if line.strip()]

        logging.info(f"Extracted data: {data}")
        
        if not data:
            logging.error("File read successfully, but no valid data was extracted.")
            return "❌ Error: The file is empty or could not be read."

        print(f"\n📂 File_reader extracted {len(data)} items from {INPUT_FILE}\n")
        return data

    except FileNotFoundError:
        logging.error(f"File not found: {INPUT_FILE}")
        return f"❌ Error: File {INPUT_FILE} not found!"
    except Exception as e:
        logging.exception(f"Unexpected error while reading the file: {str(e)}")
        return f"❌ Error: An unexpected error occurred while reading the file: {str(e)}"
