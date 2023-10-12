from typing import Any

from PySide6.QtWidgets import QWidget

from abc import abstractmethod, ABC


class UIUtils(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @staticmethod
    def remove_margins(widget: QWidget) -> Any:
        widget.setContentsMargins(0, 0, 0, 0)

        return widget
