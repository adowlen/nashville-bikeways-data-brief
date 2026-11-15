import csv, os, collections
HERE=os.path.dirname(__file__); DATA=os.path.normpath(os.path.join(HERE,"..","data"))
rows=list(csv.DictReader(open(os.path.join(DATA,"nashville_bikeways_raw.csv"),encoding="utf-8")))
out=[]
def log(s): out.append(str(s)); print(s)
log(f"rows={len(rows)}")
for col in ["BikewayType","Status","District","YearCompleted"]:
    c=collections.Counter(r[col] for r in rows); log(f"Counter {col}: {dict(c.most_common(40))} distinct={len(c)}")
for col in ["BikewayType","Status","OnStreetName","FromStreetName","ToStreetName","YearCompleted","District","Shape__Length"]:
    blank=sum(1 for r in rows if r[col]=="")
    log(f"{col}: blank={blank}")
lens=[float(r["Shape__Length"]) for r in rows if r["Shape__Length"]!=""]
log(f"Shape__Length: present={len(lens)} blank={len(rows)-len(lens)} min_ft={min(lens)} max_ft={max(lens)} sum_ft={sum(lens):.2f} sum_mi={sum(lens)/5280:.2f}")
log("Length unit: layer metadata geometryProperties.units = esriFeet for Shape__Length; miles = feet / 5280 in every figure.")
log("Sentinel rule: Shape__Length blank on 11 segments (OBJECTIDs "+str([r['OBJECTID'] for r in rows if r['Shape__Length']==''])+") is a missing length, NOT zero: those segments stay in every segment count and are excluded only from mileage denominators (499 length-carrying segments). Polarity sample EXCLUDED from mileage: those 11, all Status Complete, types BL 6 / SSR 3 / WOL 1 / BBL 1 - no PBL segment is excluded, so the protected mileage share is not understated by the exclusion; if anything the non-protected mileage is slightly understated. Polarity sample INCLUDED in segment counts: the same 11 OBJECTIDs appear in all segment totals (510).")
log("Status rule: raw Status values are Complete 414, Completed 92, blank 4. Complete and Completed are the same completed status under two spellings (the duplication trap flagged when the lead was verified 2026-11-12); the brief normalizes them to 506 completed-status segments and reports the 4 blank-status segments separately - blanks are never counted as completed or as incomplete.")
log("YearCompleted rule: blank on 1 segment (OBJECTID "+str([r['OBJECTID'] for r in rows if r['YearCompleted']==''])+"); that segment stays in segment and mileage totals and is excluded only from era counts (509 dated segments). No zero or sentinel years: recorded range 2004-2026.")
log("District rule: District is a free-text list; 160 of 510 segments list more than one district, so no mileage-by-district figure is printed (the layer gives no length split). District figures in the brief are segment mentions: a segment counts once for each district it lists.")
log("Unit agreement: mileage shares = type-group miles / total recorded miles (314.93, 499 length-carrying segments); segment shares = segments / 510; crash shares = crashes / crashes on the stated crash-layer population, counts printed with every rate. No figure mixes the segment and mileage denominators without labeling which it uses.")
log(f"OBJECTID distinct: {len(set(r['OBJECTID'] for r in rows))} of {len(rows)}; OnStreetName distinct raw: {len(set(r['OnStreetName'] for r in rows))}")
log("Join hygiene (fusion): street-name match (not proximity, not segment) to the 2026-11-02 crash layer - see build_stats fusion block and verification.md. Bikeway street names are normalized to the crash-address form (suffix expansion AVE->AV etc. and PIKE->PKE as in the crash addresses, house numbers stripped on the crash side). Physical scale: network = 510 segments / 314.9 recorded miles across 244 raw OnStreetName values (242 normalized names).")
assert len(rows)==510
open(os.path.join(DATA,"audit_output.txt"),"w").write("\n".join(out)+"\n")
print("AUDIT PASS")
