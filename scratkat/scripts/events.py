"""Event blocks that decide when a script is run."""


class EventBlock:
    """Base class for a script trigger."""

    event_name = None

    def matches(self, event):
        return event == self.event_name


class WhenRun(EventBlock):
    """Trigger a script whenever :meth:`scratkat.Project.run` is called."""

    event_name = "run"


def when_run():
    """Create a trigger for project startup."""
    return WhenRun()
