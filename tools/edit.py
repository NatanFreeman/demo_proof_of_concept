"""Edit the recorded screen clips into labelled, captioned MP4s and one final presentation video.

    python3 tools/edit.py clip NN_name   # one finished clip
    python3 tools/edit.py cards           # title + end card
    python3 tools/edit.py final           # join everything

Each raw clip (lossless, left monitor, pointer included) gets: a branded top band naming the chapter (it also
hides the desktop clock, so time jumps between clips don't show), a chapter title at the start, lower-third
captions, amber callouts around the part of the UI being used, smooth zooms while a field is filled in, and for
the run a speed badge with the real elapsed time. Events are logged in wall-clock time by tools/rec.py and are
aligned to the video at the moment recording stopped; the first pointer movement in the video cross-checks it.
"""
import json
import math
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
VIDEO = ROOT / "arrow3-presentation/video"
CLIPS = VIDEO / "clips"
OUT = VIDEO / "final"
FFMPEG, FFPROBE = "/snap/bin/ffmpeg", "/snap/bin/ffmpeg.ffprobe"
W, H, FPS = 1920, 1080, 30
NAVY, BLUE, AMBER, WHITE = (11, 42, 74), (3, 105, 161), (245, 158, 11), (255, 255, 255)
FONT = "/usr/share/fonts/truetype/ubuntu/UbuntuSans[wdth,wght].ttf"
ENCODE = ["-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-r", str(FPS), "-g", "60",
          "-vf", "scale=out_color_matrix=bt709:out_range=tv", "-colorspace", "bt709", "-color_primaries", "bt709",
          "-color_trc", "bt709", "-movflags", "+faststart"]

# name, chapter title, speed, zoom on focus areas[, options]
#   cut_before: end the clip where this caption starts (drop what follows)
MANIFEST = [
    ("00_clean-slate", "Start from a clean slate", 1.0, False),
    ("01_new-agent", "Build a new agent from scratch", 1.0, True),
    ("02_trigger", "The trigger: a new specification arrives", 1.0, True),
    ("03_baseline-register", "Baseline register: everything uploaded so far", 1.0, True),
    ("04_spec-reader", "A second Hermes, working in parallel", 1.0, True),
    ("05_analysis", "The analysis: find every inconsistency", 1.0, True),
    ("06_report-step", "The deliverable: an executive Word report", 1.0, True),
    ("07_save", "Save the agent", 1.0, False),
    ("08_launch", "Launch: the agent comes alive", 1.0, False),
    ("09_load-baseline", "Load the baseline: six specifications", 1.0, False),
    ("10_drop-new-spec", "Drop in the new specification", 1.0, False),
    ("11_run", "Two Hermes at work", 8.0, False),
    ("12_open-report", "The result: an executive Word report", 1.0, False),
    ("13_report-tour", "Inside the report", 1.0, False, {"cut_before": "Automated findings, confirmed by engineers"}),
]
HIDDEN = ("step ", "run ", "first input")


def font(size, weight="Bold"):
    f = ImageFont.truetype(FONT, size)
    f.set_variation_by_name(weight)
    return f


# ─── Clip analysis ────────────────────────────────────────────────────────────

@dataclass
class Event:
    t: float          # seconds in the raw video
    kind: str
    text: str
    x: int | None = None
    y: int | None = None
    box: tuple | None = None


@dataclass
class Clip:
    name: str
    title: str
    speed: float
    zoom: bool
    duration: float = 0.0
    start: float = 0.0
    end: float = 0.0
    offset: float = 0.0       # raw-video time = wall-clock time + offset
    events: list = field(default_factory=list)


def probe_duration(path):
    out = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True).stdout.strip().splitlines()
    return float(out[-1])


def first_motion(path, limit=8.0):
    """Seconds into the video of the first visible change below the top bar (the pointer starting to move)."""
    w, h = 480, 270
    proc = subprocess.run([FFMPEG, "-v", "error", "-t", str(limit), "-i", str(path), "-vf", f"scale={w}:{h},format=gray",
                           "-f", "rawvideo", "-"], capture_output=True)
    frames = np.frombuffer(proc.stdout, np.uint8).reshape(-1, h, w)[:, 10:, :].astype(np.int16)
    for i in range(1, len(frames)):
        if (np.abs(frames[i] - frames[i - 1]) > 18).sum() > 12:
            return i / FPS
    return None


def load_clip(name, title, speed, zoom, options=None):
    options = options or {}
    clip = Clip(name, title, speed, zoom)
    path = CLIPS / f"{name}.mkv"
    clip.duration = probe_duration(path)
    rows = [line.split("\t") for line in (CLIPS / f"{name}.events.tsv").read_text().splitlines() if line.strip()]
    motion = first_motion(path)
    legacy = rows and rows[0][1] == "label"  # clip 00: times relative to the start of the scene
    if legacy:
        first_input = next(float(r[0]) for r in rows if r[1] == "caption" and float(r[0]) > 0)
        offset = (motion or 1.0) - first_input
    else:
        end = next(float(r[0]) for r in rows if r[1] == "end")
        offset = clip.duration - (end + 0.03)
        first = next((float(r[0]) for r in rows if r[1] == "motion"), None)
        if motion is not None and first is not None:
            drift = (first + offset) - motion
            print(f"  {name}: end-aligned first input at {first + offset:.2f}s, pointer first moves at {motion:.2f}s "
                  f"(drift {drift:+.2f}s)", flush=True)
            # The end anchor is exact to ~0.1 s; a larger "drift" means something else moved first (EDK's
            # own animations during a run), so it is reported, never applied.
    clip.offset = offset
    for r in rows:
        r += [""] * (6 - len(r))
        t = float(r[0]) + offset
        box = tuple(int(v) for v in r[5].split(",")) if r[5] else None
        clip.events.append(Event(t, r[1], r[2], int(r[3]) if r[3] else None, int(r[4]) if r[4] else None, box))
    clip.events.sort(key=lambda e: e.t)
    start_from = motion if motion is not None else next((e.t for e in clip.events if e.kind == "caption"), 0.0)
    clip.start = max(0.0, start_from - 0.8)
    clip.end = clip.duration
    if "cut_before" in options:
        clip.end = next(e.t for e in clip.events if e.kind == "caption" and e.text == options["cut_before"]) + 0.1
    if name == "11_run":
        clip.events = [e for e in clip.events if e.kind != "caption"] + run_captions(clip)
        clip.events.sort(key=lambda e: e.t)
    return clip


READER_STEPS = ("New spec to Markdown", "Spec briefing")


def run_captions(clip):
    """Captions for the run from EDK's own step timings: what each Hermes is doing at every moment."""
    state = json.loads((VIDEO / "run_state_raw.json").read_text())
    agent = json.loads((VIDEO / "run_agent.json").read_text())
    agent = agent.get("agent", agent)
    labels = {n["id"]: n["label"] for n in agent["graph"]["nodes"]}
    run = [r for r in state["runs"] if r["kind"] == "workflow"][-1]
    steps = [(labels[k], v["started_at"], v["finished_at"]) for k, v in run["steps"].items()
             if v.get("started_at") and v.get("finished_at") and k in labels]
    events, last = [], None
    t = run["started_at"]
    while t < run["finished_at"]:
        main = next((label for label, a, b in steps if a <= t < b and label not in READER_STEPS), None)
        reader = next((label for label, a, b in steps if a <= t < b and label in READER_STEPS), None)
        if main is None and reader is not None:
            main = "waiting for the Spec Reader's result"
        parts = [f"Hermes: {main}" if main else None, f"Spec Reader: {reader}" if reader else None]
        text = "   ·   ".join(p for p in parts if p)
        if main == "Find inconsistencies" and not reader:
            text = "Hermes: Find inconsistencies, reasoning over every requirement"
        if text and text != last:
            events.append(Event(t + clip.offset, "caption", text))
            last = text
        t += 0.5
    events.append(Event(run["finished_at"] + clip.offset, "caption", "All steps done: the report is ready"))
    return events


def captions(clip):
    """(start, end, text, box) for each distinct visible caption."""
    caps = [e for e in clip.events if e.kind == "caption" and e.text and not e.text.startswith(HIDDEN)]
    out = []
    for e in caps:
        if out and out[-1][2] == e.text and out[-1][3] == e.box:
            continue
        if out:
            out[-1][1] = e.t
        out.append([e.t, clip.end, e.text, e.box])
    return [tuple(c) for c in out]


# ─── Camera (zoom on focus areas) ─────────────────────────────────────────────

def ease(x):
    x = min(1.0, max(0.0, x))
    return 0.5 - 0.5 * math.cos(math.pi * x)


def camera_keys(clip):
    base = (W / 2, H / 2, 1.0)
    keys = [(0.0, base)]
    if not clip.zoom:
        return keys
    segs = []
    for a, b, _, box in captions(clip):
        if not box or b - a < 1.6:
            continue
        x, y, w, h = box
        if w > 1100 or h > 760:
            continue
        z = min(1.75, (W - 120) / (w + 240), (H - 160) / (h + 260))
        if z < 1.2:
            continue
        cx, cy = x + w / 2, y + h / 2
        if segs and segs[-1][3:] == (cx, cy, z) and a - segs[-1][1] < 0.5:
            segs[-1][1] = b  # same area again: keep the zoom
        else:
            segs.append([a, b, None, cx, cy, z])
    prev_end = -10.0
    state = base
    for i, (a, b, _, cx, cy, z) in enumerate(segs):
        target = (cx, cy, z)
        t_in = max(a - 0.1, keys[-1][0] + 0.01)
        keys.append((t_in, state))
        keys.append((t_in + 0.8, target))
        keys.append((max(b - 0.15, t_in + 0.85), target))
        nxt = segs[i + 1][0] if i + 1 < len(segs) else None
        if nxt is not None and nxt - b < 1.4:
            state = target  # move straight on to the next area
        else:
            keys.append((max(b - 0.15, t_in + 0.85) + 0.8, base))
            state = base
        prev_end = b
    return keys


def camera_at(keys, t):
    if t <= keys[0][0]:
        return keys[0][1]
    for (t0, s0), (t1, s1) in zip(keys, keys[1:]):
        if t0 <= t <= t1:
            k = ease((t - t0) / max(1e-6, t1 - t0))
            z = math.exp(math.log(s0[2]) + (math.log(s1[2]) - math.log(s0[2])) * k)
            return (s0[0] + (s1[0] - s0[0]) * k, s0[1] + (s1[1] - s0[1]) * k, z)
    return keys[-1][1]


def view_box(cx, cy, z):
    vw, vh = W / z, H / z
    x0 = min(max(cx - vw / 2, 0), W - vw)
    y0 = min(max(cy - vh / 2, 0), H - vh)
    return x0, y0, vw, vh


# ─── Overlay graphics ─────────────────────────────────────────────────────────

def rounded(size, radius, fill):
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius, fill=fill)
    return img


def shadowed(img, blur=14, offset=(0, 6), alpha=110):
    pad = blur * 2
    canvas = Image.new("RGBA", (img.width + pad * 2, img.height + pad * 2), (0, 0, 0, 0))
    shadow = Image.new("RGBA", img.size, (0, 0, 0, alpha))
    shadow.putalpha(img.getchannel("A").point(lambda v: alpha if v else 0))
    canvas.alpha_composite(shadow, (pad + offset[0], pad + offset[1]))
    canvas = canvas.filter(ImageFilter.GaussianBlur(blur))
    canvas.alpha_composite(img, (pad, pad))
    return canvas, pad


_cache = {}


def caption_image(text):
    if ("cap", text) in _cache:
        return _cache[("cap", text)]
    f = font(31, "Medium")
    tw = int(f.getlength(text))
    box = rounded((tw + 92, 66), 16, NAVY + (236,))
    d = ImageDraw.Draw(box)
    d.rounded_rectangle((0, 0, 9, 65), 4, fill=(56, 189, 248, 255))
    d.text((52, 33), text, font=f, fill=WHITE, anchor="lm")
    img, pad = shadowed(box)
    _cache[("cap", text)] = (img, pad)
    return img, pad


def band_image(chapter_no, total, title):
    key = ("band", chapter_no, title)
    if key in _cache:
        return _cache[key]
    img = Image.new("RGBA", (W, 36), NAVY + (255,))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 33, W, 35), fill=BLUE + (255,))
    d.text((84, 17), "EDK", font=font(19, "ExtraBold"), fill=WHITE, anchor="lm")
    d.text((134, 17), "Find Inconsistencies in Requirements", font=font(17, "Medium"), fill=(203, 213, 225), anchor="lm")
    label = f"{chapter_no:02d} / {total:02d}   ·   {title}"
    d.text((W / 2, 17), label, font=font(18, "SemiBold"), fill=WHITE, anchor="mm")
    d.text((W - 24, 17), "Arrow 3 demo  ·  fictitious data", font=font(15, "Regular"), fill=(148, 163, 184), anchor="rm")
    _cache[key] = img
    return img


def chapter_image(chapter_no, title):
    key = ("chap", chapter_no, title)
    if key in _cache:
        return _cache[key]
    f_no, f_t = font(26, "Bold"), font(44, "Bold")
    tw = int(max(f_t.getlength(title), 200))
    box = rounded((tw + 120, 132), 20, (255, 255, 255, 246))
    d = ImageDraw.Draw(box)
    d.rounded_rectangle((0, 0, 11, 131), 5, fill=BLUE + (255,))
    d.text((52, 40), f"CHAPTER {chapter_no:02d}", font=f_no, fill=BLUE, anchor="lm")
    d.text((52, 88), title, font=f_t, fill=NAVY, anchor="lm")
    img, pad = shadowed(box, blur=18, alpha=90)
    _cache[key] = (img, pad)
    return img, pad


def speed_image(speed, elapsed):
    f1, f2 = font(30, "ExtraBold"), font(22, "Medium")
    box = rounded((360, 64), 16, NAVY + (236,))
    d = ImageDraw.Draw(box)
    d.text((26, 32), f"▶▶ {speed:g}×", font=f1, fill=(56, 189, 248), anchor="lm")
    m, s = divmod(int(elapsed), 60)
    d.text((334, 32), f"real time {m:02d}:{s:02d}", font=f2, fill=WHITE, anchor="rm")
    return shadowed(box)


def paste(frame, img, xy, alpha=1.0):
    if alpha <= 0:
        return
    if alpha < 1:
        img = img.copy()
        img.putalpha(img.getchannel("A").point(lambda v: int(v * alpha)))
    frame.alpha_composite(img, (int(xy[0]), int(xy[1])))


def callout(frame, rect, alpha):
    if alpha <= 0:
        return
    x0, y0, x1, y1 = rect
    layer = Image.new("RGBA", (int(x1 - x0) + 40, int(y1 - y0) + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle((20, 20, layer.width - 21, layer.height - 21), 12, outline=AMBER + (int(90 * alpha),), width=12)
    layer = layer.filter(ImageFilter.GaussianBlur(5))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle((20, 20, layer.width - 21, layer.height - 21), 12, outline=AMBER + (int(255 * alpha),), width=4)
    frame.alpha_composite(layer, (int(x0) - 20, int(y0) - 20))


# ─── Rendering ────────────────────────────────────────────────────────────────

def final_name(index, name):
    """Finished clips are numbered like the chapters on screen: 00_clean-slate.mkv → 01_clean-slate.mp4."""
    return f"{index:02d}_{name.split('_', 1)[1]}.mp4"


def render_clip(index, clip, total):
    caps = captions(clip)
    keys = camera_keys(clip)
    length = clip.end - clip.start
    out_frames = int(length / clip.speed * FPS)
    decoder = subprocess.Popen(
        [FFMPEG, "-v", "error", "-ss", f"{clip.start:.3f}", "-t", f"{length:.3f}", "-i", str(CLIPS / f"{clip.name}.mkv"),
         "-vf", f"setpts=(PTS-STARTPTS)/{clip.speed},fps={FPS}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        stdout=subprocess.PIPE)
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / "clips" / final_name(index, clip.name)
    target.parent.mkdir(exist_ok=True)
    encoder = subprocess.Popen([FFMPEG, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                                "-r", str(FPS), "-i", "-", *ENCODE, str(target)], stdin=subprocess.PIPE)
    band = band_image(index, total, clip.title)
    chap, chap_pad = chapter_image(index, clip.title)
    run = None
    if clip.speed > 1:
        state = json.loads((VIDEO / "run_state_raw.json").read_text())
        run = [r for r in state["runs"] if r["kind"] == "workflow"][-1]
    size = W * H * 3
    n = 0
    while True:
        raw = decoder.stdout.read(size)
        if len(raw) < size:
            break
        t_out = n / FPS
        t = clip.start + t_out * clip.speed           # time in the raw clip
        frame = Image.frombuffer("RGB", (W, H), raw)
        cx, cy, z = camera_at(keys, t)
        x0, y0, vw, vh = view_box(cx, cy, z)
        if z > 1.001:
            frame = frame.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + vw, y0 + vh))
        frame = frame.convert("RGBA")
        # callout around the focus area of the current caption
        for a, b, text, box in caps:
            if a <= t < b and box and box[2] * box[3] < W * H * 0.4:
                fade = min(ease((t - a) / 0.3), ease((b - t) / 0.2))
                bx, by, bw, bh = box
                rect = ((bx - x0) * z, (by - y0) * z, (bx + bw - x0) * z, (by + bh - y0) * z)
                callout(frame, rect, fade)
        paste(frame, band, (0, 0))
        # chapter title for the first seconds of the clip
        if t_out < 3.6:
            alpha = min(ease(t_out / 0.4), ease((3.6 - t_out) / 0.5))
            paste(frame, chap, (90 - chap_pad, 70 - chap_pad + (1 - alpha) * 12), alpha)
        # caption
        for a, b, text, box in caps:
            if a <= t < b:
                img, pad = caption_image(text)
                fade = min(ease((t - a) / (0.25 * clip.speed)), 1.0)
                paste(frame, img, ((W - img.width) / 2, H - 128 - pad + (1 - fade) * 8), fade)
                break
        if run:
            wall = t - clip.offset
            elapsed = min(max(0.0, wall - run["started_at"]), run["finished_at"] - run["started_at"])
            img, pad = speed_image(clip.speed, elapsed)
            paste(frame, img, (W - img.width + pad - 24, 52 - pad))
        encoder.stdin.write(frame.convert("RGB").tobytes())
        n += 1
        if n % 300 == 0:
            print(f"  {clip.name}: {n}/{out_frames} frames", flush=True)
    decoder.wait()
    encoder.stdin.close()
    encoder.wait()
    print(f"  {clip.name}: done, {n} frames ({n / FPS:.1f}s) → {target.relative_to(ROOT)}", flush=True)
    return target


# ─── Cards ────────────────────────────────────────────────────────────────────

def card_background():
    y = np.linspace(0, 1, H)[:, None]
    x = np.linspace(0, 1, W)[None, :]
    top, bottom = np.array([11, 42, 74]), np.array([3, 22, 44])
    k = (0.65 * y + 0.35 * x)[..., None]
    img = (top * (1 - k) + bottom * k).astype(np.uint8)
    bg = Image.fromarray(img, "RGB").convert("RGBA")
    d = ImageDraw.Draw(bg)
    for gx in range(0, W, 48):
        d.line((gx, 0, gx, H), fill=(255, 255, 255, 6))
    for gy in range(0, H, 48):
        d.line((0, gy, W, gy), fill=(255, 255, 255, 6))
    return bg


def write_card(path, frames_fn, seconds):
    encoder = subprocess.Popen([FFMPEG, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                                "-r", str(FPS), "-i", "-", *ENCODE, str(path)], stdin=subprocess.PIPE)
    for n in range(int(seconds * FPS)):
        encoder.stdin.write(frames_fn(n / FPS, seconds).convert("RGB").tobytes())
    encoder.stdin.close()
    encoder.wait()
    print("  card →", path.relative_to(ROOT), flush=True)


def title_card():
    bg = card_background()
    d = ImageDraw.Draw(bg)
    d.text((160, 330), "EDK  ·  BUILD YOUR OWN AGENT", font=font(30, "Bold"), fill=(56, 189, 248))
    d.text((152, 390), "Find Inconsistencies", font=font(104, "ExtraBold"), fill=WHITE)
    d.text((152, 510), "in Requirements", font=font(104, "ExtraBold"), fill=WHITE)
    d.rectangle((160, 662, 380, 668), fill=AMBER)
    d.text((160, 700), "An AI agent built on screen without code, then run on the Arrow 3 specifications:",
           font=font(34, "Regular"), fill=(203, 213, 225))
    d.text((160, 748), "it checks a new spec against every document uploaded so far and writes the report.",
           font=font(34, "Regular"), fill=(203, 213, 225))
    d.text((160, 980), "Real screen recording  ·  All Arrow 3 content is fictitious demonstration data",
           font=font(22, "Regular"), fill=(148, 163, 184))
    still = bg

    def frame(t, total):
        img = still.copy()
        fade = min(ease(t / 0.8), ease((total - t) / 0.6))
        black = Image.new("RGBA", (W, H), (0, 0, 0, int(255 * (1 - fade))))
        img.alpha_composite(black)
        return img
    write_card(OUT / "parts/00_title.mp4", frame, 6.0)


def end_card():
    summary = json.loads((VIDEO / "run_summary.json").read_text())
    bg = card_background()
    d = ImageDraw.Draw(bg)
    d.text((140, 110), "THE RESULT", font=font(30, "Bold"), fill=(56, 189, 248))
    d.text((132, 160), f"{summary['total']} inconsistencies found", font=font(84, "ExtraBold"), fill=WHITE)
    d.text((140, 272), f"in {summary['spec']}, checked against all {summary['baseline_docs']} baseline documents",
           font=font(30, "Regular"), fill=(203, 213, 225))
    tiles = [("CRITICAL", summary["Critical"], (185, 28, 28)), ("MAJOR", summary["Major"], (234, 88, 12)),
             ("MINOR", summary["Minor"], (202, 138, 4))]
    for i, (label, value, color) in enumerate(tiles):
        x = 140 + i * 300
        d.rounded_rectangle((x, 360, x + 270, 560), 18, fill=color)
        d.text((x + 135, 445), str(value), font=font(96, "ExtraBold"), fill=WHITE, anchor="mm")
        d.text((x + 135, 525), label, font=font(26, "Bold"), fill=WHITE, anchor="mm")
    facts = [f"{summary['minutes']} from dropping the file to the finished Word report",
             "Two Hermes agents working in parallel, each in its own conversation",
             "Built in the visual builder: 16 nodes, one trigger, no code",
             "Every finding quoted side by side, with impact, owner and fix"]
    for i, text in enumerate(facts):
        y = 640 + i * 62
        d.ellipse((142, y + 8, 160, y + 26), fill=AMBER)
        d.text((180, y), text, font=font(32, "Medium"), fill=WHITE)
    cover = Image.open(VIDEO / "report_cover.png").convert("RGBA")
    cover = cover.resize((560, int(cover.height * 560 / cover.width)), Image.LANCZOS)
    framed, pad = shadowed(cover, blur=24, offset=(0, 12), alpha=150)
    bg.alpha_composite(framed, (1220 - pad, 120 - pad))
    d.text((1220 + 280, 120 + cover.height + 34), "The generated report (page 1 of 5)", font=font(22, "Regular"),
           fill=(148, 163, 184), anchor="mm")
    d.text((140, 1000), "EDK  ·  Find Inconsistencies in Requirements  ·  fictitious Arrow 3 demonstration data",
           font=font(22, "Regular"), fill=(148, 163, 184))
    still = bg

    def frame(t, total):
        img = still.copy()
        fade = min(ease(t / 0.8), ease((total - t) / 1.0))
        img.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * (1 - fade)))))
        return img
    write_card(OUT / "parts/99_end.mp4", frame, 9.0)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    cmd = sys.argv[1]
    total = len(MANIFEST)
    if cmd == "clip":
        for wanted in sys.argv[2:]:
            for i, (name, title, speed, zoom, *opt) in enumerate(MANIFEST):
                if name == wanted:
                    render_clip(i + 1, load_clip(name, title, speed, zoom, *opt), total)
    elif cmd == "probe":
        for name, title, speed, zoom, *opt in MANIFEST:
            if (CLIPS / f"{name}.mkv").exists():
                c = load_clip(name, title, speed, zoom, *opt)
                print(f"{name}: raw {c.duration:.1f}s, from {c.start:.1f}s to {c.end:.1f}s → {(c.end - c.start) / speed:.1f}s, "
                      f"{len(captions(c))} captions, {len(camera_keys(c)) - 1} camera keys")
    elif cmd == "cards":
        (OUT / "parts").mkdir(parents=True, exist_ok=True)
        title_card()
        end_card()
    elif cmd == "final":
        parts = [OUT / "parts/00_title.mp4"] + [OUT / "clips" / final_name(i + 1, n) for i, (n, *_) in enumerate(MANIFEST)] + [OUT / "parts/99_end.mp4"]
        missing = [p for p in parts if not p.exists()]
        if missing:
            sys.exit("missing parts: " + ", ".join(str(p.relative_to(ROOT)) for p in missing))
        listing = OUT / "parts/concat.txt"
        listing.write_text("".join(f"file '{p}'\n" for p in parts))
        target = VIDEO / "Find-Inconsistencies-in-Requirements_EDK-demo.mp4"
        subprocess.run([FFMPEG, "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(listing), "-c", "copy",
                        "-movflags", "+faststart", str(target)], check=True)
        print("final →", target.relative_to(ROOT), f"{probe_duration(target):.1f}s")


if __name__ == "__main__":
    main()
