import jsonschema

# Define the JSON schema for validation
ASSET_JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "hardware": {"type": "array", "items": {"type": "string"}},
        "software": {"type": "array", "items": {"type": "string"}},
        "maintenance": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["hardware", "software", "maintenance"]
}

def validate_json_structure(json_data):
    """Validates JSON data against a predefined schema."""
    try:
        jsonschema.validate(instance=json_data, schema=ASSET_JSON_SCHEMA)
        return "JSON is valid."
    except jsonschema.exceptions.ValidationError as e:
        return f"JSON validation failed: {e.message}"
