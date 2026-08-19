import json
import os

FILE = "operators.json"


def load_operators():
    if not os.path.exists(FILE):
        return []

    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_operators(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


def add_operator(name):
    name = name.strip()
    if not name:
        return

    ops = load_operators()

    if name not in ops:
        ops.append(name)
        save_operators(ops)