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

## Special thanks
---
Special thanks to the scratch team
