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

from .scripts import Script
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
        self._base_dir = base_dir
        self._project = None

    def attach_script(self, name="Script", trigger=None):
        """Add a :class:`~scratkat.scripts.Script` to this sprite."""
        # Passing an event block as the first argument keeps script setup terse:
        # ``sprite.attach_script(when_run()).then(move(10))``.
        if trigger is None and hasattr(name, "matches"):
            trigger = name
            name = type(trigger).__name__
        script = Script(name, trigger=trigger)
        script.sprite = self
        self.scripts.append(script)
        return script

    def set_costume(self, image=None, name="Costume 1"):
        """Replace this sprite's costume and refresh it on its project.

        ``image`` may be an absolute path or a path relative to the project
        file that created the sprite.
        """
        self.costume = Costume(image=image, name=name, base_dir=self._base_dir)
        self._costume_width = 0
        self._costume_height = 0

        if self._project is not None:
            self._project._set_sprite_costume(self)

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
        sprite._project = self

        self.sprites.append(sprite)

        self._create_sprite_widget(sprite)

        return sprite

    def _create_sprite_widget(self, sprite):
        """Create the Qt widget used to display a sprite."""

        label = QLabel(self.canvas)
        label.setAlignment(Qt.AlignCenter)
        label.setAttribute(Qt.WA_TranslucentBackground)

        sprite._label = label

        self._set_sprite_costume(sprite)

        self._update_sprite(sprite)

    def _set_sprite_costume(self, sprite):
        """Load a sprite costume into its existing widget, if it has one."""
        label = sprite._label
        if label is None:
            return

        label.clear()
        sprite._costume_width = 0
        sprite._costume_height = 0

        if sprite.costume.path is None:
            self._update_sprite(sprite)
            return

        if not sprite.costume.path.is_file():
            raise FileNotFoundError(
                f"Costume image not found: {sprite.costume.path}"
            )

        pixmap = QPixmap(str(sprite.costume.path))
        if pixmap.isNull():
            raise ValueError(
                f"Could not load costume image: {sprite.costume.path}"
            )

        label.setPixmap(pixmap)
        # The label is resized from the costume's logical dimensions on every
        # stage resize, so this works consistently across Qt backends and DPI.
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
            round(sprite._costume_width * size_scale * stage_scale),
        )
        height = max(
            1,
            round(sprite._costume_height * size_scale * stage_scale),
        )
        label.resize(width, height)

        center_x, center_y = self.canvas.logical_to_screen(
            cfg["x"], cfg["y"], stage_scale
        )
        label.move(
            round(center_x - width / 2),
            round(center_y - height / 2),
        )

    def update_sprites(self):
        """Update every sprite in the project."""

        for sprite in self.sprites:
            self._update_sprite(sprite)

    def run(self, width=800, height=600):
        """Launch the project."""

        self.window.resize(width, height)
        self.trigger("run")
        self.update_sprites()
        self.window.show()

        return self.app.exec()

    def trigger(self, event):
        """Run every script listening for *event*.

        This is public so future event sources can dispatch their own events.
        """
        for sprite in self.sprites:
            for script in sprite.scripts:
                if script.runs_on(event):
                    script.run()


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
