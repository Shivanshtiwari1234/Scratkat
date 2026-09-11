import sys

from qtpy.QtWidgets import QApplication, QMainWindow


class Costume:
    """The visual appearance of a sprite."""

    def __init__(self, name="Costume 1"):
        self.name = name


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

    def __init__(self, name="Sprite"):
        self.name = name

        # One costume for now.
        self.costume = Costume()

        # Scripts exist, but are not functional yet.
        self.scripts = []

        # Sounds exist, but are not functional yet.
        self.sounds = []

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
    def __init__(self, title="ScratKat"):
        self.title = title

        self.app = QApplication.instance()

        if self.app is None:
            self.app = QApplication(sys.argv)

        self.window = QMainWindow()
        self.window.setWindowTitle(title)

        self.sprites = []

    def add_sprite(self, name="Sprite"):
        """Create and add a sprite to the project."""
        sprite = Sprite(name)
        self.sprites.append(sprite)
        return sprite

    def run(self, width=800, height=600):
        """Launch the project."""
        self.window.resize(width, height)
        self.window.show()

        return self.app.exec()


def init(title="ScratKat"):
    """Create a new ScratKat project."""
    return Project(title)
