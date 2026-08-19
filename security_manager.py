import json
import os

FILE = "security.json"


def get_password():
    if not os.path.exists(FILE):
        save_password("Matter@123")
        return "Matter@123"

    try:
        with open(FILE, "r") as f:
            data = json.load(f)
            return data.get("admin_password", "Matter@123")
    except:
        return "Matter@123"


def save_password(new_password):
    with open(FILE, "w") as f:
        json.dump(
            {"admin_password": new_password},
            f,
            indent=4
        )