"""Motion blocks for use in :class:`scratkat.scripts.Script` objects."""

from math import cos, radians, sin


class MotionBlock:
    """Base class for blocks that change a sprite's position or direction."""

    def _update(self, sprite):
        if sprite._project is not None:
            sprite._project._update_sprite(sprite)


class Move(MotionBlock):
    """Move a sprite forward by a number of Scratch-style steps."""

    def __init__(self, steps):
        self.steps = steps

    def execute(self, sprite):
        # Scratch uses 90 for right and 0 for up, unlike the usual math axis.
        angle = radians(sprite.cfg["dir"])
        sprite.cfg["x"] += sin(angle) * self.steps
        sprite.cfg["y"] += cos(angle) * self.steps
        self._update(sprite)


class Turn(MotionBlock):
    """Turn a sprite clockwise by *degrees*."""

    def __init__(self, degrees):
        self.degrees = degrees

    def execute(self, sprite):
        sprite.cfg["dir"] = (sprite.cfg["dir"] + self.degrees) % 360
        self._update(sprite)


class GoTo(MotionBlock):
    """Place a sprite at an absolute logical-stage position."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def execute(self, sprite):
        sprite.cfg.update(x=self.x, y=self.y)
        self._update(sprite)


class ChangeX(MotionBlock):
    """Change a sprite's horizontal position."""

    def __init__(self, amount):
        self.amount = amount

    def execute(self, sprite):
        sprite.cfg["x"] += self.amount
        self._update(sprite)


class ChangeY(MotionBlock):
    """Change a sprite's vertical position."""

    def __init__(self, amount):
        self.amount = amount

    def execute(self, sprite):
        sprite.cfg["y"] += self.amount
        self._update(sprite)


class PointInDirection(MotionBlock):
    """Set a sprite's Scratch-style direction (90 points right)."""

    def __init__(self, direction):
        self.direction = direction

    def execute(self, sprite):
        sprite.cfg["dir"] = self.direction % 360
        self._update(sprite)


def move(steps):
    return Move(steps)


def turn(degrees):
    return Turn(degrees)


def go_to(x, y):
    return GoTo(x, y)


def change_x(amount):
    return ChangeX(amount)


def change_y(amount):
    return ChangeY(amount)


def point_in_direction(direction):
    return PointInDirection(direction)
