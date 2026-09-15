"""Regression tests for logical-stage sprite placement."""

import os
import sys
import unittest

# Headless Qt is available on Linux CI.  Leave native backends alone on macOS
# and Windows, where developers normally run these tests with a desktop.
if sys.platform.startswith("linux"):
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from scratkat import Project, Script


class StageScalingTests(unittest.TestCase):
    def setUp(self):
        self.project = Project()
        self.project.canvas.resize(960, 540)
        self.sprite = self.project.add_sprite()
        # Supplying dimensions directly isolates coordinate conversion from
        # image decoding and verifies the widget geometry used for costumes.
        self.sprite._costume_width = 100
        self.sprite._costume_height = 50

    def tearDown(self):
        self.project.window.close()

    def test_costume_and_coordinates_scale_with_stage(self):
        self.sprite.cfg.update(x=240, y=90, size=100)
        self.project.update_sprites()

        # 960x540 is a 1.5x presentation of the 480x360 logical stage.
        # The 4:3 stage is centred in the 16:9 canvas, leaving 120 px bars.
        self.assertEqual(self.sprite._label.geometry().getRect(), (765, 98, 150, 75))

    def test_costume_size_is_relative_to_logical_stage(self):
        self.sprite.cfg["size"] = 50
        self.project.update_sprites()

        self.assertEqual(self.sprite._label.size().width(), 75)
        self.assertEqual(self.sprite._label.size().height(), 38)

    def test_script_library_is_public(self):
        script = self.sprite.attach_script("When green flag clicked")
        self.assertIsInstance(script, Script)
        self.assertEqual(script.name, "When green flag clicked")


if __name__ == "__main__":
    unittest.main()
