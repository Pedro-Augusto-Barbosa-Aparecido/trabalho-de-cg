import os


MINIMUM_SIZE_OF_APPLICATION = {
    "width": 800,
    "height": 400
}

MAX_IMAGE_SIZE = {
    "width": 300,
    "height": 250
}

ROOT_FOLDER = os.path.abspath(
    os.path.dirname("main.py")
)

APP_FOLDER = os.path.join(
    ROOT_FOLDER, "app"
)

ASSETS_FOLDER = os.path.join(
    APP_FOLDER, "assets"
) if os.path.exists(APP_FOLDER) else os.path.join(
    ROOT_FOLDER, "assets"
)

TEMP_FOLDER = os.path.join(
    ROOT_FOLDER, "temp"
)

if not os.path.exists(TEMP_FOLDER):
    os.makedirs(TEMP_FOLDER, exist_ok=True)
