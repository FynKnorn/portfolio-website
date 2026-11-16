"""Baut die Portfolio-Website nach site/ und legt ein ZIP für Netlify auf den Desktop.

    conda activate portfolio-website
    python bauen.py            # baut site/ und das ZIP
    python bauen.py --ohne-zip # nur site/ (zum Ansehen: python -m http.server -d site)

Bilder, Abbildungen und Berichte kommen aus den Projekt-Repos und vom Desktop; sie werden
hier nur verkleinert und kopiert, nicht im Repo gespeichert.
"""

import argparse
import json
import math
import shutil
import zipfile
from html import escape
from pathlib import Path

from PIL import Image

import karte as stadtkarte
from logo import favicon, logo
from inhalt import DESKTOP, GITHUB, IN_ARBEIT, PERSON, PROJEKTE, PROJEKTE_ORDNER

HIER = Path(__file__).parent
SITE = HIER / "site"
SCHRIFT = HIER / "schrift"
ZIP = DESKTOP / "Portfolio" / "portfolio-website.zip"
GEWICHTE = (400, 600, 700)
REIHE = "Leipzig in Daten"


# --- Dateien vorbereiten -------------------------------------------------------------------

def schrift_vorbereiten():
    """Inter als WOFF2, auf lateinische Zeichen gekürzt (einmalig, liegt dann im Repo)."""
    from fontTools import subset

    quelle = PROJEKTE_ORDNER / "leipzig-oepnv-anbindung" / "src" / "anbindung" / "fonts"
    SCHRIFT.mkdir(exist_ok=True)
    for g in GEWICHTE:
        ziel = SCHRIFT / f"inter-{g}.woff2"
        if ziel.exists():
            continue
        opt = subset.Options()
        opt.flavor = "woff2"
        opt.layout_features = ["*"]
        font = subset.load_font(quelle / f"Inter-{g}.ttf", opt)
        s = subset.Subsetter(opt)
        s.populate(unicodes=[*range(0x20, 0x7F), *range(0xA0, 0x100),
                             0x2009, 0x2013, 0x2014, 0x2018, 0x2019, 0x201A, 0x201C, 0x201D,
                             0x201E, 0x2022, 0x2026, 0x202F, 0x20AC, 0x2190, 0x2192, 0x2212])
        s.subset(font)
        subset.save_font(font, ziel, opt)


def webp(quelle: Path, ziel: Path, breite: int, qualitaet: int = 80) -> tuple[int, int]:
    """Verkleinert ein Bild auf höchstens `breite` Pixel und speichert es als WebP."""
    bild = Image.open(quelle)
    bild = bild.convert("RGBA" if bild.mode in ("RGBA", "LA", "P") else "RGB")
    if bild.width > breite:
        bild = bild.resize((breite, round(bild.height * breite / bild.width)), Image.LANCZOS)
    bild.save(ziel, "WEBP", quality=qualitaet, method=6)
    return bild.size


def mb(pfad: Path) -> str:
    return f"{pfad.stat().st_size / 1e6:.1f}".replace(".", ",") + " MB"


def dateien_vorbereiten():
    (SITE / "bilder").mkdir(parents=True)
    (SITE / "berichte").mkdir()
    shutil.copytree(SCHRIFT, SITE / "schrift")
    shutil.copy(HIER / "stil.css", SITE / "stil.css")
    erstes = PROJEKTE_ORDNER / PROJEKTE[0]["repo"] / "results" / "report"
    webp(erstes / "signet.png", SITE / "bilder" / "signet.webp", 96, 90)
    (SITE / "bilder" / "logo.svg").write_text(favicon(), encoding="utf-8")

    for p in PROJEKTE:
        report = PROJEKTE_ORDNER / p["repo"] / "results" / "report"
        p["koepfe"] = json.loads((report / "koepfe.json").read_text(encoding="utf-8"))
        for b in (800, 1600):
            p["foto_masse"] = webp(report / "titelbild.jpg", SITE / "bilder" / f"{p['slug']}-{b}.webp", b, 78)
        p["abb_masse"] = {a: webp(report / f"{a}.png", SITE / "bilder" / f"{p['slug']}-{a}.webp", 1800, 90)
                          for a in p["abbildungen"]}
        shutil.copy(p["pdf"], SITE / "berichte" / f"{p['slug']}.pdf")
        p["pdf_groesse"] = mb(p["pdf"])


# --- HTML-Bausteine ------------------------------------------------------------------------

def seite(titel: str, beschreibung: str, inhalt: str, tiefe: int = 0) -> str:
    w = "../" * tiefe
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>{escape(titel)}</title>
<meta name="description" content="{escape(beschreibung)}">
<link rel="preload" href="{w}schrift/inter-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{w}stil.css">
<link rel="icon" href="{w}bilder/logo.svg" type="image/svg+xml">
</head>
<body>
<header class="kopfleiste">
  <div class="rahmen kopfleiste-innen">
    <a class="marke" href="{w}./">{logo()}{escape(PERSON['name'])}</a>
    <nav><a href="{w}./#projekte">Projekte</a></nav>
  </div>
</header>
<main>
{inhalt}
</main>
<footer class="fuss">
  <div class="rahmen fuss-innen">
    <span>© 2026 {escape(PERSON['name'])} · Leipzig</span>
    <span>Kontakt: <a href="mailto:{PERSON['mail']}">{PERSON['mail']}</a> · <a href="{w}datenschutz/">Datenschutz</a> · Fotos von Wikimedia Commons, Nachweis auf den Projektseiten</span>
  </div>
</footer>
</body>
</html>
"""


def themen(liste) -> str:
    return '<ul class="themen">' + "".join(f"<li>{escape(t)}</li>" for t in liste) + "</ul>"


def bild(p, breite_css: str, wurzel: str, prio: bool) -> str:
    w, h = p["foto_masse"]
    s = p["slug"]
    attr = ' fetchpriority="high"' if prio else ' loading="lazy"'
    return (f'<img src="{wurzel}bilder/{s}-800.webp" srcset="{wurzel}bilder/{s}-800.webp 800w, '
            f'{wurzel}bilder/{s}-1600.webp 1600w" sizes="{breite_css}" width="{w}" height="{h}" '
            f'alt="{escape(p["foto"][0])}" style="view-transition-name: foto-{s}"{attr}>')


def karte(i: int, p) -> str:
    return f"""<article class="karte">
  <div class="karte-bild">{bild(p, "(min-width: 900px) 560px, 100vw", "", i == 0)}<span class="nr">Nr. {i + 1}</span></div>
  <div class="karte-text">
    <p class="dach">{REIHE} · Nr. {i + 1}</p>
    <h3><a class="ganz" href="{p['slug']}/">{escape(p['titel'])}</a></h3>
    <p class="kern">{escape(p['kernaussage'])}</p>
    {themen(p['themen'])}
    <div class="links">
      <a href="berichte/{p['slug']}.pdf">Bericht <small>PDF, {p['pdf_groesse']}</small></a>
      <a href="{GITHUB}/{p['repo']}">Code auf GitHub</a>
    </div>
  </div>
</article>"""


def karte_in_arbeit(nr: int, p) -> str:
    return f"""<article class="karte karte-arbeit">
  <div class="karte-bild leer"><img src="bilder/signet.webp" alt="" width="96" height="103" loading="lazy"><span class="nr">Nr. {nr}</span></div>
  <div class="karte-text">
    <p class="dach">{REIHE} · Nr. {nr} · {escape(p['stand'])}</p>
    <h3>{escape(p['titel'])}</h3>
    <p class="kern">{escape(p['text'])}</p>
    {themen(p['themen'])}
  </div>
</article>"""


def kartenraster() -> str:
    karten = "\n".join(karte(i, p) for i, p in enumerate(PROJEKTE))
    karten += "\n" + "\n".join(karte_in_arbeit(len(PROJEKTE) + j + 1, p) for j, p in enumerate(IN_ARBEIT))
    return f"""<section class="rahmen" id="projekte">
  <h2 class="abschnitt">Die Reihe „{REIHE}“</h2>
  <div class="raster">
{karten}
  </div>
</section>"""


def startseite_karte() -> str:
    """Startseite mit bewegter Leipzig-Karte: Farbschleier ziehen unter matten Ortsteilen."""
    namen, pfade, abst, viewbox = stadtkarte.ortsteile()
    hoehe = viewbox.split()[3]
    info = stadtkarte.steckbriefe()
    flaechen = "".join(f'<path d="{d}" data-name="{escape(n)}" data-info="{escape(info[n])}" style="--d:{a:.3f}"/>'
                       for d, n, a in zip(pfade, namen, abst))
    glut = {"g1": "#2a78d6", "g2": "#17447e", "g3": "#6aa2e6", "g4": "#9cc3ef"}  # Blautöne der Seite
    verlaeufe = "".join(f'<radialGradient id="{k}"><stop class="farbe-{k}" offset="0" stop-color="{c}" stop-opacity=".7"/>'
                        f'<stop class="farbe-{k}" offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>'
                        for k, c in glut.items())
    blobs = "".join(f'<circle class="blob b{i}" cx="{cx}" cy="{cy}" r="{r}" fill="url(#g{i})"/>'
                    for i, (cx, cy, r) in enumerate([(300, 380, 430), (720, 320, 390), (560, 800, 420), (230, 820, 300)], 1))
    alle = "".join(pfade)
    # Satellit als leuchtender Komet auf schräger Umlaufbahn: hinter der Stadt verdeckt, davor sichtbar
    cx, cy, rx, ry, neig = 500, 545, 590, 150, -16
    w = math.radians(neig)
    rechts = (cx + rx * math.cos(w), cy + rx * math.sin(w))
    links = (cx - rx * math.cos(w), cy - rx * math.sin(w))
    weg = (f"M{rechts[0]:.0f},{rechts[1]:.0f} A{rx},{ry} {neig} 0 1 {links[0]:.0f},{links[1]:.0f} "
           f"A{rx},{ry} {neig} 0 1 {rechts[0]:.0f},{rechts[1]:.0f}")
    bahn_defs = (
        f'<clipPath id="hinten"><rect x="-3000" y="-3000" width="6000" height="3000" transform="translate({cx} {cy}) rotate({neig})"/></clipPath>'
        f'<clipPath id="vorn"><rect x="-3000" y="0" width="6000" height="3000" transform="translate({cx} {cy}) rotate({neig})"/></clipPath>'
        '<radialGradient id="komet"><stop offset="0" stop-color="#fff"/><stop offset=".2" stop-color="#bcd8f7"/>'
        '<stop offset=".5" stop-color="#2a78d6" stop-opacity=".45"/><stop offset="1" stop-color="#2a78d6" stop-opacity="0"/></radialGradient>')

    def bahn(seite):
        # Leuchtspur: zwei Striche auf der Bahn, die im Takt des Satelliten mitlaufen (Ende = Satellit)
        spur = "".join(
            f'<path class="spur spur-{k}" d="{weg}" pathLength="100" stroke-dasharray="{lang} {100 - lang}">'
            f'<animate attributeName="stroke-dashoffset" values="{lang};{lang - 100}" dur="26s" repeatCount="indefinite"/></path>'
            for k, lang in ((1, 24), (2, 9)))
        return (f'<g class="bahn bahn-{seite}" clip-path="url(#{seite})"><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" '
                f'transform="rotate({neig} {cx} {cy})"/>{spur}<g class="satellit" data-name="Satellit Landsat" '
                f'data-info="liefert die Hitzedaten für Nr. 2"><animateMotion dur="26s" repeatCount="indefinite" path="{weg}"/>'
                f'<circle class="komet-glanz" r="36" fill="url(#komet)"/><circle r="7" fill="#fff"/></g></g>')
    svg = f"""<svg viewBox="{viewbox}" role="img" aria-label="Karte der 63 Leipziger Ortsteile">
        <defs><clipPath id="stadt"><path d="{alle}"/></clipPath>{verlaeufe}{bahn_defs}
          <filter id="schatten" x="-10%" y="-10%" width="120%" height="130%"><feGaussianBlur stdDeviation="16"/></filter></defs>
        <g class="unterlage" filter="url(#schatten)" transform="translate(0 18)"><path d="{alle}"/></g>
        {bahn("hinten")}
        <g class="aurora" clip-path="url(#stadt)"><rect width="1000" height="{hoehe}" fill="#eef3fb"/>{blobs}</g>
        <g class="ortsteile">{flaechen}</g>
        {bahn("vorn")}
      </svg>"""
    inhalt = f"""<section class="rahmen held held-karte">
  <div class="held-text">
    <p class="kicker"><span></span>{escape(PERSON['kicker'])}</p>
    <h1>{escape(PERSON['titel'])}</h1>
    <p class="lead">{escape(PERSON['lead'])}</p>
  </div>
  <figure class="stadtkarte">
    <div class="karte-flaeche">
      {svg}
      <div class="tipp" hidden></div>
    </div>
    <figcaption><span>Leipzigs 63 Ortsteile</span> · <span>Daten: Stadt Leipzig, dl-de/by-2-0</span></figcaption>
  </figure>
</section>
{kartenraster()}
<script>
{(HIER / "karte.js").read_text(encoding="utf-8")}
</script>"""
    return seite(f"{PERSON['name']} · {REIHE}", PERSON["lead"], inhalt)


def projektseite(i: int, p) -> str:
    s, nr = p["slug"], i + 1
    kacheln = "".join(f'<div class="kachel"><span class="zahl">{escape(z)}</span><span>{escape(t)}</span></div>'
                      for z, t in p["kacheln"])
    steck = "".join(f"<div><dt>{escape(k)}</dt><dd>{escape(v)}</dd></div>" for k, v in p["steckbrief"])
    abbs = []
    for a in p["abbildungen"]:
        k = p["koepfe"][a]
        w, h = p["abb_masse"][a]
        lese = k.get("lesehilfe", "").removeprefix("So liest man das Bild: ")
        abbs.append(f"""<figure class="abb">
  <p class="dach">{escape(k.get('dachzeile', ''))}</p>
  <h3>{escape(k['titel'])}</h3>
  <a href="../bilder/{s}-{a}.webp"><img src="../bilder/{s}-{a}.webp" width="{w}" height="{h}" alt="{escape(k['titel'])}" loading="lazy"></a>
  <details><summary>So liest man das Bild</summary><p>{escape(lese)}</p></details>
  <figcaption>{escape(k.get('quellen', ''))}</figcaption>
</figure>""")
    titel_foto, urheber, lizenz, lizenz_url = p["foto"]
    nachbarn = []
    if i > 0:
        v = PROJEKTE[i - 1]
        nachbarn.append(f'<a href="../{v["slug"]}/"><small>← Nr. {i}</small>{escape(v["titel"])}</a>')
    if i + 1 < len(PROJEKTE):
        n = PROJEKTE[i + 1]
        nachbarn.append(f'<a class="rechts" href="../{n["slug"]}/"><small>Nr. {i + 2} →</small>{escape(n["titel"])}</a>')
    inhalt = f"""<div class="rahmen">
<a class="zurueck" href="../">← Alle Projekte</a>
<section class="projekt-kopf">
  <div>
    <p class="dach">{REIHE} · Nr. {nr}</p>
    <h1>{escape(p['titel'])}</h1>
    <p class="lead">{escape(p['untertitel'])}</p>
    {themen(p['themen'])}
    <div class="knoepfe">
      <a class="knopf voll" href="../berichte/{s}.pdf">Bericht lesen <small>PDF, {p['pdf_groesse']}</small></a>
      <a class="knopf" href="{GITHUB}/{p['repo']}">Code auf GitHub</a>
    </div>
  </div>
  <figure class="titelfoto">{bild(p, "(min-width: 900px) 540px, 100vw", "../", True)}
    <figcaption>{escape(titel_foto)}. Foto: {escape(urheber)}, <a href="{lizenz_url}">{lizenz}</a>, bearbeitet</figcaption>
  </figure>
</section>
<section class="kacheln">{kacheln}</section>
<section>
  <h2 class="abschnitt">Steckbrief</h2>
  <dl class="steckbrief">{steck}</dl>
</section>
<section>
  <h2 class="abschnitt">Die wichtigsten Abbildungen</h2>
  <div class="abbildungen">
{chr(10).join(abbs)}
  </div>
  <p class="mehr">Alle Ergebnisse, Grenzen und die Technik stehen im <a href="../berichte/{s}.pdf">Bericht</a>.</p>
</section>
<nav class="nachbarn">{''.join(nachbarn)}</nav>
</div>"""
    return seite(f"{p['titel']} · {PERSON['name']}", p["untertitel"], inhalt, tiefe=1)


# --- Ablauf --------------------------------------------------------------------------------

def datenschutzseite() -> str:
    m = escape(PERSON["mail"])
    inhalt = f"""<section class="rahmen textseite">
  <h1>Datenschutz</h1>
  <p>Diese Website ist ein privates, nicht kommerzielles Portfolio. Sie setzt keine Cookies, nutzt
  keine Analyse- oder Tracking-Dienste und lädt nichts von fremden Servern: Schriften, Bilder und
  Berichte liegen hier auf dem Server.</p>
  <h2>Verantwortlich</h2>
  <p>{escape(PERSON['name'])}, Leipzig · <a href="mailto:{m}">{m}</a></p>
  <h2>Hosting</h2>
  <p>Die Website liegt bei Netlify, Inc. (USA). Beim Aufruf verarbeitet Netlify technisch nötige
  Daten wie IP-Adresse, Zeitpunkt und aufgerufene Seite, um die Seiten auszuliefern und vor
  Missbrauch zu schützen (Art. 6 Abs. 1 lit. f DSGVO). Dabei können Daten in die USA übertragen
  werden. Mehr dazu in der <a href="https://www.netlify.com/privacy/">Datenschutzerklärung von Netlify</a>.</p>
  <h2>E-Mail</h2>
  <p>Wer mir schreibt, dessen Angaben nutze ich nur, um zu antworten.</p>
  <h2>Ihre Rechte</h2>
  <p>Sie haben das Recht auf Auskunft, Berichtigung, Löschung und Einschränkung der Verarbeitung
  sowie auf Beschwerde bei einer Datenschutz-Aufsichtsbehörde.</p>
</section>"""
    return seite(f"Datenschutz · {PERSON['name']}", "Hinweise zum Datenschutz", inhalt, tiefe=1)


def bauen(mit_zip: bool):
    schrift_vorbereiten()
    if SITE.exists():
        shutil.rmtree(SITE)
    dateien_vorbereiten()
    (SITE / "index.html").write_text(startseite_karte(), encoding="utf-8")
    (SITE / "datenschutz").mkdir()
    (SITE / "datenschutz" / "index.html").write_text(datenschutzseite(), encoding="utf-8")
    for i, p in enumerate(PROJEKTE):
        (SITE / p["slug"]).mkdir()
        (SITE / p["slug"] / "index.html").write_text(projektseite(i, p), encoding="utf-8")
    groesse = sum(f.stat().st_size for f in SITE.rglob("*") if f.is_file())
    print(f"site/ gebaut: {groesse / 1e6:.1f} MB")
    if mit_zip:
        ZIP.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(SITE.rglob("*")):
                if f.is_file():
                    z.write(f, f.relative_to(SITE))
        print(f"ZIP: {ZIP}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--ohne-zip", action="store_true", help="nur site/ bauen")
    bauen(not ap.parse_args().ohne_zip)
