#!/usr/bin/env python3
"""Build static formula pages (/formulas/<slug>/) from the free Shang Han Lun tool data.

Source of truth: the `const F = {...}` object in shang-han-lun/tool/index.html
(free edition: Taiyang + Yangming only — never add paid-edition formulas here)
plus EXTRA below for formulas people search for that the tool does not hold.

Run:  python3 tools/build_formulas.py   (needs node on PATH to read the JS object)
It rewrites formulas/**, the herb-page formula links, and sitemap.xml.
"""
import html, json, os, re, subprocess, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://herbbluemap.com"
TODAY = datetime.date.today().isoformat()

# Chinese names for the tool formulas (key = pinyin part of the tool name)
ZH = {
 "Gui Zhi Tang":"桂枝汤","Gui Zhi Jia Ge Gen Tang":"桂枝加葛根汤","Ma Huang Tang":"麻黄汤",
 "Ge Gen Tang":"葛根汤","Da Qing Long Tang":"大青龙汤","Xiao Qing Long Tang":"小青龙汤",
 "Ma Xing Gan Shi Tang":"麻杏甘石汤","Gui Zhi Jia Hou Po Xing Zi Tang":"桂枝加厚朴杏子汤",
 "Wu Ling San":"五苓散","Mai Men Dong Tang":"麦门冬汤","Jie Geng Tang":"桔梗汤",
 "Zhu Ye Shi Gao Tang":"竹叶石膏汤","Zhi Gan Cao Tang":"炙甘草汤","Ling Gui Zhu Gan Tang":"苓桂术甘汤",
 "Gui Zhi Jia Fu Zi Tang":"桂枝加附子汤","Tao He Cheng Qi Tang":"桃核承气汤",
 "Gui Zhi Ma Huang Ge Ban Tang":"桂枝麻黄各半汤","Gui Zhi Er Ma Huang Yi Tang":"桂枝二麻黄一汤",
 "Gui Zhi Er Yue Bi Yi Tang":"桂枝二越婢一汤","Ge Gen Huang Qin Huang Lian Tang":"葛根黄芩黄连汤",
 "Gui Zhi Gan Cao Tang":"桂枝甘草汤","Ling Gan Jiang Wei Xin Xia Ren Tang":"苓甘五味姜辛夏仁汤",
 "Qian Jin Wei Jing Tang":"千金苇茎汤","Ma Huang Lian Qiao Chi Xiao Dou Tang":"麻黄连翘赤小豆汤",
 "Bai Hu Tang":"白虎汤","Bai Hu Jia Ren Shen Tang":"白虎加人参汤","Tiao Wei Cheng Qi Tang":"调胃承气汤",
 "Xiao Cheng Qi Tang":"小承气汤","Da Cheng Qi Tang":"大承气汤","Yin Chen Hao Tang":"茵陈蒿汤",
 "Zhu Ling Tang":"猪苓汤","Ma Zi Ren Wan":"麻子仁丸",
}
# House modifications in the tool, not classical formulas -> no standalone page
SKIP = {"Gui Zhi Tang Jia Xin Yi", "Ma Xing Gan Shi Tang Jia Xin Yi"}

# Formulas searched for but not in the free tool. Classical facts only.
EXTRA = {
 "Ze Xie Tang (Alisma Decoction)": {
  "zh":"泽泻汤","meridian":"Taiyin (water-rheum)","pulse":"wiry or submerged pulse",
  "modern":"Vertigo and dizziness from fluid retention, Ménière's disease, positional vertigo with heavy head",
  "pattern":"Propping rheum below the heart; turbid fluid blocks clear yang from rising to the head",
  "source":"Jin Gui Yao Lue, Phlegm-Rheum chapter",
  "original":"When there is propping rheum below the heart and the person suffers from veiling dizziness: Ze Xie Tang governs it. [心下有支饮，其人苦冒眩，泽泻汤主之。]",
  "herbs":[{"n":"Ze Xie (alisma rhizome)","a":"15g","p":"classical ratio 5 liang"},{"n":"Bai Zhu (white atractylodes rhizome)","a":"6g","p":"classical ratio 2 liang"}],
  "prep":"Decoct the two herbs in about 2 cups of water down to 1 cup; take warm, split into two doses. The 5:2 ratio of Ze Xie to Bai Zhu is the point of the formula.",
  "contra":"Not for dizziness from blood or yin deficiency without fluid retention. Dizziness can signal stroke, heart or inner-ear disease — get it assessed first.",
  "note":"Two herbs, one job: Ze Xie drains the water that is clouding the head, Bai Zhu strengthens the spleen so the water stops collecting. It is one of the shortest formulas in the classics and a favorite teaching example of how ratio, not herb count, makes a formula.",
 },
 "Huang Long Tang (Yellow Dragon Decoction)": {
  "zh":"黄龙汤","meridian":"Yangming (Yang Brightness)","pulse":"deficient, or submerged and forceless pulse",
  "modern":"Constipation or foul watery 'overflow' diarrhea in weak, elderly or exhausted patients; bowel obstruction with collapse of strength",
  "pattern":"Yangming bowel repletion (heat binding) with qi and blood deficiency — purge and support at the same time",
  "source":"Shang Han Liu Shu (Tao Hua, Ming dynasty), building on Da Cheng Qi Tang",
  "original":"Built on Da Cheng Qi Tang (Shang Han Lun line 209) with Ren Shen and Dang Gui added, for heat binding in the bowels when the patient is too weak to bear a purge alone. [热结旁流，或大便秘结，腹痛拒按，身热口渴，神疲少气，宜黄龙汤。]",
  "herbs":[{"n":"Da Huang (rhubarb rhizome)","a":"9g","p":"added late"},{"n":"Mang Xiao (mirabilite / sodium sulfate)","a":"9g","p":"dissolved into strained decoction"},
           {"n":"Zhi Shi (immature bitter orange)","a":"9g"},{"n":"Hou Po (magnolia bark)","a":"9g"},
           {"n":"Ren Shen (ginseng)","a":"6g"},{"n":"Dang Gui (Chinese angelica root)","a":"9g"},
           {"n":"Gan Cao (raw licorice root)","a":"3g"},{"n":"Jie Geng (platycodon root)","a":"3g"},
           {"n":"Sheng Jiang (fresh ginger)","a":"3 slices"},{"n":"Da Zao (jujube)","a":"2 pieces"}],
  "prep":"Decoct Zhi Shi, Hou Po, Ren Shen, Dang Gui, Gan Cao, Jie Geng, Sheng Jiang and Da Zao; add Da Huang near the end; strain and dissolve Mang Xiao. Stop once the bowels move.",
  "contra":"A strong purgative: not in pregnancy, not without real bowel repletion. Severe abdominal pain, vomiting or no bowel movement with distension can be a surgical emergency — go to a hospital first.",
  "note":"The name says it: a 'dragon' of purging herbs (the Da Cheng Qi Tang core) carried by ginseng and angelica, so that a patient too weak for a plain purge can still have the blockage cleared. It is the classic answer to the dilemma 'he needs a purge, but he cannot survive one.'",
 },
}

# pinyin (no spaces, lowercase) -> bencao page
HERB_PAGE = {p: p for p in ["baizhu","banxia","chaihu","chuanxiong","dahuang","danggui","dazao","ejiao","fuling","fuzi",
 "gancao","gegen","guizhi","houpo","huanglian","huangqi","huangqin","mahuang","mangxiao","renshen","shaoyao",
 "shengjiang","shigao","wuweizi","xingren","xixin","zexie","zhigancao","zhimu","zhishi","zhizi","zhuling"]}
HERB_PAGE.update({"baishao":"shaoyao","paofuzi":"fuzi"})


def esc(s): return html.escape(s, quote=True)
def slugify(p): return re.sub(r"[^a-z0-9]+", "-", p.lower()).strip("-")
def herb_key(n): return re.sub(r"[^a-z]", "", n.split("(")[0].lower())


def load_tool():
    js = (r"const fs=require('fs');const s=fs.readFileSync(process.argv[1],'utf8');"
          r"const a=s.indexOf('const F = {');const b=s.indexOf('\n};',a);"
          r"process.stdout.write(JSON.stringify(eval('('+s.slice(a+10,b+2)+')')));")
    out = subprocess.check_output(["node", "-e", js, os.path.join(ROOT, "shang-han-lun/tool/index.html")])
    return json.loads(out)


def collect():
    items = []
    for name, f in load_tool().items():
        py = name.split(" (")[0]
        if py in SKIP: continue
        items.append(dict(f, name=name, py=py, en=name[len(py)+2:-1], zh=ZH[py], in_tool=True))
    for name, f in EXTRA.items():
        py = name.split(" (")[0]
        items.append(dict(f, name=name, py=py, en=name[len(py)+2:-1], in_tool=False))
    for it in items:
        it["slug"] = slugify(it["py"])
        it["hkeys"] = {herb_key(h["n"]) for h in it["herbs"]}
    return items


def split_original(o):
    m = re.search(r"\[([^\]]+)\]\s*$", o)
    return (o[:m.start()].strip(), m.group(1)) if m else (o, "")


def herb_li(h):
    k = herb_key(h["n"]); page = HERB_PAGE.get(k)
    label = esc(h["n"])
    if page: label = f'<a href="/bencao/{page}.html">{label}</a>'
    extra = esc(h["a"]) + (f' · {esc(h["p"])}' if h.get("p") else "")
    return f"<li>{label} — {extra}</li>"


def related(it, items):
    scored = []
    for o in items:
        if o is it: continue
        n = len(it["hkeys"] & o["hkeys"])
        if n >= 2: scored.append((-n, o["py"], o))
    return [o for _, _, o in sorted(scored)[:6]]


def page(it, items):
    py, zh, en = it["py"], it["zh"], it["en"]
    url = f"{SITE}/formulas/{it['slug']}/"
    title = f"{py} ({zh}): Ingredients, Uses & Original Text | HerbBlueMap"
    herb_names = ", ".join(h["n"].split(" (")[0] for h in it["herbs"])
    desc = (f"{py} ({zh}, {en}): {len(it['herbs'])} herbs — {herb_names}. "
            f"Used for {it['modern'][0].lower() + it['modern'][1:]}. Classical source, dosage, preparation and cautions in plain English.")
    if len(desc) > 300: desc = desc[:297].rsplit(" ", 1)[0] + "…"
    en_line, zh_line = split_original(it["original"])
    rel = related(it, items)
    faq = [
      (f"What is {py} used for?", f"In classical terms {py} treats {it['pattern'][0].lower()+it['pattern'][1:]}. Modern references apply it to {it['modern'][0].lower()+it['modern'][1:]}. It should be chosen by pattern, by a qualified practitioner — not by a disease name alone."),
      (f"What are the ingredients of {py}?", f"{py} ({zh}) contains {len(it['herbs'])} herbs: " + "; ".join(f"{h['n']} {h['a']}" for h in it["herbs"]) + "."),
      (f"Where does {py} come from?", f"{it['source']}."),
    ]
    ld = {"@context":"https://schema.org","@graph":[
      {"@type":"Article","headline":f"{py} ({zh}) — {en}","description":desc,"url":url,"inLanguage":"en",
       "dateModified":TODAY,"about":{"@type":"Thing","name":py,"alternateName":[zh,en]},
       "author":{"@type":"Organization","name":"HerbBlueMap"},"publisher":{"@type":"Organization","name":"HerbBlueMap"}},
      {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]},
      {"@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},
        {"@type":"ListItem","position":2,"name":"Formulas","item":SITE+"/formulas/"},
        {"@type":"ListItem","position":3,"name":py,"item":url}]}]}
    tool_cta = ('<p><a class="btn" href="/shang-han-lun/tool/">Try it in the free formula finder →</a></p>'
                '<p class="hero-note">Walk the signs step by step and see where this formula sits among its neighbors.</p>') if it["in_tool"] else \
               '<p><a class="btn" href="/shang-han-lun/tool/">Open the free Shang Han Lun formula finder →</a></p>'
    rel_html = "".join(f'<li><a href="/formulas/{o["slug"]}/"><strong>{esc(o["py"])} · {o["zh"]} →</strong><span>{esc(o["en"])}</span></a></li>' for o in rel)
    note = f'<p>{esc(it["note"])}</p>' if it.get("note") else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}" />
<link rel="canonical" href="{url}" />
<link rel="icon" type="image/svg+xml" href="/favicon.svg" />
<meta property="og:type" content="article" />
<meta property="og:site_name" content="HerbBlueMap" />
<meta property="og:title" content="{esc(py)} ({zh}) — {esc(en)}" />
<meta property="og:description" content="{esc(desc)}" />
<meta property="og:url" content="{url}" />
<link rel="stylesheet" href="/style.css" />
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
</script>
</head>
<body>
<header class="site-hdr">
  <a class="brand" href="/">
    <img src="/favicon.svg" alt="" width="30" height="30" />
    <span class="brand-name">Herb<em>Blue</em>Map</span>
  </a>
  <nav class="site-nav">
    <a href="/body-relief/">Pain Point Finder</a>
    <a href="/bencao/">Herb Library</a>
    <a href="/formulas/">Formulas</a>
    <a href="/find/">Find an Acupuncturist</a>
  </nav>
</header>
<main>
  <article class="article">
    <p class="crumbs"><a href="/">Home</a> · <a href="/formulas/">Formulas</a> · {esc(py)}</p>
    <h1>{esc(py)} ({zh}): Ingredients, Uses &amp; Original Text</h1>
    <p class="lede"><strong>{esc(py)}</strong> — {zh}, the <em>{esc(en)}</em> — is a classical Chinese herbal formula of {len(it['herbs'])} herbs from the {esc(it['source'].split(',')[0])}. It belongs to the {esc(it['meridian'])} stage and is aimed at one pattern: {esc(it['pattern'][0].lower()+it['pattern'][1:])}.</p>
    {note}
    <h2>Ingredients of {esc(py)}</h2>
    <ul class="formula-herbs">
      {''.join(herb_li(h) for h in it['herbs'])}
    </ul>
    <p class="hero-note">Doses are typical modern textbook amounts for one day's decoction, shown for study. They are not a prescription.</p>
    <h2>What {esc(py)} is used for</h2>
    <p><strong>Classical pattern:</strong> {esc(it['pattern'])}.</p>
    <p><strong>Typical pulse:</strong> {esc(it['pulse'])}.</p>
    <p><strong>Modern clinical uses:</strong> {esc(it['modern'])}.</p>
    <h2>The original line</h2>
    <blockquote class="pull">{esc(en_line)}</blockquote>
    {f'<p lang="zh">{esc(zh_line)}</p>' if zh_line else ''}
    <p class="hero-note">— {esc(it['source'])}</p>
    <h2>How to prepare {esc(py)}</h2>
    <p>{esc(it['prep'])}</p>
    <h2>Cautions</h2>
    <p>{esc(it['contra'])}</p>
    {tool_cta}
<aside class="doctor-note">
  <strong>When to see a doctor instead:</strong> persistent or worsening symptoms, high or returning fever, severe pain, chest pain, fainting, or anything that frightens you. A classical pattern name is a way of seeing — it is never a reason to delay real medical care. Herbs can interact with prescription drugs; tell your clinician what you take.
</aside>
    <section class="faq">
      <h2>Questions about {esc(py)}</h2>
      {''.join(f'<div class="faq-item"><h3>{esc(q)}</h3><p>{esc(a)}</p></div>' for q,a in faq)}
    </section>
    <section class="seealso">
      <h2>Related formulas</h2>
      <ul class="lib-grid">
      {rel_html}
      <li><a href="/formulas/"><strong>All classical formulas →</strong><span>The full index, A–Z with Chinese names.</span></a></li>
      <li><a href="/shang-han-lun/"><strong>Shang Han Lun for beginners →</strong><span>The 1,800-year-old handbook these formulas come from.</span></a></li>
      </ul>
    </section>
    <p class="disclaimer">Educational content only. HerbBlueMap does not diagnose, prescribe, or promise cures. Herbs are medicine — talk to a qualified practitioner or your clinician before using them, especially alongside medication, in pregnancy, or for serious conditions.</p>
  </article>
</main>
<footer class="site-ftr">
  <p>© 2026 HerbBlueMap · The blueprint of Chinese herbal wisdom, in plain English.</p>
  <p><a href="/body-relief/">Pain Point Finder</a> · <a href="/bencao/">Herb Library</a> · <a href="/formulas/">Formulas</a> · <a href="/find/">Find an Acupuncturist</a> · <a href="/#about">About</a></p>
</footer>
</body>
</html>
"""


def index_page(items):
    url = f"{SITE}/formulas/"
    title = "Chinese Herbal Formulas A–Z: Shang Han Lun & Classical Formulas in English | HerbBlueMap"
    desc = (f"{len(items)} classical Chinese herbal formulas in plain English — Gui Zhi Tang, Ma Huang Tang, Wu Ling San, "
            "Bai Hu Tang, Da Cheng Qi Tang and more — with pinyin, Chinese names, ingredients, uses and the original Shang Han Lun lines.")
    rows = "".join(f'<li><a href="/formulas/{o["slug"]}/"><strong>{esc(o["py"])} · {o["zh"]} →</strong><span>{esc(o["en"])} — {esc(o["modern"].split(",")[0])}</span></a></li>'
                   for o in sorted(items, key=lambda o: o["py"]))
    ld = {"@context":"https://schema.org","@graph":[
      {"@type":"CollectionPage","name":"Chinese Herbal Formulas A–Z","url":url,"description":desc,"inLanguage":"en"},
      {"@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"url":f"{SITE}/formulas/{o['slug']}/","name":f"{o['py']} ({o['zh']})"}
                                            for i,o in enumerate(sorted(items, key=lambda o: o['py']))]}]}
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}" />
<link rel="canonical" href="{url}" />
<link rel="icon" type="image/svg+xml" href="/favicon.svg" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="HerbBlueMap" />
<meta property="og:title" content="Chinese Herbal Formulas A–Z" />
<meta property="og:description" content="{esc(desc)}" />
<meta property="og:url" content="{url}" />
<link rel="stylesheet" href="/style.css" />
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
</script>
</head>
<body>
<header class="site-hdr">
  <a class="brand" href="/">
    <img src="/favicon.svg" alt="" width="30" height="30" />
    <span class="brand-name">Herb<em>Blue</em>Map</span>
  </a>
  <nav class="site-nav">
    <a href="/body-relief/">Pain Point Finder</a>
    <a href="/bencao/">Herb Library</a>
    <a href="/formulas/">Formulas</a>
    <a href="/find/">Find an Acupuncturist</a>
  </nav>
</header>
<main>
  <article class="article">
    <p class="crumbs"><a href="/">Home</a> · Formulas</p>
    <h1>Chinese Herbal Formulas A–Z</h1>
    <p class="lede">Chinese medicine rarely prescribes a single herb. It prescribes a <em>formula</em>: a small team of herbs aimed at one pattern. These are the classical formulas of the <a href="/shang-han-lun/">Shang Han Lun</a> and its companion texts — each with its pinyin and Chinese name, ingredients, typical uses, the original line, and cautions. Every herb links to its page in the <a href="/bencao/">herb library</a>.</p>
    <p><a class="btn" href="/shang-han-lun/tool/">Find a formula by symptoms (free) →</a></p>
    <ul class="lib-grid">
      {rows}
    </ul>
    <p class="disclaimer">Educational content only. HerbBlueMap does not diagnose, prescribe, or promise cures. Formulas are medicine — use them only under a qualified practitioner.</p>
  </article>
</main>
<footer class="site-ftr">
  <p>© 2026 HerbBlueMap · The blueprint of Chinese herbal wisdom, in plain English.</p>
  <p><a href="/body-relief/">Pain Point Finder</a> · <a href="/bencao/">Herb Library</a> · <a href="/formulas/">Formulas</a> · <a href="/find/">Find an Acupuncturist</a> · <a href="/#about">About</a></p>
</footer>
</body>
</html>
"""


def link_herb_pages(items):
    """Turn 'Classical pairings' formula tags on herb pages into links to formula pages."""
    by_key = {re.sub(r"[^a-z]", "", o["py"].lower()): o for o in items}
    tag = re.compile(r'<(a|span) (?:href="[^"]*" )?class="formula-tag( highlight)?"(?: href="[^"]*")?>([^<]+)</(?:a|span)>')
    for fn in sorted(os.listdir(os.path.join(ROOT, "bencao"))):
        if not fn.endswith(".html") or fn == "index.html": continue
        p = os.path.join(ROOT, "bencao", fn); s = open(p, encoding="utf-8").read()
        def rep(m):
            label = m.group(3); hl = m.group(2) or ""
            o = by_key.get(re.sub(r"[^a-z]", "", html.unescape(label).split("(")[0].lower()))
            href = f"/formulas/{o['slug']}/" if o else "/shang-han-lun/tool/"
            return f'<a href="{href}" class="formula-tag{hl}">{label}</a>'
        n = tag.sub(rep, s)
        if n != s: open(p, "w", encoding="utf-8").write(n)


def sitemap():
    urls = []
    for d, _, files in os.walk(ROOT):
        if "/." in d or "/tools" in d or "/functions" in d or "/research" in d: continue
        for f in files:
            if not f.endswith(".html"): continue
            rel = os.path.relpath(os.path.join(d, f), ROOT).replace(os.sep, "/")
            path = "/" + (rel[:-10] if rel.endswith("index.html") else rel)
            pr = "1.0" if path == "/" else "0.8" if path.count("/") <= 2 and path.endswith("/") else "0.7"
            urls.append((path, pr))
    out = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, pr in sorted(urls, key=lambda u: (u[0] != "/", u[0])):
        out.append(f"  <url><loc>{SITE}{path}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>")
    out.append("</urlset>\n")
    open(os.path.join(ROOT, "sitemap.xml"), "w").write("\n".join(out))
    return len(urls)


def main():
    items = collect()
    for it in items:
        d = os.path.join(ROOT, "formulas", it["slug"]); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page(it, items))
    open(os.path.join(ROOT, "formulas", "index.html"), "w", encoding="utf-8").write(index_page(items))
    link_herb_pages(items)
    print(f"{len(items)} formula pages; sitemap {sitemap()} urls")


if __name__ == "__main__":
    main()
