# Source audit: Nashville Bikeways brief (2026-11-15)

Every figure in brief-draft.md, traced to its derivation. Counts were produced by code/build_stats.py and are stored in stats.json; the independent recomputation is in data/verify_independent_output.json (23 of 23 checks passed); the pre-flight audit is in data/audit_output.txt and in verification.md.

## The datasets

1. Bikeways (primary dataset for all network figures)
- Name: Bikeways (Bikeways_view, layer 0), Metro Nashville open data, owner NashvilleOpenData
- Endpoint used: https://services2.arcgis.com/HdTo6HJqh92wn4D8/arcgis/rest/services/Bikeways_view/FeatureServer/0
- Pull: 2026-11-15, paginated query ordered by OBJECTID, 510 records; server count confirmed with returnCountOnly before download and equal to the local count. Service data last edit 2026-11-12 (layer metadata at pull; the count was 511 when the lead was verified live on 2026-11-12 and is 510 at this pull - one segment fewer, recorded here, no figure compares the two pulls).
- Saved copy: data/nashville_bikeways_raw.csv; layer metadata as served: data/source-metadata-layer.json; pull log: data/pull_log.json.
- Fields relied on: BikewayType ("Bikeway Type"; definitions in the layer description: BL Bike Lane, BBL Buffered Bike Lane, SSR Signed Shared Route, WOL Wide Outside Lane, PBL Protected Bike Lane, PBBL Protected Buffered Bike Lane - PBBL appears on no segment), Status, OnStreetName, FromStreetName, ToStreetName, YearCompleted, District, Shape__Length (feet, per the metadata's geometryProperties units: esriFeet).

2. Crash layer (fusion section only)
- Nashville Traffic Accidents (Traffic_Accidents_2, layer 0), as published in the Nashville Traffic Accidents brief (2026-11-02, adowlen/nashville-traffic-accidents-data-brief): 222,903 reported crashes, January 1, 2019 to October 31, 2026; the fusion uses the 222,902 rows with counts populated from that package's cleaned warehouse layer (stack/nashville/layers/traffic_accidents_clean.parquet).
- Measures used: pedalcycle involvement is the layer's pedalcycle_involved_flag; injuries and fatalities are Number_of_Injuries and Number_of_Fatalities.
- Join: street-name match only (method and limits in verification.md and in the brief's fusion section). No segment-level or proximity join is claimed.

3. High Injury Network layer (street-overlap section only)
- Vision Zero High Injury Network (Vision_Zero_High_Injury_Network_view, layer 0), as published in the Nashville High Injury Network brief (2026-11-14, adowlen/nashville-high-injury-network-data-brief): 297 segments, 175 named streets (full_name). The overlap in this brief is a street-name comparison only.

4. Program context (Who can act naming only; no figure derives from these)
- Choose How You Move, Metro Nashville's transportation improvement program (voter-approved November 2024), named as the capital-program context for the Metro Council lever; Metro Council meets Tuesday, November 17, 2026 (the regular meeting date in the pick record for this brief, leads_log.md CHOSEN BY ALEX 2026-11-14); the brief asserts no bikeway item on that meeting's agenda.

## Figure-by-figure audit

1. **510 segments, 244 raw street names, 499 length-carrying segments, 314.93 recorded miles (1,662,856.34 feet / 5,280)** - stats.json: rows, distinct_streets_raw, segments_with_length, segments_blank_length, total_miles_recorded.
2. **Types: SSR 194 segments / 143.35 mi / 45.52 percent of miles; BL 178 / 94.95 / 30.15; PBL 72 / 45.64 / 14.49; BBL 52 / 22.28 / 7.07; WOL 14 / 8.72 / 2.77** - stats.json: by_type; panel: data/type_panel.csv. The brief rounds miles to one decimal and shares to one decimal.
3. **Other-than-PBL total 269.30 miles, 85.51 percent (derived)** - stats.json: non_protected.
4. **Human scale: about 1 in 7 protected (45.64 / 314.93); 3.14 miles of SSR per PBL mile (143.35 / 45.64)** - stats.json: human_scale_derived, ssr_vs_pbl_miles_ratio.
5. **Status: Complete 414, Completed 92, blank 4; normalized completed-status 506 of 510 = 99.22 percent** - stats.json: status_raw, status_normalized; audit Counter.
6. **Eras (509 dated segments): 2004-2009: 102 segments / 68.30 mi; 2010-2014: 146 / 109.32; 2015-2019: 142 / 82.27; 2020-2026: 119 / 54.78. PBL by era: 0 / 0 / 19 (12.56 mi) / 53 (33.08 mi); PBL dated 2020-2026 = 53 of 72 = 73.61 percent. SSR by era: 70 / 70 / 32 / 22 segments** - stats.json: by_era, by_era_type, pbl_by_era, pbl_completed_2020_2026_share_of_pbl_pct; panel: data/era_panel.csv.
7. **Streets: Old Hickory Blvd 7 segments / 19.59 mi; Hwy 100 5 / 12.17; Charlotte Pike 8 / 12.01; Murfreesboro Pike 6 / 9.58; Dickerson Pike 6 / 7.94, all SSR** - stats.json: top_streets_by_miles; panel: data/street_panel.csv.
8. **Districts: 160 multi-district segments, 350 single; 37 districts mentioned; mentions - 19: 102, 06: 50, 21: 48, 24: 42, 18: 41** - stats.json: district_segments_multi, district_segments_single, district_mentions_distinct, district_mentions_top10; panel: data/district_mentions_panel.csv. No mileage by district is printed anywhere.
9. **Fusion: crash layer known-count rows 222,902; address-present 222,279 (99.72 percent), missing 623; all-crashes name-matched 100,306 (45.13 percent); pedalcycle crashes 530 known-count, 529 address-present, 343 name-matched (64.84 percent); pedalcycle injuries 517 and fatalities 8 on the address-present pedalcycle population; pedalcycle injury-or-fatal crashes 490, of which 320 name-matched; pedalcycle share of name-matched crashes 0.342 percent (343 / 100,306) and of not-matched crashes 0.152 percent (186 / 121,973); injury-or-fatal rate 32.65 percent name-matched vs 29.14 percent not matched (control, printed in verification.md, not as a brief finding); bikeway names normalized 242, matched 224, unmatched 18 (listed in stats.json)** - stats.json: fusion_crash_layer.
10. **HIN street overlap: 214 bikeway segments / 159.15 miles (50.53 percent) on 70 streets that also carry HIN segments; HIN names normalized 175** - stats.json: hin_street_overlap.
11. **Hero figure: 45.6 of 314.9 (14.5 percent)** - Item 2's PBL figures, composited from stats.json by code/hero_composite.py; hero-headline.txt carries the same text.
