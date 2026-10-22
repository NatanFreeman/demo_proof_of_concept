"""Clip 13: a guided scroll through the generated report (stops planned from a dry pass: 60 px per wheel notch)."""
import time

import _common  # noqa: F401
from rec import clip, glide, hold, shot, xdo


def scroll_to(notches, caption, pace=0.075):
    shot(caption)
    for _ in range(notches):
        xdo("click", 5)
        time.sleep(pace)
    time.sleep(0.35)


with clip("13_report-tour", "Inside the report", "Inside the report"):
    glide(1500, 640, caption="The verdict: not ready for baseline")
    hold(2, "The verdict: not ready for baseline")
    scroll_to(8, "The blocking findings, on page 1")
    hold(3, "The blocking findings, on page 1")
    scroll_to(16, "Executive summary: severity and where the conflicts are")
    hold(4, "Executive summary: severity and where the conflicts are")
    scroll_to(8, "Conflict heat map: category × baseline document")
    hold(3, "Conflict heat map: category × baseline document")
    scroll_to(8, "Every finding at a glance")
    hold(3, "Every finding at a glance")
    scroll_to(8, "Each finding quoted side by side: new spec vs. baseline")
    hold(5, "Each finding quoted side by side: new spec vs. baseline")
    scroll_to(48, "With its impact and a recommended fix", pace=0.09)
    hold(1, "With its impact and a recommended fix")
    scroll_to(8, "An action plan with owners and due dates")
    hold(4, "An action plan with owners and due dates")
    scroll_to(8, "Appendix: the baseline documents that were checked")
    hold(3, "Appendix: the baseline documents that were checked")
    scroll_to(6, "Automated findings, confirmed by engineers")
    hold(3, "Automated findings, confirmed by engineers")
