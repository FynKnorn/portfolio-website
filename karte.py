"""Leipzig-Karte für die Startseite: die 63 Ortsteile als flache SVG-Karte.

Die Grenzen kommen aus dem Projekt Stadtentwicklung (EPSG:25833, Meter). Hier werden sie nur
vereinfacht und in SVG-Koordinaten umgerechnet; die Bewegung macht stil.css.
"""

import csv
import json
import math

from inhalt import PROJEKTE_ORDNER

QUELLE = PROJEKTE_ORDNER / "leipzig-stadtentwicklung" / "data" / "raw"
GRENZEN = QUELLE / "ortsteile.json"
EINWOHNER = QUELLE / "statistik" / "k02_r01.csv"   # Amt für Statistik und Wahlen
JAHRE = ("2010", "2025")
BREITE = 1000          # Breite der Karte in SVG-Einheiten
TOLERANZ = 25          # Vereinfachung in Metern (Douglas-Peucker)

def _dp(punkte, tol):
    """Douglas-Peucker: lässt Punkte weg, die weniger als `tol` von der Linie abweichen."""
    if len(punkte) < 3:
        return punkte
    (x1, y1), (x2, y2) = punkte[0], punkte[-1]
    dx, dy = x2 - x1, y2 - y1
    laenge = math.hypot(dx, dy) or 1e-9
    abst = [abs(dy * x - dx * y + x2 * y1 - y2 * x1) / laenge for x, y in punkte[1:-1]]
    i = max(range(len(abst)), key=abst.__getitem__)
    if abst[i] <= tol:
        return [punkte[0], punkte[-1]]
    return _dp(punkte[: i + 2], tol)[:-1] + _dp(punkte[i + 1:], tol)


def _ring(ring, tol):
    """Geschlossener Ring: am weitesten entfernten Punkt teilen, beide Hälften vereinfachen."""
    x0, y0 = ring[0]
    k = max(range(len(ring)), key=lambda i: math.hypot(ring[i][0] - x0, ring[i][1] - y0))
    return _dp(ring[: k + 1], tol)[:-1] + _dp(ring[k:], tol)


def ortsteile():
    """Namen, SVG-Pfade, Abstand zum Zentrum (0 bis 1, für die Einblend-Welle) und viewBox."""
    feats = json.loads(GRENZEN.read_text(encoding="utf-8"))["features"]
    alle = [p for f in feats for ring in f["geometry"]["coordinates"] for p in ring]
    x0, x1 = min(p[0] for p in alle), max(p[0] for p in alle)
    y0, y1 = min(p[1] for p in alle), max(p[1] for p in alle)
    m = BREITE / (x1 - x0)

    namen, pfade, ringe, mitten = [], [], [], []
    for f in feats:
        teile = []
        for j, ring in enumerate(f["geometry"]["coordinates"]):
            pts = [(round((x - x0) * m, 1), round((y1 - y) * m, 1)) for x, y in _ring(ring, TOLERANZ)]
            teile.append("M" + " ".join(f"{x:g},{y:g}" for x, y in pts) + "Z")
            if j == 0:
                ringe.append(pts[:-1])
        namen.append(f["properties"]["Name"])
        pfade.append("".join(teile))
        mitten.append((sum(p[0] for p in ringe[-1]) / len(ringe[-1]), sum(p[1] for p in ringe[-1]) / len(ringe[-1])))
    zx, zy = mitten[namen.index("Zentrum")]
    abst = [math.dist(mp, (zx, zy)) for mp in mitten]
    weit = max(abst)
    return namen, pfade, [a / weit for a in abst], f"0 0 {BREITE} {round((y1 - y0) * m)}"


def steckbriefe():
    """Je Ortsteil ein kurzer Text: Einwohner heute und Wachstum seit 2010."""
    with open(EINWOHNER, encoding="utf-8") as f:
        zeilen = [r for r in csv.DictReader(f) if r["Sachmerkmal"].strip() == "Einwohner insgesamt"]
    vorher, jetzt = JAHRE
    texte = {}
    for r in zeilen:
        a, b = int(r[vorher]), int(r[jetzt])
        wachstum = round(100 * (b / a - 1))
        texte[r["Gebiet"]] = (f"{b:,} Einwohner".replace(",", ".")
                              + f" · {'+' if wachstum >= 0 else '−'}{abs(wachstum)} % seit {vorher}")
    return texte
