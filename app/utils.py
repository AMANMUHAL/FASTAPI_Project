import json
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "patients.json"

def load_data():
    with open(DATA_PATH, "r") as file:
        return json.load(file)

def save_data(data):
    with open(DATA_PATH, "w") as file:
        json.dump(data, file, indent=4)
