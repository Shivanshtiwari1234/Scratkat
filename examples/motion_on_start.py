"""Move a sprite as soon as the project's run method is called."""

from scratkat import init
from scratkat.scripts import change_y, go_to, move, turn, when_run


project = init("Motion on start")
sprite = project.add_sprite("Player")

(sprite.attach_script(when_run())
 .then(go_to(-100, -50))
 .then(move(80))
 .then(turn(90))
 .then(change_y(40)))

project.run()
