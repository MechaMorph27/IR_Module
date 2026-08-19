import json
import os

CONFIG_FILE = "config.json"


def load_config():

    if not os.path.exists(CONFIG_FILE):
        default = {
            "ip": "192.168.1.1",
            "read_command": "READ?\n",
            "admin_password": "1234",
            "points": [
                "B-", "B1", "B2", "B3", "B4", "B5",
                "B6", "B7", "B8", "B9", "B10",
                "B11", "B12", "B13", "Module"
            ],
            "limits": {
                "cell_v_min": 3.565,
                "cell_v_max": 3.580,
                "cell_ir_min": 1.50,
                "cell_ir_max": 1.98,
                "module_v_min": 49.91,
                "module_v_max": 50.12,
                "module_ir_min": 18.0,
                "module_ir_max": 19.9,
            },
            "excel_file": "Module_Test_Log.xlsx"
        }

        save_config(default)
        return default

    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)