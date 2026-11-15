# Nashville Bikeways - Machine Readable brief, 2026-11-15

Of the 510 segments in Nashville's Bikeways layer, the 499 segments that carry a recorded length total 314.9 miles; protected bike lanes account for 45.6 of those miles (14.5 percent, derived), and the largest single share is signed shared routes at 143.4 miles (45.5 percent, derived).

Full brief: brief-draft.md. Headline graphic: hero.png.

## Contents
- brief-draft.md - the brief
- stats.json - every headline figure with its population printed
- charts/ - miles by type, segments by era and type, top streets by bikeway miles, crash street-name match (upper bound, labeled on the chart)
- data/ - panels, the raw snapshot CSV, the pre-flight audit output, the pull log, the source layer metadata, and the independent verifier output
- code/ - pull_data.py, audit_section10.py, build_stats.py, verify_independent.py, charts.py, hero_composite.py
- verification.md - pre-flight audit, methods checklist, join hygiene, sync gate, story gate
- sources.md, reviewer-notes.md, social-drafts.md

## Reproduce
```
python3 code/pull_data.py
python3 code/audit_section10.py
python3 code/build_stats.py
python3 code/verify_independent.py
python3 code/charts.py
python3 code/hero_composite.py
```
Dependencies (matching the code's actual imports): Python 3 standard library for pull, audit, and verifier; pandas, numpy, and pyarrow for build_stats.py only (it reads the 2026-11-02 warehouse crash layer and the 2026-11-14 HIN snapshot for the fusion and overlap sections - those layers are not in this repo; every bikeway-network figure reproduces from data/nashville_bikeways_raw.csv alone); matplotlib and numpy for charts only; Pillow for the hero composite only.

## Source
Bikeways (Bikeways_view), Metropolitan Government of Nashville and Davidson County, ArcGIS FeatureServer layer 0 (services2.arcgis.com/HdTo6HJqh92wn4D8). Snapshot November 15, 2026; service data last edit November 12, 2026.

## License
Brief text and derived data products: CC BY 4.0 (see LICENSE). Underlying records are Metro Nashville government open data.

Part of Machine Readable: https://adowlen.github.io/machine-readable/
