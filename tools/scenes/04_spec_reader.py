"""Clip 04: a second Hermes, the Spec Reader, in its own (purple) lane: convert → search → briefing → Output."""
import _common  # noqa: F401
from canvas import S, drop_point, palette
from rec import clip, drag, hold, replace_text

with clip("04_spec-reader", "A second Hermes, in parallel", "Spec Reader: a second Hermes working in parallel"):
    drag(*palette("Hermes"), *drop_point(-300, 420), caption="A second Hermes: its own conversation, working in parallel")
    replace_text(217, 703, "Spec Reader", caption="Name it Spec Reader", focus=(70, 640, 300, 120))
    hold(1, "Each Hermes gets its own lane colour")
    drag(571, 557, *S(-200, 450), caption="The same Trigger wakes both Hermes")

    drag(*palette("Run command"), *drop_point(0, 420), caption="Spec Reader, step 1: a Run command")
    INS = (70, 690, 290, 390)
    replace_text(210, 747, "New spec to Markdown", caption="Convert the incoming spec to text", focus=INS)
    replace_text(210, 869, "pandoc {trigger_file} -t gfm --wrap=none -o {output}",
                 caption="pandoc: Word to Markdown, one requirement per line", focus=INS)
    hold(2, "EDK checks the command live: ✓ Command OK", focus=INS)
    replace_text(210, 1019, "{run_folder}/new-spec.md", caption="The result file is piped on", focus=INS)
    drag(547, 904, 700, 935, caption="Spec Reader runs it")

    drag(*palette("Search"), *drop_point(840, 190), caption="Search: grep every requirement line")
    INS = (70, 640, 300, 230)
    replace_text(217, 703, "Requirement lines", caption="Search: every requirement line of the new spec", focus=INS)
    replace_text(217, 764, "shall", caption="…every line with \"shall\"", focus=INS)
    hold(1, "…every line with \"shall\"", focus=INS)
    drag(717, 958, 1370, 745, caption="Pipe the Markdown into the Search")

    drag(*palette("Prompt"), *drop_point(280, 420), caption="Spec Reader, step 2: a Prompt in plain words")
    INS = (70, 640, 300, 270)
    replace_text(217, 703, "Spec briefing", caption="A one-page briefing for management", focus=INS)
    replace_text(217, 790, "{files} is the new document {trigger_name} as Markdown. Write a one-page briefing for management "
                 "in Markdown: what it specifies, one bullet per subsystem with its key values, and the documents and "
                 "standards it cites.", caption="Instructions in plain English", focus=INS)
    hold(1, "Instructions in plain English", focus=INS)
    drag(812, 918, 925, 935, caption="Order: after the conversion (solid arrow)")
    drag(717, 958, 905, 940, caption="Input: the converted spec (dashed arrow)")
    drag(*palette("Output"), *drop_point(560, 420), caption="Publish the briefing")
    replace_text(217, 703, "Spec briefing", caption="Publish the briefing", focus=(70, 640, 300, 100))
    drag(940, 958, 1150, 940, caption="Publish the briefing")
    hold(2, "Spec Reader lane: done")
