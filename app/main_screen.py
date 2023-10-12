import os
import shutil
import pathlib
from typing import Literal

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QFileDialog

from app.components.alert import Alert
from app.components.button import Button
from app.image_manager import ImageManager
from app.settings import ASSETS_FOLDER, TEMP_FOLDER, MAX_IMAGE_SIZE
from app.utils.ui import UIUtils


class MainScreen(QFrame):
    def __init__(self):
        super(MainScreen, self).__init__()

        self.layout = QVBoxLayout()

        self._config_styles()
        self._config_layout()

    def _get_image_widget(self, name_of_widget: str) -> QLabel:
        image_widget = QLabel()
        image_widget = UIUtils.remove_margins(image_widget)

        setattr(self, name_of_widget, image_widget)
        return image_widget

    def _config_layout(self):
        self._image_container_widget = QWidget()
        self._image_container_layout = QHBoxLayout()

        self._image_preview_empty_pixmap = QPixmap(os.path.join(ASSETS_FOLDER, "image_preview_empty.png"))

        self._image_preview_original = self._get_image_widget("_image_preview_original")
        self._image_preview_original.setContentsMargins(0, 0, 64, 0)
        self._image_preview_original.setPixmap(self._image_preview_empty_pixmap)
        self._image_container_layout.addWidget(self._image_preview_original, alignment=Qt.AlignmentFlag.AlignCenter)

        self._image_preview_without_background = self._get_image_widget("_image_preview_without_background")
        self._image_preview_without_background.setPixmap(self._image_preview_empty_pixmap)
        self._image_container_layout.addWidget(self._image_preview_without_background,
                                               alignment=Qt.AlignmentFlag.AlignCenter)

        self._image_container_widget = UIUtils.remove_margins(self._image_container_widget)
        self._image_container_widget.setContentsMargins(0, 0, 0, 10)
        self._image_container_widget.setLayout(self._image_container_layout)

        self.layout.addWidget(self._image_container_widget,
                              alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        self._button_container_widget = QWidget()
        self._button_container_layout = QHBoxLayout()

        self._remove_bg_button: Button = UIUtils.remove_margins(Button("Remove Background"))
        self._remove_bg_button.set_button_action(self._remove_background)
        self._button_container_layout.addWidget(self._remove_bg_button,
                                                alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        self._import_image_button: Button = UIUtils.remove_margins(Button("Import Image"))
        self._import_image_button.set_button_action(self._import_image)
        self._button_container_layout.addWidget(self._import_image_button,
                                                alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        self._clear_image_button: Button = UIUtils.remove_margins(Button("Clear Content"))
        self._clear_image_button.set_button_action(self._clear_images)
        self._button_container_layout.addWidget(self._clear_image_button,
                                                alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        self._save_image_button: Button = UIUtils.remove_margins(Button("Save"))
        self._save_image_button.set_button_action(self._save_image)
        self._button_container_layout.addWidget(self._save_image_button,
                                                alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        self._button_container_widget.setLayout(self._button_container_layout)
        self.layout.addWidget(self._button_container_widget,
                              alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)

        self.setLayout(self.layout)

    @staticmethod
    def _set_image_preview(image_component: QLabel, image_path: str) -> QLabel:
        image_pixmap = QPixmap(image_path)

        if image_pixmap.width() > MAX_IMAGE_SIZE["width"]:
            image_pixmap = image_pixmap.scaled(
                MAX_IMAGE_SIZE["width"], image_pixmap.height(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding
            )

        if image_pixmap.height() > MAX_IMAGE_SIZE["height"]:
            image_pixmap = image_pixmap.scaled(
                image_pixmap.width(),
                MAX_IMAGE_SIZE["height"],
                Qt.AspectRatioMode.KeepAspectRatioByExpanding
            )

        image_component.setPixmap(image_pixmap)
        return image_component

    def _save_image(self):
        if not hasattr(self, "_image_path_without_background"):
            self._alert_box("Warning", "No image to save, please import an image and remove background")
            return

        path_to_open = os.path.join(
            os.path.expanduser("~"),
            "Downloads"
        )

        folder = str(
            QFileDialog.getExistingDirectory(
                self,
                "Select directory to export template",
                dir=path_to_open,
            )
        )

        if folder == "":
            self._alert_box("Warning", "No folder selected")
            return

        filepath = pathlib.Path(self._image_path_without_background)
        filename = os.path.basename(self._image_path_without_background)
        filename = f"{filename.replace(filepath.suffix, '')}_without_background.png"
        filepath = os.path.join(
            folder, filename
        )

        shutil.move(
            self._image_path_without_background,
            filepath
        )

        self._alert_box("Success", f"Image has saved on {filepath}")

    def _remove_background(self):
        if not hasattr(self, "_image_path_original"):
            self._alert_box("Warning", "No image to remove background")
            return

        self._image_path_without_background = ImageManager.remove_bg(self._image_path_original)
        self._set_image_preview(self._image_preview_without_background, self._image_path_without_background)
        self._alert_box("Success", "Background has removed!")

    def _clear_images(self):
        self._image_preview_original.setPixmap(self._image_preview_empty_pixmap)
        self._image_preview_without_background.setPixmap(self._image_preview_empty_pixmap)

        if hasattr(self, "_image_path_original"):
            self._image_path_original = ""

        if hasattr(self, "_image_path_without_background"):
            self._image_path_without_background = ""

        self._alert_box("Success", "Cleared system!")

    def _import_image(self):
        image_path, _ = QFileDialog.getOpenFileName(
            self,
            "Upload a image to remove background",
            "filename",
            "Image(*.png *.jpg *.jpeg *.jfif *.pjpeg *.pjp)",
        )

        if image_path is None or not image_path:
            self._alert_box("Warning", "No path selected")
            return

        temp_file = os.path.join(
            TEMP_FOLDER,
            os.path.basename(image_path)
        )

        if not os.path.exists(temp_file):
            shutil.copy(
                image_path,
                temp_file
            )

        self._image_path_original = temp_file
        self._set_image_preview(self._image_preview_original, image_path)
        self._alert_box("Success", "Image imported with success")

    def _config_styles(self):
        self.setStyleSheet("""
          QFrame: {
            background-color: #18181b;
          }
        """)

    @staticmethod
    def _alert_box(
        title: str,
        message: str,
        message_type: Literal["warning", "info", "error", "question"] = "error",
    ):
        alert = Alert(title, message, message_type)
        alert.exec()

