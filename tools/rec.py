"""Human-style control of the LEFT monitor (DP-1, 0..1919 x 0..1079 on display :1), recorded as video clips.

Each scene runs inside `with clip("NN_name", "Label")`: ffmpeg captures the left monitor (pointer included,
lossless) only while the scene acts, so the operator's thinking time between scenes is never recorded.
A clip never ends on the last click: it keeps rolling until the screen has been still for a moment (pages
loaded, uploads done, replies drawn), so no action is cut off. Captions are logged with their time in the
clip (`<clip>.events.tsv`) for labels and callouts in the edit.
"""
import contextlib
import json
import math
import os
import random
import re
import subprocess
import time
from pathlib import Path

from PIL import Image, ImageChops

os.environ.setdefault("DISPLAY", ":1")
XDO = str(Path.home() / ".local/bin/xdotool")
SCROT = str(Path.home() / ".local/bin/scrot")
FFMPEG = "/snap/bin/ffmpeg"
VIDEO = Path(__file__).resolve().parents[1] / "arrow3-presentation/video"
CLIPS = VIDEO / "clips"
LIVE = Path(os.environ.get("REC_PEEK_DIR", VIDEO / "work/peek"))
CLIPS.mkdir(parents=True, exist_ok=True)
LIVE.mkdir(parents=True, exist_ok=True)
W, H = 1920, 1080
DWELL = 0.7          # seconds per "beat" of hold(): long enough for a viewer to read the result
random.seed(11)

_clip = {"name": None, "proc": None, "chapter": "", "moved": False}


def xdo(*args):
    if _clip["name"] and not _clip["moved"]:
        _clip["moved"] = True  # the first real input: the edit aligns events to the video with it
        _event("motion", "first input")
    subprocess.run([XDO, *map(str, args)], check=True)


def _event(kind, text, x="", y="", box=""):
    with open(CLIPS / f"{_clip['name']}.events.tsv", "a") as f:
        f.write(f"{time.time():.3f}\t{kind}\t{text}\t{x}\t{y}\t{box}\n")


def ease(t):
    return 0.5 - 0.5 * math.cos(math.pi * t)


def mouse():
    out = subprocess.check_output([XDO, "getmouselocation"]).decode()
    return int(re.search(r"x:(\d+)", out)[1]), int(re.search(r"y:(\d+)", out)[1])


# ─── Screen state ─────────────────────────────────────────────────────────────
def grab(path=None):
    path = path or LIVE / "_grab.png"
    subprocess.run([SCROT, "-p", "-a", f"0,0,{W},{H}", "-o", str(path)], check=True)
    return path


def peek(name="peek.png", crop=None):
    """A screenshot for checking the screen; never part of a recording."""
    path = grab(LIVE / name)
    if crop:
        x, y, w, h = crop
        subprocess.run(["convert", str(path), "-crop", f"{w}x{h}+{x}+{y}", "+repage", str(path)], check=True)
    return path


def _small():
    # Below the GNOME top bar (its clock changes every minute), downscaled: cheap to compare.
    return Image.open(grab()).convert("L").crop((0, 34, W, H)).resize((480, 262))


def wait_settled(quiet=1.2, timeout=10.0, threshold=40):
    """Return once the screen has not changed for `quiet` seconds (or after `timeout`).
    A blinking text cursor changes only a few downscaled pixels, below `threshold`."""
    end = time.time() + timeout
    last, still_since = _small(), time.time()
    while time.time() < end:
        time.sleep(0.25)
        now = _small()
        changed = ImageChops.difference(now, last).point(lambda v: 255 if v > 24 else 0).histogram()[255]
        if changed > threshold:
            still_since = time.time()
        last = now
        if time.time() - still_since >= quiet:
            return True
    return False


# ─── Clips ────────────────────────────────────────────────────────────────────
@contextlib.contextmanager
def clip(name, label, chapter_title=""):
    """Record the left monitor while the block runs, then until the screen settles.
    Events carry wall-clock times; the edit aligns them with the video at the first real input."""
    out = CLIPS / f"{name}.mkv"
    events = CLIPS / f"{name}.events.tsv"
    events.write_text("")
    _clip.update(name=name, moved=False)
    _event("start", label)
    if chapter_title:
        _event("chapter", chapter_title)
    proc = subprocess.Popen(
        [FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-f", "x11grab", "-draw_mouse", "1", "-framerate", "30",
         "-video_size", f"{W}x{H}", "-i", ":1.0+0,0", "-c:v", "libx264rgb", "-preset", "ultrafast", "-qp", "0", str(out)],
        stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=open(CLIPS / f"{name}.ffmpeg.log", "w"))
    _clip["proc"] = proc
    time.sleep(2.0)  # the snap ffmpeg needs ~1 s to start capturing; the edit trims any extra still lead-in
    try:
        yield
        wait_settled()
        time.sleep(0.8)  # a beat of the final state
        _event("end", label)
    finally:
        proc.stdin.write(b"q")
        proc.stdin.close()
        proc.wait(timeout=60)
        _clip.update(name=None, proc=None)


def chapter(name):
    _clip["chapter"] = name


def shot(caption="", focus=None):
    """Mark a caption at this moment of the clip (for labels and callouts in the edit)."""
    if not _clip["name"]:
        return
    x, y = mouse()
    _event("caption", caption, x, y, ",".join(map(str, focus)) if focus else "")


def hold(beats=1, caption="", pause=0.0, focus=None):
    """A still moment for the viewer: `beats` × DWELL seconds (plus `pause`)."""
    shot(caption, focus)
    time.sleep(pause + beats * DWELL)


# ─── Mouse ────────────────────────────────────────────────────────────────────
def glide(x1, y1, shots=2, duration=None, caption="", focus=None, held=False):
    """Move like a hand: eased, slightly arced. (`shots` is kept for compatibility with the frame scenes.)"""
    x1, y1 = max(0, min(W - 1, int(x1))), max(0, min(H - 1, int(y1)))
    x0, y0 = mouse()
    if x0 >= W:  # pointer is on the right monitor: bring it over first
        xdo("mousemove", W - 40, min(max(y0, 200), H - 200))
        time.sleep(0.1)
        x0, y0 = mouse()
    dist = math.hypot(x1 - x0, y1 - y0)
    if caption:
        shot(caption, focus)
    if dist < 2:
        return
    duration = duration if duration is not None else min(1.0, 0.35 + dist / 2000)
    steps = max(12, int(dist / 14))
    bow = random.choice((-1, 1)) * min(50, dist * 0.07)
    nx, ny = -(y1 - y0) / dist, (x1 - x0) / dist
    for i in range(1, steps + 1):
        t = ease(i / steps)
        arc = math.sin(math.pi * i / steps) * bow
        xdo("mousemove", int(x0 + (x1 - x0) * t + nx * arc), int(y0 + (y1 - y0) * t + ny * arc))
        time.sleep(duration / steps)


def click(x, y, caption="", shots=2, settle=0.45, after=1, double=False, focus=None, button=1):
    glide(x, y, caption=caption, focus=focus)
    time.sleep(0.15)
    xdo("click", *(["--repeat", 2, "--delay", 90] if double else []), button)
    time.sleep(settle)
    if after:
        hold(after, caption, focus=focus)


def drag(x0, y0, x1, y1, caption="", shots=4, settle=0.6, focus=None, approach=1):
    glide(x0, y0, caption=caption, focus=focus)
    time.sleep(0.15)
    xdo("mousedown", 1)
    time.sleep(0.2)
    for k in range(1, 6):  # beyond the drag threshold
        xdo("mousemove", x0 + k * 3, y0 + k * 2)
        time.sleep(0.03)
    glide(x1, y1, duration=None, held=True)
    time.sleep(0.3)
    xdo("mouseup", 1)
    time.sleep(settle)
    shot(caption, focus)


# ─── Keyboard ─────────────────────────────────────────────────────────────────
def key(*keys, caption="", after=1, settle=0.3, focus=None):
    for k in keys:
        xdo("key", "--clearmodifiers", k)
        time.sleep(0.1)
    time.sleep(settle)
    if after:
        hold(after, caption, focus=focus)


def type_text(text, caption="", every=36, delay=None, focus=None):
    """Type like a person: short entries at a natural pace, long prompts briskly (a viewer reads, not waits)."""
    shot(caption, focus)
    delay = delay if delay is not None else (45 if len(text) <= 40 else 22 if len(text) <= 160 else 10)
    # Text goes through stdin: a leading "-" would otherwise be read as an option.
    subprocess.run([XDO, "type", "--clearmodifiers", "--delay", str(delay), "--file", "-"], input=text.encode(), check=True)
    time.sleep(0.25)


def replace_text(x, y, text, caption="", every=36, focus=None):
    """Click into a field, select its content and type over it."""
    click(x, y, caption=caption, settle=0.2, after=0, focus=focus)
    xdo("key", "--clearmodifiers", "ctrl+a")
    time.sleep(0.25)
    type_text(text, caption=caption, focus=focus)


def scroll(clicks, caption="", every=2, down=True, focus=None):
    shot(caption, focus)
    for _ in range(clicks):
        xdo("click", 5 if down else 4)
        time.sleep(0.12)
