#!/usr/bin/env python3
"""Build acupuncture / TCM landing pages aimed at US searchers (head terms + New York local terms).

Pages: /acupuncture/ (pillar), /acupuncture/insurance/, /acupuncture/new-york/ + one page per
verified area in the /find/ directory, /traditional-chinese-medicine/ (pillar).
Area pages list practitioners live from /api/search (same D1 data as /find/), so listings stay current.
Run: python3 tools/build_local.py   then   python3 tools/build_formulas.py  (regenerates sitemap)
"""
import html, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://herbbluemap.com"
esc = lambda s: html.escape(s, quote=True)

HEADER = """<header class="site-hdr">
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
</header>"""
FOOTER = """<footer class="site-ftr">
  <p>© 2026 HerbBlueMap · The blueprint of Chinese herbal wisdom, in plain English.</p>
  <p><a href="/acupuncture/">Acupuncture</a> · <a href="/acupuncture/new-york/">Acupuncture in New York</a> · <a href="/acupuncture/insurance/">Insurance</a> · <a href="/traditional-chinese-medicine/">Chinese Medicine</a> · <a href="/formulas/">Formulas</a> · <a href="/find/">Find an Acupuncturist</a></p>
</footer>"""
DISCLAIMER = '<p class="disclaimer">Educational content only. HerbBlueMap does not diagnose or treat, and listing is not an endorsement. Check any practitioner\'s license yourself, and see a physician for new, severe or worsening symptoms.</p>'

LIST_JS = """<script>
(function(){
  var box=document.getElementById('live-list'); if(!box) return;
  var city=box.getAttribute('data-city')||'';
  var url='/api/search?mode=area&state=NY'+(city?'&city='+encodeURIComponent(city):'')+'&page=1';
  function e(s){return String(s||'').replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  fetch(url).then(function(r){return r.json()}).then(function(d){
    if(!d||!d.results||!d.results.length){box.innerHTML='<p>Listings are loading slowly — <a href="/find/">open the full directory</a>.</p>';return;}
    box.innerHTML='<p class="hero-note">'+d.total+' verified licensed acupuncturists'+(city?'':' across New York')+'. Showing '+d.results.length+'.</p><ul class="lib-grid">'+d.results.map(function(p){
      return '<li><a href="/find/?lic='+e(p.lic)+'"><strong>'+e(p.name)+' →</strong><span>'+e(p.addr||'')+' '+e(p.zip||'')+(p.since?' · licensed since '+e(String(p.since).slice(0,4)):'')+'</span></a></li>'}).join('')+'</ul>';
  }).catch(function(){box.innerHTML='<p><a href="/find/">Open the directory →</a></p>'});
})();
</script>"""


def faq_html(faq):
    return '<section class="faq"><h2>Questions, answered straight</h2>' + "".join(
        f'<div class="faq-item"><h3>{esc(q)}</h3><p>{a}</p></div>' for q, a in faq) + "</section>"


def strip(s):
    import re
    return html.unescape(re.sub(r"<[^>]+>", "", s))


def render(path, title, desc, h1, crumbs, body, faq, live_city=None, og_type="article"):
    url = SITE + path
    crumb_items = [("Home", "/")] + crumbs
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article" if og_type == "article" else "CollectionPage", "headline": h1, "description": desc, "url": url,
         "inLanguage": "en-US", "author": {"@type": "Organization", "name": "HerbBlueMap"},
         "publisher": {"@type": "Organization", "name": "HerbBlueMap"}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in faq]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(crumb_items)]}]}
    crumb_html = " · ".join(f'<a href="{u}">{esc(n)}</a>' for n, u in crumb_items[:-1]) + " · " + esc(crumb_items[-1][0])
    live = f'<div id="live-list" data-city="{live_city}"><p><a href="/find/">Loading verified practitioners…</a></p></div>' if live_city is not None else ""
    doc = f"""<!doctype html>
<html lang="en-US">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}" />
<link rel="canonical" href="{url}" />
<link rel="icon" type="image/svg+xml" href="/favicon.svg" />
<meta property="og:type" content="{og_type}" />
<meta property="og:site_name" content="HerbBlueMap" />
<meta property="og:title" content="{esc(h1)}" />
<meta property="og:description" content="{esc(desc)}" />
<meta property="og:url" content="{url}" />
<link rel="stylesheet" href="/style.css" />
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
</script>
</head>
<body>
{HEADER}
<main>
  <article class="article">
    <p class="crumbs">{crumb_html}</p>
    <h1>{esc(h1)}</h1>
{body.replace('{{LIVE}}', live)}
{faq_html(faq)}
{DISCLAIMER}
  </article>
</main>
{FOOTER}
{LIST_JS if live_city is not None else ''}
</body>
</html>
"""
    d = os.path.join(ROOT, path.strip("/")); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(doc)


VERIFY = """<h2>How to check an acupuncturist's license in New York</h2>
    <p>New York licenses acupuncturists through the State Education Department's Office of the Professions. Anyone can look up a license number, its status and its registration date on the Office of the Professions online verification page. Look for a license that is current, a registration that has not lapsed, and no disciplinary actions. Every practitioner in our directory was checked this way, one by one, and anyone with a disciplinary record is left out.</p>"""

FIRST_VISIT = """<h2>What to expect at your first visit</h2>
    <p>A first appointment usually runs 60 to 90 minutes. Expect questions about your main complaint, sleep, digestion and medications; many practitioners also look at your tongue and take your pulse at both wrists (<a href="/tongue-diagnosis/">here is what they look for</a>). Needles are hair-thin, sterile and single-use. Most people feel a brief pinch, then heaviness or warmth. Follow-ups are shorter, and for chronic problems a typical plan is weekly sessions for four to eight weeks before deciding whether it is working.</p>"""

AREAS = [
    ("flushing", "Flushing, Queens", "Flushing",
     "Flushing has one of the densest concentrations of acupuncturists in the country, and many practice in Mandarin or Cantonese as well as English. That makes it a good place to find practitioners trained in China who also prescribe Chinese herbs, often at lower prices than Manhattan. Clinics cluster around Main Street, Roosevelt Avenue and the streets near the 7 train terminal."),
    ("manhattan", "Manhattan", "Manhattan",
     "Manhattan practices range from solo L.Ac. offices to integrative clinics working alongside physical therapists and physicians. Expect higher fees than in Queens, more practices that bill insurance directly, and more appointments available before and after office hours in Midtown and the Financial District."),
    ("buffalo", "Buffalo", "Buffalo",
     "Buffalo and its suburbs have a smaller but growing group of licensed acupuncturists, several working within chiropractic, physical therapy or integrative medicine practices. If you are searching for acupuncture in Western New York, start here."),
    ("rochester", "Rochester", "Rochester",
     "Rochester's acupuncturists are spread across the city and the suburbs of Monroe County, with a number of practices focused on pain, fertility support and stress. Many accept HSA and FSA cards."),
    ("syracuse", "Syracuse", "Syracuse",
     "Syracuse and Central New York have a compact community of licensed acupuncturists, some working in integrative and chiropractic offices. Check each practitioner's license and their specialties before booking."),
]


def build():
    area_links = "".join(f'<li><a href="/acupuncture/{k}/"><strong>Acupuncture in {esc(lbl)} →</strong><span>Verified licensed acupuncturists, listed live.</span></a></li>' for k, lbl, _, _ in AREAS)

    # ── Pillar: acupuncture ──
    render("/acupuncture/",
        "Acupuncture: What It Is, What It Helps, Cost & Insurance (US Guide) | HerbBlueMap",
        "A plain-English guide to acupuncture in the US: how it works, what research says it helps, what a session costs, whether insurance, Medicare or your HSA covers it, and how to find a licensed acupuncturist near you.",
        "Acupuncture: What It Is, What It Helps, and How to Find a Good Acupuncturist",
        [("Acupuncture", "/acupuncture/")],
        f"""    <p class="lede">Acupuncture is the practice of inserting very thin, sterile needles at specific points on the body. It comes from <a href="/traditional-chinese-medicine/">traditional Chinese medicine</a>, where the points sit on channels that map how the body's systems connect. In the US today it is offered by licensed acupuncturists, and by some physicians, chiropractors and physical therapists with extra training. Millions of Americans use it every year, most often for pain.</p>
    <p><a class="btn" href="/find/">Find a verified acupuncturist →</a></p>
    <h2>What acupuncture is used for</h2>
    <p>The strongest research support is for chronic pain. The American College of Physicians lists acupuncture among first-line non-drug treatments for chronic low back pain, and reviews summarized by the National Institutes of Health find it can help neck pain, knee osteoarthritis pain, tension headaches and migraine prevention. People also seek it for insomnia, anxiety and stress, nausea, digestive complaints, allergies, menstrual pain and fertility support. The evidence for those is more mixed, and a good practitioner will tell you so.</p>
    <p>Not sure where your pain fits? Our <a href="/body-relief/">Pain Point Finder</a> maps common aches to the classical acupoints used for them.</p>
    <h2>How it works — two ways to say it</h2>
    <p><strong>The classical way:</strong> qi and blood flow through channels; pain and illness come from blockage or imbalance; needling specific points restores the flow. <strong>The research way:</strong> needling stimulates nerves, muscle and connective tissue, changes how the brain processes pain signals, and triggers the release of the body's own pain-relieving chemicals. You do not have to believe the first to benefit from the second.</p>
    <h2>Is acupuncture safe?</h2>
    <p>In the hands of a licensed practitioner, serious problems are rare. Needles sold in the US are regulated by the FDA as medical devices and must be sterile and single-use. Common minor effects are small bruises, brief soreness or feeling tired afterward. Tell your practitioner if you are pregnant, have a pacemaker, take blood thinners or have a bleeding disorder.</p>
    {FIRST_VISIT}
    <h2>How much does acupuncture cost?</h2>
    <p>Prices vary a lot by city. Many US clinics charge roughly $75–$150 for a follow-up session, with first visits costing more. Manhattan and other high-rent areas often charge more, while community acupuncture clinics, where several patients are treated in one room, can cost much less. Ask about package prices, and whether the clinic gives you a receipt you can submit to insurance or your HSA.</p>
    <h2>Does insurance cover acupuncture?</h2>
    <p>Often, partly. Medicare covers acupuncture for chronic low back pain. Many private and employer plans cover a set number of visits, and acupuncture is an eligible expense for HSA and FSA accounts. Read our full guide: <a href="/acupuncture/insurance/">Is acupuncture covered by insurance?</a></p>
    <h2>Find acupuncture near you</h2>
    <p>Our directory starts with New York, where we check every license against state records and leave out anyone with a disciplinary history.</p>
    <ul class="lib-grid">
      <li><a href="/acupuncture/new-york/"><strong>Acupuncture in New York →</strong><span>NYC and upstate, verified licenses only.</span></a></li>
      {area_links}
    </ul>
    <section class="seealso">
      <h2>Keep reading</h2>
      <ul class="lib-grid">
      <li><a href="/traditional-chinese-medicine/"><strong>Traditional Chinese medicine, explained →</strong><span>Acupuncture is one branch. Here is the whole tree.</span></a></li>
      <li><a href="/body-clock/"><strong>The Chinese body clock →</strong><span>Why you wake at 3 a.m.</span></a></li>
      </ul>
    </section>""",
        [("Does acupuncture hurt?", "Usually very little. The needles are much thinner than injection needles. Most people feel a quick pinch, then a dull ache, heaviness or warmth at the point, which practitioners consider a sign the point is working."),
         ("How many acupuncture sessions do I need?", "For a recent problem, a few sessions may be enough. For chronic pain, a common plan is once a week for four to eight weeks, then reassess. If nothing has changed after five or six sessions, it is reasonable to stop."),
         ("Is acupuncture covered by insurance?", "Often partly. Medicare covers it for chronic low back pain, many private plans cover a limited number of visits, and it is an HSA/FSA-eligible expense. See <a href=\"/acupuncture/insurance/\">our insurance guide</a>."),
         ("What is the difference between acupuncture and dry needling?", "They use similar needles. Dry needling is done by physical therapists and others, targets trigger points in tight muscles, and is based on Western anatomy only. Acupuncture is done by licensed acupuncturists, uses the full system of points and channels, and treats more than muscle pain."),
         ("How do I find a good acupuncturist?", "Check the license with your state board, ask what conditions they treat most, and ask how they will measure progress. In New York you can start with our <a href=\"/find/\">verified directory</a>.")])

    # ── Insurance ──
    render("/acupuncture/insurance/",
        "Is Acupuncture Covered by Insurance? Medicare, HSA/FSA & Private Plans | HerbBlueMap",
        "Does insurance cover acupuncture? What Medicare covers (chronic low back pain), how private and employer plans usually handle it, using HSA and FSA money, and the questions to ask before your first visit.",
        "Is Acupuncture Covered by Insurance?",
        [("Acupuncture", "/acupuncture/"), ("Insurance", "/acupuncture/insurance/")],
        """    <p class="lede">Short answer: often, but rarely in full and rarely for everything. Coverage depends on your plan, the condition being treated, and who does the needling. Here is how it usually works in the US, and the five questions that save you a surprise bill.</p>
    <h2>Medicare</h2>
    <p>Since 2020, Original Medicare (Part B) covers acupuncture for <strong>chronic low back pain</strong>: pain lasting 12 weeks or longer with no identifiable systemic cause such as cancer or infection, and not related to surgery or pregnancy. It covers up to 12 sessions in 90 days, and 8 more if you are improving, up to 20 a year. One catch: Medicare does not let licensed acupuncturists bill it on their own. The acupuncturist must work under the supervision of a physician or other qualifying provider who bills Medicare. Medicare Advantage plans may cover more, so check your plan's benefits.</p>
    <h2>Private and employer plans</h2>
    <p>Many commercial plans now include acupuncture, usually with limits: a set number of visits a year, a copay per visit, and coverage only for certain conditions, most often pain and nausea. Some plans require a referral or pre-authorization. If your acupuncturist is out of network, ask for a superbill (an itemized receipt with diagnosis and procedure codes) to submit for reimbursement.</p>
    <h2>HSA and FSA</h2>
    <p>Acupuncture is a qualified medical expense under IRS rules, so you can pay with a Health Savings Account or Flexible Spending Account card even when your insurance does not cover it. Herbs prescribed for a specific condition may qualify too; ask your plan administrator.</p>
    <h2>Medicaid and workers' comp</h2>
    <p>Medicaid coverage of acupuncture depends on the state and changes over time, so check your state's current benefits. Workers' compensation and no-fault auto insurance often cover acupuncture for injury-related pain when it is part of the treatment plan.</p>
    <h2>Five questions to ask before you book</h2>
    <ol class="formula-herbs">
      <li>Is acupuncture a covered benefit on my plan, and for which conditions?</li>
      <li>How many visits a year, and what is my copay or coinsurance?</li>
      <li>Do I need a referral or pre-authorization?</li>
      <li>Is this acupuncturist in network? If not, will they give me a superbill?</li>
      <li>Does the clinic accept HSA/FSA cards?</li>
    </ol>
    <p><a class="btn" href="/find/">Find a verified acupuncturist in New York →</a></p>""",
        [("Does Medicare cover acupuncture?", "Yes, for chronic low back pain: up to 12 sessions in 90 days, plus 8 more if you improve, up to 20 a year. The acupuncturist must work under a provider who can bill Medicare."),
         ("Can I use my HSA or FSA for acupuncture?", "Yes. Acupuncture is a qualified medical expense under IRS rules, so HSA and FSA funds can pay for it."),
         ("Does insurance cover acupuncture for anxiety or fertility?", "Sometimes. Many plans limit coverage to pain and nausea. Ask your insurer whether your specific diagnosis is covered before you start."),
         ("What is a superbill?", "An itemized receipt with diagnosis and procedure codes that you can send to your insurer to request out-of-network reimbursement.")])

    # ── New York hub ──
    render("/acupuncture/new-york/",
        "Acupuncture in New York: Find a Licensed Acupuncturist in NYC & Upstate | HerbBlueMap",
        "Find a licensed acupuncturist in New York — Manhattan, Flushing (Queens), Buffalo, Rochester and Syracuse. Every license checked against New York State records; anyone with a disciplinary record is left out.",
        "Acupuncture in New York: Licensed Acupuncturists, Verified One by One",
        [("Acupuncture", "/acupuncture/"), ("New York", "/acupuncture/new-york/")],
        f"""    <p class="lede">New York has thousands of licensed acupuncturists, and New York City has one of the largest acupuncture communities in the country. Finding one is easy. Finding one you can trust is the hard part. Every practitioner below has a current New York license that we checked against state records, and anyone with a disciplinary record, ever, is left out.</p>
    <h2>Choose your area</h2>
    <ul class="lib-grid">{area_links}</ul>
    <h2>Verified acupuncturists in New York</h2>
    {{{{LIVE}}}}
    <p><a class="btn" href="/find/">Search by ZIP code or concern →</a></p>
    {VERIFY}
    {FIRST_VISIT}
    <h2>Paying for acupuncture in New York</h2>
    <p>Many New York acupuncturists accept HSA and FSA cards, and a growing number bill insurance directly. Medicare covers acupuncture for chronic low back pain under specific rules. See <a href="/acupuncture/insurance/">is acupuncture covered by insurance</a>.</p>""",
        [("How do I check if an acupuncturist is licensed in New York?", "Use the New York State Office of the Professions online license verification. Search by name or license number, and check that the license is current with no disciplinary actions."),
         ("Where are the most acupuncturists in New York City?", "Flushing in Queens and Manhattan have the highest concentration. Flushing has many Mandarin- and Cantonese-speaking practitioners who also prescribe Chinese herbs."),
         ("What does L.Ac. mean?", "Licensed Acupuncturist: the state license for practicing acupuncture. In New York it is issued by the State Education Department.")],
        live_city="")

    for key, label, short, intro in AREAS:
        render(f"/acupuncture/{key}/",
            f"Acupuncture in {label}, NY: Verified Licensed Acupuncturists | HerbBlueMap",
            f"Looking for acupuncture in {label}? A list of licensed acupuncturists in {short}, each checked against New York State records, with no disciplinary history. What a first visit is like, cost and insurance.",
            f"Acupuncture in {label}: Licensed Acupuncturists You Can Check",
            [("Acupuncture", "/acupuncture/"), ("New York", "/acupuncture/new-york/"), (short, f"/acupuncture/{key}/")],
            f"""    <p class="lede">{esc(intro)}</p>
    <h2>Verified acupuncturists in {esc(short)}</h2>
    {{{{LIVE}}}}
    <p><a class="btn" href="/find/">Search by ZIP code or by concern →</a></p>
    {VERIFY}
    {FIRST_VISIT}
    <h2>Cost and insurance</h2>
    <p>Ask each clinic for its first-visit and follow-up prices, whether it bills your insurance, and whether it takes HSA/FSA cards. Our <a href="/acupuncture/insurance/">insurance guide</a> lists the questions to ask before booking.</p>
    <section class="seealso"><h2>Other areas</h2><ul class="lib-grid">{"".join(f'<li><a href="/acupuncture/{k}/"><strong>Acupuncture in {esc(l)} →</strong><span>Verified licenses only.</span></a></li>' for k, l, _, _ in AREAS if k != key)}</ul></section>""",
            [(f"How do I find a good acupuncturist in {short}?", "Start with a verified license, then ask what conditions they treat most often, how many sessions they expect, and how you will measure progress. The list on this page only includes licenses checked against New York State records."),
             (f"Do acupuncturists in {short} take insurance?", "Some do, especially for back pain and injury-related pain; many accept HSA and FSA cards. Call ahead and ask whether they are in network with your plan."),
             ("Is my practitioner missing from this list?", "We add practitioners as their licenses are verified. Licensed acupuncturists can also claim and complete their profile for free; we never sell rankings.")],
            live_city=key)

    # ── TCM pillar ──
    render("/traditional-chinese-medicine/",
        "Traditional Chinese Medicine (TCM): A Plain-English Guide for Americans | HerbBlueMap",
        "What is traditional Chinese medicine? Yin and yang, qi, the five branches (acupuncture, herbs, cupping and gua sha, tui na, tai chi and qigong), what research supports, safety with herbs, and how to find a qualified TCM practitioner in the US.",
        "Traditional Chinese Medicine (TCM), Explained in Plain English",
        [("Traditional Chinese Medicine", "/traditional-chinese-medicine/")],
        """    <p class="lede">Traditional Chinese medicine (TCM) is a 2,000-year-old system of health care built on one idea: look for the <em>pattern</em> behind the symptoms, not just the symptoms. In the US it reaches most people through acupuncture, Chinese herbs, cupping and tai chi. This guide explains the core ideas, the main branches, what the research says, and how to use TCM safely alongside your regular doctor.</p>
    <h2>The core ideas, in one paragraph each</h2>
    <p><strong>Yin and yang.</strong> Every condition leans hot or cold, excess or deficient, outward or inward. Treatment pushes back toward balance: cooling herbs for heat patterns, warming herbs for cold ones. Our <a href="/chinese-herbs-for-beginners/">beginner's roadmap</a> starts here for a reason.</p>
    <p><strong>Qi and blood.</strong> Qi is the body's functional activity, blood its nourishment. Most patterns are a story of one of them being stuck, weak or misdirected.</p>
    <p><strong>Organ systems and channels.</strong> A TCM "Spleen" or "Liver" is a network of functions, not just the anatomical organ. Channels connect them to the surface, which is where acupuncture points sit. The <a href="/body-clock/">body clock</a> and <a href="/tongue-diagnosis/">tongue reading</a> are two classic ways of seeing these systems.</p>
    <p><strong>Patterns, not diseases.</strong> Two people with "insomnia" may get different treatments because their patterns differ. <a href="/dampness/">Dampness</a> is a good example of a pattern that has no single Western equivalent.</p>
    <h2>The five branches of TCM</h2>
    <ul class="lib-grid">
      <li><a href="/acupuncture/"><strong>Acupuncture →</strong><span>The branch most Americans meet first. Best evidence: chronic pain.</span></a></li>
      <li><a href="/bencao/"><strong>Chinese herbal medicine →</strong><span>The classical 32 herbs, one at a time.</span></a></li>
      <li><a href="/formulas/"><strong>Herbal formulas →</strong><span>How herbs are combined, from the Shang Han Lun.</span></a></li>
      <li><a href="/body-relief/"><strong>Acupressure and tui na →</strong><span>Points you can press yourself, by symptom.</span></a></li>
      <li><a href="/chinese-herbal-medicine/"><strong>Adaptogens and tonics →</strong><span>Ginseng, astragalus, reishi in their classical context.</span></a></li>
    </ul>
    <p>Cupping and gua sha (scraping) loosen tight tissue and are often added to an acupuncture visit. Tai chi and qigong are gentle movement practices with good research support for balance, fall prevention and stress.</p>
    <h2>What the research supports</h2>
    <p>The best evidence is for acupuncture in chronic pain, and for tai chi in balance and fall prevention in older adults. Some individual herbs and formulas have promising trials, but quality varies and many have not been studied well. Treat TCM as a complement to medical care, not a replacement for it.</p>
    <h2>Using Chinese herbs safely</h2>
    <p>Herbs are medicine. Some interact with prescription drugs, especially blood thinners, diabetes and blood-pressure medications. Buy from suppliers that test for heavy metals and contamination, avoid herbs in pregnancy unless a qualified practitioner prescribes them, and always tell your doctor what you take.</p>
    <h2>Finding a qualified TCM practitioner in the US</h2>
    <p>Acupuncture is licensed state by state, and most states require the national NCCAOM board exams. For herbs, look for training or certification in Chinese herbology as well. In New York, start with our <a href="/acupuncture/new-york/">verified acupuncturists</a>.</p>""",
        [("What is traditional Chinese medicine?", "A system of health care developed in China over two thousand years. It diagnoses patterns of imbalance and treats them with acupuncture, herbal formulas, massage, movement and diet."),
         ("Is traditional Chinese medicine safe?", "Acupuncture by a licensed practitioner is generally safe. Herbs need more care because they can interact with medications and vary in quality. Use a qualified practitioner and keep your doctor informed."),
         ("What is the difference between TCM and acupuncture?", "Acupuncture is one branch of traditional Chinese medicine. TCM also includes herbal medicine, cupping, gua sha, tui na massage, tai chi, qigong and dietary therapy."),
         ("Do I need a referral to see a TCM practitioner?", "Usually not. You can book directly, though some insurance plans require a referral to cover acupuncture.")])


if __name__ == "__main__":
    build()
    print("built", 4 + len(AREAS), "pages")
