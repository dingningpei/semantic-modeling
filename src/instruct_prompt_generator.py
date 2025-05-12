import json

def load_ontologies(file_path):
    """Load ontologies from a JSON file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        ontologies = json.load(file)
    return ontologies

