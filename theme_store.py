import json
import os


FILE = "theme.json"


DEFAULT_THEME = {

    "background": "#0b0f14",

    "text": "#ffffff",

    "button": "#2d6cdf",

    "input": "#1c1f26",

    "table": "#101820",

    "locked": False
}



def load_theme():

    if not os.path.exists(FILE):

        save_theme(DEFAULT_THEME)

        return DEFAULT_THEME.copy()


    try:

        with open(FILE, "r") as f:

            return json.load(f)


    except:

        return DEFAULT_THEME.copy()



def save_theme(data):

    with open(FILE, "w") as f:

        json.dump(
            data,
            f,
            indent=4
        )