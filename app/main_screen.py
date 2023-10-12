import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QFileDialog

from app.components.button import Button
from app.settings import ASSETS_FOLDER
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

        self._button_container_widget.setLayout(self._button_container_layout)
        self.layout.addWidget(self._button_container_widget, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        self.setLayout(self.layout)

    @staticmethod
    def _set_image_preview(image_component: QLabel, image_path: str) -> QLabel:
        image_pixmap = QPixmap(image_path)
        image_component.setPixmap(image_pixmap)

        return image_component

    def _clear_images(self):
        self._image_preview_original.setPixmap(self._image_preview_empty_pixmap)
        self._image_preview_without_background.setPixmap(self._image_preview_empty_pixmap)

        if hasattr(self, "_image_path_original"):
            self._image_path_original = ""

        if hasattr(self, "_image_path_without_background"):
            self._image_path_without_background = ""

    def _import_image(self):
        image_path, _ = QFileDialog.getOpenFileName(
            self,
            "Upload a image to remove background",
            "filename",
            "Image(*.png *.jpg *.jpeg *.jfif *.pjpeg *.pjp)",
        )

        if image_path is None or not image_path:
            return

        self._image_path_original = image_path
        self._set_image_preview(self._image_preview_original, image_path)

    def _config_styles(self):
        self.setStyleSheet("""
          QFrame: {
            background-color: #18181b;
          }
        """)
