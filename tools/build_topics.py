#!/usr/bin/env python3
"""Keyword-map batch 4: 'chinese herbs for <problem>' pages + cupping / gua sha / moxibustion.
Run: python3 tools/build_topics.py  then  python3 tools/build_formulas.py (sitemap)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_local import render  # noqa: E402

HERB_SAFETY = """<aside class="doctor-note"><strong>Before you take Chinese herbs:</strong> herbs are medicine. They can interact with prescription drugs (blood thinners, blood-pressure, diabetes and psychiatric medications especially), and quality varies by supplier. Avoid them in pregnancy unless a qualified practitioner prescribes them, buy from suppliers that test for heavy metals, and tell your doctor what you take.</aside>"""

def more(links):
    return '<section class="seealso"><h2>Keep reading</h2><ul class="lib-grid">' + "".join(
        f'<li><a href="{u}"><strong>{t} →</strong><span>{d}</span></a></li>' for u, t, d in links) + "</ul></section>"

STD_MORE = [("/formulas/", "Chinese herbal formulas A–Z", "Ingredients, uses and the original lines."),
            ("/bencao/", "The Classical 32 herb library", "One page per core herb."),
            ("/traditional-chinese-medicine/", "Traditional Chinese medicine, explained", "The ideas behind the herbs.")]

HERBS_FOR = [
 dict(slug="cold-and-flu", kw="Colds and Flu",
  title="Chinese Herbs for Colds & Flu: Classic Formulas by Symptom (Plain English) | HerbBlueMap",
  desc="Which Chinese herbs and formulas are used for colds and flu? How Chinese medicine sorts a cold by chills, sweating and thirst, the classic formulas for each (Gui Zhi Tang, Ma Huang Tang, Ge Gen Tang), and when to see a doctor.",
  body="""    <p class="lede">Chinese medicine does not have one "cold remedy". It first asks what kind of cold you have — mostly chills or mostly fever, sweating or not, thirsty or not — and picks the formula that matches. That logic comes straight from the <a href="/shang-han-lun/">Shang Han Lun</a>, a 1,800-year-old handbook written during an epidemic.</p>
    <h2>Cold with chills, no sweat, body aches</h2>
    <p>The classical "wind-cold, tight exterior" picture. The textbook formula is <a href="/formulas/ma-huang-tang/">Ma Huang Tang</a>; with a stiff neck and upper back, <a href="/formulas/ge-gen-tang/">Ge Gen Tang</a>. Note: ephedra (ma huang) products are banned as dietary supplements in the US, and ephedra is not safe with heart disease or high blood pressure — this is strictly practitioner territory.</p>
    <h2>Cold with light sweating and aversion to wind</h2>
    <p>The milder, "leaky" exterior picture, often in people who are run down. The classic is <a href="/formulas/gui-zhi-tang/">Gui Zhi Tang</a> — cinnamon twig, peony, licorice, <a href="/bencao/shengjiang">fresh ginger</a> and <a href="/bencao/dazao">jujube</a> — followed by hot rice porridge.</p>
    <h2>Cold with watery mucus, sneezing and cough</h2>
    <p>Cold plus fluid: <a href="/formulas/xiao-qing-long-tang/">Xiao Qing Long Tang</a>, also used in allergic rhinitis.</p>
    <h2>Fever, sore throat, thirst, yellow phlegm</h2>
    <p>Now the picture is heat. Practitioners turn to cooling formulas such as <a href="/formulas/ma-xing-gan-shi-tang/">Ma Xing Gan Shi Tang</a> for heat with cough and wheeze, or later-dynasty formulas like Yin Qiao San for early sore-throat colds.</p>
    <h2>The kitchen version</h2>
    <p>For the first hours of a mild chilly cold, the traditional home step is simple: fresh ginger and scallion whites simmered for a few minutes, drunk hot, then rest under a blanket until slightly damp with sweat. That is food, not medicine — anything more is a job for a practitioner.</p>
""" + HERB_SAFETY + """
    <aside class="doctor-note"><strong>See a doctor</strong> for trouble breathing, chest pain, confusion, a fever above 103°F (39.4°C) or lasting more than three days, or if you are elderly, pregnant or have heart or lung disease. Ask about antiviral treatment for flu early.</aside>""",
  faq=[("What is the best Chinese herb for a cold?", "There is no single best herb; Chinese medicine matches the formula to the type of cold. Fresh ginger is the classic kitchen herb for an early chilly cold."),
       ("Is Gui Zhi Tang good for colds?", "It is the classical formula for a mild cold with light sweating and aversion to wind, especially in someone run down. It is not for high fever or a hot, sore throat."),
       ("Can I take Chinese herbs with cold medicine?", "Ask a pharmacist first. Some formulas contain ephedra or licorice, which can interact with decongestants and blood-pressure drugs.")]),
 dict(slug="cough", kw="Cough",
  title="Chinese Herbs for Cough: Dry Cough, Phlegm & Lingering Post-Viral Cough | HerbBlueMap",
  desc="Chinese herbs and classic formulas for cough: dry irritating cough, cough with watery or yellow phlegm, and the cough that lingers for weeks after a cold. How Chinese medicine tells them apart and when to see a doctor.",
  body="""    <p class="lede">A cough is a symptom, and Chinese medicine treats coughs very differently depending on the phlegm: none, thin and watery, or thick and yellow. Here is the classical map, with the formulas practitioners reach for.</p>
    <h2>Thin, watery phlegm, worse with cold</h2>
    <p>Cold-fluid cough. Classic choices are <a href="/formulas/xiao-qing-long-tang/">Xiao Qing Long Tang</a> when chills are still present, and <a href="/formulas/ling-gan-jiang-wei-xin-xia-ren-tang/">Ling Gan Wu Wei Jiang Xin Xia Ren Tang</a> for the lingering cold-type cough. Key herbs: <a href="/bencao/banxia">ban xia</a>, <a href="/bencao/xixin">xi xin</a>, <a href="/bencao/wuweizi">wu wei zi</a>.</p>
    <h2>Thick, yellow phlegm, heat signs</h2>
    <p>Heat in the lung: <a href="/formulas/ma-xing-gan-shi-tang/">Ma Xing Gan Shi Tang</a> for cough and wheeze with heat; <a href="/formulas/qian-jin-wei-jing-tang/">Qian Jin Wei Jing Tang</a> for thick, foul phlegm.</p>
    <h2>Dry, tickly cough that lingers after a cold</h2>
    <p>The cough that hangs on for weeks with a dry throat. The classical formula is <a href="/formulas/mai-men-dong-tang/">Mai Men Dong Tang</a>, which moistens rather than dries.</p>
    <h2>Sore throat with cough</h2>
    <p>The two-herb <a href="/formulas/jie-geng-tang/">Jie Geng Tang</a> (platycodon and licorice) is the ancestor of many throat formulas.</p>
    <h2>Kitchen helpers</h2>
    <p>Pear steamed with a little rock sugar is the classic home remedy for a dry cough; fresh ginger tea for a chilly one. Honey soothes cough in adults and children over one year old (never give honey to babies under one).</p>
""" + HERB_SAFETY + """
    <aside class="doctor-note"><strong>See a doctor</strong> for a cough lasting more than three weeks, coughing blood, shortness of breath, chest pain, wheezing that is new, night sweats or weight loss.</aside>""",
  faq=[("What Chinese herb is good for a dry cough?", "Practitioners use moistening herbs; the classic formula for a lingering dry cough is Mai Men Dong Tang (ophiopogon decoction). Steamed pear is the home version."),
       ("What Chinese medicine is good for cough with phlegm?", "It depends on the phlegm: warming formulas such as Xiao Qing Long Tang for thin, watery phlegm; cooling formulas such as Ma Xing Gan Shi Tang for thick, yellow phlegm."),
       ("How long should a cough last before seeing a doctor?", "If it lasts more than three weeks, or comes with blood, breathlessness or chest pain, see a doctor.")]),
 dict(slug="constipation", kw="Constipation",
  title="Chinese Herbs for Constipation: Gentle vs Strong Formulas Explained | HerbBlueMap",
  desc="Chinese herbs for constipation: why Chinese medicine separates dry-heat constipation from the dry, weak constipation of older adults, the classic formulas (Ma Zi Ren Wan, the Cheng Qi Tang family), and the risks of strong purgatives.",
  body="""    <p class="lede">Chinese medicine splits constipation into two very different problems: a hot, full blockage that needs clearing, and a dry, weak bowel that needs moistening. Using a strong purgative for the second kind is a classic mistake.</p>
    <h2>Dry, weak constipation (older adults, after surgery, chronic)</h2>
    <p>The gentle classic is <a href="/formulas/ma-zi-ren-wan/">Ma Zi Ren Wan</a> (hemp seed pill), built around oily seeds that moisten the bowel, with a small dose of rhubarb. It is one of the most widely sold Chinese patent formulas in the US.</p>
    <h2>Hot, full constipation (dry stool, bloating, bad breath)</h2>
    <p>The "Order the Qi" family, from mild to strong: <a href="/formulas/tiao-wei-cheng-qi-tang/">Tiao Wei Cheng Qi Tang</a>, <a href="/formulas/xiao-cheng-qi-tang/">Xiao Cheng Qi Tang</a> and <a href="/formulas/da-cheng-qi-tang/">Da Cheng Qi Tang</a>. Their engine is <a href="/bencao/dahuang">da huang (rhubarb root)</a> with <a href="/bencao/mangxiao">mang xiao</a>, <a href="/bencao/zhishi">zhi shi</a> and <a href="/bencao/houpo">hou po</a>. These are strong purgatives for short-term use under a practitioner — not for daily use, not in pregnancy.</p>
    <h2>When someone is both blocked and exhausted</h2>
    <p>For the patient who needs a purge but is too weak to bear one, later doctors added ginseng and angelica: <a href="/formulas/huang-long-tang/">Huang Long Tang</a>.</p>
    <h2>Before any herb</h2>
    <p>Water, fiber, movement and a regular morning time on the toilet fix most constipation. Our <a href="/body-relief/">Pain Point Finder</a> also lists acupressure points traditionally used for sluggish bowels (such as ST25 beside the navel).</p>
""" + HERB_SAFETY + """
    <aside class="doctor-note"><strong>See a doctor</strong> for blood in the stool, black stools, a sudden change in bowel habits after age 45, weight loss, severe abdominal pain, vomiting, or no bowel movement with a swollen belly — that can be an obstruction and is an emergency.</aside>""",
  faq=[("What is the best Chinese herb for constipation?", "For chronic, dry constipation the classic is Ma Zi Ren Wan (hemp seed pill). Rhubarb-based formulas are much stronger and meant for short-term use."),
       ("Is rhubarb root safe for constipation?", "Short-term, under guidance. Long-term use of anthraquinone laxatives like rhubarb can make the bowel dependent; avoid in pregnancy."),
       ("Can Chinese medicine cure chronic constipation?", "It can help, especially combined with diet and habits, but persistent constipation should be checked by a doctor first.")]),
 dict(slug="anxiety-and-insomnia", kw="Anxiety and Insomnia",
  title="Chinese Herbs for Anxiety & Insomnia: Classic Formulas, Safety & Interactions | HerbBlueMap",
  desc="Chinese herbs used for anxiety, stress and insomnia: how Chinese medicine reads restlessness and poor sleep, classic formulas such as Suan Zao Ren Tang and Gan Mai Da Zao Tang, and important interactions with antidepressants and sleep medication.",
  body="""    <p class="lede">In Chinese medicine, anxiety and insomnia are usually read together: a mind that cannot settle by day will not settle by night. The classical texts describe several distinct patterns, and the herbs follow the pattern rather than the diagnosis.</p>
    <h2>Restless, can't fall asleep, tired but wired</h2>
    <p>Often read as blood and yin not nourishing the heart. The best-known formula is Suan Zao Ren Tang (sour jujube seed decoction), from the Jin Gui Yao Lue, built around sour jujube seed with <a href="/bencao/fuling">poria</a>, <a href="/bencao/zhimu">zhi mu</a>, <a href="/bencao/chuanxiong">chuan xiong</a> and licorice.</p>
    <h2>Weepy, sighing, emotionally fragile</h2>
    <p>The tiny three-ingredient Gan Mai Da Zao Tang — licorice, wheat and <a href="/bencao/dazao">jujube</a> — written for "restless organ" emotional distress. It is food-grade, which is part of why it is still popular.</p>
    <h2>Palpitations and a racing heart</h2>
    <p>The Shang Han Lun treats palpitations after over-sweating with <a href="/formulas/gui-zhi-gan-cao-tang/">Gui Zhi Gan Cao Tang</a>, and a knotted, irregular pulse with <a href="/formulas/zhi-gan-cao-tang/">Zhi Gan Cao Tang</a>. Palpitations always need a medical check first.</p>
    <h2>Stress, irritability, tight chest</h2>
    <p>Classically "liver qi constraint", treated with <a href="/bencao/chaihu">chai hu (bupleurum)</a>-based formulas. <a href="/bencao/wuweizi">Schisandra</a> is the traditional calming tonic.</p>
    <h2>Pair with acupuncture</h2>
    <p>Many people combine herbs with <a href="/acupuncture/for/anxiety/">acupuncture for anxiety</a>, which has gentle, well-tolerated effects on the stress response.</p>
""" + HERB_SAFETY + """
    <aside class="doctor-note"><strong>Important:</strong> herbs can add to or interfere with antidepressants, anti-anxiety drugs and sleep medication — never stop or combine them without your prescriber. If you have thoughts of harming yourself, call or text 988 (Suicide &amp; Crisis Lifeline, US) now.</aside>""",
  faq=[("What is the best Chinese herb for sleep?", "Sour jujube seed (suan zao ren) is the classic sleep herb, usually given in the formula Suan Zao Ren Tang. Choice depends on the pattern, so see a practitioner."),
       ("Are Chinese herbs for anxiety safe with SSRIs?", "Some herbs interact with psychiatric medications. Always check with your prescriber and a qualified practitioner before combining them."),
       ("Can Chinese medicine help insomnia?", "Many people report better sleep with herbs and acupuncture, and some studies are encouraging, but evidence is mixed. Good sleep habits come first.")]),
]

THERAPIES = [
 dict(path="/cupping/", h1="Cupping Therapy: Benefits, Side Effects, Marks and What to Expect",
  title="Cupping Therapy: Benefits, Side Effects, Marks & Cost (Plain-English Guide) | HerbBlueMap",
  desc="What is cupping therapy? How it works, what the round marks mean, benefits and evidence, side effects, who should avoid it, cost, and how to find a licensed practitioner for cupping.",
  body="""    <p class="lede">Cupping uses glass, plastic or silicone cups to create suction on the skin, lifting the tissue underneath. It is one of the oldest therapies in Chinese medicine and became famous worldwide when Olympic swimmers showed up with round purple marks in 2016.</p>
    <h2>How cupping works</h2>
    <p>Suction pulls skin and muscle upward, increasing local blood flow and stretching tight fascia. Practitioners leave cups in place for 5–15 minutes or slide them along oiled skin. In classical terms, it moves stuck qi and blood.</p>
    <h2>What do the marks mean?</h2>
    <p>The round marks are small broken capillaries under the skin, not ordinary bruises from injury. They are usually painless and fade in 3–10 days. Practitioners read darker marks as more stagnation; science has not confirmed that reading.</p>
    <h2>Benefits and evidence</h2>
    <p>Studies suggest cupping may reduce neck and back pain and muscle tension in the short term, though many trials are small. It is best seen as a hands-on therapy for tight, sore muscles, often added to an <a href="/acupuncture/">acupuncture</a> session.</p>
    <h2>Side effects and who should avoid it</h2>
    <p>Expect marks and mild soreness. Avoid cupping on broken or inflamed skin, varicose veins, or over the belly and lower back in pregnancy, and talk to your doctor if you take blood thinners or have a bleeding disorder. Fire cupping should only be done by trained practitioners because of burn risk.</p>
    <h2>Cost</h2>
    <p>Cupping is often added to an acupuncture visit for a small extra fee or offered as a standalone session. See <a href="/acupuncture/cost/">acupuncture cost</a> for typical US prices.</p>
    <p><a class="btn" href="/find/">Find a verified practitioner in New York →</a></p>""",
  faq=[("Does cupping hurt?", "Usually not. It feels like a strong pulling or deep massage. Sliding cupping can feel intense over very tight muscles."),
       ("How long do cupping marks last?", "Typically 3 to 10 days, depending on the person and how strong the suction was."),
       ("Is cupping safe?", "Generally yes with a trained practitioner. Avoid it on damaged skin, and check with your doctor if you take blood thinners or are pregnant.")]),
 dict(path="/gua-sha/", h1="Gua Sha: The Real Body Technique Behind the Face Tool",
  title="Gua Sha: Benefits, Body vs Face, How to Do It & Side Effects | HerbBlueMap",
  desc="What is gua sha? The traditional Chinese scraping technique for the body, how it differs from the face-roller trend, benefits and evidence, the red 'sha' marks, safety, and how to do gentle gua sha at home.",
  body="""    <p class="lede">Gua sha means "scraping sha": a smooth-edged tool is stroked firmly over oiled skin until faint red speckles (the "sha") appear. Long before it became a jade face tool on social media, it was a folk and clinical remedy for neck and back stiffness, fever and heatstroke.</p>
    <h2>Body gua sha vs face gua sha</h2>
    <p><strong>Body gua sha</strong> is firm, done on the back, neck, shoulders and limbs, and is meant to bring up sha. <strong>Face gua sha</strong> is very light, never meant to mark the skin, and works more like lymphatic massage — it may reduce puffiness for a few hours.</p>
    <h2>Benefits and evidence</h2>
    <p>Small studies report less neck and back pain and better range of motion after gua sha, and increased local blood flow in the treated area. Evidence is limited but the technique is low-risk when done properly.</p>
    <h2>Side effects and safety</h2>
    <p>Body gua sha leaves red-purple petechiae that fade in 2–4 days and can feel tender. Skip it over broken skin, rashes, varicose veins or recent injuries, and check with your doctor if you take blood thinners.</p>
    <h2>Gentle gua sha at home (neck and shoulders)</h2>
    <p>Apply oil, hold the tool at a low angle, and stroke downward from the base of the skull toward the shoulder, 10–15 strokes per line. Stop if it is painful. Pair it with the self-massage points in our <a href="/body-relief/">Pain Point Finder</a>.</p>
    <p><a class="btn" href="/find/">Find a verified practitioner in New York →</a></p>""",
  faq=[("Does gua sha really work?", "Small studies suggest it can ease neck and back pain and stiffness. Face gua sha may reduce puffiness briefly; claims of permanent face-lifting are not supported."),
       ("Is gua sha supposed to bruise?", "Body gua sha is meant to bring up red speckles (sha) that fade in a few days. Face gua sha should never mark the skin."),
       ("How often can I do gua sha?", "Body gua sha: wait until the marks fade, usually several days. Gentle face gua sha can be done daily.")]),
 dict(path="/moxibustion/", h1="Moxibustion: What It Is, Benefits, Breech Babies and Safety",
  title="Moxibustion: Benefits, Breech Baby Use, How It Works & Safety | HerbBlueMap",
  desc="What is moxibustion? How burning mugwort (moxa) near acupuncture points is used for cold-type pain, digestion and breech babies, what the research says, and how to use moxa safely.",
  body="""    <p class="lede">Moxibustion warms acupuncture points by burning moxa — dried, aged mugwort (ai ye) — close to the skin. In Chinese medicine it is the treatment of choice when a problem is cold, weak or chronic, and it is the second half of the Chinese word for acupuncture itself: zhen jiu, "needle and moxa".</p>
    <h2>How it is done</h2>
    <p>Most common in the US is indirect moxa: a cigar-shaped moxa stick is held an inch above the skin until the area feels pleasantly warm, or moxa is burned on top of an acupuncture needle or on a slice of ginger. Smokeless and stick-on moxa patches exist for home use.</p>
    <h2>What it is used for</h2>
    <p>Cold-type joint and back pain, menstrual cramps that improve with warmth, digestive weakness with loose stools, and fatigue. A classic home point is ST36 below the knee.</p>
    <h2>Moxibustion for breech babies</h2>
    <p>Warming the point BL67 at the outer corner of the little toenail, usually around weeks 33–35, is a traditional way to encourage a breech baby to turn. Reviews of the trials suggest it may reduce the number of babies still breech at birth, but the evidence is low-quality. Only do this with your obstetrician or midwife's agreement.</p>
    <h2>Safety</h2>
    <p>Burns are the main risk: keep the stick moving, keep it an inch away, and never use moxa on numb skin (for example with diabetic neuropathy) or on the face. Moxa smoke is strong; ventilate the room and avoid it with asthma.</p>
    <p><a class="btn" href="/find/">Find a verified practitioner in New York →</a></p>""",
  faq=[("What is moxibustion good for?", "Traditionally for cold-type, chronic problems: joint and back pain that improves with heat, menstrual cramps, weak digestion, and turning breech babies."),
       ("Does moxibustion work for breech babies?", "Trials suggest it may help, but the evidence is low-quality. Use it only with your obstetrician's or midwife's agreement, usually around weeks 33–35."),
       ("Is moxibustion safe at home?", "Indirect moxa with care is generally safe. Avoid burns, never use it on numb skin, and ventilate the room.")]),
]


def build():
    for c in HERBS_FOR:
        render(f"/chinese-herbs-for/{c['slug']}/", c["title"], c["desc"], f"Chinese Herbs for {c['kw']}: What Chinese Medicine Uses and Why",
               [("Chinese Medicine", "/traditional-chinese-medicine/"), (f"Herbs for {c['kw']}", f"/chinese-herbs-for/{c['slug']}/")],
               c["body"] + "\n" + more(STD_MORE), c["faq"])
    for t in THERAPIES:
        render(t["path"], t["title"], t["desc"], t["h1"],
               [("Chinese Medicine", "/traditional-chinese-medicine/"), (t["h1"].split(":")[0], t["path"])],
               t["body"] + "\n" + more([("/acupuncture/", "Acupuncture, explained", "What it helps, cost, insurance."),
                                        ("/traditional-chinese-medicine/", "Traditional Chinese medicine", "The five branches."),
                                        ("/acupuncture/does-acupuncture-work/", "Does acupuncture work?", "Honest answers.")]),
               t["faq"])


if __name__ == "__main__":
    build()
    print("built", len(HERBS_FOR) + len(THERAPIES), "pages")
