import csv, json, os, collections
BASE=os.path.expanduser("~/workspace/goals/daily-civic-data-brief/hidden_files/nashville-bikeways-brief-2026-11-15")
rows=list(csv.DictReader(open(f"{BASE}/data/nashville_bikeways_raw.csv")))
stats=json.load(open(f"{BASE}/stats.json")); checks=[]
def chk(name, a, b): checks.append({"check":name,"expected":b,"got":a,"pass":a==b})
chk("rows", len(rows), stats['rows'])
chk("segments with length", sum(1 for r in rows if r['Shape__Length']!=""), stats['segments_with_length'])
chk("total miles rounded", round(sum(float(r['Shape__Length']) for r in rows if r['Shape__Length']!="")/5280,2), stats['total_miles_recorded'])
for t in ['SSR','BL','PBL','BBL','WOL']:
    g=[r for r in rows if r['BikewayType']==t]
    chk(f"{t} segments", len(g), stats['by_type'][t]['segments'])
    chk(f"{t} miles rounded", round(sum(float(r['Shape__Length']) for r in g if r['Shape__Length']!="")/5280,2), stats['by_type'][t]['miles'])
chk("status Complete", sum(1 for r in rows if r['Status']=='Complete'), 414)
chk("status Completed", sum(1 for r in rows if r['Status']=='Completed'), 92)
chk("status blank", sum(1 for r in rows if r['Status']==''), 4)
chk("completed normalized", sum(1 for r in rows if r['Status'] in ('Complete','Completed')), stats['status_normalized']['completed_status_segments'])
chk("dated segments", sum(1 for r in rows if r['YearCompleted']!=""), stats['dated_segments'])
chk("PBL dated 2020-2026", sum(1 for r in rows if r['BikewayType']=='PBL' and r['YearCompleted']!="" and 2020<=float(r['YearCompleted'])<=2026), 53)
chk("PBL dated before 2015", sum(1 for r in rows if r['BikewayType']=='PBL' and r['YearCompleted']!="" and float(r['YearCompleted'])<2015), 0)
chk("distinct streets raw", len(set(r['OnStreetName'] for r in rows)), stats['distinct_streets_raw'])
chk("multi-district segments", sum(1 for r in rows if ',' in r['District']), stats['district_segments_multi'])
agg={}
for r in rows:
    if r['Shape__Length']!="": agg[r['OnStreetName']]=agg.get(r['OnStreetName'],0)+float(r['Shape__Length'])/5280
chk("top street Old Hickory Blvd miles rounded", round(agg['Old Hickory Blvd'],2), 19.59)
res={"checks":len(checks),"passed":sum(1 for c in checks if c['pass']),"detail":checks}
json.dump(res, open(f"{BASE}/data/verify_independent_output.json","w"), indent=2)
print(res['passed'],"/",res['checks'],"passed"); assert res['passed']==res['checks']
