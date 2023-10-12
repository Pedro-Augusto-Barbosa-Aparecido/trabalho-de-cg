import os.path
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QApplication

from app.settings import MINIMUM_SIZE_OF_APPLICATION, ASSETS_FOLDER
from app.main_screen import MainScreen


class Application(QMainWindow):
    def __init__(self, parent=None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        self.setWindowTitle("Remove BG - RBG")
        self.setMinimumSize(MINIMUM_SIZE_OF_APPLICATION["width"], MINIMUM_SIZE_OF_APPLICATION["height"])

        self.setWindowIcon(
            QIcon(
                os.path.join(
                    ASSETS_FOLDER, "naruto_icon.ico"
                )
            )
        )

        screen = MainScreen()
        self.setCentralWidget(screen)

        self._config_styles()

    def _config_styles(self):
        self.setStyleSheet("""
        background-color: #18181b;
        """)


if __name__ == "__main__":
    import ctypes

    app_id = "13.remove_bg_rbg"  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

    # application to open as window
    application = QApplication(sys.argv)

    # main screen
    main_application = Application()
    main_application.show()

    application.exec()
