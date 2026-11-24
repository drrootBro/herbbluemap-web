import json,urllib.request,urllib.parse,concurrent.futures as cf,string
seeds=["acupuncture","acupuncture near me","acupuncture new york","acupuncture nyc","acupuncture manhattan","acupuncture brooklyn","acupuncture flushing","acupuncture for","acupuncture benefits","acupuncture cost","does acupuncture","acupuncturist","acupuncturist near me","chinese medicine","chinese medicine near me","chinese medicine nyc","traditional chinese medicine","tcm","chinese herbal medicine","chinese herbs for","chinese herbalist","chinese herbalist nyc","herbal medicine","cupping","cupping therapy","moxibustion","gua sha","tcm doctor","chinese medicine doctor","acupuncture insurance","acupuncture school","acupuncture license new york","electroacupuncture","fertility acupuncture","acupuncture for back pain","acupuncture for anxiety","chinese herbs","herbal formula","jizhi syrup","shennong bencaojing"]
def sug(q):
    u="https://suggestqueries.google.com/complete/search?client=firefox&hl=en&gl=us&q="+urllib.parse.quote(q)
    try: return json.loads(urllib.request.urlopen(u,timeout=15).read().decode('utf-8','ignore'))[1]
    except Exception: return []
qs=list(seeds)+[s+" "+c for s in seeds[:12]+["chinese herbs for","acupuncture for","chinese medicine for"] for c in string.ascii_lowercase]
out={}
with cf.ThreadPoolExecutor(8) as ex:
    for q,r in zip(qs,ex.map(sug,qs)):
        for k in r: out.setdefault(k,q)
json.dump(out,open('suggest.json','w'),ensure_ascii=False,indent=0)
print(len(out))
