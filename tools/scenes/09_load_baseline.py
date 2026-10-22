"""Clip 09: Run on upload OFF; open Files from the dock; drag the whole baseline onto the agent."""
import _common  # noqa: F401
from rec import clip, click, drag, glide, hold, key, wait_settled

FILES = (1182, 605, 668, 395)
with clip("09_load-baseline", "Load everything uploaded so far", "Load the baseline"):
    click(311, 192, caption="Run on upload OFF while loading the existing baseline", settle=0.4, after=1,
          focus=(290, 178, 140, 30))
    click(33, 70, caption="Open Files", settle=1.2, after=1, focus=(10, 45, 50, 50))
    hold(1, "The Arrow 3 baseline: six specifications and the report kit", focus=FILES)
    click(1430, 713, caption="The Arrow 3 baseline: six specifications and the report kit", settle=0.3, after=0, focus=FILES)
    key("ctrl+a", caption="Select them all", after=1, focus=FILES)
    drag(1420, 817, 860, 420, caption="Drag the whole baseline onto the agent", settle=1.0)
    wait_settled(quiet=1.5, timeout=20)
    hold(2, "Uploaded into the agent's private workspace: 7 of 7")
    click(1410, 311, caption="Done", settle=0.8, after=1)
