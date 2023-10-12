import os.path
from typing import Literal

from PySide6.QtGui import QFontDatabase, QIcon
from PySide6.QtWidgets import QGridLayout, QMessageBox

from app.settings import ASSETS_FOLDER
from app.utils.colors import Colors


class Alert(QMessageBox):
    def __init__(
        self,
        title: str,
        message: str,
        message_type: Literal["warning", "info", "error", "question"],
        icon: QMessageBox.Icon = QMessageBox.Icon.Information,
        *args,
        **kwargs,
    ):
        """Constructor
        :param title:
        :param message:
        :param message_type: Type of message
        :param icon: optional param, choose by class automatic
        :return:
        """
        super(Alert, self).__init__(*args, **kwargs)

        self.findChild(QGridLayout).setColumnMinimumWidth(1, 370)

        self.setWindowIcon(
            QIcon(
                os.path.join(
                    ASSETS_FOLDER,
                    "naruto_icon.ico"
                )
            )
        )

        self.setWindowTitle(f"{message_type.capitalize()}: {title}")
        self.setText(message)

        self._fonts = QFontDatabase()
        self._config_style()

    def _config_style(self):
        self.setStyleSheet(
            """
            QDialogButtonBox > QPushButton[text="OK"] {
                all: unset;
                background-color: """
            + Colors.GRAY_800
            + """;
                text-align: center;
                padding: 8px 24px;
                color: """
            + Colors.ZINC_500
            + """;
                font-weight: bold;
                border-radius: 3px;
                cursor: pointer;
            }
        """
        )
