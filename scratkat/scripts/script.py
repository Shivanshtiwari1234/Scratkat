"""Script definitions used by ScratKat sprites."""


class Script:
    """An ordered set of blocks attached to a sprite.

    A script can be given an event trigger and one or more blocks.  Blocks are
    deliberately small objects: they only need an ``execute(sprite)`` method,
    which makes custom blocks straightforward to write too.
    """

    def __init__(self, name="Script 1", trigger=None):
        self.name = name
        self.trigger = trigger
        self.blocks = []
        self.sprite = None

    def add(self, block):
        """Append a block and return this script for fluent construction."""
        if not hasattr(block, "execute") and not callable(block):
            raise TypeError("A script block must be callable or define execute(sprite)")
        self.blocks.append(block)
        return self

    then = add

    def runs_on(self, event):
        """Return whether this script responds to *event*."""
        return self.trigger is not None and self.trigger.matches(event)

    def run(self):
        """Execute this script's blocks in attachment order."""
        if self.sprite is None:
            raise RuntimeError("Attach the script to a sprite before running it")

        for block in self.blocks:
            if hasattr(block, "execute"):
                block.execute(self.sprite)
            else:
                block(self.sprite)
