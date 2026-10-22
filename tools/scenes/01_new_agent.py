"""Clip 01: Home → Build Your Own Agent → Blank canvas; name, description, icon and colour."""
import _common  # noqa: F401
from rec import clip, click, glide, hold, replace_text, type_text

with clip("01_new-agent", "A new agent, from scratch", "Build a new agent"):
    card = (632, 786, 220, 294)
    glide(741, 880, caption="Your agents: build a brand-new one", focus=card)
    hold(1, "Your agents: build a brand-new one", focus=card)
    click(741, 890, caption="Build Your Own Agent", settle=2.0, after=1)
    blank = (613, 464, 372, 167)
    glide(780, 548, caption="Start from a blank canvas", focus=blank)
    hold(1, "Start from a blank canvas", focus=blank)
    click(780, 548, caption="Blank canvas: Hermes and one Trigger", settle=1.2, after=2)
    ID = (70, 180, 300, 450)
    replace_text(217, 247, "Find Inconsistencies in Requirements", caption="Name the agent", focus=ID)
    hold(1, "Name the agent", focus=ID)
    click(217, 328, caption="Describe its purpose", settle=0.2, after=0, focus=ID)
    type_text("Checks every new Arrow 3 specification against all documents uploaded so far, with two Hermes agents "
              "working in parallel, and issues an executive Word report of every inconsistency.",
              caption="Describe its purpose", focus=ID)
    hold(1, "Describe its purpose", focus=ID)
    click(146, 462, caption="Pick an icon", settle=0.4, after=1, focus=ID)
    click(247, 565, caption="Pick a colour: the builder turns Arrow blue", settle=0.6, after=2, focus=ID)
