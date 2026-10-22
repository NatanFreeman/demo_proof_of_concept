"""Clip 00: remove the open conversation and every custom agent, so the build starts from nothing."""
import time

import _common  # noqa: F401
from rec import clip, click, glide, hold, key, scroll, xdo

with clip("00_clean-slate", "Clean slate", "Start from a clean slate"):
    hold(1, "Existing conversations")
    click(1507, 221, caption="Delete the open conversation", after=0, settle=0.5)
    click(1507, 221, caption="Confirm: deleted with its container", after=2, settle=1.5)
    glide(1500, 640)
    scroll(12, down=False, caption="Back up to Your agents")
    time.sleep(0.8)
    glide(985, 930, caption="The last custom agent")
    hold(1, "The last custom agent")
    click(1059, 806, caption="Delete it permanently", after=1, settle=0.9)
    key("Return", caption="Delete it permanently", after=2, settle=1.0)
    glide(1250, 900, caption="Your agents: empty, ready for a new one")
    hold(2, "Your agents: empty, ready for a new one")
