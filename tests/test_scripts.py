"""Tests for script blocks and project events."""

import os
import sys
import unittest

if sys.platform.startswith("linux"):
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from scratkat import Project
from scratkat.scripts import change_y, go_to, move, turn, when_run


class ScriptTests(unittest.TestCase):
    def setUp(self):
        self.project = Project()
        self.sprite = self.project.add_sprite("Player")

    def tearDown(self):
        self.project.window.close()

    def test_motion_blocks_run_in_order(self):
        (self.sprite.attach_script(when_run())
         .then(go_to(5, 10))
         .then(move(20))
         .then(turn(90))
         .then(change_y(-3)))

        self.project.trigger("run")

        self.assertAlmostEqual(self.sprite.cfg["x"], 25)
        self.assertAlmostEqual(self.sprite.cfg["y"], 7)
        self.assertEqual(self.sprite.cfg["dir"], 180)

    def test_non_matching_events_do_not_run_script(self):
        self.sprite.attach_script(when_run()).then(move(10))

        self.project.trigger("key_pressed")

        self.assertEqual(self.sprite.cfg["x"], 0)


if __name__ == "__main__":
    unittest.main()
