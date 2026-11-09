"""Build every Carewise page (index.html + 10 inner pages).

Usage:  python tools/build-site.py
All copy lives in this file; layout classes come from assets/css/site.css and
behaviour from assets/js/site.js. Re-run after editing.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
import time
V = str(int(time.time()))  # cache-busting stamp for css/js links

PHONE = "+91 96062 68777"
TEL = "tel:+919606268777"
WA = "https://wa.me/919606268777"
EMAIL = "support@carewise.in"
YEAR = "2026"

IMG = {
    "hero": ("assets/img/hero-family-nurse.png", "Elderly father smiling with his daughter and a Carewise nurse"),
    "room": ("assets/img/centre-private-room.png", "Private room at Carewise Centre"),
    "room2": ("assets/img/centre-private-room-2.png", "Private room with attendant bed at Carewise Centre"),
    "home": ("assets/img/home-care-nurse-visit.png", "Nurse visiting an elderly man at home"),
    "family": ("assets/img/elderly-couple-family.png", "Elderly couple with their adult children"),
}

NAV = [
    ("Care Programs", [
        ("centre", "Carewise Centre", "24/7 care in private & general rooms"),
        ("home-care", "Home Healthcare", "Nurses, doctors & therapy at home"),
        ("services", "Our Services", "Everything we treat and offer"),
    ]),
    ("Experience", [
        ("about", "About Us", "Our story and values"),
        ("team", "Our Team", "Doctor-led, verified staff"),
        ("gallery", "Facility Gallery", "Inside the centre"),
        ("videos", "Videos & Stories", "Hear from families"),
    ]),
]


def ico(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<i data-lucide="{name}"{c}></i>'


def img(key, cls="", loading="lazy"):
    src, alt = IMG[key]
    c = f' class="{cls}"' if cls else ""
    return f'<img src="{src}" alt="{alt}"{c} loading="{loading}" />'


# ------------------------------------------------------------------ chrome --
def head(title, desc):
    return f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title}</title>
    <meta name="description" content="{desc}" />
    <meta name="theme-color" content="#fbf7f0" />
    <link rel="preload" href="assets/fonts/fraunces.woff2" as="font" type="font/woff2" crossorigin />
    <link rel="preload" href="assets/fonts/dm-sans.woff2" as="font" type="font/woff2" crossorigin />
    <link rel="stylesheet" href="assets/css/site.css?v={V}" />
    <link rel="stylesheet" href="assets/css/motion.css?v={V}" />
    <script>document.documentElement.classList.add("js");</script>
  </head>
  <body>'''


def brand(href="index.html", white=False):
    src = "assets/img/logo-white.png" if white else "assets/img/logo.png"
    return f'''<a class="brand" href="{href}" aria-label="Carewise home">
          <img src="{src}" alt="Carewise" width="916" height="420" />
        </a>'''


def header(slug):
    def cur(s):
        return ' aria-current="page"' if s == slug else ""

    nav_items = ""
    for label, links in NAV:
        menu = "".join(f'<li><a href="{s}.html"{cur(s)}>{t}<small>{d}</small></a></li>' for s, t, d in links)
        nav_items += f'''
            <li>
              <button type="button" aria-haspopup="true">{label} {ico("chevron-down")}</button>
              <ul class="menu">{menu}</ul>
            </li>'''
    nav_items += f'<li><a href="contact.html"{cur("contact")}>Contact</a></li>'

    drawer = ""
    for label, links in NAV:
        drawer += f'<div class="drawer-group"><h4>{label}</h4>' + "".join(
            f'<a href="{s}.html"{cur(s)}>{t}</a>' for s, t, _ in links) + "</div>"
    drawer += f'<div class="drawer-group"><h4>Get in touch</h4><a href="contact.html"{cur("contact")}>Contact</a></div>'
    drawer += f'<a class="btn btn-primary btn-lg" href="{TEL}">{ico("phone")} Call {PHONE}</a>'

    return f'''
    <div class="topbar">
      <div class="wrap">
        <span class="topbar-note" data-type='["Mysuru&#39;s first palliative care centre","Trusted by families for 6+ years","Doctor-guided care, 24 hours a day","Care at our centre or in your home"]'><span class="type-text">Mysuru's first palliative care centre · Trusted by families for 6+ years</span><span class="type-caret" aria-hidden="true"></span></span>
        <a href="{TEL}">{ico("phone")} {PHONE}</a>
      </div>
    </div>
    <header class="header">
      <div class="wrap">
        {brand()}
        <nav aria-label="Main">
          <ul class="nav">{nav_items}
          </ul>
        </nav>
        <a class="btn btn-dark header-cta" href="contact.html">Talk to our team</a>
        <button class="nav-toggle" type="button" aria-label="Menu" aria-expanded="false" aria-controls="drawer">
          {ico("menu", "icon-menu")}{ico("x", "icon-close")}
        </button>
      </div>
    </header>
    <div class="drawer" id="drawer">{drawer}</div>
    <main>'''


def footer():
    return f'''
    </main>
    <footer class="footer">
      <div class="wrap">
        <div class="footer-grid">
          <div>
            {brand(white=True)}
            <p>Mysuru's first palliative care centre. Doctor-guided, dignified care for your parents, at our centre or in their home.</p>
            <div class="social">
              <a href="https://www.instagram.com/care_wise_/" aria-label="Instagram"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg></a>
              <a href="https://linkedin.com/company/carewise" aria-label="LinkedIn"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z"/></svg></a>
              <a href="{WA}" aria-label="WhatsApp">{ico("message-circle")}</a>
            </div>
          </div>
          <div>
            <h4>Care</h4>
            <ul>
              <li><a href="centre.html">Carewise Centre</a></li>
              <li><a href="home-care.html">Home Healthcare</a></li>
              <li><a href="services.html">Our Services</a></li>
              <li><a href="services.html#conditions">Conditions We Treat</a></li>
            </ul>
          </div>
          <div>
            <h4>Company</h4>
            <ul>
              <li><a href="about.html">About Us</a></li>
              <li><a href="team.html">Our Team</a></li>
              <li><a href="gallery.html">Gallery</a></li>
              <li><a href="videos.html">Videos &amp; Stories</a></li>
              <li><a href="contact.html">Contact</a></li>
            </ul>
          </div>
          <div>
            <h4>Reach us</h4>
            <ul class="footer-contact">
              <li>{ico("phone")}<a href="{TEL}">{PHONE}</a></li>
              <li>{ico("mail")}<a href="mailto:{EMAIL}">{EMAIL}</a></li>
              <li>{ico("map-pin")}<span>Carewise Healthcare, Mysuru, Karnataka, India</span></li>
              <li>{ico("clock")}<span>Centre open 24/7 · Enquiries 8am–9pm</span></li>
            </ul>
          </div>
        </div>
        <div class="footer-bottom">
          <p>© {YEAR} Carewise Healthcare. All rights reserved.</p>
          <nav aria-label="Legal">
            <a href="privacy-policy.html">Privacy Policy</a>
            <a href="terms-of-service.html">Terms of Service</a>
          </nav>
        </div>
      </div>
    </footer>
    <div class="sticky-bar">
      <a class="btn btn-dark" href="{TEL}" aria-label="Call {PHONE}">{ico("phone")}<span>Call {PHONE}</span></a>
      <a class="btn btn-wa" href="{WA}" aria-label="Chat on WhatsApp">{ico("message-circle")}<span>Chat on WhatsApp</span></a>
    </div>
    <script src="assets/js/lucide.min.js?v={V}"></script>
    <script src="assets/js/site.js?v={V}"></script>
    <script src="assets/js/motion.js?v={V}"></script>
  </body>
</html>
'''


# --------------------------------------------------------------- snippets --
def section(inner, cls="", id_=""):
    i = f' id="{id_}"' if id_ else ""
    return f'\n      <section class="section {cls}"{i}>\n        <div class="wrap">{inner}\n        </div>\n      </section>'


def section_head(eyebrow, title, lead=None, center=True):
    c = " center" if center else ""
    l = f'<p class="lead measure">{lead}</p>' if lead else ""
    return f'''
          <div class="section-head{c} reveal">
            <span class="eyebrow">{eyebrow}</span>
            <h2 class="measure">{title}</h2>
            {l}
          </div>'''


def icon_cards(items, cols="grid-3", show=None):
    """show=N renders only N cards open; the rest sit behind a View more button."""
    extra = f' data-collapsible="{show}"' if show else ""
    html = f'<div class="grid {cols}"{extra}>' + "".join(f'''
            <article class="card reveal">
              <span class="ico-ring">{ico(i)}</span>
              <h3>{t}</h3>
              <p>{d}</p>
            </article>''' for i, t, d in items) + "</div>"
    if show:
        html += f'''
          <div class="center" style="margin-top:2rem">
            <button class="btn btn-outline view-more" type="button" aria-expanded="false" data-more="View more conditions" data-less="View less">View more conditions {ico("chevron-down")}</button>
          </div>'''
    return html


def check_list(items, cls="check-list"):
    return f'<ul class="{cls}">' + "".join(f'<li>{ico("check")}<span>{b}</span></li>' for b in items) + "</ul>"


def steps(items):
    return '<div class="steps">' + "".join(f'''
            <article class="step reveal"><h3>{t}</h3><p>{d}</p></article>''' for t, d in items) + "</div>"


def faq(items):
    return '<div class="faq reveal">' + "".join(f'''
            <details><summary>{q}{ico("plus")}</summary><p>{a}</p></details>''' for q, a in items) + "</div>"


def stats(dark=False):
    data = [("6+", "Years caring for Mysuru families"), ("1st", "Palliative care centre in Mysuru"),
            ("24/7", "Doctor-guided supervision"), ("100%", "Background-verified staff")]
    inner = '<div class="stats">' + "".join(f'<div class="stat reveal"><b>{n}</b><span>{l}</span></div>' for n, l in data) + "</div>"
    return section(inner, "bg-ink" if dark else "")


TESTIMONIALS = [
    ("RM", "Son · Bengaluru", "Carewise gave my father the dignity and medical care he needed when we couldn't manage at home. The staff treated him like family."),
    ("PS", "Daughter · London", "Living abroad, I was constantly worried about my mother's post-stroke recovery. The daily updates kept me connected and at peace."),
    ("AK", "Son · Mysuru", "The palliative care team didn't just manage the pain. They brought a sense of calm to our entire family during a difficult time."),
]


def testimonials():
    cards = "".join(f'''
            <figure class="quote-card">
              <div class="mark">&ldquo;</div>
              <p>{q}</p>
              <footer><span>{i}</span><span>{w}</span></footer>
            </figure>''' for i, w, q in TESTIMONIALS)
    return f'''
          <div class="marquee marquee--slow reveal" aria-label="Family stories">
            <div class="marquee-track">{cards}{cards}</div>
          </div>'''


def cta(title="Ready to talk about your parent's care?",
        lead="Our care coordinators are available every day. Call, WhatsApp or book a visit to the centre."):
    return section(f'''
          <div class="cta reveal">
            <div><h2>{title}</h2><p>{lead}</p></div>
            <div class="cta-actions">
              <a class="btn btn-primary btn-lg" href="{TEL}">{ico("phone")} Call {PHONE}</a>
              <a class="btn btn-ghost-light btn-lg" href="{WA}">{ico("message-circle")} WhatsApp</a>
            </div>
          </div>''')


def page_hero(eyebrow, title, lead, image=None):
    media = f'<div class="reveal">{img(image, loading="eager")}</div>' if image else ""
    return f'''
      <section class="page-hero">
        <div class="wrap">
          <div class="reveal">
            <span class="eyebrow">{eyebrow}</span>
            <h1>{title}</h1>
            <p class="lead">{lead}</p>
          </div>
          {media}
        </div>
      </section>'''


def split(image, eyebrow, title, paras, bullets=None, flip=False, cta_link=None):
    b = check_list(bullets) if bullets else ""
    link = f'<p style="margin-top:1.75rem"><a class="text-link" href="{cta_link[0]}">{cta_link[1]} {ico("arrow-right")}</a></p>' if cta_link else ""
    return f'''
          <div class="split{" split--flip" if flip else ""}">
            <div class="reveal">{img(image)}</div>
            <div class="reveal">
              <span class="eyebrow">{eyebrow}</span>
              <h2>{title}</h2>
              <div class="lead stack">{"".join(f"<p>{p}</p>" for p in paras)}</div>
              {b}{link}
            </div>
          </div>'''


# ---------------------------------------------------------------- content --
CONDITIONS = [
    ("heart-pulse", "Palliative &amp; end-of-life care", "Comfort-focused care for serious illness, with pain and symptom relief led by doctors."),
    ("user-round", "Elderly nursing care", "Help with daily living and medical needs, delivered with patience and respect."),
    ("brain", "Stroke &amp; neuro rehabilitation", "Intensive physiotherapy and occupational therapy to regain independence."),
    ("stethoscope", "Post-surgical care", "Monitoring, medication and wound management in the weeks after surgery."),
    ("bandage", "Wound care &amp; dressing", "Expert management of chronic ulcers, bedsores and surgical wounds."),
    ("wind", "Ventilator / BiPAP / CPAP", "Advanced respiratory support with trained staff round the clock."),
    ("ribbon", "Cancer &amp; oncology support", "Pain management, nutrition and emotional support through treatment."),
    ("puzzle", "Dementia &amp; Alzheimer's care", "A safe, structured environment that supports cognitive health and calm."),
    ("calendar-clock", "Long-term medical care", "Ongoing support for diabetes, heart, kidney and other chronic conditions."),
]

HOME_SERVICES = [
    ("user-plus", "Doctor visits at home", "Consultations in the comfort of your home."),
    ("heart", "Nursing care at home", "Injections, IV lines, catheter care and daily medical needs."),
    ("users", "Caretaker support", "Trained attendants for bathing, feeding, mobility and company."),
    ("accessibility", "Physiotherapy at home", "Recovery after stroke, surgery or falls."),
    ("apple", "Nutritionist services", "Diet plans for diabetes, heart health and recovery."),
    ("monitor", "Remote monitoring", "Vitals tracked and reviewed regularly by a doctor."),
    ("flask-conical", "Lab tests at home", "Sample collection at your door, reports shared digitally."),
    ("clipboard-check", "Post-operative care", "Wound care and medication management after surgery."),
    ("activity", "Chronic condition care", "A plan and regular reviews for long-term illnesses."),
]

INSTAGRAM_HANDLE = "care_wise_"
INSTAGRAM_URL = f"https://www.instagram.com/{INSTAGRAM_HANDLE}/"
# Post shortcodes shown in the Instagram strip (newest first). Update to refresh the feed.
INSTAGRAM_POSTS = ["CNmEuzLrTh0", "CNOkXDWrLIW", "CMWU74XLWYZ", "CMRGBtfrEkU",
                   "CL6tSC2LFdu", "CL4Yj8ArRl1", "CLWenmlLXsk", "CLSIp7rLh_K"]


def instagram_section():
    cards = "".join(f'''
            <li class="ig-card">
              <iframe src="https://www.instagram.com/p/{code}/embed/" title="Instagram post by @{INSTAGRAM_HANDLE}" loading="lazy" allowtransparency="true" scrolling="no" frameborder="0"></iframe>
            </li>''' for code in INSTAGRAM_POSTS)
    head = f'''
          <div class="ig-head reveal">
            <div>
              <span class="eyebrow">Follow our journey</span>
              <h2>Moments from <span class="serif-italic">@{INSTAGRAM_HANDLE}</span></h2>
              <p class="lead">Everyday life at the Carewise Centre and the families we care for, straight from our Instagram.</p>
            </div>
            <div class="ig-tools">
              <button class="ig-arrow" type="button" data-dir="-1" aria-label="Previous posts">{ico("arrow-left")}</button>
              <button class="ig-arrow" type="button" data-dir="1" aria-label="Next posts">{ico("arrow-right")}</button>
              <a class="btn btn-dark" href="{INSTAGRAM_URL}" target="_blank" rel="noopener">{ico("instagram") if False else '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>'} Follow on Instagram</a>
            </div>
          </div>
          <ul class="ig-row reveal" data-ig>{cards}
          </ul>'''
    return section(head, "", "instagram")


ROOMS = f'''
          <div class="grid grid-2">
            <article class="room reveal">
              <h3>General Ward</h3>
              <p class="muted">Professional care in a calm shared setting.</p>
              <ul>{"".join(f"<li>{ico('check')}<span>{b}</span></li>" for b in ["Semi-private medical bay with nursing station access", "Standard medical monitoring", "Nutritious plated meals", "Daily doctor rounds", "Shared, clean bathroom facilities"])}</ul>
              <a class="btn btn-outline" href="contact.html">Enquire for General</a>
            </article>
            <article class="room room--featured reveal">
              <span class="pill">Most preferred</span>
              <h3>Private Room</h3>
              <p>Maximum privacy and a personalised space for family.</p>
              <ul>{"".join(f"<li>{ico('check')}<span>{b}</span></li>" for b in ["Individual spacious room", "Dedicated attendant bed", "Private ensuite bathroom", "Personalised nutrition plan", "Priority nursing response", "Flexible visiting hours"])}</ul>
              <a class="btn btn-primary" href="contact.html">Enquire for Private</a>
            </article>
          </div>'''


def home_page():
    hero = f'''
      <section class="hero hero--bg">
        <div class="hero-bg">
          {img("hero", loading="eager")}
          <div class="hero-shade"></div>
        </div>
        <div class="wrap">
          <div class="hero-copy reveal in">
            <span class="eyebrow">Mysuru's first palliative care centre</span>
            <h1>Better care for your parents, <span class="serif-italic">wherever they need it.</span></h1>
            <p class="lead">From specialised care at our centre to professional healthcare at home, Carewise supports your parents through recovery, rehabilitation and every stage where they need extra care.</p>
            <div class="hero-actions">
              <a class="btn btn-primary btn-lg" href="contact.html">{ico("phone-call")} Talk to our team</a>
              <a class="btn btn-ghost-light btn-lg" href="services.html">Explore our care {ico("arrow-right")}</a>
            </div>
            <div class="hero-proof">
              <div class="avatars"><span>RM</span><span>PS</span><span>AK</span></div>
              <span>Trusted by families in Mysuru, Bengaluru and abroad for over six years.</span>
            </div>
          </div>
          <div class="hero-badge reveal in">
            <span class="ico">{ico("shield-check")}</span>
            <div><strong>Doctor-guided, 24/7</strong><small>Verified staff · Daily family updates</small></div>
          </div>
        </div>
      </section>
      <div class="trust">
        <div class="wrap">
          <div class="trust-item">{ico("stethoscope")} Doctor-guided protocols</div>
          <div class="trust-item">{ico("badge-check")} Verified &amp; trained staff</div>
          <div class="trust-item">{ico("message-square-heart")} Transparent daily updates</div>
          <div class="trust-item">{ico("home")} Centre or home, your choice</div>
        </div>
      </div>'''

    pathways = section(section_head("Two pathways", "Care where it suits your family best",
                                    "Choose the environment that fits your parent's condition today. Moving between the two is always possible.") + f'''
          <div class="grid grid-2">
            <article class="pathway reveal">
              {img("room")}
              <div class="pathway-body">
                <span class="tag">At the centre</span>
                <h3>Care at Carewise Centre</h3>
                <p>A specialised facility with 24/7 medical supervision, private rooms and a calm, healing environment.</p>
                <ul>{"".join(f"<li>{ico('check')}<span>{b}</span></li>" for b in ["Palliative and long-term medical care", "Rehabilitation after stroke or surgery", "Ventilator and respiratory support"])}</ul>
                <a class="btn btn-dark" href="centre.html">Explore the centre {ico("arrow-right")}</a>
              </div>
            </article>
            <article class="pathway reveal">
              {img("home")}
              <div class="pathway-body">
                <span class="tag">At home</span>
                <h3>Care at Home</h3>
                <p>Nurses, doctors, physiotherapists and caretakers who come to you, on a schedule that fits.</p>
                <ul>{"".join(f"<li>{ico('check')}<span>{b}</span></li>" for b in ["Single visits to round-the-clock care", "Doctor visits, nursing and physiotherapy", "Lab tests and remote monitoring"])}</ul>
                <a class="btn btn-dark" href="home-care.html">Explore home care {ico("arrow-right")}</a>
              </div>
            </article>
          </div>''')

    quote = f'''
      <section class="section quote-band bg-teal">
        <div class="wrap">
          <div class="reveal">{img("family")}</div>
          <blockquote class="reveal">
            <p>&ldquo;Not just treating their condition. <em>Celebrating their existence.</em>&rdquo;</p>
            <cite>Our philosophy centres on dignity, comfort and the joy of living, for every person in our care.</cite>
          </blockquote>
        </div>
      </section>'''

    conditions = section(section_head("Conditions we treat", "Comprehensive support for chronic and acute conditions") + icon_cards(CONDITIONS, cols="grid-4", show=4)
                         + f'<p class="center" style="margin-top:1.5rem"><a class="text-link" href="services.html">See all services {ico("arrow-right")}</a></p>', "bg-sand")

    cards = "".join(f'''
            <article class="card"><span class="ico-ring">{ico(i)}</span><h3>{t}</h3><p>{d}</p></article>''' for i, t, d in HOME_SERVICES)
    instagram = instagram_section()

    home_row = section(section_head("Inside home healthcare", "Personalised senior care at your doorstep", center=False) + f'''
          <div class="marquee reveal" aria-label="Home healthcare services">
            <div class="marquee-track">{cards}{cards}</div>
          </div>
          <p style="margin-top:2rem"><a class="text-link" href="home-care.html">All home healthcare services {ico("arrow-right")}</a></p>''')

    rooms = section(section_head("Your comfort is our priority", "Rooms designed for healing and peace") + ROOMS, "bg-sand")

    stories = section(section_head("Stories", "Heartfelt stories from our families") + testimonials())

    questions = section(section_head("Questions", "What families usually ask us") + faq([
        ("How do I know which option is right for my parent?", "Call us and describe the situation. A doctor or senior nurse assesses your parent, at home or at the centre, and recommends the right pathway. You can always move between the two."),
        ("Can I get updates if I live in another city or abroad?", "Yes. Every family receives daily updates from the care team, and you can reach your coordinator at any time."),
        ("Are your staff verified?", "Every nurse, caretaker and therapist is identity and background verified and trained in elderly and palliative care before joining."),
        ("How quickly can care start?", "Home care usually begins within 24 to 48 hours of assessment. Admission to the centre can often be arranged the same day."),
    ]), "bg-sand")

    return hero + pathways + quote + conditions + instagram + home_row + rooms + stats(dark=True) + stories + questions + cta()


def about_page():
    body = page_hero("Our story", "Care that treats people, <span class='serif-italic'>not just conditions.</span>",
                     "Carewise was founded to give Mysuru's families a place where ageing parents receive medical excellence and genuine warmth, at our centre or at home.", "family")
    body += section(split("room", "Who we are", "Mysuru's first dedicated palliative care centre",
                          ["Six years ago we opened our doors with a simple belief: nobody should face illness or old age without comfort, dignity and expert medical support close at hand.",
                           "Today Carewise runs a fully equipped care centre in Mysuru and a home healthcare service trusted by families in Mysuru, Bengaluru and abroad."],
                          ["Doctor-guided protocols for every patient", "Verified, trained and compassionate staff", "Transparent daily updates to the family", "Care plans built around the person, not the diagnosis"]))
    body += section(section_head("Our values", "What guides every decision we make") + icon_cards([
        ("heart-handshake", "Dignity first", "We protect the independence, privacy and preferences of every person in our care."),
        ("shield-check", "Medical excellence", "Experienced doctors set the protocols; trained nurses and therapists follow them precisely."),
        ("message-square-heart", "Honest communication", "Families receive daily updates and straight answers, wherever in the world they live."),
        ("home", "Home-like comfort", "Clean, calm spaces, nutritious food and familiar routines help healing."),
        ("users", "Family partnership", "You stay part of every decision; we simply make it easier to carry."),
        ("sparkles", "Celebrating life", "Not just treating their condition. Celebrating their existence."),
    ]), "bg-sand")
    body += stats(dark=True)
    body += section(section_head("Stories", "Heartfelt stories from our families") + testimonials())
    body += cta("Want to know more about Carewise?", "Visit our centre, meet the team or speak to us about your parent's needs.")
    return body


def centre_page():
    body = page_hero("Carewise Centre", "Specialised care with <span class='serif-italic'>24/7 medical supervision.</span>",
                     "A calm, fully equipped facility in Mysuru for palliative care, rehabilitation and long-term medical support, with private and general rooms.", "room")
    body += section(section_head("Your comfort is our priority", "Rooms designed for healing and peace") + ROOMS)
    body += section(section_head("Conditions we treat", "Comprehensive medical support at the centre",
                                 "For chronic and acute conditions that need supervision beyond what a home can offer.") + icon_cards(CONDITIONS), "bg-sand")
    body += section(section_head("Admission", "How admission works") + steps([
        ("Call or visit", "Speak with our care coordinator about your parent's condition and needs."),
        ("Medical assessment", "Our doctor reviews reports and examines the patient to set a care plan."),
        ("Room &amp; plan", "Choose a general or private room; we share the plan, routine and costs clearly."),
        ("Daily updates", "Once admitted, your family receives daily updates and can visit freely."),
    ]))
    body += section(section_head("FAQ", "Common questions about the centre") + faq([
        ("Is a doctor available at night?", "Yes. Nursing staff are on duty 24/7 and a doctor is on call at all times, with scheduled rounds every day."),
        ("Can a family member stay overnight?", "Private rooms include a dedicated attendant bed so one family member can stay with the patient."),
        ("Do you accept ventilator-dependent patients?", "Yes. We provide ventilator, BiPAP and CPAP support with trained respiratory care staff."),
        ("How are meals handled?", "Meals are prepared in-house to the diet plan set by our nutritionist and the treating doctor."),
    ]), "bg-sand")
    body += cta("Would you like to visit the centre?", "Book a walk-through with our care coordinator at a time that suits you.")
    return body


def home_care_page():
    body = page_hero("Home healthcare", "Professional care, <span class='serif-italic'>at your parents' doorstep.</span>",
                     "Doctors, nurses, physiotherapists and caretakers who come to you, so recovery and long-term care can happen in familiar surroundings.", "home")
    body += section(section_head("Inside home healthcare", "Personalised senior care at your doorstep") + icon_cards(HOME_SERVICES))
    body += section(section_head("How it works", "Getting started takes one call") + steps([
        ("Tell us the need", "Call or WhatsApp us with a short description of your parent's condition."),
        ("Home assessment", "A doctor or senior nurse visits to assess and build a care plan."),
        ("Care begins", "Verified staff start on the agreed schedule, from single visits to 24-hour care."),
        ("Stay informed", "You receive daily updates and can reach the team any time."),
    ]), "bg-sand")
    body += section(split("hero", "Why families choose us", "Trusted by families in Mysuru, Bengaluru and abroad",
                          ["Many of our families live in another city or country. Daily updates, remote doctor monitoring and a single point of contact keep you close to your parents' care wherever you are."],
                          ["Background-verified, trained nurses and caretakers", "Doctor-guided care plans with regular review", "Flexible hours: visits, day shifts or round-the-clock", "Transparent pricing with no hidden charges"], flip=True))
    body += section(section_head("FAQ", "Questions about care at home") + faq([
        ("Which areas do you cover?", "We serve Mysuru city and nearby areas. Contact us to confirm availability for your location."),
        ("Can I book a single nurse visit?", "Yes. Single visits for injections, dressing or sample collection are available, as well as ongoing care."),
        ("How quickly can care start?", "In most cases within 24 to 48 hours of the home assessment."),
        ("What if my parent's condition changes?", "Our doctor reviews the plan and, if needed, we arrange a smooth transfer to the Carewise Centre."),
    ]), "bg-sand")
    body += cta("Need care at home this week?", "Call us and a care coordinator will arrange an assessment.")
    return body


def services_page():
    body = page_hero("Our services", "Everything your parents need, <span class='serif-italic'>in one place.</span>",
                     "Palliative care, nursing, rehabilitation, doctor visits and physiotherapy, delivered at the Carewise Centre or in your home.")
    body += section(section_head("Two pathways", "Where would you like care to happen?") + f'''
          <div class="grid grid-2">
            <a class="pathway reveal" href="centre.html">{img("room")}<div class="pathway-body"><span class="tag">At the centre</span><h3>Care at Carewise Centre</h3><p>24/7 medical supervision, private rooms and a calm, healing environment.</p><span class="text-link">Explore the centre {ico("arrow-right")}</span></div></a>
            <a class="pathway reveal" href="home-care.html">{img("home")}<div class="pathway-body"><span class="tag">At home</span><h3>Care at Home</h3><p>Nursing, doctor visits, therapy and caretakers at your doorstep.</p><span class="text-link">Explore home care {ico("arrow-right")}</span></div></a>
          </div>''')
    body += section(section_head("Medical services", "Conditions we treat") + icon_cards(CONDITIONS), "bg-sand", "conditions")
    body += section(section_head("Home services", "Care delivered at home") + icon_cards(HOME_SERVICES), "", "home")
    body += cta("Not sure which service fits?", "Describe the situation to our team and we will recommend the right care pathway.")
    return body


def team_page():
    roles = [
        ("Medical Director", "Palliative &amp; geriatric medicine", "Sets the clinical protocols and reviews every care plan at the centre and at home."),
        ("Consultant Physician", "Internal medicine", "Leads daily rounds and manages long-term and multi-morbidity conditions."),
        ("Head of Nursing", "Critical &amp; palliative nursing", "Supervises the 24/7 nursing team and the quality of bedside care."),
        ("Senior Physiotherapist", "Neuro &amp; ortho rehabilitation", "Designs stroke, post-surgical and mobility recovery programmes."),
        ("Clinical Nutritionist", "Geriatric nutrition", "Builds personalised diet plans for recovery, diabetes and heart health."),
        ("Family Counsellor", "Psycho-social support", "Supports patients and families through difficult decisions and transitions."),
        ("Care Coordinator", "Admissions &amp; home care", "Your single point of contact for scheduling, updates and questions."),
        ("Respiratory Care Lead", "Ventilator / BiPAP / CPAP", "Manages advanced respiratory support for critical patients."),
    ]
    cards = "".join(f'''
            <article class="card person reveal"><span class="avatar">{ico("user-round")}</span><h3>{r}</h3><p class="role">{s}</p><p>{d}</p></article>''' for r, s, d in roles)
    body = page_hero("Our team", "Experienced hands. <span class='serif-italic'>Caring hearts.</span>",
                     "Doctors, nurses, therapists and coordinators who treat every patient the way they would their own parents.")
    body += section(section_head("Who looks after your family", "A doctor-led, fully verified team",
                                 "Every member is background-verified and trained in elderly and palliative care.") + f'<div class="grid grid-4">{cards}</div>')
    body += section(section_head("Our standards", "What every Carewise team member commits to") + icon_cards([
        ("badge-check", "Verified &amp; trained", "Identity, qualification and background checks before joining, plus ongoing training."),
        ("clipboard-list", "Protocol-driven", "Doctor-guided protocols for medication, wound care, hygiene and emergencies."),
        ("bell-ring", "Responsive", "Priority nursing response at the centre and a reachable coordinator for home care."),
    ]), "bg-sand")
    body += cta("Want to join the Carewise team?", "We are always looking for compassionate nurses, caretakers and therapists in Mysuru.")
    return body


def gallery_page():
    tiles = [("room", "wide"), ("room2", ""), ("home", ""), ("hero", ""), ("family", "wide")]
    grid = "".join(f'<figure class="{c} reveal">{img(k)}<figcaption>{IMG[k][1]}</figcaption></figure>' for k, c in tiles)
    body = page_hero("Facility gallery", "Take a look <span class='serif-italic'>inside Carewise.</span>",
                     "Our rooms, common spaces and the people who make them feel like home.")
    body += section(f'<div class="gallery">{grid}</div>')
    body += cta("Prefer to see it in person?", "Book a visit and walk through the centre with our coordinator.")
    return body


def videos_page():
    vids = [
        ("A day at Carewise Centre", "How our nurses, doctors and therapists care for residents from morning rounds to evening.", "room"),
        ("Home care: a family's experience", "A daughter in Bengaluru shares how daily updates kept her close to her father's recovery.", "home"),
        ("Why palliative care matters", "Our medical team explains comfort-focused care and how it supports the whole family.", "family"),
    ]
    cards = "".join(f'''
            <article class="reveal">
              <a class="video" href="{WA}" aria-label="Watch: {t}">{img(k)}<span class="play"><span>{ico("play")}</span></span></a>
              <div class="video-meta"><h3>{t}</h3><p>{d}</p></div>
            </article>''' for t, d, k in vids)
    body = page_hero("Videos &amp; stories", "Hear it from <span class='serif-italic'>our families.</span>",
                     "Short films and stories from the people who know Carewise best.")
    body += section(f'<div class="grid grid-3">{cards}</div><p class="center muted" style="margin-top:2.5rem;font-size:.9rem">Videos are being added. Message us on WhatsApp to receive our latest stories.</p>')
    body += section(section_head("Stories", "Heartfelt stories from our families") + testimonials(), "bg-sand")
    body += cta()
    return body


def contact_page():
    info = "".join(f'<li><span class="ico-ring">{ico(i)}</span><div><strong>{t}</strong>{d}</div></li>' for i, t, d in [
        ("phone", "Phone", f'<a href="{TEL}">{PHONE}</a>'),
        ("message-circle", "WhatsApp", f'<a href="{WA}">Chat with us</a>'),
        ("mail", "Email", f'<a href="mailto:{EMAIL}">{EMAIL}</a>'),
        ("map-pin", "Address", "Carewise Healthcare, Mysuru, Karnataka, India"),
        ("clock", "Hours", "Centre open 24/7 · Enquiries 8am to 9pm daily"),
    ])
    tiles = "".join(f'<input id="care-{v}" name="care_type" type="radio" value="{l}"{" checked" if i == 0 else ""} /><label for="care-{v}">{l}</label>'
                    for i, (v, l) in enumerate([("centre", "Carewise Centre"), ("home", "Home care"), ("unsure", "Not sure yet")]))
    body = page_hero("Contact", "Talk to <span class='serif-italic'>our team.</span>",
                     "Available every day for questions, assessments and admissions. Call, WhatsApp or send us a message.")
    body += section(f'''
          <div class="contact-grid">
            <ul class="contact-list reveal">{info}</ul>
            <form class="form reveal" data-contact novalidate>
              <h2>Send us a message</h2>
              <div class="field-row">
                <div class="field"><label for="name">Your name</label><input id="name" name="name" type="text" required /></div>
                <div class="field"><label for="phone">Phone</label><input id="phone" name="phone" type="tel" required /></div>
              </div>
              <div class="field"><span>Type of care</span><div class="tiles">{tiles}</div></div>
              <div class="field"><label for="message">Tell us about your parent's needs</label><textarea id="message" name="message" rows="4"></textarea></div>
              <button class="btn btn-primary btn-lg" type="submit">Send message {ico("send")}</button>
              <p class="form-note">We reply within a few hours. For urgent needs please call {PHONE}.</p>
            </form>
          </div>''')
    body += section('''
          <div class="map reveal"><iframe loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=Mysuru,+Karnataka,+India&amp;output=embed" title="Carewise Healthcare location map"></iframe></div>''', "bg-sand")
    return body


def legal(title, sections):
    body = page_hero("Legal", title, "Last updated: 9 November 2026")
    body += section('<div class="prose reveal">' + "".join(f"<h2>{h}</h2>" + "".join(f"<p>{p}</p>" for p in ps) for h, ps in sections) + "</div>")
    return body


def privacy_page():
    return legal("Privacy Policy", [
        ("Who we are", ["Carewise Healthcare (\"Carewise\", \"we\", \"us\") operates the Carewise Centre in Mysuru, Karnataka and a home healthcare service. This policy explains how we handle personal information collected through this website and our services."]),
        ("Information we collect", ["Contact details you share through our forms, phone or WhatsApp, such as name, phone number and email.",
                                    "Health information about a patient that you choose to share so we can recommend and provide care. We treat this as sensitive personal data.",
                                    "Basic technical information such as browser type and pages visited, used only to keep the website working well."]),
        ("How we use it", ["To respond to enquiries, assess care needs, provide and coordinate care, send updates to the family, and meet legal and medical record-keeping obligations. We do not sell personal information."]),
        ("Sharing", ["Information is shared only with the Carewise clinical team involved in care, with service providers who help us run the website or communications under confidentiality terms, or where the law requires."]),
        ("Retention and security", ["Medical records are kept for the period required by Indian law. Other information is kept only as long as needed for the purpose it was collected. We use reasonable technical and organisational safeguards to protect it."]),
        ("Your rights", [f"You may ask to access, correct or delete your personal information, or withdraw consent, by emailing {EMAIL}. We will respond within a reasonable time, subject to legal record-keeping duties."]),
        ("Contact", [f"Questions about this policy can be sent to {EMAIL} or {PHONE}."]),
    ])


def terms_page():
    return legal("Terms of Service", [
        ("Acceptance", ["By using this website or engaging Carewise Healthcare for care at the Carewise Centre or at home, you agree to these terms."]),
        ("Our services", ["Carewise provides palliative care, nursing, rehabilitation, doctor visits and related services under the guidance of qualified medical professionals. Information on this website is general and does not replace an individual medical assessment."]),
        ("Not for emergencies", ["This website and our messaging channels are not emergency services. In a medical emergency, call 108 or go to the nearest emergency department."]),
        ("Care agreements", ["Admission to the centre or the start of home care is governed by a separate written care agreement covering the care plan, schedule, fees and responsibilities. In case of conflict, that agreement prevails."]),
        ("Fees and payment", ["Fees are shared transparently before care begins. Payment terms, deposits and refunds are set out in the care agreement."]),
        ("Your responsibilities", ["You agree to share accurate medical information, follow safety instructions from our team, and treat staff with respect."]),
        ("Limitation of liability", ["To the extent permitted by law, Carewise is not liable for indirect or consequential losses arising from use of this website. Nothing in these terms limits liability that cannot be limited under Indian law."]),
        ("Governing law", ["These terms are governed by the laws of India and subject to the jurisdiction of the courts of Mysuru, Karnataka."]),
        ("Contact", [f"For questions about these terms, write to {EMAIL} or call {PHONE}."]),
    ])


PAGES = {
    "index": ("Carewise | Palliative &amp; Senior Healthcare Centre, Mysuru", "Mysuru's first palliative care centre and professional home healthcare. Trusted for 6+ years by families in Mysuru, Bengaluru and abroad.", home_page),
    "about": ("About Us | Carewise", "Learn about Carewise, Mysuru's first palliative care centre and home healthcare service trusted by families for 6+ years.", about_page),
    "centre": ("Carewise Centre | 24/7 Palliative &amp; Senior Care in Mysuru", "Private and general rooms with 24/7 medical supervision, palliative care, rehabilitation and long-term care at the Carewise Centre, Mysuru.", centre_page),
    "home-care": ("Home Healthcare in Mysuru | Carewise", "Doctor visits, nursing, physiotherapy, caretakers and lab tests at home for elderly parents in Mysuru.", home_care_page),
    "services": ("Our Services | Carewise", "Palliative care, nursing, rehabilitation, doctor visits and physiotherapy at the Carewise Centre or at home.", services_page),
    "team": ("Our Team | Carewise", "Meet the doctor-led, verified team of nurses, therapists and coordinators behind Carewise.", team_page),
    "gallery": ("Facility Gallery | Carewise", "Photos of the Carewise Centre rooms, spaces and care in Mysuru.", gallery_page),
    "videos": ("Videos &amp; Stories | Carewise", "Films and stories from Carewise families and our care team.", videos_page),
    "contact": ("Contact Carewise | Talk to Our Team", "Call, WhatsApp or message Carewise Healthcare in Mysuru. Available every day for enquiries and admissions.", contact_page),
    "privacy-policy": ("Privacy Policy | Carewise", "How Carewise Healthcare collects, uses and protects personal information.", privacy_page),
    "terms-of-service": ("Terms of Service | Carewise", "Terms governing use of the Carewise website and services.", terms_page),
}


def build():
    for slug, (title, desc, fn) in PAGES.items():
        html = head(title, desc) + header(slug) + fn() + footer()
        (ROOT / f"{slug}.html").write_text(html, encoding="utf-8")
        print("wrote", f"{slug}.html")


if __name__ == "__main__":
    sys.exit(build())
