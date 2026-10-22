"""Clip 10: Run on upload ON; in Files go up to the documents folder, open incoming, drag the new spec onto the agent."""
import _common  # noqa: F401
from rec import clip, click, drag, hold

FILES = (1182, 605, 668, 395)
with clip("10_drop-new-spec", "Drop in the new specification", "The trigger: a new specification"):
    click(311, 192, caption="Run on upload ON", settle=0.4, after=1, focus=(290, 178, 140, 30))
    click(33, 70, caption="Back to Files", settle=1.0, after=0, focus=(10, 45, 50, 50))
    click(1446, 622, caption="Up to the Arrow 3 documents folder", settle=0.9, after=1, focus=FILES)
    click(1279, 765, caption="The incoming folder", settle=1.0, after=1, double=True, focus=FILES)
    click(1420, 713, caption="The new Interceptor Segment Specification, Rev A", settle=0.3, after=1, focus=FILES)
    drag(1420, 713, 860, 420, caption="Drop it onto the agent", settle=1.0)
    hold(2, "Uploaded: 1 run started")
    click(1410, 311, caption="Two Hermes start working", settle=0.8, after=1)
