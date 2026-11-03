# MAP: draws story/charts/account-overview.png from source/metrics_data.py (views by date, weekly median, followers per 1,000, reactions vs benchmark).
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, datetime as dt, statistics as st
import os, sys; sys.path.insert(0, os.path.dirname(__file__)); from metrics_data import D
G="#9aa3ad";H="#e0457b";B="#2f6fdf";T="#222"
d0=dt.date(2026,9,30)
fig,ax=plt.subplots(2,2,figsize=(10.8,12),facecolor="white")
# 1 views over time
a=ax[0,0]
for x in D:
    t=dt.datetime.fromisoformat(x[1]); c=H if x[3]>=4500 else G
    a.scatter(t,x[3],s=60,color=c,zorder=3)
    if x[3]>=4500: a.annotate(x[0],(t,x[3]),fontsize=7,xytext=(4,4),textcoords="offset points")
a.set_yscale("log"); a.set_ylabel("views (log scale)")
a.set_title("1. Every film by date posted (pink = 4,500+ views)",loc="left",fontsize=11,color=T)
a.tick_params(axis="x",rotation=45)
import matplotlib.dates as md; a.xaxis.set_major_formatter(md.DateFormatter("%d %b"))
# 2 weekly
a=ax[0,1]
wk=lambda x:(dt.date.fromisoformat(x[1][:10])-d0).days//7
lab=["30 Sep","7 Oct","14 Oct","21 Oct","28 Oct"]
med=[st.median(x[3] for x in D if wk(x)==w) for w in range(5)]
n=[sum(1 for x in D if wk(x)==w) for w in range(5)]
a.bar(lab,med,color=[G,G,G,G,H])
for i,(m,k) in enumerate(zip(med,n)): a.text(i,m+80,f"{m:,.0f}\n({k} films)",ha="center",fontsize=8)
a.set_title("2. Typical (middle) film each week",loc="left",fontsize=11,color=T)
a.set_ylabel("median views"); a.set_xlabel("week starting")
# 3 followers per 1000
a=ax[1,0]
e=[x for x in D if x[10] is not None and "promoted" not in x[0] and x[3]>=1000]
e=sorted(e,key=lambda x:1000*x[10]/x[3])
a.barh([x[0] for x in e],[1000*x[10]/x[3] for x in e],color=[H if x[0]=="TERFwarts" else G for x in e])
a.axvline(3,ls=":",color=B); a.text(3.1,0,"our target: 3",color=B,fontsize=8)
for i,x in enumerate(e): a.text(1000*x[10]/x[3]+.05,i,f"{1000*x[10]/x[3]:.1f}",va="center",fontsize=8)
a.set_title("3. New followers per 1,000 views (films over 1K)",loc="left",fontsize=11,color=T)
# 4 engagement vs benchmark
a=ax[1,1]
er=lambda s:100*sum(x[4]+x[5]+x[6]+x[7] for x in s)/sum(x[3] for x in s)
pat=[x for x in D if "Patriots" in x[0]]; rest=[x for x in D if "Patriots" not in x[0]]
names=["TikTok average\n(small accounts)","Our films,\nall together","Patriots\nseries"]
vals=[4.4,er(D),er(pat)]
a.bar(names,vals,color=[G,B,H])
for i,v in enumerate(vals): a.text(i,v+.2,f"{v:.1f}%",ha="center",fontsize=9)
a.set_ylabel("likes + comments + shares + saves, % of views")
a.set_title("4. How much people react",loc="left",fontsize=11,color=T)
for q in ax.flat:
    for s in("top","right"): q.spines[s].set_visible(False)
    q.tick_params(labelsize=8)
fig.suptitle("CranbriJoos: first five weeks (26 films, 92K views)",fontsize=14,x=0.04,ha="left",color=T)
fig.tight_layout(rect=(0,0,1,.96))
fig.savefig(os.path.join(os.path.dirname(__file__),"..","story","charts","account-overview.png"),dpi=100)
print(med, er(D), er(pat), st.median(x[3] for x in pat), st.median(x[3] for x in rest))
