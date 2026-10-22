"""The 2-minute management film: problem → build the agent → run it → the result → why it matters.

    python3 tools/story.py

Cuts the recorded screen clips (arrow3-presentation/video/clips) into a story with simple-English captions,
labelled callouts on the parts of the system that matter, gentle zooms, a three-part progress band, honest
speed badges (with the real elapsed time during the run) and short dissolves between shots.
"""
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
import edit  # noqa: E402
from edit import (AMBER, BLUE, CLIPS, ENCODE, FFMPEG, FPS, H, NAVY, VIDEO, W, WHITE, callout, card_background,  # noqa: E402
                  ease, font, paste, rounded, shadowed, view_box)

TARGET = VIDEO / "Find-Inconsistencies_2-minute-film.mp4"
ACTS = ["Build the agent", "Run it", "Read the result"]
XFADE = 9  # frames of dissolve between shots

# Screen boxes (x, y, w, h) in the recorded frames.
FIT = {"register": (850, 506, 194, 92), "reader": (412, 853, 843, 95), "find": (1273, 506, 194, 105),
       "report": (1483, 506, 194, 109)}
RUNVIEW = {"hermes": (342, 503, 170, 63), "reader": (110, 859, 170, 62), "terminal": (1450, 174, 466, 900),
           "report_out": (1212, 304, 190, 84)}

# One shot = a stretch of one clip. Times a/b are seconds in the raw clip; captions and callouts use seconds
# into the shot. cam = (cx, cy, zoom, start, ramp): ease from the full screen to that view.
SHOTS = [
    # ── 1 · BUILD ──
    dict(act=0, clip="01_new-agent", a=1.8, b=21.0, speed=3.5,
         caption="We build a new AI agent in EDK. No code: just drag and drop."),
    dict(act=0, clip="02_trigger", a=1.9, b=9.2, speed=3.0,
         caption="It starts by itself when a new Word file arrives."),
    dict(act=0, clip="03_baseline-register", a=1.9, b=47.3, speed=7.0,
         caption="Part 1: it keeps a register of all approved requirements."),
    dict(act=0, clip="04_spec-reader", a=1.9, b=10.7, speed=2.2,
         caption="Part 2: a second AI agent works at the same time.",
         callouts=[(1.8, (378, 872, 175, 65), "AI agent 2")]),
    dict(act=0, clip="04_spec-reader", a=10.7, b=58.3, speed=9.0,
         caption="Agent 2 reads the new spec and lists every requirement in it."),
    dict(act=0, clip="05_analysis", a=1.9, b=28.1, speed=6.0,
         caption="Part 3: the two results come together."),
    dict(act=0, clip="05_analysis", a=31.4, b=35.6, speed=1.1, cam=(220, 805, 1.55, 0.0, 0.5),
         caption="The task is written in plain English: find every conflict."),
    dict(act=0, clip="06_report-step", a=1.9, b=28.1, speed=8.0,
         caption="Part 4: it writes a Word report."),
    dict(act=0, clip="06_report-step", a=30.3, b=35.0, speed=0.8,
         caption="The full agent: 16 blocks, 2 AI agents, no code.",
         callouts=[(0.5, FIT["register"], "1 · Register of approved requirements"),
                   (1.4, FIT["reader"], "2 · Agent 2 reads the new spec"),
                   (2.3, FIT["find"], "3 · Find conflicts"),
                   (3.2, FIT["report"], "4 · Word report")]),
    # ── 2 · RUN ──
    dict(act=1, clip="07_save", a=1.9, b=7.0, speed=2.5,
         caption="Save the agent. Start it."),
    dict(act=1, clip="08_launch", a=1.9, b=20.2, speed=4.0,
         caption="The agent opens. On the right, you can watch the AI think.",
         callouts=[(1.6, RUNVIEW["terminal"], "Live AI terminal")]),
    dict(act=1, clip="09_load-baseline", a=1.9, b=17.5, speed=3.5,
         caption="First, we upload the 6 approved specifications (the baseline)."),
    dict(act=1, clip="10_drop-new-spec", a=9.4, b=18.5, speed=1.8,
         caption="Now a new specification arrives. We drop it in."),
    dict(act=1, clip="11_run", a=0.4, b=220.0, speed=15.0, run=True,
         callouts=[(0.4, RUNVIEW["hermes"], "AI agent 1", 4.6), (0.4, RUNVIEW["reader"], "AI agent 2", 4.6)]),
    dict(act=1, clip="11_run", a=220.0, b=239.2, speed=4.0, run=True,
         callouts=[(2.9, RUNVIEW["report_out"], "Report ready")]),
    # ── 3 · RESULT ──
    dict(act=2, clip="12_open-report", a=3.3, b=12.8, speed=1.7,
         caption="Open the report in Word."),
    dict(act=2, clip="12_open-report", a=12.8, b=18.5, speed=1.0, cam=(957, 511, 1.33, 0.4, 1.6),
         caption="11 conflicts found. 4 of them are critical.",
         callouts=[(1.3, (568, 501, 776, 118), "11 conflicts found"),
                   (2.6, (568, 642, 778, 70), "Not ready for the design review")]),
    dict(act=2, clip="13_report-tour", a=13.8, b=17.7, speed=1.0, cam=(957, 470, 1.3, 0.6, 1.2),
         caption="Where are the conflicts? Most are in the launcher interface.",
         callouts=[(1.2, (1044, 354, 154, 250), "Launcher interface (ICD-110)")]),
    dict(act=2, clip="13_report-tour", a=22.6, b=26.9, speed=1.0, cam=(957, 545, 1.42, 0.1, 1.2),
         caption="Each conflict shows both texts, side by side.",
         callouts=[(0.7, (570, 475, 389, 90), "New spec says…"), (1.5, (957, 475, 388, 90), "Approved ICD says…")]),
    dict(act=2, clip="13_report-tour", a=37.6, b=41.7, speed=1.0, cam=(957, 340, 1.28, 0.5, 1.2),
         caption="And an action plan: who fixes what, and when.",
         callouts=[(0.9, (1078, 186, 266, 300), "Owner and due date")]),
]

# During the run: what each agent is doing, by seconds since the new spec was dropped (EDK's own step times).
RUN_CAPTIONS = [(0, "Two AI agents work at the same time."),
                (43, "Agent 2 sums up the new spec. Agent 1 studies all requirements."),
                (86, "Agent 1 compares every new requirement with all 66 approved ones."),
                (170, "Values, units, interfaces, standards: it checks them all."),
                (258, "The Word report is written.")]


# ─── Graphics ─────────────────────────────────────────────────────────────────

_cache = {}


def band(act):
    if act in _cache:
        return _cache[act]
    img = Image.new("RGBA", (W, 40), NAVY + (255,))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 37, W, 39), fill=BLUE + (255,))
    d.text((84, 19), "EDK", font=font(20, "ExtraBold"), fill=WHITE, anchor="lm")
    d.text((134, 19), "Find inconsistencies in requirements", font=font(18, "Medium"), fill=(203, 213, 225), anchor="lm")
    x = 1010
    for i, name in enumerate(ACTS):
        on = i == act
        label = f"{i + 1}  {name}"
        f = font(18, "Bold" if on else "Medium")
        w = int(f.getlength(label)) + 34
        if on:
            d.rounded_rectangle((x, 6, x + w, 32), 13, fill=(56, 189, 248))
        d.text((x + w / 2, 19), label, font=f, fill=NAVY if on else (148, 163, 184), anchor="mm")
        x += w + 14
    d.text((W - 24, 19), "demo data", font=font(15, "Regular"), fill=(148, 163, 184), anchor="rm")
    _cache[act] = img
    return img


def caption(text):
    key = ("cap", text)
    if key in _cache:
        return _cache[key]
    f = font(36, "SemiBold")
    tw = int(f.getlength(text))
    box = rounded((tw + 100, 78), 18, NAVY + (238,))
    d = ImageDraw.Draw(box)
    d.rounded_rectangle((0, 0, 10, 77), 5, fill=(56, 189, 248, 255))
    d.text((56, 39), text, font=f, fill=WHITE, anchor="lm")
    _cache[key] = shadowed(box)
    return _cache[key]


def label(text):
    key = ("label", text)
    if key in _cache:
        return _cache[key]
    f = font(25, "Bold")
    box = rounded((int(f.getlength(text)) + 36, 44), 12, AMBER + (255,))
    ImageDraw.Draw(box).text((18, 22), text, font=f, fill=NAVY, anchor="lm")
    _cache[key] = shadowed(box, blur=10, alpha=90)
    return _cache[key]


def badge(speed, elapsed=None):
    f1, f2 = font(26, "ExtraBold"), font(22, "Medium")
    text = f"{speed:g}× faster"
    w = int(f1.getlength(text)) + 78 + (int(f2.getlength("real time 00:00")) + 30 if elapsed is not None else 0)
    box = rounded((w, 54), 15, NAVY + (232,))
    d = ImageDraw.Draw(box)
    sky = (56, 189, 248)
    for x in (22, 37):  # fast-forward icon (the UI font has no ▶ glyph)
        d.polygon([(x, 17), (x + 15, 27), (x, 37)], fill=sky)
    d.text((60, 27), text, font=f1, fill=sky, anchor="lm")
    if elapsed is not None:
        m, s = divmod(int(elapsed), 60)
        d.text((w - 22, 27), f"real time {m:02d}:{s:02d}", font=f2, fill=WHITE, anchor="rm")
    return shadowed(box)


# ─── Rendering ────────────────────────────────────────────────────────────────

class Film:
    def __init__(self, path):
        self.encoder = subprocess.Popen([FFMPEG, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s",
                                         f"{W}x{H}", "-r", str(FPS), "-i", "-", *ENCODE, str(path)], stdin=subprocess.PIPE)
        self.last = None
        self.frames = 0
        self.marks = []

    def write(self, frame):
        frame = frame.convert("RGB")
        self.encoder.stdin.write(frame.tobytes())
        self.last = frame
        self.frames += 1

    def dissolve_into(self, frame, k):
        if self.last is None:
            return frame
        return Image.blend(self.last, frame.convert("RGB"), k).convert("RGBA")

    def close(self):
        self.encoder.stdin.close()
        self.encoder.wait()


def place_label(frame, rect, text, alpha):
    img, pad = label(text)
    x0, y0, x1, y1 = rect
    x = min(max(x0 - pad, 10 - pad), W - img.width + pad - 10)
    y = y0 - img.height + pad - 6 if y0 - 60 > 46 else y1 + 6 - pad
    paste(frame, img, (x, y), alpha)


def shot_frames(film, shot, run_info):
    clip = edit.load_clip(shot["clip"], "", 1.0, False)
    length = shot["b"] - shot["a"]
    n_out = round(length / shot["speed"] * FPS)
    decoder = subprocess.Popen(
        [FFMPEG, "-v", "error", "-ss", f"{shot['a']:.3f}", "-t", f"{length:.3f}", "-i", str(CLIPS / f"{shot['clip']}.mkv"),
         "-vf", f"setpts=(PTS-STARTPTS)/{shot['speed']},fps={FPS}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        stdout=subprocess.PIPE)
    size = W * H * 3
    first_frame = True
    for n in range(n_out):
        raw = decoder.stdout.read(size)
        if len(raw) < size:
            break
        t = n / FPS                                  # seconds into the shot
        src = shot["a"] + t * shot["speed"]          # seconds in the raw clip
        frame = Image.frombuffer("RGB", (W, H), raw)
        cx, cy, z = W / 2, H / 2, 1.0
        if "cam" in shot:
            tcx, tcy, tz, start, ramp = shot["cam"]
            k = ease((t - start) / ramp)
            cx, cy, z = W / 2 + (tcx - W / 2) * k, H / 2 + (tcy - H / 2) * k, 1.0 + (tz - 1.0) * k
        x0, y0, vw, vh = view_box(cx, cy, z)
        if z > 1.001:
            frame = frame.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + vw, y0 + vh))
        frame = frame.convert("RGBA")
        for co in shot.get("callouts", []):
            start, (bx, by, bw, bh), text = co[:3]
            until = co[3] if len(co) > 3 else 1e9
            alpha = min(ease((t - start) / 0.35), ease((until - t) / 0.35))
            if alpha > 0:
                rect = ((bx - x0) * z, (by - y0) * z, (bx + bw - x0) * z, (by + bh - y0) * z)
                callout(frame, rect, alpha)
                place_label(frame, rect, text, alpha)
        paste(frame, band(shot["act"]), (0, 0))
        text = shot.get("caption")
        elapsed = None
        if shot.get("run"):
            elapsed = min(max(0.0, src - run_info["raw_start"]), run_info["total"])
            text = [c for s, c in RUN_CAPTIONS if elapsed >= s][-1]
            if elapsed >= run_info["total"] - 0.01:
                text = f"Done: from new file to Word report in {run_info['minutes']}."
        if text:
            img, pad = caption(text)
            fade = ease(t / 0.3) if first_caption_fade(film, text) else 1.0
            paste(frame, img, ((W - img.width) / 2, H - 140 - pad + (1 - fade) * 8), fade)
        if shot["speed"] >= 1.5:
            img, pad = badge(shot["speed"], elapsed)
            paste(frame, img, (W - img.width + pad - 24, 56 - pad))
        if first_frame and film.last is not None:
            for k in range(1, XFADE + 1):
                film.write(film.dissolve_into(frame, k / (XFADE + 1)))
            first_frame = False
        film.write(frame)
    decoder.stdout.close()
    decoder.wait()


_shown = {}


def first_caption_fade(film, text):
    """Fade a caption in only the first time it appears (the run keeps the same caption across two shots)."""
    if text not in _shown:
        _shown[text] = film.frames
    return film.frames - _shown[text] < 10


def text_card(film, seconds, draw):
    for n in range(int(seconds * FPS)):
        img = draw(n / FPS)
        if n < XFADE and film.last is not None:
            img = film.dissolve_into(img, (n + 1) / (XFADE + 1))
        film.write(img)


def opening():
    bg = card_background()
    lines = ["A new specification arrives.",
             "Does it agree with all our approved documents?",
             "Checking by hand is slow, and it is easy to miss a conflict.",
             "So we build an AI agent that checks it for us."]
    f_kick, f_title, f_line = font(30, "Bold"), font(96, "ExtraBold"), font(44, "Medium")

    def draw(t):
        img = bg.copy()
        d = ImageDraw.Draw(img)
        a0 = ease(t / 0.8)
        d.text((160, 250), "EDK  ·  SYSTEMS ENGINEERING", font=f_kick, fill=(56, 189, 248, int(255 * a0)))
        d.text((152, 300), "Find inconsistencies in requirements", font=f_title, fill=WHITE + (int(255 * a0),))
        d.rectangle((160, 440, 160 + 240 * ease((t - 0.4) / 0.8), 446), fill=AMBER)
        for i, line in enumerate(lines):
            a = ease((t - 1.3 - i * 1.25) / 0.6)
            if a > 0:
                y = 520 + i * 78 + (1 - a) * 14
                color = AMBER if i == 3 else (226, 232, 240)
                d.text((160, y), line, font=f_line, fill=color + (int(255 * a),))
        d.text((160, 980), "Real screen recording  ·  Arrow 3 demo documents (fictitious)", font=font(22, "Regular"),
               fill=(148, 163, 184))
        return img
    return draw


def ending():
    summary = json.loads((VIDEO / "run_summary.json").read_text())
    bg = card_background()
    cover = Image.open(VIDEO / "report_cover.png").convert("RGBA")
    cover = cover.resize((520, int(cover.height * 520 / cover.width)), Image.LANCZOS)
    framed, pad = shadowed(cover, blur=24, offset=(0, 12), alpha=150)
    tiles = [("CRITICAL", summary["Critical"], (185, 28, 28)), ("MAJOR", summary["Major"], (234, 88, 12)),
             ("MINOR", summary["Minor"], (202, 138, 4))]
    facts = [f"{summary['minutes']} from new file to Word report",
             "2 AI agents working at the same time",
             "Built with no code: 16 blocks",
             "Every finding quotes both documents, so engineers can check it"]

    def draw(t):
        img = bg.copy()
        d = ImageDraw.Draw(img)
        a = ease(t / 0.6)
        d.text((140, 120), "THE RESULT", font=font(30, "Bold"), fill=(56, 189, 248, int(255 * a)))
        d.text((132, 170), f"We hid {summary['total']} conflicts in the new spec.", font=font(64, "ExtraBold"),
               fill=WHITE + (int(255 * a),))
        a2 = ease((t - 0.7) / 0.6)
        d.text((132, 252), f"The agent found all {summary['total']}.", font=font(64, "ExtraBold"),
               fill=AMBER + (int(255 * a2),))
        for i, (name, value, color) in enumerate(tiles):
            ai = ease((t - 1.3 - i * 0.2) / 0.5)
            if ai <= 0:
                continue
            x = 140 + i * 290
            d.rounded_rectangle((x, 370 + (1 - ai) * 16, x + 260, 560 + (1 - ai) * 16), 18, fill=color + (int(255 * ai),))
            d.text((x + 130, 450 + (1 - ai) * 16), str(value), font=font(92, "ExtraBold"), fill=WHITE + (int(255 * ai),),
                   anchor="mm")
            d.text((x + 130, 527 + (1 - ai) * 16), name, font=font(26, "Bold"), fill=WHITE + (int(255 * ai),), anchor="mm")
        for i, fact in enumerate(facts):
            af = ease((t - 2.2 - i * 0.35) / 0.5)
            if af <= 0:
                continue
            y = 630 + i * 64
            d.ellipse((142, y + 10, 160, y + 28), fill=AMBER + (int(255 * af),))
            d.text((182, y), fact, font=font(34, "Medium"), fill=WHITE + (int(255 * af),))
        ac = ease((t - 0.9) / 0.8)
        if ac > 0:
            paste(img, framed, (1250 - pad, 110 - pad + (1 - ac) * 20), ac)
        d.text((140, 1000), "EDK  ·  Find inconsistencies in requirements  ·  Arrow 3 demo documents (fictitious)",
               font=font(22, "Regular"), fill=(148, 163, 184))
        fade_out = ease((summary_seconds - t) / 0.8)
        if fade_out < 1:
            img.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * (1 - fade_out)))))
        return img
    return draw


summary_seconds = 8.0


def main():
    clip11 = edit.load_clip("11_run", "", 1.0, False)
    state = json.loads((VIDEO / "run_state_raw.json").read_text())
    run = [r for r in state["runs"] if r["kind"] == "workflow"][-1]
    summary = json.loads((VIDEO / "run_summary.json").read_text())
    run_info = {"raw_start": run["started_at"] + clip11.offset, "total": run["finished_at"] - run["started_at"],
                "minutes": summary["minutes"]}
    film = Film(TARGET)
    text_card(film, 7.6, opening())
    for i, shot in enumerate(SHOTS):
        start = film.frames
        shot_frames(film, shot, run_info)
        print(f"  shot {i + 1:2d}/{len(SHOTS)} {shot['clip']} {shot['a']:.1f}-{shot['b']:.1f}s ×{shot['speed']:g} "
              f"→ {(film.frames - start) / FPS:.1f}s", flush=True)
    text_card(film, summary_seconds, ending())
    film.close()
    print(f"→ {TARGET.relative_to(edit.ROOT)}  {film.frames / FPS:.1f}s", flush=True)


if __name__ == "__main__":
    main()
