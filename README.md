# Scratkat
---
A scratch-based python API for making games and tools

ScratKat uses a 480×360 logical stage. Sprite coordinates and costume sizes
scale uniformly whenever the window changes size, preserving their Scratch-like
layout on Windows, macOS, and Linux.

Scripts are available from the package library:

```python
from scratkat import init
from scratkat.scripts import Script

project = init("My project")
sprite = project.add_sprite("Cat", "assets/cat.png")
sprite.attach_script("When green flag clicked")
sprite.set_costume("assets/cat-alt.png")
```

## Scripts, events, and motion

Scripts run blocks in the order they are added.  Use ``when_run()`` to run a
script at project startup, then compose it with motion blocks:

```python
from scratkat import init
from scratkat.scripts import go_to, move, turn, when_run

project = init("Moving sprite")
sprite = project.add_sprite("Player", "assets/player.png")

(sprite.attach_script(when_run())
 .then(go_to(-100, 0))
 .then(move(80))
 .then(turn(90)))

project.run()
```

Motion coordinates use the Scratch convention: ``x`` increases to the right,
``y`` increases upward, and direction ``90`` points right.  Available blocks
are ``move``, ``turn``, ``go_to``, ``change_x``, ``change_y``, and
``point_in_direction``.  See [examples](examples/) for runnable projects.

## Special thanks
---
Special thanks to the scratch team
