"""Clip 06: the Executive Word report step and its Output; Fit to show the whole pipeline; review two nodes."""
import _common  # noqa: F401
from canvas import drop_point, palette
from rec import clip, click, drag, hold, replace_text

with clip("06_report-step", "The deliverable: a Word report", "The deliverable: an executive Word report"):
    drag(*palette("Run command"), *drop_point(1120, -40), caption="Final step: build the Word report")
    INS = (70, 690, 290, 390)
    replace_text(210, 747, "Executive Word report", caption="Executive Word report", focus=INS)
    replace_text(210, 869, "python3 consistency_report.py {files} --index index/arrow3-baseline.md --source {trigger_file} -o {output}",
                 caption="The program's report kit turns the findings into a Word report", focus=INS)
    hold(2, "Checked live: ✓ Command OK", focus=INS)
    replace_text(210, 1019, "reports/{trigger_name}_Consistency_Report.docx", caption="One report per incoming spec",
                 focus=INS)
    hold(1, "One report per incoming spec", focus=INS)
    drag(1482, 558, 1590, 560, caption="Runs after the analysis")
    drag(1387, 605, 1590, 575, caption="…on the findings")
    drag(*palette("Output"), *drop_point(1120, -300), caption="Publish the report")
    replace_text(217, 703, "Inconsistency report", caption="Publish the report", focus=(70, 640, 300, 100))
    drag(1611, 612, 1611, 355, caption="Publish the report")
    hold(1, "Every check passes: ready to save", focus=(1600, 125, 310, 45))
    click(1688, 1056, caption="Fit: the whole pipeline at a glance", settle=0.9, after=1, focus=(1580, 1030, 140, 50))
    click(1000, 1010, caption="Two Hermes · 16 nodes · one trigger", settle=0.4, after=3)
    click(1370, 545, caption="The analyst's brief, in plain English", settle=0.4, after=3, focus=(70, 640, 300, 330))
    click(1580, 520, caption="The report step", settle=0.4, after=2, focus=(70, 690, 290, 390))
