"""Clip 08: launch a conversation with the agent; EDK starts a private worker and briefs both Hermes.
Keeps recording until the briefing reply has landed (the terminal stops changing)."""
import _common  # noqa: F401
from rec import clip, click, glide, hold, wait_settled

with clip("08_launch", "Launch: the agent comes alive", "Launch"):
    card = (877, 450, 219, 298)
    glide(985, 610, caption="Launch the new agent", focus=card)
    hold(1, "Launch the new agent", focus=card)
    click(985, 610, caption="EDK starts a private worker for the conversation", settle=1.0, after=0)
    glide(700, 660, caption="Graph on the left, live Hermes terminal on the right")
    wait_settled(quiet=3.0, timeout=120)
    hold(2, "Briefed and ready: no runs yet")
