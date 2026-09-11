import sys

from qtpy.QtWidgets import QApplication, QMainWindow


def init(title="ScratKat"):
    """Initialize ScratKat and open the main application window."""

    app = QApplication.instance()

    if app is None:
        app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle(title)
    window.resize(800, 600)
    window.show()

    # Keep the window alive and exit cleanly when it is closed.
    exit_code = app.exec()

    window.close()
    app.quit()

    return exit_code
