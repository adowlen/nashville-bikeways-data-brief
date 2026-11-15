# Reviewer notes - Nashville Bikeways, 2026-11-15

## Thesis (recorded before the analysis, 2026-11-15 morning run, before any build figure was computed)
Thesis: Most of Nashville's existing bikeway mileage is not protected - signed shared routes and standard bike lanes dominate the mileage and protected lanes are a small minority - so the network's total mileage overstates separated infrastructure; and bicycle-involved crashes in the published crash layer will name-match to bikeway streets as an upper bound only, because bikeway segments are specific stretches of those streets.

## Claims most likely to be challenged
- The headline (45.6 of 314.9 recorded miles are protected, 14.5%). Both inputs are the layer's own fields; the mileage population is the 499 length-carrying segments, printed wherever the figure is used. "Protected" is the layer's own PBL label and definition, not an audit of physical separation on the ground.
- The era pattern (no PBL segment dated before 2015; 53 of 72 dated 2020-2026). YearCompleted is one recorded year per segment in a current inventory; the brief's interpretation section carries the alternative reading (inventory labels at pull time, not a construction history, and conversions/removals are not recorded).
- The crash name-match (343 of 529 address-carrying pedalcycle crashes, 64.8%): printed only as a labeled upper bound, never as on-segment crashes; the all-crashes control (45.1% name-matched) is printed with it.
- The HIN overlap (50.5% of bikeway miles on streets that also carry HIN segments): a street-name comparison, labeled as such wherever it appears; it is not a segment-level overlap.

## Methods checks that could not be completed
- Exposure: neither layer carries a traffic-volume or bicycle-volume field, so no exposure rate can be computed; stated prominently in the brief.
- Segment-level join to the crash layer: impossible from published attributes (the bikeways pull is attributes-only and the crash layer carries addresses, not segment keys). Replaced with the labeled street-name upper bound; the limitation is a finding of the brief.
- Mileage by district: not printed - 160 of 510 segments list multiple districts and the layer gives no length split.
- Ground-truth of the PBL label: the brief reports the layer's recorded type; it does not field-verify physical protection.

## Findings that surprised us
- The layer shrank by one segment between the lead verification (511 on 2026-11-12) and this pull (510 on 2026-11-15); recorded in sources.md, no figure compares the pulls.
- Protected segments are not just a small share - they are entirely recent in the inventory's own dating: zero PBL segments carry a YearCompleted before 2015, and in 2020-2026 protected segments (53) outnumber every other type's new segments.
- Half the bikeway mileage (50.5%, name level) sits on streets that also carry High Injury Network segments - the same arterial set appears in both registers.
