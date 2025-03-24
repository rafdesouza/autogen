# llm_config.py

# ...existing code...

llm_config = {
    "config_list": [
        {
            "api_type": "azure",
            "model": "gpt-4o",  # Your Azure deployment name
            "base_url": "https://cog-swedc-aoiadalle3.openai.azure.com/",
            # "azure_deployment": "gpt-4o",  # Matches the Azure deployment name
            "api_version": "2024-05-01-preview",
            "api_key": "652e67a2e9a946509d47f53b99a7f6d2"
            # "max_tokens": 2000
            # Remove or comment out any unsupported parameters (e.g., temperature)
        }
    ],
    "cache_seed": 42
}

# Optional: Adjust individual agent configurations:
categorizer_llm_config = llm_config.copy()
categorizer_llm_config["config_list"][0]["model"] = "gpt-4o"

json_formatter_llm_config = llm_config.copy()
json_formatter_llm_config["config_list"][0]["model"] = "gpt-4o"
