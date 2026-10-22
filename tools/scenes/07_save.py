"""Clip 07: save the agent; it appears on Home under Your agents."""
import _common  # noqa: F401
from rec import clip, click, hold

with clip("07_save", "Save the agent", "Save"):
    click(1846, 146, caption="Save the agent", settle=2.5, after=2, focus=(1690, 125, 220, 45))
    hold(2, "The new agent, on Home")
