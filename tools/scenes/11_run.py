"""Clip 11: the whole run, recorded continuously in real time (sped up in the edit).
Shows the Spec Reader's terminal while its lane works, then the main Hermes; stops when the run is done."""
import json
import subprocess
import sys
import time

import _common  # noqa: F401
from rec import clip, click, glide, hold, shot

CONTAINER = sys.argv[1]
TAB_HERMES, TAB_READER = (1500, 187), (1607, 187)


def run_state():
    out = subprocess.run(["docker", "exec", "-u", "vibe", CONTAINER, "cat", "/home/vibe/.edk/state.json"],
                         capture_output=True, text=True).stdout
    try:
        runs = [r for r in json.loads(out)["runs"] if r.get("kind") == "workflow"]
    except (ValueError, KeyError):
        return {}
    return runs[-1] if runs else {}


with clip("11_run", "Two Hermes at work", "Two Hermes at work"):
    glide(700, 640, caption="Both Hermes start at once, each in its own lane")
    shown_reader = done_reader = False
    last_step = None
    while True:
        run = run_state()
        nodes = run.get("current_nodes") or {}
        reader = any(agent != "hermes" for agent in nodes)
        step = run.get("current_node")
        if step != last_step:
            shot(f"step {step}")
            last_step = step
        if reader and not shown_reader:
            click(*TAB_READER, caption="The Spec Reader's own terminal", settle=0.8, after=3)
            glide(700, 900, caption="Spec Reader: convert, then brief")
            shown_reader = True
        elif shown_reader and not reader and not done_reader:
            hold(2, "Spec Reader done: briefing written")
            click(*TAB_HERMES, caption="Back to the main Hermes", settle=0.8, after=1)
            glide(1080, 640, caption="Main Hermes: study, then find every inconsistency")
            done_reader = True
        if run.get("status") in ("done", "failed", "cancelled", "interrupted"):
            shot(f"run {run.get('status')}")
            print("run", run.get("status"), run.get("error"), flush=True)
            hold(3, "All steps done")
            break
        time.sleep(1.0)
