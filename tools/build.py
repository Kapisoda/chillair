#!/usr/bin/env python3
"""
Generator statične web stranice ChillAir d.o.o.

Uredite podatke u bloku FIRMA ispod (telefon, e-mail, domena) i pokrenite:
    python3 tools/build.py
Skripta prepisuje sve .html datoteke u korijenu repozitorija.
"""
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# PODACI FIRME — izvor: sudski registar / fininfo.hr
# Polja označena s TODO treba potvrditi ili upisati.
# ---------------------------------------------------------------------------
FIRMA = {
    "naziv": "Chillair d.o.o.",
    "brand": "ChillAir",
    "adresa": "Ulica Bernarda Vukasa 37",
    "grad": "10000 Zagreb",          # TODO: potvrdite poštanski broj
    "oib": "47070681198",
    "mb": "05987423",
    "direktor": "Zdravko Kušurin",
    "godina": 2024,
    "telefon_prikaz": "+385 91 328 7215",
    "telefon_link": "+385913287215",
    "email": "zdravko@chillair.hr",
    "domena": "https://chillair.hr",        # TODO: potvrdite domenu
    "karta": "https://www.google.com/maps/search/?api=1&query=Ulica+Bernarda+Vukasa+37+Zagreb",
}
F = FIRMA

# ---------------------------------------------------------------------------
# Ikone (inline SVG, bez vanjskih ovisnosti)
# ---------------------------------------------------------------------------
def ic(path, vb="0 0 24 24"):
    return (f'<svg viewBox="{vb}" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{path}</svg>')

I = {
    "snow": ic('<path d="M12 2v20M4.9 6l14.2 12M19.1 6L4.9 18"/><path d="M9.5 3.5L12 6l2.5-2.5M9.5 20.5L12 18l2.5 2.5M3 9.2l3.3.9-.8 3.3M21 14.8l-3.3-.9.8-3.3M3.9 15.6l3.2-1-.8-3.3M20.1 8.4l-3.2 1 .8 3.3"/>'),
    "heat": ic('<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="10" cy="12" r="4"/><path d="M10 8v8M6 12h8M17 9h1.5M17 12h1.5M17 15h1.5"/>'),
    "tool": ic('<path d="M14.7 6.3a4 4 0 0 0-5.4 5.1L3.5 17.2a1.8 1.8 0 0 0 2.5 2.5l5.8-5.8a4 4 0 0 0 5.1-5.4l-2.5 2.5-2.3-.3-.3-2.3 2.9-2.1z"/>'),
    "phone": ic('<path d="M5 4h3.5l1.7 4.3-2.2 1.4a11 11 0 0 0 6.3 6.3l1.4-2.2L20 15.5V19a1.5 1.5 0 0 1-1.6 1.5A16.5 16.5 0 0 1 3.5 5.6 1.5 1.5 0 0 1 5 4z"/>'),
    "mail": ic('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 6.5L12 13l8.5-6.5"/>'),
    "pin": ic('<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>'),
    "doc": ic('<path d="M7 3h7l4 4v14H7z"/><path d="M14 3v4h4M10 12h5M10 16h5"/>'),
    "target": ic('<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r=".6" fill="currentColor"/>'),
    "bolt": ic('<path d="M13 3L5 13.5h6L10 21l8-10.5h-6z"/>'),
    "shield": ic('<path d="M12 3l7 3v5.5c0 4.5-3 8-7 9.5-4-1.5-7-5-7-9.5V6z"/><path d="M8.8 12l2.2 2.2 4.4-4.4"/>'),
    "leaf": ic('<path d="M5 19c0-8 5-13 15-14-1 10-6 15-14 15"/><path d="M5 19l7-7"/>'),
    "menu": ic('<path d="M4 7h16M4 12h16M4 17h16"/>'),
}

# ---------------------------------------------------------------------------
# Ilustracije (originalne, u bojama logotipa — zamjena za fotografije)
# ---------------------------------------------------------------------------
def art_airflow(seed=0):
    """Apstraktni prikaz strujanja zraka na tamnoplavoj podlozi."""
    s = seed * 14
    return f'''<svg viewBox="0 0 500 400" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
<rect width="500" height="400" fill="#18618B"/>
<g fill="none" stroke-linecap="round">
<path d="M-20 {120+s} C 120 {40+s}, 260 {220-s}, 520 {90+s}" stroke="#40A4DD" stroke-width="16" opacity=".9"/>
<path d="M-20 {185+s} C 150 {110+s}, 300 {300-s}, 520 {170+s}" stroke="#fff" stroke-width="5" opacity=".55"/>
<path d="M-20 {250+s} C 140 {180+s}, 280 {360-s}, 520 {240+s}" stroke="#40A4DD" stroke-width="9" opacity=".6"/>
<path d="M-20 {310+s} C 170 {250+s}, 310 {400-s}, 520 {310+s}" stroke="#fff" stroke-width="3" opacity=".35"/>
<path d="M-20 {60+s} C 130 {10+s}, 250 {120-s}, 520 {30+s}" stroke="#fff" stroke-width="2.5" opacity=".3"/>
</g>
<g fill="#fff" opacity=".85"><circle cx="{380-s}" cy="{110+s}" r="4"/><circle cx="{120+s}" cy="{300-s}" r="3"/><circle cx="{260}" cy="{80+s}" r="2.5"/></g>
</svg>'''


def art_unit():
    """Zidna unutarnja jedinica klima uređaja s mlazom zraka — za hero."""
    return '''<svg class="unit" viewBox="0 0 340 260" aria-hidden="true">
<defs><linearGradient id="u" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#E4EFF6"/></linearGradient></defs>
<rect x="10" y="20" width="320" height="104" rx="22" fill="url(#u)" stroke="#18618B" stroke-width="4"/>
<rect x="34" y="96" width="272" height="10" rx="5" fill="#18618B" opacity=".85"/>
<circle cx="292" cy="50" r="6" fill="#40A4DD"/>
<g fill="none" stroke="#40A4DD" stroke-width="7" stroke-linecap="round">
<path d="M60 136 C 70 170, 50 200, 66 240"/><path d="M120 136 C 132 172, 112 204, 130 246"/>
<path d="M180 136 C 192 172, 172 204, 190 246"/><path d="M240 136 C 252 170, 232 200, 250 240"/>
</g>
</svg>'''


# ---------------------------------------------------------------------------
# Navigacija
# ---------------------------------------------------------------------------
NAV = [
    ("index.html", "Naslovna", None),
    ("usluge.html", "Usluge", [
        ("klimatizacijski-sustavi.html", "Klimatizacijski sustavi"),
        ("grijanje-i-dizalice-topline.html", "Grijanje i dizalice topline"),
        ("servis-i-odrzavanje.html", "Servis i održavanje"),
    ]),
    ("novosti.html", "Novosti", None),
    ("o-nama.html", "O nama", None),
    ("kontakt.html", "Kontakt", None),
]


def nav_html(current):
    out = []
    for href, label, sub in NAV:
        cur = ' aria-current="page"' if href == current else ""
        if sub:
            items = "".join(
                f'<li><a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{l}</a></li>'
                for h, l in sub)
            out.append(f'<li class="has-sub"><a href="{href}"{cur}>{label}</a><ul class="sub">{items}</ul></li>')
        else:
            out.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    return "".join(out)


def layout(filename, title, description, body):
    full_title = f"{title} | {F['brand']}" if title else f"{F['brand']} | Klimatizacija, grijanje i hlađenje"
    canonical = f"{F['domena']}/" + ("" if filename == "index.html" else filename)
    return f'''<!doctype html>
<html lang="hr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:locale" content="hr_HR">
<meta property="og:site_name" content="{F['brand']}">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{F['domena']}/assets/img/og-image.jpg">
<meta name="theme-color" content="#18618B">
<link rel="icon" type="image/png" sizes="32x32" href="assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/saira-semi-condensed-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
<a class="skip" href="#sadrzaj">Idi na sadržaj</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html"><img src="assets/img/chillair-logo.png" alt="ChillAir HVAC Solutions" width="640" height="162"></a>
    <button class="menu-btn" aria-controls="nav" aria-expanded="false" aria-label="Otvori izbornik">{I['menu']}</button>
    <nav class="nav" id="nav" aria-label="Glavna navigacija">
      <ul>{nav_html(filename)}</ul>
      <a class="btn header-call" href="tel:{F['telefon_link']}">{I['phone']} Nazovite nas</a>
    </nav>
  </div>
</header>
<main id="sadrzaj">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div>
      <img src="assets/img/chillair-logo-white.png" alt="ChillAir HVAC Solutions" width="640" height="162" loading="lazy">
      <p>Montaža, servis i održavanje klima uređaja, dizalica topline i sustava grijanja za kuće, stanove i poslovne prostore u Zagrebu i okolici.</p>
    </div>
    <div>
      <h4>Kontakt</h4>
      <ul>
        <li><a href="tel:{F['telefon_link']}">{F['telefon_prikaz']}</a></li>
        <li><a href="mailto:{F['email']}?subject=Upit%20s%20web%20stranice">{F['email']}</a></li>
        <li><a href="{F['karta']}" target="_blank" rel="noopener">{F['adresa']}, {F['grad']}</a></li>
      </ul>
    </div>
    <div>
      <h4>Pravne informacije</h4>
      <ul>
        <li>{F['naziv']}</li>
        <li>OIB: {F['oib']}</li>
        <li>MB: {F['mb']}</li>
        <li><a href="politika-privatnosti.html">Politika privatnosti</a></li>
        <li><a href="politika-kolacica.html">Politika kolačića</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom"><div class="wrap">
    <span>Copyright © <span data-year>{date.today().year}</span> {F['naziv']} Sva prava pridržana.</span>
  </div></div>
</footer>
<script src="assets/js/main.js" defer></script>
</body>
</html>
'''


def page_head(title, intro, crumbs=None, extra=""):
    c = ""
    if crumbs:
        c = '<div class="crumbs">' + " / ".join(
            f'<a href="{h}">{l}</a>' if h else l for h, l in crumbs) + "</div>"
    return f'''<section class="page-head">
  <img class="mark" src="assets/img/chillair-znak.png" alt="" width="400" height="381">
  <div class="wrap">{c}<h1>{title}</h1><p>{intro}</p>{extra}</div>
</section>'''


def cta():
    return f'''<section class="cta">
  <img class="mark" src="assets/img/chillair-znak.png" alt="" width="400" height="381" loading="lazy">
  <div class="wrap">
    <div>
      <h2>Zatražite ponudu za svoj prostor</h2>
      <p>Opišite nam prostor i što vam treba. Javit ćemo se s prijedlogom rješenja i terminom za pregled.</p>
    </div>
    <div class="cta-actions">
      <a class="btn btn--light" href="kontakt.html">Pošaljite upit</a>
      <a class="btn btn--light" href="tel:{F['telefon_link']}">{I['phone']} Nazovite</a>
    </div>
  </div>
</section>'''


def ticks(items):
    return '<ul class="ticks">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


# ---------------------------------------------------------------------------
# Sadržaj usluga (dijeli se između naslovnice, stranice Usluge i podstranica)
# ---------------------------------------------------------------------------
SERVICES = [
    {
        "file": "klimatizacijski-sustavi.html", "icon": "snow",
        "title": "Klimatizacijski sustavi",
        "short": ["Split i multi-split sustavi", "VRF / VRV sustavi", "Kanalne i kazetne jedinice",
                  "Klimatizacija poslovnih prostora", "Server sobe i tehnički prostori", "Rashladni sustavi"],
        "intro": "Klimatizacija za stan, kuću, ured ili cijelu zgradu — od jedne zidne jedinice do VRF sustava s centralnim upravljanjem.",
        "body": [
            ("Što radimo", "Pregledamo prostor, izračunamo potrebni kapacitet i predložimo sustav koji odgovara rasporedu prostorija, načinu korištenja i budžetu. Nakon dogovora isporučujemo opremu, izvodimo montažu, puštamo sustav u rad i pokazujemo vam kako ga koristiti."),
            ("Za koga", "Za kućanstva koja žele ugodnu temperaturu ljeti i zimi, za urede, trgovine i ugostiteljske objekte kojima treba stabilna klima tijekom radnog vremena te za tehničke prostore gdje oprema mora raditi bez pregrijavanja."),
        ],
        "list_title": "Sustavi koje ugrađujemo",
        "list": ["Zidni split uređaji za pojedinačne prostorije", "Multi-split sustavi s jednom vanjskom jedinicom",
                 "VRF / VRV sustavi za veće objekte", "Kanalne jedinice skrivene u stropu",
                 "Kazetne i parapetne jedinice", "Klimatizacija server soba i tehničkih prostora",
                 "Wi-Fi i centralno upravljanje sustavom"],
    },
    {
        "file": "grijanje-i-dizalice-topline.html", "icon": "heat",
        "title": "Grijanje i dizalice topline",
        "short": ["Dizalice topline zrak-voda", "Podno grijanje", "Fan-coil sustavi",
                  "Hidraulički razvod", "Priprema potrošne tople vode", "Pametno upravljanje"],
        "intro": "Učinkovito grijanje s dizalicama topline, podnim grijanjem i fan-coil jedinicama — za novogradnju i za zamjenu postojećeg sustava.",
        "body": [
            ("Što radimo", "Dimenzioniramo sustav prema toplinskim gubicima objekta, predlažemo dizalicu topline odgovarajuće snage i izvodimo cijeli hidraulički dio: razvod, spremnike, podno grijanje ili fan-coil jedinice te regulaciju."),
            ("Zašto dizalica topline", "Dizalica topline iz vanjskog zraka dobiva većinu energije potrebne za grijanje, pa troši znatno manje električne energije od klasičnih električnih grijalica. Isti sustav ljeti može i hladiti, a zimi grijati i pripremati toplu vodu."),
        ],
        "list_title": "Rješenja za grijanje",
        "list": ["Dizalice topline zrak-voda i zrak-zrak", "Podno i zidno grijanje",
                 "Fan-coil jedinice za grijanje i hlađenje", "Spremnici i priprema potrošne tople vode",
                 "Zamjena kotlova i modernizacija kotlovnica", "Regulacija i pametno upravljanje po zonama"],
    },
    {
        "file": "servis-i-odrzavanje.html", "icon": "tool",
        "title": "Servis i održavanje",
        "short": ["Redovni godišnji servis", "Dijagnostika i popravak kvarova", "Preventivno održavanje",
                  "Puštanje u pogon", "Rad s F-plinovima", "Ugovorno održavanje"],
        "intro": "Redovni servis produljuje vijek uređaja, smanjuje potrošnju i sprječava kvarove u najgorem trenutku.",
        "body": [
            ("Što uključuje servis", "Čišćenje i dezinfekciju unutarnje jedinice i filtera, pranje izmjenjivača vanjske jedinice, provjeru tlaka i propuštanja radne tvari, provjeru odvoda kondenzata te mjerenje radnih parametara. Nakon servisa dobivate zapisnik s nalazom."),
            ("Kvarovi i popravci", "Ako uređaj ne hladi, ne grije, curi ili javlja grešku, dolazimo na dijagnostiku, pronalazimo uzrok i predlažemo popravak ili zamjenu dijela. Radimo s rashladnim i klimatizacijskim uređajima te dizalicama topline, uključujući provjeru propuštanja i punjenje fluoriranih plinova."),
        ],
        "list_title": "Servisne usluge",
        "list": ["Redovni servis klima uređaja i dizalica topline", "Dijagnostika i otklanjanje kvarova",
                 "Provjera propuštanja i punjenje radne tvari (F-plinovi)", "Puštanje sustava u pogon",
                 "Zamjena i modernizacija dotrajale opreme", "Ugovorno održavanje za poslovne objekte",
                 "Redoviti pregled sustava grijanja i hlađenja u zgradi"],
    },
]


def service_cards():
    cards = []
    for s in SERVICES:
        cards.append(f'''<article class="service">
  <div class="service-icon">{I[s["icon"]]}</div>
  <h3>{s["title"]}</h3>
  {ticks(s["short"])}
  <a class="more" href="{s["file"]}">Saznajte više o usluzi</a>
</article>''')
    return '<div class="services">' + "".join(cards) + "</div>"


# ---------------------------------------------------------------------------
# Novosti
# ---------------------------------------------------------------------------
POSTS = [
    {
        "file": "novosti-servis-prije-sezone.html", "date": "2026-04-15", "date_hr": "15. travnja 2026.",
        "title": "Zašto servisirati klima uređaj prije ljeta",
        "summary": "Prljavi filteri i izmjenjivač smanjuju učinak i povećavaju potrošnju. Što se radi na servisu i kada ga naručiti.",
        "body": """<p>Klima uređaj koji je cijelu zimu stajao ili grijao skuplja prašinu, pelud i vlagu. Kad dođu prvi vrući dani, prljavi filteri i izmjenjivač smanjuju protok zraka, pa uređaj radi duže i troši više struje za isti učinak.</p>
<h2>Što se radi na servisu</h2>
<ul><li>Čišćenje i dezinfekcija filtera i unutarnje jedinice</li><li>Pranje izmjenjivača vanjske jedinice</li><li>Provjera odvoda kondenzata</li><li>Mjerenje tlaka i provjera propuštanja radne tvari</li><li>Provjera rada ventilatora, senzora i daljinskog upravljača</li></ul>
<h2>Kada naručiti</h2>
<p>Najbolje u proljeće, prije početka sezone. U lipnju i srpnju termini se brzo popune, a kvar u vrućem tjednu znači čekanje. Za kućanstva preporučujemo servis jednom godišnje, a za poslovne prostore s intenzivnim korištenjem dva puta godišnje.</p>
<p>Ako uređaj neugodno miriše, curi ili hladi slabije nego prije, ne čekajte redovni termin — javite nam se.</p>""",
    },
    {
        "file": "novosti-dizalica-topline.html", "date": "2026-02-10", "date_hr": "10. veljače 2026.",
        "title": "Dizalica topline: kada se isplati",
        "summary": "Kratki vodič za vlasnike kuća koji razmišljaju o zamjeni plinskog ili električnog grijanja.",
        "body": """<p>Dizalica topline uzima toplinu iz vanjskog zraka i predaje je vodi u sustavu grijanja. Za svaki kilovatsat struje koji potroši može isporučiti nekoliko kilovatsati topline, zato je jedna od najučinkovitijih opcija za grijanje kuće.</p>
<h2>Kada ima najviše smisla</h2>
<ul><li>U novogradnji ili nakon energetske obnove, kad su toplinski gubici manji</li><li>Uz podno grijanje ili fan-coil jedinice, koji rade s nižom temperaturom vode</li><li>Kad želite jedan sustav za grijanje, hlađenje i toplu vodu</li></ul>
<h2>Na što paziti</h2>
<p>Ključno je ispravno dimenzioniranje. Premala dizalica neće pokriti najhladnije dane, a prevelika će se često paliti i gasiti. Zato prije ponude izlazimo na teren, gledamo objekt i postojeću instalaciju te računamo potrebnu snagu.</p>
<p>Za mnoge projekte moguće je koristiti i poticaje za energetsku učinkovitost, pa se isplati provjeriti aktualne natječaje prije kupnje opreme.</p>""",
    },
]


def post_cards():
    out = []
    for i, p in enumerate(POSTS):
        out.append(f'''<article class="post">
  <div class="post-cover">{art_airflow(i + 1)}</div>
  <div class="post-body">
    <time datetime="{p["date"]}">{p["date_hr"]}</time>
    <h3><a href="{p["file"]}">{p["title"]}</a></h3>
    <p>{p["summary"]}</p>
    <a class="more" href="{p["file"]}">Pročitajte članak</a>
  </div>
</article>''')
    return '<div class="posts">' + "".join(out) + "</div>"


REASONS = [
    ("target", "Rješenje prema prostoru", "Ne prodajemo isti uređaj svima. Prvo pogledamo prostor, pa predložimo sustav koji mu odgovara."),
    ("bolt", "Brz odgovor", "Na upite reagiramo brzo i dogovaramo jasan termin za pregled ili servis."),
    ("shield", "Uredna izvedba", "Radimo prema dogovoru i u roku, čisto i bez naknadnih iznenađenja u cijeni."),
]


def reasons():
    return '<div class="reasons">' + "".join(
        f'<div class="reason"><div class="reason-icon">{I[i]}</div><div><h3>{t}</h3><p>{d}</p></div></div>'
        for i, t, d in REASONS) + "</div>"


def facts():
    items = [
        (str(F["godina"]), "Godina osnivanja"),
        ("Zagreb", "Sjedište i područje rada"),
        ("F-plinovi", "Rad s rashladnim uređajima i dizalicama topline"),
        ("Od A do Ž", "Savjet, montaža, servis i održavanje"),
    ]
    return '<section class="facts" aria-label="O tvrtki ukratko"><div class="wrap">' + "".join(
        f'<div class="fact"><strong>{a}</strong><span>{b}</span></div>' for a, b in items) + "</div></section>"


# ---------------------------------------------------------------------------
# Stranice
# ---------------------------------------------------------------------------
pages = {}

DESC_HOME = ("Montaža, servis i održavanje klima uređaja, dizalica topline i sustava grijanja za kuće, "
             "stanove i poslovne prostore u Zagrebu. Od odabira opreme do puštanja u rad.")

pages["index.html"] = (None, DESC_HOME, f'''
<section class="hero">
  <div class="wrap">
    <div>
      <h1>Klimatizacija, grijanje i hlađenje bez komplikacija</h1>
      <p class="lead">Savjetujemo, isporučujemo i ugrađujemo klima uređaje, dizalice topline i HVAC sustave za kuće, stanove i poslovne prostore — i brinemo o njima nakon montaže.</p>
      <div class="hero-actions">
        <a class="btn" href="kontakt.html">Zatražite ponudu</a>
        <a class="btn btn--ghost" href="usluge.html">Pogledajte usluge</a>
      </div>
    </div>
    <div class="hero-art">
      <img class="swirl" src="assets/img/chillair-znak.png" alt="" width="400" height="381">
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker">Usluge</span>
      <h2>Sve na jednom mjestu</h2>
      <p class="lead">{F['brand']} se bavi klimatizacijom, grijanjem i hlađenjem privatnih, turističkih i poslovnih objekata. Nakon pregleda prostora predlažemo sustav i vodimo cijeli posao — od opreme i montaže do servisa.</p>
    </div>
    {service_cards()}
  </div>
</section>

<section class="section section--ice">
  <div class="wrap split">
    <div>
      <span class="kicker">O nama</span>
      <h2>Vaš partner za ugodnu temperaturu cijele godine</h2>
      <p>{F['naziv']} je zagrebačka tvrtka osnovana {F['godina']}. godine, specijalizirana za instalacije grijanja, hlađenja i klimatizacije. Radimo na stanovima, kućama, apartmanima, uredima i ugostiteljskim objektima.</p>
      <p>Uz montažu i servis nudimo i energetske preglede te redovite preglede sustava grijanja i hlađenja u zgradama, pa na jednom mjestu dobivate i izvedbu i stručnu provjeru.</p>
      <p>Pristupamo jednostavno i profesionalno: jasan dogovor, uredna izvedba i podrška nakon završetka radova.</p>
      <a class="btn btn--ghost" href="o-nama.html">Više o nama</a>
    </div>
    <div class="split-media">{art_airflow(0)}</div>
  </div>
</section>

{facts()}

<section class="section">
  <div class="wrap split split--rev">
    <div>
      <h2>Zašto odabrati nas?</h2>
      <p class="lead">Pouzdanost, korektan odnos i kvalitetna izvedba. Svaki posao želimo odraditi tako da nas idući put nazovete opet.</p>
      {reasons()}
    </div>
    <div class="split-media">{art_airflow(2)}</div>
  </div>
</section>

{cta()}
''')

# --- Usluge
pages["usluge.html"] = ("Usluge", "Klimatizacijski sustavi, grijanje i dizalice topline te servis i održavanje — sve usluge ChillAir d.o.o. na jednom mjestu.", f'''
{page_head("Usluge", "Od prvog pregleda prostora do redovnog servisa — vodimo cijeli posao umjesto vas.", [("index.html","Naslovna"),(None,"Usluge")])}
<section class="section">
  <div class="wrap">{service_cards()}</div>
</section>
<section class="section section--ice">
  <div class="wrap">
    <div class="section-head"><h2>Kako radimo</h2><p class="lead">Isti jasan tijek za svaki projekt, bez obzira radi li se o jednoj klimi ili cijeloj zgradi.</p></div>
    <ol class="steps">
      <li><h3>Upit</h3><p>Javite se telefonom ili putem obrasca i opišite prostor.</p></li>
      <li><h3>Pregled</h3><p>Dolazimo na teren, mjerimo i predlažemo rješenje.</p></li>
      <li><h3>Ponuda i montaža</h3><p>Dobivate jasnu ponudu, a nakon dogovora izvodimo radove.</p></li>
      <li><h3>Puštanje u rad</h3><p>Testiramo sustav, objasnimo korištenje i dogovorimo servis.</p></li>
    </ol>
  </div>
</section>
<section class="section">
  <div class="wrap grid-2">
    <div class="panel"><div class="service-icon">{I["doc"]}</div><h3>Energetski pregledi i certificiranje</h3><p>Energetsko certificiranje, energetski pregled zgrade te redoviti pregled sustava grijanja, hlađenja i klimatizacije u zgradi.</p></div>
    <div class="panel"><div class="service-icon">{I["leaf"]}</div><h3>Projektiranje i nadzor</h3><p>Projektiranje instalacija i stručni nadzor građenja, upravljanje i održavanje nekretnina te najam opreme.</p></div>
  </div>
</section>
{cta()}
''')

# --- Podstranice usluga
for s in SERVICES:
    body_sections = "".join(f"<h2>{h}</h2><p>{p}</p>" for h, p in s["body"])
    others = "".join(
        f'<li><a href="{o["file"]}">{o["title"]}</a></li>' for o in SERVICES if o is not s)
    pages[s["file"]] = (s["title"], s["intro"], f'''
{page_head(s["title"], s["intro"], [("index.html","Naslovna"),("usluge.html","Usluge"),(None,s["title"])])}
<section class="section">
  <div class="wrap split" style="align-items:start">
    <div class="prose">{body_sections}</div>
    <aside class="panel">
      <h3>{s["list_title"]}</h3>
      {ticks(s["list"])}
      <a class="btn" href="kontakt.html">Zatražite ponudu</a>
      <h4 style="margin-top:28px">Ostale usluge</h4>
      <ul>{others}</ul>
    </aside>
  </div>
</section>
{cta()}
''')

# --- Novosti
pages["novosti.html"] = ("Novosti", "Savjeti i novosti o klimatizaciji, dizalicama topline i održavanju sustava.", f'''
{page_head("Novosti", "Savjeti o odabiru, korištenju i održavanju klima uređaja i sustava grijanja.", [("index.html","Naslovna"),(None,"Novosti")])}
<section class="section"><div class="wrap">{post_cards()}</div></section>
{cta()}
''')

for p in POSTS:
    pages[p["file"]] = (p["title"], p["summary"], f'''
{page_head(p["title"], p["summary"], [("index.html","Naslovna"),("novosti.html","Novosti"),(None,p["title"])],
           f'<div class="article-meta"><time datetime="{p["date"]}">{p["date_hr"]}</time></div>')}
<section class="section"><div class="wrap"><article class="prose">{p["body"]}
<p><a class="btn" href="kontakt.html">Pošaljite upit</a></p></article></div></section>
''')

# --- O nama
pages["o-nama.html"] = ("O nama", f"{F['naziv']} je zagrebačka tvrtka za klimatizaciju, grijanje i hlađenje osnovana {F['godina']}. godine.", f'''
{page_head("O nama", "Zagrebačka tvrtka za instalacije grijanja, hlađenja i klimatizacije.", [("index.html","Naslovna"),(None,"O nama")])}
<section class="section">
  <div class="wrap split">
    <div class="prose">
      <h2>Tko smo</h2>
      <p>{F['naziv']} osnovana je {F['godina']}. godine u Zagrebu. Bavimo se uvođenjem instalacija za grijanje i klimatizaciju te servisom i održavanjem rashladnih i klimatizacijskih uređaja i dizalica topline.</p>
      <p>Radimo za kućanstva, iznajmljivače apartmana, urede, trgovine i ugostiteljske objekte. Svaki posao počinje pregledom prostora, jer samo tako možemo predložiti sustav koji će raditi dugo i bez problema.</p>
      <h2>Čime se bavimo</h2>
      <ul>
        <li>Montaža klima uređaja, VRF sustava i dizalica topline</li>
        <li>Instalacije grijanja, podno grijanje i fan-coil sustavi</li>
        <li>Servis, provjera propuštanja i punjenje rashladnih uređaja (F-plinovi)</li>
        <li>Energetsko certificiranje i energetski pregledi zgrada</li>
        <li>Projektiranje i stručni nadzor građenja</li>
        <li>Upravljanje i održavanje nekretnina, najam opreme</li>
      </ul>
    </div>
    <div class="split-media">{art_airflow(1)}</div>
  </div>
</section>
{facts()}
<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Kako pristupamo poslu</h2></div>
    {reasons()}
  </div>
</section>
{cta()}
''')

# --- Kontakt
service_opts = "".join(f"<option>{s['title']}</option>" for s in SERVICES)
pages["kontakt.html"] = ("Kontakt", f"Kontaktirajte {F['naziv']} — telefon, e-mail i obrazac za upit. {F['adresa']}, {F['grad']}.", f'''
{page_head("Kontakt", "Pošaljite upit ili nas nazovite — javit ćemo vam se s terminom za pregled.", [("index.html","Naslovna"),(None,"Kontakt")])}
<section class="section">
  <div class="wrap contact-grid">
    <div>
      <h2>Kontakt informacije</h2>
      <ul class="contact-list">
        <li><span class="ci">{I["phone"]}</span><div><small>Telefon</small><a href="tel:{F['telefon_link']}">{F['telefon_prikaz']}</a></div></li>
        <li><span class="ci">{I["mail"]}</span><div><small>E-mail</small><a href="mailto:{F['email']}?subject=Upit%20s%20web%20stranice">{F['email']}</a></div></li>
        <li><span class="ci">{I["pin"]}</span><div><small>Adresa</small><a href="{F['karta']}" target="_blank" rel="noopener">{F['adresa']}, {F['grad']}</a></div></li>
      </ul>
      <div class="panel">
        <h3>Podaci o tvrtki</h3>
        <p style="margin:0">{F['naziv']}<br>{F['adresa']}, {F['grad']}<br>OIB: {F['oib']}<br>MB: {F['mb']}<br>Direktor: {F['direktor']}</p>
      </div>
    </div>
    <div class="panel">
      <h2 style="font-size:1.8rem">Pošaljite upit</h2>
      <form class="form" id="upit" data-to="{F['email']}" novalidate>
        <div class="row">
          <div><label for="ime">Ime i prezime</label><input id="ime" name="ime" autocomplete="name" required></div>
          <div><label for="telefon">Telefon</label><input id="telefon" name="telefon" type="tel" autocomplete="tel"></div>
        </div>
        <div class="row">
          <div><label for="email">E-mail</label><input id="email" name="email" type="email" autocomplete="email" required></div>
          <div><label for="lokacija">Lokacija objekta</label><input id="lokacija" name="lokacija" placeholder="npr. Zagreb, Trešnjevka"></div>
        </div>
        <div><label for="usluga">Usluga</label><select id="usluga" name="usluga"><option value="">Odaberite uslugu</option>{service_opts}<option>Energetski pregled / certificiranje</option><option>Nešto drugo</option></select></div>
        <div><label for="poruka">Opis upita</label><textarea id="poruka" name="poruka" required placeholder="Vrsta i veličina prostora, broj prostorija, postojeća oprema…"></textarea></div>
        <label class="check"><input type="checkbox" name="privola" required> <span>Slažem se da se moji podaci koriste za odgovor na upit, prema <a href="politika-privatnosti.html">politici privatnosti</a>.</span></label>
        <p class="form-error" role="alert"></p>
        <div><button class="btn" type="submit">Pošaljite upit</button></div>
        <p class="form-note">Klikom na gumb otvara se vaš e-mail program s pripremljenom porukom.</p>
      </form>
    </div>
  </div>
</section>
''')

# --- Pravne stranice
pages["politika-privatnosti.html"] = ("Politika privatnosti", f"Politika privatnosti {F['naziv']}", f'''
{page_head("Politika privatnosti", "Kako prikupljamo i koristimo osobne podatke.", [("index.html","Naslovna"),(None,"Politika privatnosti")])}
<section class="section"><div class="wrap prose">
<h2>Voditelj obrade</h2>
<p>{F['naziv']}, {F['adresa']}, {F['grad']}, OIB {F['oib']}. Za sva pitanja o osobnim podacima pišite na <a href="mailto:{F['email']}">{F['email']}</a>.</p>
<h2>Koje podatke prikupljamo</h2>
<p>Podatke koje nam sami pošaljete e-mailom, telefonom ili putem obrasca za upit: ime i prezime, e-mail adresu, broj telefona, lokaciju objekta i opis upita.</p>
<h2>Svrha i pravna osnova</h2>
<p>Podatke koristimo isključivo za odgovor na upit, izradu ponude i izvršenje ugovorenih usluga (čl. 6. st. 1. t. b) Opće uredbe o zaštiti podataka), te za ispunjavanje zakonskih obveza (čl. 6. st. 1. t. c).</p>
<h2>Koliko dugo čuvamo podatke</h2>
<p>Podatke iz upita koji nisu doveli do suradnje čuvamo najdulje 12 mjeseci. Podatke vezane uz ugovore i račune čuvamo onoliko dugo koliko to propisuju zakoni.</p>
<h2>Dijeljenje podataka</h2>
<p>Podatke ne prodajemo niti ih dajemo trećim stranama u marketinške svrhe. Mogu ih obrađivati samo naši izvršitelji obrade (npr. pružatelj e-mail usluge ili knjigovodstveni servis) u mjeri potrebnoj za njihov posao.</p>
<h2>Vaša prava</h2>
<p>Imate pravo na pristup, ispravak, brisanje i ograničenje obrade svojih podataka, pravo na prigovor te pravo podnijeti pritužbu Agenciji za zaštitu osobnih podataka (azop.hr).</p>
<p><em>Posljednja izmjena: {date.today().strftime("%d. %m. %Y.")}</em></p>
</div></section>
''')

pages["politika-kolacica.html"] = ("Politika kolačića", f"Politika kolačića {F['naziv']}", f'''
{page_head("Politika kolačića", "Koje kolačiće koristi ova stranica.", [("index.html","Naslovna"),(None,"Politika kolačića")])}
<section class="section"><div class="wrap prose">
<h2>Kolačići na ovoj stranici</h2>
<p>Ova web stranica ne koristi kolačiće za praćenje, analitiku ni oglašavanje. Fontovi i sve ostale datoteke učitavaju se izravno s naše stranice, bez vanjskih servisa.</p>
<h2>Vanjske poveznice</h2>
<p>Poveznica na kartu otvara Google Maps u novom prozoru. Na toj stranici vrijede pravila privatnosti i kolačića tvrtke Google.</p>
<h2>Promjene</h2>
<p>Ako u budućnosti uvedemo analitiku ili druge kolačiće, ova će stranica biti ažurirana i prije postavljanja tražit ćemo vašu privolu.</p>
<p><em>Posljednja izmjena: {date.today().strftime("%d. %m. %Y.")}</em></p>
</div></section>
''')

pages["404.html"] = ("Stranica nije pronađena", "Tražena stranica ne postoji.", f'''
{page_head("Stranica nije pronađena", "Adresa možda nije ispravna ili je stranica premještena.")}
<section class="section"><div class="wrap"><p>Vratite se na <a href="index.html">naslovnicu</a> ili pogledajte naše <a href="usluge.html">usluge</a>.</p></div></section>
''')

# ---------------------------------------------------------------------------
for fname, (title, desc, body) in pages.items():
    (ROOT / fname).write_text(layout(fname, title, desc, body), encoding="utf-8")

urls = "".join(f"<url><loc>{F['domena']}/{'' if f == 'index.html' else f}</loc></url>"
               for f in pages if f != "404.html")
(ROOT / "sitemap.xml").write_text(
    f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n',
    encoding="utf-8")
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {F['domena']}/sitemap.xml\n", encoding="utf-8")
print(f"Generirano {len(pages)} stranica.")
