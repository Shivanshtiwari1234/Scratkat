import inspect
import sys
from pathlib import Path

from qtpy.QtCore import Qt
from qtpy.QtGui import QPixmap
from qtpy.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
)

from .stage import Stage


class Costume:
    """The visual appearance of a sprite."""

    def __init__(self, image=None, name="Costume 1", base_dir=None):
        self.name = name
        self.image = image

        if image is not None:
            image_path = Path(image)

            if not image_path.is_absolute() and base_dir is not None:
                image_path = Path(base_dir) / image_path

            self.path = image_path.resolve()
        else:
            self.path = None


class Script:
    """A sprite script.

    Scripts are currently stored only and are not executed.
    """

    def __init__(self, name="Script 1"):
        self.name = name


class Sound:
    """A sound belonging to a sprite."""

    def __init__(self, name="Sound 1"):
        self.name = name


class Sprite:
    """A ScratKat sprite."""

    def __init__(self, name="Sprite", costume=None, base_dir=None):
        self.name = name

        self.cfg = {
            "x": 0.0,
            "y": 0.0,
            "visible": True,
            "size": 100,
            "dir": 90.0,
        }

        self.costume = Costume(
            image=costume,
            base_dir=base_dir,
        )

        self.scripts = []
        self.sounds = []

        self._label = None
        self._costume_width = 0
        self._costume_height = 0

    def attach_script(self, name="Script"):
        """Add a script to this sprite.

        Script execution is not implemented yet.
        """
        script = Script(name)
        self.scripts.append(script)
        return script

    def wire_sound(self, name="Sound"):
        """Add a sound to this sprite."""
        sound = Sound(name)
        self.sounds.append(sound)
        return sound


class Project:
    def __init__(self, title="ScratKat", base_dir=None):
        self.title = title

        self.app = QApplication.instance()

        if self.app is None:
            self.app = QApplication(sys.argv)

        self.window = QMainWindow()
        self.window.setWindowTitle(title)

        self.canvas = Stage(self)
        self.window.setCentralWidget(self.canvas)

        self.sprites = []

        self.base_dir = (
            Path(base_dir).resolve()
            if base_dir
            else Path.cwd()
        )

    def add_sprite(self, name="Sprite", costume=None):
        """Create and add a sprite to the project."""

        sprite = Sprite(
            name=name,
            costume=costume,
            base_dir=self.base_dir,
        )

        self.sprites.append(sprite)

        self._create_sprite_widget(sprite)

        return sprite

    def _create_sprite_widget(self, sprite):
        """Create the Qt widget used to display a sprite."""

        label = QLabel(self.canvas)
        label.setAlignment(Qt.AlignCenter)
        label.setAttribute(Qt.WA_TranslucentBackground)

        sprite._label = label

        if sprite.costume.path is not None:
            if not sprite.costume.path.exists():
                raise FileNotFoundError(
                    f"Costume image not found: "
                    f"{sprite.costume.path}"
                )

            pixmap = QPixmap(str(sprite.costume.path))

            if pixmap.isNull():
                raise ValueError(
                    f"Could not load costume image: "
                    f"{sprite.costume.path}"
                )

            label.setPixmap(pixmap)
            label.setScaledContents(True)

            sprite._costume_width = pixmap.width()
            sprite._costume_height = pixmap.height()

        self._update_sprite(sprite)

    def _update_sprite(self, sprite):
        """Apply the sprite configuration to its widget."""

        label = sprite._label

        if label is None:
            return

        cfg = sprite.cfg

        if not cfg["visible"]:
            label.hide()
            return

        label.show()

        if (
            sprite._costume_width <= 0
            or sprite._costume_height <= 0
        ):
            return

        stage_scale = self.canvas.get_scale()

        size_scale = cfg["size"] / 100.0

        width = max(
            1,
            int(
                sprite._costume_width
                * size_scale
                * stage_scale
            ),
        )

        height = max(
            1,
            int(
                sprite._costume_height
                * size_scale
                * stage_scale
            ),
        )

        label.resize(width, height)

        center_x, center_y = self.canvas.logical_to_screen(
            cfg["x"],
            cfg["y"],
            stage_scale,
        )

        label.move(
            int(center_x - width / 2),
            int(center_y - height / 2),
        )

    def update_sprites(self):
        """Update every sprite in the project."""

        for sprite in self.sprites:
            self._update_sprite(sprite)

    def run(self, width=800, height=600):
        """Launch the project."""

        self.window.resize(width, height)
        self.update_sprites()
        self.window.show()

        return self.app.exec()


def init(title="ScratKat"):
    """Create a new ScratKat project.

    Relative costume paths are resolved relative to the
    Python file that called this function.
    """

    caller = inspect.stack()[1]
    caller_file = Path(caller.filename).resolve()

    return Project(
        title=title,
        base_dir=caller_file.parent,
    )
