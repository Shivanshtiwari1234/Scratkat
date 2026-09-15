"""Script definitions used by ScratKat sprites."""


class Script:
    """A named script attached to a sprite.

    Script execution is intentionally not implemented yet; this class keeps
    script data in a stable, importable library for future script blocks.
    """

    def __init__(self, name="Script 1"):
        self.name = name
