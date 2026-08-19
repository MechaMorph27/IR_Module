import json
import os


THEME_FILE = "theme.json"


DEFAULT_THEME = {
    "background": "#0b0f14",
    "text": "#ffffff",
    "button": "#2d6cdf",
    "input": "#1c1f26",
    "table": "#0a0f19",
    "header": "#14203c"
}


def load_theme():

    if not os.path.exists(THEME_FILE):

        save_theme(DEFAULT_THEME)
        return DEFAULT_THEME


    try:

        with open(THEME_FILE, "r") as f:
            return json.load(f)


    except:

        return DEFAULT_THEME



def save_theme(theme):

    with open(THEME_FILE, "w") as f:

        json.dump(
            theme,
            f,
            indent=4
        )