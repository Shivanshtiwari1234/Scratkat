from qtpy.QtWidgets import QWidget


STAGE_WIDTH = 480
STAGE_HEIGHT = 360


class Stage(QWidget):
    """The logical ScratKat stage.

    The stage always behaves as 480x360 internally and
    scales uniformly to fit the actual window.
    """

    def __init__(self, project):
        super().__init__()
        self.project = project

    def get_scale(self):
        """Return the uniform scale from logical stage to window."""

        if self.width() <= 0 or self.height() <= 0:
            return 1.0

        return min(
            self.width() / STAGE_WIDTH,
            self.height() / STAGE_HEIGHT,
        )

    def get_origin(self, scale):
        """Return the top-left corner of the scaled stage."""

        scaled_width = STAGE_WIDTH * scale
        scaled_height = STAGE_HEIGHT * scale

        offset_x = (self.width() - scaled_width) / 2
        offset_y = (self.height() - scaled_height) / 2

        return offset_x, offset_y

    def logical_to_screen(self, x, y, scale):
        """Convert ScratKat coordinates to screen coordinates."""

        origin_x, origin_y = self.get_origin(scale)

        screen_x = (
            origin_x
            + (x + STAGE_WIDTH / 2) * scale
        )

        # Logical Y increases upward.
        # Qt Y increases downward.
        screen_y = (
            origin_y
            + (STAGE_HEIGHT / 2 - y) * scale
        )

        return screen_x, screen_y

    def resizeEvent(self, event):
        """Update sprites whenever the stage is resized."""

        super().resizeEvent(event)
        self.project.update_sprites()
