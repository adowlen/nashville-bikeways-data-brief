import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt, pandas as pd, json, os
BASE=os.path.expanduser("~/workspace/goals/daily-civic-data-brief/hidden_files/nashville-bikeways-brief-2026-11-15")
stats=json.load(open(f"{BASE}/stats.json"))
CHAR="#232323"; AMBER="#E8A33D"; TEAL="#2A9D8F"; GREY="#8A8A8A"
plt.rcParams.update({"font.size":10,"axes.edgecolor":GREY,"text.color":CHAR,"axes.labelcolor":CHAR,"xtick.color":CHAR,"ytick.color":CHAR})
def save(fig,name): fig.tight_layout(); fig.savefig(f"{BASE}/charts/{name}",dpi=200); plt.close(fig); print(name)
order=['SSR','BL','PBL','BBL','WOL']
labels={'SSR':'Signed Shared\nRoute (SSR)','BL':'Bike Lane\n(BL)','PBL':'Protected Bike\nLane (PBL)','BBL':'Buffered Bike\nLane (BBL)','WOL':'Wide Outside\nLane (WOL)'}
miles=[stats['by_type'][t]['miles'] for t in order]; shares=[stats['by_type'][t]['mile_share_pct'] for t in order]; segs=[stats['by_type'][t]['segments'] for t in order]
fig,ax=plt.subplots(figsize=(6.6,3.9))
bars=ax.bar([labels[t] for t in order],miles,color=[GREY,TEAL,AMBER,GREY,CHAR])
for b,v,s,n in zip(bars,miles,shares,segs): ax.text(b.get_x()+b.get_width()/2,v+4,f"{v:.1f} mi\n{s:.1f}% ({n} segs)",ha='center',fontsize=8.5)
ax.set_ylabel("Recorded miles (Shape__Length, feet / 5280)")
ax.set_title("Bikeway miles by type - Nashville Bikeways layer, 510 segments\n499 length-carrying segments, 314.9 recorded miles total",fontsize=11)
ax.set_ylim(0,165); save(fig,"chart_miles_by_type.png")
# era: PBL vs SSR segments by era
eras=['2004-2009','2010-2014','2015-2019','2020-2026']
pbl=[stats['by_era_type'].get(e,{}).get('PBL',{'segments':0})['segments'] for e in eras]
ssr=[stats['by_era_type'].get(e,{}).get('SSR',{'segments':0})['segments'] for e in eras]
bl=[stats['by_era_type'].get(e,{}).get('BL',{'segments':0})['segments'] for e in eras]
import numpy as np
x=np.arange(4); w=0.27
fig,ax=plt.subplots(figsize=(6.6,3.9))
ax.bar(x-w,ssr,w,color=GREY,label="Signed Shared Route"); ax.bar(x,bl,w,color=TEAL,label="Bike Lane"); ax.bar(x+w,pbl,w,color=AMBER,label="Protected Bike Lane")
for xi,vals in zip(x,zip(ssr,bl,pbl)):
    for off,v in zip([-w,0,w],vals): ax.text(xi+off,v+1.5,str(v),ha='center',fontsize=8.5)
ax.set_xticks(x); ax.set_xticklabels(eras); ax.legend(fontsize=8); ax.set_ylabel("Segments by YearCompleted (509 dated segments)")
ax.set_title("Segments completed by era and type - Bikeways layer\nProtected lanes: 0 before 2015, 53 of 72 in 2020-2026",fontsize=11); ax.set_ylim(0,80); save(fig,"chart_era_by_type.png")
# top streets by miles
top=pd.DataFrame(stats['top_streets_by_miles']).head(8).iloc[::-1]
fig,ax=plt.subplots(figsize=(6.8,4.2))
bars=ax.barh(top.OnStreetName,top.miles,color=TEAL)
for b,v,n in zip(bars,top.miles,top.segments): ax.text(v+0.4,b.get_y()+b.get_height()/2,f"{v:.1f} mi ({n} segs)",va='center',fontsize=9)
ax.set_xlabel("Recorded bikeway miles on the street (all its segments in the layer)")
ax.set_title("Streets carrying the most bikeway miles - Bikeways layer",fontsize=11); ax.set_xlim(0,25); save(fig,"chart_top_streets_miles.png")
# fusion chart
fus=stats['fusion_crash_layer']
fig,ax=plt.subplots(figsize=(6.6,3.9))
cats=['All reported\ncrashes','Pedalcycle-involved\ncrashes']
vals=[fus['all_crashes_name_matched_share_pct'],fus['pedalcycle_name_matched_share_pct']]
ns=[fus['all_crashes_name_matched'],fus['pedalcycle_name_matched']]; tots=[fus['addr_present'],fus['pedalcycle_addr_present']]
bars=ax.bar(cats,vals,color=[GREY,AMBER])
for b,v,n,t in zip(bars,vals,ns,tots): ax.text(b.get_x()+b.get_width()/2,v+2,f"{v:.1f}%\n({n} of {t})",ha='center',fontsize=9)
ax.set_ylabel("Share name-matched to a bikeway street (%)")
ax.set_title("Crashes on streets that carry a bikeway segment (street-name match,\nupper bound - NOT on-segment) - crash layer 2019-2026, address-present crashes",fontsize=10.5)
ax.set_ylim(0,78); save(fig,"chart_crash_name_match.png")
