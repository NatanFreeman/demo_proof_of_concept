"""Clip 03: Files → Filter → Index (the baseline register) → Output, wired to the main Hermes."""
import _common  # noqa: F401
from canvas import drop_point, palette
from rec import clip, drag, hold, replace_text

INS = (70, 640, 300, 330)
with clip("03_baseline-register", "The baseline register", "Baseline register: everything uploaded so far"):
    drag(*palette("Files"), *drop_point(0, 190), caption="Files: every specification uploaded so far")
    replace_text(217, 703, "All uploaded specs", caption="Files: every specification uploaded so far", focus=INS)
    replace_text(217, 792, "*.docx", caption="Files: every specification uploaded so far", focus=INS)
    hold(1, "Files: every specification uploaded so far", focus=INS)

    drag(*palette("Filter"), *drop_point(280, 190), caption="Filter: keep only the baseline")
    replace_text(217, 703, "Baseline only", caption="Filter: keep only the baseline", focus=INS)
    replace_text(217, 824, "reports/*", caption="…not generated reports, not the new spec itself", focus=INS)
    hold(1, "…not generated reports, not the new spec itself", focus=INS)
    drag(717, 775, 930, 740, caption="Pipe the files into the Filter (dashed arrow)")

    drag(*palette("Index"), *drop_point(280, -40), caption="Index: the living baseline register")
    replace_text(217, 703, "Baseline register", caption="Index: the living baseline register", focus=INS)
    replace_text(217, 790, "the document number, revision and title, then every requirement row exactly as printed by: "
                 "pandoc FILE -t gfm --wrap=none | grep shall", caption="Each entry: every requirement of every document",
                 focus=INS)
    replace_text(217, 941, "index/arrow3-baseline.md", caption="Kept up to date: only new or changed documents are re-read",
                 focus=INS)
    hold(2, "Kept up to date: only new or changed documents are re-read", focus=INS)
    drag(786, 536, 930, 560, caption="Hermes' first step: update the register (solid arrow)")
    drag(940, 775, 925, 565, caption="Feed it the baseline documents")

    drag(*palette("Output"), *drop_point(280, -300), caption="Output: the register, ready to download")
    replace_text(217, 703, "Baseline register", caption="Output: the register, ready to download", focus=(70, 640, 300, 100))
    drag(940, 592, 945, 335, caption="Publish the register")
    hold(2, "Baseline register: done")
