"""Clip 12: click the report in the Output node, open it from Chrome's download bubble, show it in Word (LibreOffice)."""
import subprocess
import time

import _common  # noqa: F401
from rec import XDO, W, clip, click, glide, hold, wait_settled

with clip("12_open-report", "Open the Word report", "The result"):
    out_node = (1214, 306, 186, 80)
    glide(1240, 640, caption="Every step done")
    hold(1, "Every step done")
    glide(1305, 362, caption="The Inconsistency report is ready", focus=out_node)
    hold(1, "The Inconsistency report is ready", focus=out_node)
    click(1305, 362, caption="Download it", settle=1.2, after=0, focus=out_node)
    click(1600, 178, caption="Open it in Word", settle=0.2, after=0)
    wid = None
    for _ in range(120):
        found = subprocess.run([XDO, "search", "--onlyvisible", "--name", "Consistency_Report"], capture_output=True,
                               text=True).stdout.split()
        if found:
            wid = found[-1]
            break
        time.sleep(0.25)
    assert wid, "LibreOffice did not open the report"
    time.sleep(1.5)
    geometry = subprocess.run([XDO, "getwindowgeometry", wid], capture_output=True, text=True).stdout
    subprocess.run([XDO, "windowactivate", "--sync", wid])
    time.sleep(0.3)
    if "Position: 19" in geometry or "Position: 2" in geometry:   # opened on the right monitor
        subprocess.run([XDO, "key", "--clearmodifiers", "super+shift+Left"])
        time.sleep(1.0)
    geometry = subprocess.run([XDO, "getwindowgeometry", wid], capture_output=True, text=True).stdout
    if "Geometry: 1854x" not in geometry:
        subprocess.run([XDO, "key", "--clearmodifiers", "super+Up"])
        time.sleep(1.0)
    glide(960, 640, caption="The executive Word report")
    wait_settled(quiet=1.5, timeout=10)
    hold(3, "The executive Word report")
