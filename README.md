# Portfolio-Website „Leipzig in Daten“

Schlichte Website für die Bewerbung: Startseite mit der Berichtsreihe, je Projekt eine Seite mit
Kennzahlen, Steckbrief, den wichtigsten Abbildungen, PDF-Bericht und Link zum Code.

Reines HTML und CSS, kein Framework. Ein Python-Skript erzeugt die Seiten aus `inhalt.py`.

## Bauen

```bash
conda env create -f environment.yml   # einmalig
conda activate portfolio-website
python bauen.py                        # baut site/ und legt das ZIP auf den Desktop
python -m http.server 8000 -d site     # Vorschau unter http://localhost:8000
```

Bilder, Abbildungen und Berichte kommen aus den Projekt-Repos (`results/report/`) und von
`Desktop\Projekte`. `bauen.py` verkleinert sie (WebP) und kopiert sie nach `site/`, das nicht im
Repo liegt.

## Aufbau

| Datei | Inhalt |
|---|---|
| `inhalt.py` | Texte, Kennzahlen, Reihenfolge der Projekte (= Nummer in der Reihe) |
| `bauen.py` | erzeugt die HTML-Seiten, Bilder und das ZIP |
| `stil.css` | Aussehen (Inter, Navy `#17447e`, helle Karten) |
| `schrift/` | Inter (Fließtext) und Space Grotesk (Überschriften, aus Fontsource, SIL OFL), selbst gehostet, keine Google-Server |
| `karte.py`, `karte.js` | Leipzig-Karte der Startseite mit Satellit auf Umlaufbahn |
| `logo.py` | Logo (Glas-Kachel mit Sternbild), auch als Favicon |

## Veröffentlichen

Netlify per ZIP: `Desktop\Projekte\Portfolio\portfolio-website.zip` im Netlify-Projekt unter
„Deploys“ hineinziehen. Die Seiten tragen `noindex`, Suchmaschinen listen sie also nicht.

<details>
<summary>English summary</summary>

Static portfolio site for job applications in Leipzig's city administration. `bauen.py` renders
the start page and one page per project from `inhalt.py`, converts figures and cover photos from
the project repositories to WebP and bundles everything into a ZIP for Netlify. No framework,
self-hosted Inter font, `noindex` on every page.

</details>
