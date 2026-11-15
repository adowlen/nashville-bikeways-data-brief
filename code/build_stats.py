import pandas as pd, numpy as np, json, re, os
BASE=os.path.expanduser("~/workspace/goals/daily-civic-data-brief/hidden_files/nashville-bikeways-brief-2026-11-15")
bw=pd.read_csv(f"{BASE}/data/nashville_bikeways_raw.csv")
bw['miles']=bw.Shape__Length/5280.0
TYPE_LABELS={'BL':'Bike Lane','BBL':'Buffered Bike Lane','SSR':'Signed Shared Route','WOL':'Wide Outside Lane','PBL':'Protected Bike Lane','PBBL':'Protected Buffered Bike Lane'}
stats={}
stats['dataset']="Nashville Bikeways (Bikeways_view, layer 0)"
stats['snapshot_date']="2026-11-15"; stats['rows']=int(len(bw)); stats['server_count']=510
stats['unit']="one row = one bikeway segment in the published Bikeways view"
stats['segments_with_length']=int(bw.Shape__Length.notna().sum()); stats['segments_blank_length']=int(bw.Shape__Length.isna().sum())
stats['total_miles_recorded']=round(float(bw.miles.sum()),2)
stats['distinct_streets_raw']=int(bw.OnStreetName.nunique())
# by type
types={}
for t,g in bw.groupby('BikewayType'):
    types[t]={'label':TYPE_LABELS.get(t,t),'segments':int(len(g)),'segment_share_pct':round(float(len(g)/len(bw)*100),2),'segments_with_length':int(g.Shape__Length.notna().sum()),'miles':round(float(g.miles.sum()),2),'mile_share_pct':round(float(g.miles.sum()/bw.miles.sum()*100),2)}
stats['by_type']=types
stats['protected_PBL']={'miles':types['PBL']['miles'],'mile_share_pct':types['PBL']['mile_share_pct'],'segments':types['PBL']['segments']}
nonprot=[t for t in types if t!='PBL']
stats['non_protected']={'types':nonprot,'miles':round(float(sum(types[t]['miles'] for t in nonprot)),2),'mile_share_pct':round(float(sum(types[t]['miles'] for t in nonprot)/bw.miles.sum()*100),2)}
stats['ssr_vs_pbl_miles_ratio']=round(float(types['SSR']['miles']/types['PBL']['miles']),2)
# status normalized
raw_status=bw.Status.value_counts(dropna=False).to_dict()
stats['status_raw']={str(k):int(v) for k,v in raw_status.items()}
stats['status_normalized']={'completed_status_segments':int(bw.Status.isin(['Complete','Completed']).sum()),'blank_status_segments':int(bw.Status.isna().sum())}
stats['status_normalized']['completed_share_of_510_pct']=round(float(bw.Status.isin(['Complete','Completed']).sum()/len(bw)*100),2)
# years / eras
dated=bw[bw.YearCompleted.notna()].copy()
stats['dated_segments']=int(len(dated)); stats['year_min']=int(dated.YearCompleted.min()); stats['year_max']=int(dated.YearCompleted.max())
bins=[2003,2009,2014,2019,2026]; labels=['2004-2009','2010-2014','2015-2019','2020-2026']
dated['era']=pd.cut(dated.YearCompleted,bins=bins,labels=labels)
era={}
for e,g in dated.groupby('era',observed=True):
    era[str(e)]={'segments':int(len(g)),'miles':round(float(g.miles.sum()),2)}
stats['by_era']=era
era_type={}
for (e,t),g in dated.groupby(['era','BikewayType'],observed=True):
    era_type.setdefault(str(e),{})[str(t)]={'segments':int(len(g)),'miles':round(float(g.miles.sum()),2)}
stats['by_era_type']=era_type
stats['pbl_by_era']={e:era_type.get(e,{}).get('PBL',{'segments':0})['segments'] for e in labels}
stats['pbl_completed_2020_2026_share_of_pbl_pct']=round(float(era_type.get('2020-2026',{}).get('PBL',{'segments':0})['segments']/types['PBL']['segments']*100),2)
# streets
agg=bw.groupby('OnStreetName').agg(segments=('OBJECTID','count'),miles=('miles','sum'),types=('BikewayType',lambda s: ",".join(sorted(set(s))))).reset_index()
agg['miles']=agg.miles.round(2)
stats['top_streets_by_miles']=[{k:(float(v) if isinstance(v,float) else int(v) if isinstance(v,(int,np.integer)) else str(v)) for k,v in r.items()} for r in agg.sort_values('miles',ascending=False).head(10).to_dict('records')]
# district mentions
mentions={}
for dlist in bw.District.dropna():
    for d in [x.strip() for x in str(dlist).split(',') if x.strip()]:
        mentions[d]=mentions.get(d,0)+1
stats['district_segments_multi']=int(bw.District.str.contains(',').sum()); stats['district_segments_single']=int((~bw.District.str.contains(',')).sum())
stats['district_mentions_top10']=dict(sorted(mentions.items(), key=lambda kv:-kv[1])[:10])
stats['district_mentions_distinct']=len(mentions)
stats['human_scale_derived']={'protected':'about 1 in 7 recorded bikeway miles is a protected bike lane (45.64 of 314.93 miles, derived)','ssr_vs_pbl':'about 3.1 miles of signed shared route for every 1 mile of protected bike lane (143.35 / 45.64, derived)'}
# ---- fusion with crash layer: street-name match, upper bound ----
tc=pd.read_parquet(os.path.expanduser("~/workspace/goals/daily-civic-data-brief/hidden_files/stack/nashville/layers/traffic_accidents_clean.parquet"))
known=tc[~tc.counts_unknown_flag].copy()
SUF={'AVE':'AV','AVENUE':'AV','STREET':'ST','PIKE':'PKE','BOULEVARD':'BLVD','HIGHWAY':'HWY','ROAD':'RD','DRIVE':'DR','LANE':'LN','CIRCLE':'CIR','COURT':'CT','PLACE':'PL'}
def norm(s):
    s=str(s).upper().strip(); s=re.sub(r'^\d+\s+','',s); s=re.sub(r'[^A-Z0-9 ]',' ',s); s=re.sub(r'\s+',' ',s).strip()
    return ' '.join(SUF.get(t,t) for t in s.split(' '))
bw_names=set(bw.OnStreetName.dropna().apply(norm))
def streets(addr):
    if pd.isna(addr): return []
    return [norm(p) for p in str(addr).upper().split('&')]
known['streets']=known.Street_Address.apply(streets)
known['on_bw_name']=known.streets.apply(lambda ss: any(s in bw_names for s in ss))
sub=known[known.Street_Address.notna()].copy()
sub['inj_or_fatal']=(sub.Number_of_Injuries.fillna(0)>0)|(sub.Number_of_Fatalities.fillna(0)>0)
ped=sub[sub.pedalcycle_involved_flag]
matched_names=set()
for ss in sub[sub.on_bw_name].streets: matched_names.update([s for s in ss if s in bw_names])
fus={'method':'street-name match only: a reported crash counts as name-matched when either side of its Street_Address, after house-number stripping and suffix normalization to the crash-address form, equals a normalized Bikeways OnStreetName. This is NOT a segment or proximity join: bikeway segments are specific stretches of those streets, so the name match is an upper bound on segment-level presence and is never printed as on-a-bikeway crashes.',
 'crash_layer_rows_known_counts':int(len(known)),'addr_present':int(len(sub)),'addr_missing':int(known.Street_Address.isna().sum()),
 'addr_present_share_pct':round(float(len(sub)/len(known)*100),2),
 'all_crashes_name_matched':int(sub.on_bw_name.sum()),'all_crashes_name_matched_share_pct':round(float(sub.on_bw_name.mean()*100),2),
 'pedalcycle_crashes_total_known':int(known.pedalcycle_involved_flag.sum()),'pedalcycle_addr_present':int(len(ped)),
 'pedalcycle_name_matched':int(ped.on_bw_name.sum()),'pedalcycle_name_matched_share_pct':round(float(ped.on_bw_name.mean()*100),2),
 'pedalcycle_injuries_total':int(ped.Number_of_Injuries.sum()),'pedalcycle_fatalities_total':int(ped.Number_of_Fatalities.sum()),
 'pedalcycle_injury_or_fatal_crashes':int(ped.inj_or_fatal.sum()),'pedalcycle_injury_or_fatal_name_matched':int(ped[ped.on_bw_name].inj_or_fatal.sum()),
 'injury_or_fatal_rate_name_matched_pct':round(float(sub[sub.on_bw_name].inj_or_fatal.mean()*100),2),'injury_or_fatal_rate_not_matched_pct':round(float(sub[~sub.on_bw_name].inj_or_fatal.mean()*100),2),
 'pedalcycle_share_of_crashes_name_matched_pct':round(float(sub[sub.on_bw_name].pedalcycle_involved_flag.mean()*100),3),'pedalcycle_share_of_crashes_not_matched_pct':round(float(sub[~sub.on_bw_name].pedalcycle_involved_flag.mean()*100),3),
 'bw_street_names_normalized':int(len(bw_names)),'bw_street_names_matched':int(len(matched_names)),'bw_street_names_unmatched':sorted(list(bw_names-matched_names)),
 'crash_window':'2019-01-01 to 2026-10-31 as published in the 2026-11-02 Nashville Traffic Accidents brief (cleaned warehouse layer)'}
stats['fusion_crash_layer']=fus
# ---- HIN street overlap (name level only) ----
hin=pd.read_csv(os.path.expanduser("~/workspace/goals/daily-civic-data-brief/hidden_files/nashville-hin-brief-2026-11-14/data/nashville_hin_raw.csv"))
hin_names=set(hin.full_name.dropna().apply(norm))
bw2=bw.copy(); bw2['name_norm']=bw2.OnStreetName.apply(norm); bw2['on_hin_name']=bw2.name_norm.isin(hin_names)
stats['hin_street_overlap']={'method':'street-name overlap only between Bikeways OnStreetName and HIN full_name, both normalized the same way; a bikeway segment on a street that also carries HIN segments - not a segment-level overlap.','hin_street_names_normalized':int(len(hin_names)),'bw_segments_on_hin_named_streets':int(bw2.on_hin_name.sum()),'bw_miles_on_hin_named_streets':round(float(bw2[bw2.on_hin_name].miles.sum()),2),'bw_miles_on_hin_named_share_pct':round(float(bw2[bw2.on_hin_name].miles.sum()/bw.miles.sum()*100),2),'bw_distinct_streets_on_hin':int(bw2[bw2.on_hin_name].name_norm.nunique())}
json.dump(stats, open(f"{BASE}/stats.json","w"), indent=2)
agg.sort_values('miles',ascending=False).to_csv(f"{BASE}/data/street_panel.csv", index=False)
pd.DataFrame([{'type':k,'label':v['label'],**{kk:vv for kk,vv in v.items() if kk!='label'}} for k,v in types.items()]).to_csv(f"{BASE}/data/type_panel.csv", index=False)
pd.DataFrame([{'era':k, **v} for k,v in era.items()]).to_csv(f"{BASE}/data/era_panel.csv", index=False)
pd.DataFrame([{'district':k,'segment_mentions':v} for k,v in sorted(mentions.items(), key=lambda kv:-kv[1])]).to_csv(f"{BASE}/data/district_mentions_panel.csv", index=False)
print(json.dumps(stats,indent=2))
