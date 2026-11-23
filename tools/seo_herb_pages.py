#!/usr/bin/env python3
"""One-off SEO pass on bencao herb pages: pinyin-first titles (spaced pinyin = how people search),
real <h1>, and Formulas link in the site nav. Idempotent."""
import os, re, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPACED = {"baizhu":"Bai Zhu","banxia":"Ban Xia","chaihu":"Chai Hu","chuanxiong":"Chuan Xiong","dahuang":"Da Huang",
 "danggui":"Dang Gui","dazao":"Da Zao","ejiao":"E Jiao","fuling":"Fu Ling","fuzi":"Fu Zi","gancao":"Gan Cao",
 "gegen":"Ge Gen","guizhi":"Gui Zhi","houpo":"Hou Po","huanglian":"Huang Lian","huangqi":"Huang Qi",
 "huangqin":"Huang Qin","mahuang":"Ma Huang","mangxiao":"Mang Xiao","renshen":"Ren Shen","shaoyao":"Bai Shao",
 "shengjiang":"Sheng Jiang","shigao":"Shi Gao","wuweizi":"Wu Wei Zi","xingren":"Xing Ren","xixin":"Xi Xin",
 "zexie":"Ze Xie","zhigancao":"Zhi Gan Cao","zhimu":"Zhi Mu","zhishi":"Zhi Shi","zhizi":"Zhi Zi","zhuling":"Zhu Ling"}
for key, sp in SPACED.items():
    p = os.path.join(ROOT, "bencao", key + ".html"); s = open(p, encoding="utf-8").read()
    cn = re.search(r'class="herb-cn">([^<]+)', s).group(1)
    en = html.unescape(re.search(r'class="herb-en">([^<]+)', s).group(1))
    title = f"{sp} ({cn}, {en}): Benefits, Uses &amp; Classical Formulas | HerbBlueMap"
    s = re.sub(r"<title>[^<]*</title>", f"<title>{title}</title>", s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + title, s, count=1)
    s = re.sub(r'("headline": ")[^"]*', lambda m: m.group(1) + f"{sp} ({cn}, {html.escape(en)}) — Shennong Bencao Jing", s, count=1)
    s = s.replace('<div class="herb-names">', '<h1 class="herb-names">', 1)
    s = re.sub(r'(<h1 class="herb-names">.*?)</div>', r'\1</h1>', s, count=1, flags=re.S)
    s = re.sub(r'class="herb-pinyin">[^<]+', f'class="herb-pinyin">{sp.split(" (")[0]}', s, count=1)
    if "h1.herb-names" not in s:
        s = s.replace(".herb-names{", "h1.herb-names{font-size:inherit;font-weight:400}\n.herb-names{", 1)
    open(p, "w", encoding="utf-8").write(s)
# Formulas link in site nav, sitewide
for d, _, files in os.walk(ROOT):
    if "/." in d or "/tools" in d: continue
    for f in files:
        if not f.endswith(".html"): continue
        p = os.path.join(d, f); s = open(p, encoding="utf-8").read()
        if 'href="/formulas/">Formulas' in s: continue
        n = s.replace('<a href="/bencao/">Herb Library</a>\n', '<a href="/bencao/">Herb Library</a>\n    <a href="/formulas/">Formulas</a>\n', 1)
        if n != s: open(p, "w", encoding="utf-8").write(n)
