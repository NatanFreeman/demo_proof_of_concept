"""Clip 02: the Trigger (a new .docx arrives), then zoom out and pan to make room for the pipeline.
Afterwards the canvas maps world (x, y) to screen (620.7 + 0.7986 x, 540.2 + 0.7986 y) — see canvas.py."""
import _common  # noqa: F401
from rec import clip, click, drag, hold, replace_text

with clip("02_trigger", "The trigger: a new spec arrives", "Trigger"):
    node = (735, 573, 275, 120)
    click(872, 645, caption="The Trigger wakes Hermes when a file is uploaded", settle=0.5, after=1, focus=node)
    INS = (70, 640, 300, 200)
    replace_text(217, 703, "New spec arrives", caption="Trigger: a new specification arrives", focus=INS)
    replace_text(217, 792, "*.docx", caption="…any Word document dropped on the agent", focus=INS)
    hold(2, "…any Word document dropped on the agent", focus=(70, 560, 960, 300))
    for i in range(2):
        click(1649, 1056, caption="Zoom out to make room for the whole pipeline", settle=0.4, after=1,
              focus=(1560, 1020, 170, 70))
    drag(1300, 960, 828, 886, caption="Pan the canvas")
    drag(453, 528, 477, 528, caption="Tidy up: move the Trigger")
    hold(1, "Ready to build")
