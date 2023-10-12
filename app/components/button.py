# Callable type reference
# https://docs.python.org/3.6/library/typing.html#typing.Callable

from typing import Callable

from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor, QFontDatabase
from PySide6.QtWidgets import QPushButton

from app.utils.colors import Colors


class Button(QPushButton):
    """Button component"""

    def __init__(self, *args, **kwargs):
        super(Button, self).__init__(*args, **kwargs)

        self._fonts = QFontDatabase()
        self._config_styles()

    def set_button_action(self, action: Callable[[], None]):
        """Connect action on button
        :param action: function to button execute
        :return:
        """
        self.clicked.connect(action)

    def set_size(
        self,
        width: int = 130,
        height: int = 45,
        font_size: str = 14,
        padding: str = ...,
    ):
        self.setMinimumSize(width, height)
        self.setStyleSheet(
            f"""
            all: unset;
            background-color: {Colors.GRAY_800};
            text-align: center;
            padding: {padding};
            color: {Colors.ZINC_500};
            border-radius: 3px;
            font-size: {font_size}px;
            cursor: pointer;
        """
        )

    def _config_styles(self):
        """Configure dropdown styles"""
        self.setStyleSheet(
            f"""
            all: unset;
            background-color: {Colors.GRAY_800};
            text-align: center;
            padding: 17px 48px;
            color: {Colors.ZINC_500};
            border-radius: 3px;
            cursor: pointer;
            font-size: 12px;
            font-weight: bold;
        """
        )

        # setting cursor
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
