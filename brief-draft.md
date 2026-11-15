# Nashville's bikeway miles: 45.6 of the 314.9 recorded miles are protected bike lanes - 14.5 percent

**One-line summary:** Of the 510 segments in Nashville's Bikeways layer pulled on November 15, 2026, the 499 segments that carry a recorded length total 314.9 miles; protected bike lanes (PBL, the layer's own type label) account for 45.6 of those miles (14.5 percent, derived), and the largest single share is signed shared routes (SSR) at 143.4 miles (45.5 percent, derived).

Start with the scale. Machine Readable pulled the full layer from Metro's ArcGIS service on November 15, 2026; the pulled row count matches the server's own count exactly (510). One row is one bikeway segment. The layer's length field (Shape__Length) is recorded in feet in the layer metadata; every mileage in this brief is feet divided by 5,280. Eleven segments carry no recorded length: they are counted in every segment total and excluded from every mileage figure, so the mileage population is 499 segments. The layer carries no traffic-volume or bicycle-volume field, so no figure in this brief is an exposure rate, and no causal pattern is claimed from the crash comparison in the fusion section.

## The network by type

The layer records five bikeway types, using its own labels and definitions (BL = Bike Lane, BBL = Buffered Bike Lane, SSR = Signed Shared Route, WOL = Wide Outside Lane, PBL = Protected Bike Lane; a sixth defined type, PBBL, appears on no segment).

- Signed Shared Route (SSR): 194 segments, 143.4 miles - 45.5 percent of recorded miles (derived).
- Bike Lane (BL): 178 segments, 94.9 miles - 30.1 percent (derived).
- Protected Bike Lane (PBL): 72 segments, 45.6 miles - 14.5 percent (derived).
- Buffered Bike Lane (BBL): 52 segments, 22.3 miles - 7.1 percent (derived).
- Wide Outside Lane (WOL): 14 segments, 8.7 miles - 2.8 percent (derived).

The four types other than protected lanes total 269.3 miles, 85.5 percent of recorded miles (derived).

Human scale (derived): about 1 in 7 recorded bikeway miles is a protected bike lane, and there are about 3.1 miles of signed shared route for every 1 mile of protected bike lane (143.4 / 45.6).

Status: the layer's Status field records 414 segments as "Complete" and 92 as "Completed" - the same completed status under two spellings - for 506 of 510 segments (99.2 percent, derived). Four segments carry a blank status; they are reported as blank, not counted as either completed or incomplete.

## When the segments were completed

YearCompleted is recorded on 509 of the 510 segments (range 2004-2026; one segment is undated and is excluded from the era counts only).

- 2004-2009: 102 segments, 68.3 recorded miles. Signed shared routes are 70 of the 102 segments.
- 2010-2014: 146 segments, 109.3 miles. Signed shared routes are 70 of the 146.
- 2015-2019: 142 segments, 82.3 miles. The first protected bike lane segments appear in this era: 19 segments, 12.6 miles.
- 2020-2026: 119 segments, 54.8 miles. Protected bike lanes are 53 of the 119 segments and 33.1 of the miles.

No protected bike lane segment in the layer carries a completion year before 2015. Of the 72 protected segments, 53 (73.6 percent, derived) carry completion years in 2020-2026.

## Streets and districts

Aggregating each street's segments in the layer (the figures describe the street's bikeway segments, not the whole street):

- Old Hickory Blvd: 7 segments, 19.6 miles - the highest street total (types BL, PBL, SSR).
- Hwy 100: 5 segments, 12.2 miles.
- Charlotte Pike: 8 segments, 12.0 miles.
- Murfreesboro Pike: 6 segments, 9.6 miles.
- Dickerson Pike: 6 segments, 7.9 miles, all signed shared route.

The layer's District field is a list, not a single value: 160 of the 510 segments list more than one council district, and the layer gives no length split for those segments, so this brief prints no mileage by district. Counted as segment mentions (a segment counts once for each district it lists), District 19 has the most mentions (102), followed by District 06 (50), District 21 (48), District 24 (42), and District 18 (41), across 37 districts mentioned in total.

## What the published crash layer can and cannot add

The Nashville Traffic Accidents layer published on November 2, 2026 (222,902 reported crashes with counts populated, January 1, 2019 to October 31, 2026) carries a pedalcycle-involved flag. It records 530 pedalcycle-involved crashes; 529 of them carry a street address, recording 517 injuries and 8 fatalities in total.

The join between the two layers is a street-name match only: a crash name-matches when either side of its street address, after house-number stripping and suffix normalization, equals a bikeway street name. Bikeway segments are specific stretches of those streets, so a name match is an upper bound on segment-level presence. No figure below is a count of crashes on a bikeway segment, and the brief prints none.

- Of the 529 address-carrying pedalcycle-involved crashes, 343 (64.8 percent, derived) name-match to a street that carries at least one bikeway segment. Of the 490 pedalcycle-involved crashes that recorded an injury or a fatality, 320 name-match on the same basis.
- As the internal control, 100,306 of all 222,279 address-carrying reported crashes (45.1 percent, derived) name-match to a bikeway street. Bikeway streets are, in large part, the city's arterial streets, so a high name-match share is expected for any crash subset.
- Pedalcycle-involved crashes are 0.34 percent of name-matched crashes (343 of 100,306) and 0.15 percent of crashes that do not name-match (derived from the same populations). The crash layer carries no bicycle-volume field, so this comparison is not an exposure rate and is not printed as one.
- 224 of the layer's 242 normalized bikeway street names matched at least one reported crash. The 18 unmatched names include compound entries recorded in the layer itself (for example "16TH AV S MUSIC SQ E" and "JAMES ROBERTSON PKWY ROSA L PARKS BLVD").

## Overlap with the High Injury Network streets

The High Injury Network layer published on November 14, 2026 names 175 streets. Comparing street names only (the same normalization as the crash match; not a segment-level overlap): 214 of the 510 bikeway segments, carrying 159.2 of the 314.9 recorded miles (50.5 percent, derived), sit on 70 streets that also carry High Injury Network segments. The bikeway type mix on those streets is the layer's overall mix printed above; this brief does not split mileage by type within the overlap, because the overlap is a street-name comparison, not a segment join.

## What this might mean

One reading of the type mix is that the network's recorded mileage and its protected mileage describe different networks: 314.9 recorded miles in total, 45.6 of them recorded as protected lanes. The era counts are consistent with a change in what gets built - no protected segment is dated before 2015, and protected segments are the largest single type among segments dated 2020-2026 (53 of 119).

The strongest alternative explanation is that the layer is an inventory of what exists under its own labels at pull time, not a construction history: YearCompleted is a single recorded year per segment, the layer does not record conversions or removals, and a segment's current type may differ from the type it was completed as. On that reading the era pattern shows which types the current inventory dates to each period, not a complete record of what was built in each period. The crash name-match, on either reading, cannot show whether a crash occurred on a bikeway segment, and no bicycle-volume denominator exists in either layer to turn the crash counts into rates.

## Who can act

- **Nashville Department of Transportation and Multimodal Infrastructure (NDOT)**, which publishes this layer and designs Metro bikeways: the lever is the type assigned when a segment is built or rebuilt - recording a segment as a protected lane requires a design decision on that segment. Cost class: budget decision per corridor (design and construction funding; no cost figure is printed because the layer records none). Outcome measure: the protected-lane mileage and share in this same Bikeways layer on a later pull, using the same feet-to-miles conversion and the same 499-segment mileage basis stated in this brief.
- **Metro Council**, which appropriates capital funding, including under the Choose How You Move transportation program: the lever is which corridors are funded for construction or conversion. Cost class: major policy / capital program decision. Outcome measure: the same layer's protected mileage in funded corridors, and the pedalcycle-involved crash count in the Traffic Accidents layer for the same streets, read with the name-match limits printed in this brief.
- **NDOT as publisher of the layer itself**: two recording fixes are low-cost operational changes - record a length for the 11 segments that carry none, and record Status in one spelling (Complete / Completed) so the register reads without normalization. Outcome measure: blank-length and blank-status counts in this layer on a later pull.

## Methods

- Snapshot: Bikeways (Bikeways_view, ArcGIS FeatureServer layer 0), Metropolitan Government of Nashville and Davidson County, pulled November 15, 2026; server count 510, pulled rows 510. Service data last edit November 12, 2026 (recorded in the layer metadata at pull).
- Lengths: Shape__Length is in feet per the layer metadata (geometryProperties units: esriFeet); miles = feet / 5,280. Eleven segments with a blank length stay in segment counts and are excluded from mileage figures.
- Status normalization: "Complete" (414) and "Completed" (92) are counted together as completed status (506); the 4 blank-status segments are reported separately.
- Eras are groups of the recorded YearCompleted field (509 dated segments); the one undated segment is excluded from era counts only.
- District figures are segment mentions because 160 segments list multiple districts; no mileage by district is printed.
- Crash fusion: street-name match only, as described in its section; the crash layer is the cleaned warehouse layer behind the November 2, 2026 brief. Pedalcycle involvement is that layer's pedalcycle_involved_flag; injuries and fatalities are its recorded Number_of_Injuries and Number_of_Fatalities sums on the address-carrying pedalcycle population.
- Exposure: neither layer carries a traffic-volume or bicycle-volume field. No exposure rate is printed anywhere in this brief.
- Full audit, join-hygiene, and verification records: verification.md and sources.md in this package; every figure reproduces from data/nashville_bikeways_raw.csv except the fusion figures, which also use the warehouse crash layer named in sources.md.
