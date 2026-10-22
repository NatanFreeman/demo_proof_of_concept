"""Clip 05: join the lanes (Append), Read both into Hermes, and the analyst's brief: Find inconsistencies."""
import _common  # noqa: F401
from canvas import drop_point, palette
from rec import clip, drag, hold, replace_text

with clip("05_analysis", "The analysis", "Find every inconsistency"):
    drag(*palette("Append"), *drop_point(560, 190), caption="Append: join two collections into one")
    replace_text(217, 703, "Register + new requirements", caption="The register plus the new requirement lines",
                 focus=(70, 640, 300, 100))
    drag(940, 592, 1150, 735, caption="The baseline register…")
    drag(1387, 775, 1185, 740, caption="…plus the Spec Reader's requirement lines")
    hold(1, "Two lanes, one collection")

    drag(*palette("Read"), *drop_point(560, -40), caption="Main Hermes, step 2: Read")
    replace_text(217, 703, "Study register + new spec", caption="Read: Hermes studies both, completely", focus=(70, 640, 300, 100))
    drag(1035, 551, 1140, 560, caption="After the register…")
    drag(1163, 775, 1150, 575, caption="…read the joined collection")
    hold(1, "The main Hermes will wait for the Spec Reader's result automatically")

    drag(*palette("Prompt"), *drop_point(840, -40), caption="The heart of the agent: a Prompt")
    INS = (70, 640, 300, 300)
    replace_text(217, 703, "Find inconsistencies", caption="Find inconsistencies", focus=INS)
    replace_text(217, 790,
                 "You have just read {files}: the register of every Arrow 3 document uploaded so far and the requirement "
                 "lines of the new document {trigger_name}. Do not write or run code: reason yourself. Take the new "
                 "requirements one by one, find the register requirements on the same subject (parent ID or same quantity) "
                 "and compare them. Report every inconsistency: different values, limits or units, interface mismatches, "
                 "timeline overruns, environmental or reliability shortfalls, outdated document or standard revisions. "
                 "Write {output} as a JSON array only, one object per finding, with keys id, severity (Critical, Major or "
                 "Minor), category, title, new_req, new_text, baseline_req, baseline_doc, baseline_text, impact, recommendation.",
                 caption="The analyst's brief, in plain English", focus=INS)
    hold(2, "The analyst's brief, in plain English", focus=INS)
    drag(1259, 551, 1370, 560, caption="After the Read step")
    drag(1163, 592, 1360, 575, caption="…with the register and the new requirements as input")
    hold(2, "Analysis wired")
