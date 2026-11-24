#!/usr/bin/env python3
"""Week-2 guide pages from the keyword map (/mnt/project-files/herbbluemap/关键词地图_2026-11-24.md):
cost, 'does acupuncture work' question hub, and 'acupuncture for <condition>' pages.
Run: python3 tools/build_guides.py  then  python3 tools/build_formulas.py (sitemap)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_local import render, FIRST_VISIT  # noqa: E402

NEXT = """<section class="seealso"><h2>Keep reading</h2><ul class="lib-grid">
      <li><a href="/acupuncture/"><strong>Acupuncture, explained →</strong><span>What it is, what it helps, how to find a good acupuncturist.</span></a></li>
      <li><a href="/acupuncture/insurance/"><strong>Is acupuncture covered by insurance? →</strong><span>Medicare, private plans, HSA and FSA.</span></a></li>
      <li><a href="/acupuncture/new-york/"><strong>Acupuncture in New York →</strong><span>Licensed acupuncturists, verified one by one.</span></a></li>
    </ul></section>"""

CONDITIONS = [
 dict(slug="back-pain", kw="Back Pain and Sciatica",
  title="Acupuncture for Back Pain & Sciatica: Does It Work, How Many Sessions, Cost | HerbBlueMap",
  desc="Does acupuncture help back pain and sciatica? What the research and US guidelines say, how many sessions it takes, which points are used, what it costs, and when back pain needs a doctor instead.",
  body="""    <p class="lede">Low back pain is the number-one reason Americans try acupuncture, and it is the condition with the strongest evidence behind it. The American College of Physicians recommends acupuncture as a first-line, non-drug treatment for chronic low back pain, and Medicare covers it for exactly that.</p>
    <h2>Does acupuncture help back pain?</h2>
    <p>For chronic low back pain, large reviews find that acupuncture reduces pain and improves function more than no treatment, and modestly more than sham needling. The effect is real but not magic: think of it as one tool next to movement, physical therapy and time, and one that has far fewer side effects than long-term pain medication.</p>
    <h2>What about sciatica?</h2>
    <p>Sciatica — pain running from the buttock down the leg, usually from an irritated nerve root — has less research than plain back pain, but several trials report less leg pain and better function with acupuncture. Practitioners often add electro-acupuncture (a mild current between needles) for nerve pain.</p>
    <h2>Which points are used?</h2>
    <p>Common choices are points along the lower back beside the spine, at the back of the knee (BL40, which classical texts call the command point of the back), and along the outer leg for sciatica. Our <a href="/body-relief/">Pain Point Finder</a> shows these by body area.</p>
    <h2>How many sessions?</h2>
    <p>A typical plan is one or two sessions a week for four to six weeks. Most people who will respond notice some change within the first four or five sessions. Medicare's own rule (up to 12 sessions in 90 days, 8 more if improving) is a reasonable benchmark.</p>
    <h2>Cost and insurance</h2>
    <p>Back pain is the condition insurers are most likely to cover. See <a href="/acupuncture/insurance/">is acupuncture covered by insurance</a> and <a href="/acupuncture/cost/">how much acupuncture costs</a>.</p>
    <aside class="doctor-note"><strong>See a doctor first if:</strong> back pain follows a fall or accident, comes with fever, unexplained weight loss, numbness in the groin, loss of bladder or bowel control, or leg weakness that is getting worse. These need medical care before anything else.</aside>
    <p><a class="btn" href="/find/">Find a verified acupuncturist →</a></p>""",
  faq=[("Is acupuncture good for lower back pain?", "Yes — it is the best-studied use of acupuncture. US physician guidelines list it as a first-line non-drug option for chronic low back pain, and Medicare covers it."),
       ("Can acupuncture make sciatica worse?", "It is uncommon. Some people feel sore for a day after treatment. Pain that is sharply worse or new weakness should be checked by a doctor."),
       ("How quickly does acupuncture work for back pain?", "Some people feel relief after the first session, but most need four to six sessions to judge whether it is working.")]),
 dict(slug="anxiety", kw="Anxiety and Stress",
  title="Acupuncture for Anxiety & Stress: Does It Help? Points, Sessions, What to Expect | HerbBlueMap",
  desc="Can acupuncture help anxiety, stress and panic? What studies show, which points are used, how a session feels, how many you need, and how it fits with therapy and medication.",
  body="""    <p class="lede">Many people come to acupuncture for pain and notice they sleep better and feel calmer. Others come for anxiety directly. The research is younger than for pain, but encouraging, and the treatment itself is one of the gentlest things you can try.</p>
    <h2>Does acupuncture help with anxiety?</h2>
    <p>Small and medium-sized trials report lower anxiety scores after a course of acupuncture, with few side effects. The studies vary in quality, so the honest summary is: promising, worth trying alongside proven treatments, not a replacement for them. Acupuncture appears to calm the body's stress response — slower heart rate, more parasympathetic ("rest and digest") activity — which is also how most people describe the feeling on the table.</p>
    <h2>Which points are used?</h2>
    <p>Classic calming points include Yintang between the eyebrows, HT7 at the wrist crease, PC6 on the inner forearm, and points on the ear (the NADA protocol, used widely in US addiction and trauma clinics). In Chinese medicine terms, anxiety often maps to a heart–kidney or liver-qi pattern, and the point choice follows the pattern.</p>
    <h2>What a session feels like</h2>
    <p>Most people feel heavy and drowsy within ten minutes and many fall asleep. A course is usually weekly for six to eight weeks.</p>
    <h2>Chinese herbs for anxiety</h2>
    <p>Practitioners may also prescribe herbal formulas. Herbs can interact with antidepressants and sedatives, so tell both your practitioner and your doctor what you take. See our <a href="/formulas/">formula library</a> for how formulas are built.</p>
    <aside class="doctor-note"><strong>Get help now</strong> if you have thoughts of harming yourself: call or text 988 (Suicide &amp; Crisis Lifeline, US). Acupuncture is a complement to therapy and medical care, not a substitute.</aside>
    <p><a class="btn" href="/find/">Find a verified acupuncturist →</a></p>""",
  faq=[("Can acupuncture cure anxiety?", "No treatment 'cures' anxiety on its own, but studies suggest acupuncture can lower anxiety symptoms, and it pairs well with therapy and medication."),
       ("Where do the needles go for anxiety?", "Common points are between the eyebrows, at the wrist, on the inner forearm, and on the ear. Your practitioner chooses based on your pattern."),
       ("How many acupuncture sessions for anxiety?", "Usually weekly for six to eight weeks, then less often if it helps.")]),
 dict(slug="fertility", kw="Fertility and IVF",
  title="Acupuncture for Fertility & IVF: What the Evidence Says, Cost, Timing | HerbBlueMap",
  desc="Does fertility acupuncture work? What studies show for IVF and natural conception, acupuncture around embryo transfer, how often to go, cost, and how to choose a fertility acupuncturist.",
  body="""    <p class="lede">Fertility acupuncture is one of the fastest-growing reasons Americans see an acupuncturist, often alongside IVF. It is also an area where honest information matters, because hope is expensive.</p>
    <h2>Does acupuncture help fertility?</h2>
    <p>The evidence is mixed. Early studies suggested acupuncture around embryo transfer raised IVF pregnancy rates; larger, better-designed trials since then mostly found no clear difference in live births. What studies more consistently show is lower stress and anxiety during treatment, which many patients value for its own sake. Any acupuncturist who promises higher pregnancy rates is overselling.</p>
    <h2>How it is usually done</h2>
    <p>Typical plans are weekly sessions for two to three months before a cycle or transfer, sometimes with sessions on the day of embryo transfer. Chinese medicine practitioners may add herbs; if you are in an IVF cycle, only take herbs with your fertility clinic's knowledge, because some can affect hormones or bleeding.</p>
    <h2>For men too</h2>
    <p>A few studies look at sperm quality with acupuncture; results are preliminary. Fertility is a two-person workup, so make sure both partners have been evaluated medically.</p>
    <h2>Cost</h2>
    <p>Fertility acupuncture is rarely covered by insurance, but it is an HSA/FSA-eligible expense. See <a href="/acupuncture/cost/">acupuncture cost</a>.</p>
    <aside class="doctor-note"><strong>See a fertility specialist</strong> if you are under 35 and have been trying for a year, over 35 and trying for six months, or have irregular periods, known endometriosis or prior pelvic infection.</aside>
    <p><a class="btn" href="/find/">Find a verified acupuncturist →</a></p>""",
  faq=[("Does acupuncture actually work for fertility?", "The best recent trials do not show a clear increase in IVF live-birth rates, but acupuncture can reduce stress during treatment. Be wary of anyone promising results."),
       ("When should I start fertility acupuncture?", "Many practitioners suggest two to three months before an IVF cycle or transfer, weekly."),
       ("Is fertility acupuncture covered by insurance?", "Rarely, but you can usually pay with HSA or FSA funds.")]),
 dict(slug="neuropathy", kw="Neuropathy and Nerve Pain",
  title="Acupuncture for Neuropathy & Nerve Pain: Does It Help? Feet, Diabetes, Chemo | HerbBlueMap",
  desc="Can acupuncture help peripheral neuropathy — numbness, burning and tingling in the feet from diabetes or chemotherapy? What research shows, how treatment works, sessions, and safety.",
  body="""    <p class="lede">Peripheral neuropathy — numbness, tingling, burning or electric pain, usually starting in the feet — affects millions of Americans, most often from diabetes or chemotherapy. Medication helps some people only partly, which is why many ask about acupuncture.</p>
    <h2>Does acupuncture help neuropathy?</h2>
    <p>Several trials and reviews report improvement in symptoms and, in some studies, nerve conduction, for diabetic and chemotherapy-induced neuropathy. Study sizes are modest and results vary, so treat it as a reasonable thing to try with your doctor's knowledge, not a guaranteed fix. Major US cancer centers offer acupuncture in their integrative medicine programs, including for chemotherapy side effects.</p>
    <h2>How it is done</h2>
    <p>Needles are placed on the legs and feet (for example ST36 below the knee, and the Bafeng points between the toes), often with electro-acupuncture. A typical course is one or two sessions a week for eight to twelve weeks.</p>
    <h2>Safety with diabetes</h2>
    <p>People with diabetes heal more slowly and may not feel a small injury on numb feet. Make sure your acupuncturist uses sterile single-use needles, cleans the skin, and checks your feet. Do not needle feet with open sores or poor circulation.</p>
    <aside class="doctor-note"><strong>See a doctor</strong> for new numbness or weakness, symptoms that spread quickly, or any foot wound that is not healing. Neuropathy has many causes, including B12 deficiency and thyroid disease, that are worth ruling out.</aside>
    <p><a class="btn" href="/find/">Find a verified acupuncturist →</a></p>""",
  faq=[("Can acupuncture reverse neuropathy?", "It is not proven to reverse nerve damage, but several studies report fewer symptoms and some improvement in nerve function."),
       ("How many acupuncture sessions for neuropathy?", "Often one or two a week for eight to twelve weeks before judging the result."),
       ("Is acupuncture safe for diabetic feet?", "Generally yes with sterile technique, but avoid needling skin with sores or very poor circulation, and tell your practitioner you have diabetes.")]),
]


def build():
    render("/acupuncture/cost/",
        "How Much Does Acupuncture Cost? Per Session, Without Insurance & in NYC | HerbBlueMap",
        "How much does acupuncture cost in the US? Typical prices per session, first visit vs follow-up, NYC prices, community acupuncture, cost with and without insurance, HSA/FSA, and how to keep it affordable.",
        "How Much Does Acupuncture Cost?",
        [("Acupuncture", "/acupuncture/"), ("Cost", "/acupuncture/cost/")],
        """    <p class="lede">Short answer: in most of the US, plan on roughly $75–$150 for a follow-up session, more for the first visit, and more again in Manhattan. Community clinics can be much cheaper, and insurance or an HSA can bring the real cost down. Here is how pricing usually works.</p>
    <h2>Typical prices per session</h2>
    <ul class="formula-herbs">
      <li><strong>First visit:</strong> often longer (60–90 minutes) and priced higher, because it includes a full intake.</li>
      <li><strong>Follow-up session:</strong> roughly $75–$150 in many US cities.</li>
      <li><strong>Manhattan and other high-rent areas:</strong> often above that range; Queens practices, including Flushing, are frequently lower.</li>
      <li><strong>Community acupuncture:</strong> treatment in a shared room on a sliding scale, often far cheaper per visit.</li>
      <li><strong>Add-ons:</strong> cupping, gua sha, electro-acupuncture or herbs may cost extra.</li>
    </ul>
    <p>These are rough ranges, not quotes. Always ask the clinic for its current prices before booking.</p>
    <h2>Cost with insurance</h2>
    <p>If your plan covers acupuncture, you usually pay a copay or coinsurance per visit, up to a yearly visit limit. Medicare covers it for chronic low back pain. Details are in our <a href="/acupuncture/insurance/">insurance guide</a>.</p>
    <h2>Cost without insurance</h2>
    <p>Ask about package prices for a series of sessions, community or student clinics (acupuncture school clinics are supervised and cheaper), and whether the clinic accepts HSA/FSA cards — acupuncture is an eligible expense.</p>
    <h2>How many sessions will I need?</h2>
    <p>For a chronic problem, budget for about six sessions before deciding whether it works. A practitioner who cannot give you a rough plan and a way to measure progress is a warning sign.</p>
    <p><a class="btn" href="/acupuncture/new-york/">Compare acupuncturists in New York →</a></p>
""" + NEXT,
        [("How much is an acupuncture session without insurance?", "In many US cities, roughly $75–$150 for a follow-up session, with first visits costing more. Community clinics can be much cheaper."),
         ("How much does acupuncture cost in NYC?", "Manhattan prices are often above the national range; Queens, including Flushing, is frequently lower. Ask each clinic for current prices."),
         ("Can I use my HSA for acupuncture?", "Yes. Acupuncture is a qualified medical expense, so HSA and FSA funds can pay for it."),
         ("Do you tip an acupuncturist?", "Tipping is not expected in a medical setting. Some spa-style clinics accept tips, but a licensed acupuncturist will not expect one.")])

    render("/acupuncture/does-acupuncture-work/",
        "Does Acupuncture Work? Does It Hurt? 15 Honest Answers | HerbBlueMap",
        "Does acupuncture really work? Does it hurt, bleed or bruise? Are needles reused? Do you undress? Honest, research-based answers to the questions people ask before their first acupuncture appointment.",
        "Does Acupuncture Work? Honest Answers to the Questions Everyone Asks",
        [("Acupuncture", "/acupuncture/"), ("Does it work?", "/acupuncture/does-acupuncture-work/")],
        """    <p class="lede">These are the questions Americans type into Google before their first appointment, answered straight — including the parts where the evidence is thin.</p>
    <h2>Does acupuncture actually work?</h2>
    <p>For some things, yes. The strongest evidence is for chronic pain: low back pain, neck pain, knee osteoarthritis, tension headaches and migraine prevention. For nausea, anxiety, insomnia and many other uses, studies are encouraging but less consistent. Part of the benefit in trials comes from the ritual of care itself — but real acupuncture usually beats sham needling for pain, and both beat no treatment.</p>
    <h2>How does it work?</h2>
    <p>Needling stimulates nerves in skin and muscle, which changes how the spinal cord and brain process pain and releases the body's own pain-relieving chemicals. Chinese medicine describes the same effect as restoring the flow of qi through the channels. See <a href="/acupuncture/">acupuncture, explained</a>.</p>
""" + FIRST_VISIT + """
    <h2>Acupuncture for specific problems</h2>
    <ul class="lib-grid">
      <li><a href="/acupuncture/for/back-pain/"><strong>Back pain and sciatica →</strong><span>The best-studied use.</span></a></li>
      <li><a href="/acupuncture/for/anxiety/"><strong>Anxiety and stress →</strong><span>Promising, gentle, pairs with therapy.</span></a></li>
      <li><a href="/acupuncture/for/fertility/"><strong>Fertility and IVF →</strong><span>What the evidence really says.</span></a></li>
      <li><a href="/acupuncture/for/neuropathy/"><strong>Neuropathy →</strong><span>Feet, diabetes, chemotherapy.</span></a></li>
    </ul>
""" + NEXT,
        [("Does acupuncture hurt?", "Usually very little. The needles are hair-thin; most people feel a quick pinch, then a dull ache, heaviness or warmth."),
         ("Does acupuncture bleed or bruise?", "A drop of blood or a small bruise sometimes happens when a needle is removed. It is harmless and fades in days."),
         ("Are acupuncture needles reused?", "No. Licensed US acupuncturists use sterile, single-use disposable needles, which the FDA regulates as medical devices."),
         ("Do you have to undress for acupuncture?", "Usually only enough to reach the points — rolled-up sleeves and pant legs are common. Clinics provide gowns or sheets when needed."),
         ("Can acupuncture make you tired?", "Yes, many people feel relaxed or sleepy afterward. Plan a calm rest of the day after your first session."),
         ("Does acupuncture detox your body?", "There is no good evidence that acupuncture removes toxins. Its studied effects are on pain, nerves and the stress response."),
         ("Is acupuncture the same as dry needling?", "No. Dry needling targets muscle trigger points and is done by physical therapists and others; acupuncture uses a full system of points and is done by licensed acupuncturists."),
         ("Does insurance cover acupuncture?", "Often partly — see our <a href='/acupuncture/insurance/'>insurance guide</a>.")])

    for c in CONDITIONS:
        render(f"/acupuncture/for/{c['slug']}/", c["title"], c["desc"], f"Acupuncture for {c['kw']}: What It Can and Can't Do",
               [("Acupuncture", "/acupuncture/"), (c["kw"], f"/acupuncture/for/{c['slug']}/")],
               c["body"] + "\n" + NEXT, c["faq"])


if __name__ == "__main__":
    build()
    print("built", 2 + len(CONDITIONS), "guide pages")
