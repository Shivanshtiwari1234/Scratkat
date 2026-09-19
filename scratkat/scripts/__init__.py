"""Building blocks for scripts attached to ScratKat sprites."""

from .script import Script
from .events import EventBlock, WhenRun, when_run
from .motion import (
    ChangeX,
    ChangeY,
    GoTo,
    Move,
    MotionBlock,
    PointInDirection,
    Turn,
    change_x,
    change_y,
    go_to,
    move,
    point_in_direction,
    turn,
)

__all__ = [
    "Script", "EventBlock", "WhenRun", "when_run", "MotionBlock", "Move",
    "Turn", "GoTo", "ChangeX", "ChangeY", "PointInDirection", "move",
    "turn", "go_to", "change_x", "change_y", "point_in_direction",
]
