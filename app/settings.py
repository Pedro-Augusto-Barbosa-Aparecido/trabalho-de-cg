import os


MINIMUM_SIZE_OF_APPLICATION = {
    "width": 800,
    "height": 400
}

ROOT_FOLDER = os.path.abspath(
    os.path.dirname("main.py")
)

APP_FOLDER = os.path.join(
    ROOT_FOLDER, "app"
)

ASSETS_FOLDER = os.path.join(
    APP_FOLDER, "assets"
)

TEMP_FOLDER = os.path.join(
    ROOT_FOLDER, "temp"
)
