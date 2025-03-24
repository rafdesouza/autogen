def read_asset_file(file_path):
    """Reads asset data from a given text file and returns a list of items."""
    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines()]
