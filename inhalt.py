"""Inhalte der Portfolio-Website.

Die Reihenfolge in PROJEKTE ist die Reihenfolge auf der Website (nach Relevanz für die
Bewerbung, Nr. 1 zuerst) und entspricht den Nummern der Berichtsreihe „Leipzig in Daten“.
"""

from pathlib import Path

PROJEKTE_ORDNER = Path.home() / "code" / "projekte"
DESKTOP = Path("/mnt/c/Users/PC/Desktop/Projekte")
GITHUB = "https://github.com/FynKnorn"

PERSON = {
    "name": "Fyn Knorn",
    "kicker": "Leipzig in Daten",
    "titel": "Offene Daten über Leipzig, so aufbereitet, dass man sie versteht.",
    "lead": "Stadtentwicklung, Klima und Mobilität in Leipzig, untersucht mit offenen Daten "
            "und als Bericht für alle aufgeschrieben.",
    "mail": "fynyork@gmail.com",
}

PROJEKTE = [
    {
        "slug": "wandel-der-ortsteile",
        "repo": "leipzig-stadtentwicklung",
        "titel": "Wandel der Leipziger Ortsteile 2011 bis 2025",
        "untertitel": "Wo die Aufwertung gerade ankommt: ein Lagebild für alle 63 Ortsteile, "
                      "das sich selbst überprüft",
        "kernaussage": "Die Aufwertung wandert durch den Leipziger Osten.",
        "pdf": DESKTOP / "Stadtentwicklung" / "Wandel-der-Ortsteile_Leipzig_2026-11.pdf",
        "foto": ("Völkerschlachtdenkmal", "RealPixelStreet", "CC BY-SA 4.0",
                 "https://creativecommons.org/licenses/by-sa/4.0/deed.de"),
        "themen": ["Statistik", "Hauptkomponenten", "Clustering", "Rückblick-Test"],
        "steckbrief": [
            ("Frage", "Wie haben sich die 63 Ortsteile seit 2011 verändert, und wo kommt die "
                      "Aufwertung als Nächstes an?"),
            ("Daten", "48 kleinräumige Reihen des Amts für Statistik und Wahlen: Bürgerumfrage "
                      "und Bevölkerungsstatistik, 2011 bis 2025."),
            ("Methode", "Umfragewerte per Gauß-Prozess geglättet, zu einem Aufwertungs-Index "
                        "verdichtet, sechs Entwicklungstypen gebildet. Eine „Zeitmaschine“ sucht, "
                        "welcher Ortsteil heute so dasteht wie ein anderer vor zehn Jahren."),
            ("Prüfung", "Rückblick-Test mit Daten bis 2015 und 2019, Halbzeit-Prüfung mit der "
                        "SGB-II-Quote 2025, Abgleich mit den Erhaltungsgebieten der Stadt."),
        ],
        "kacheln": [
            ("63", "Ortsteile, 13 Merkmale, 2011 bis 2025"),
            ("+53 %", "Grundmiete in Lindenau seit 2011/13"),
            ("0,38", "Trefferqualität im Rückblick-Test, besser als jede einfache Regel"),
            ("6 von 10", "stärksten Hinweisen liegen in einem Erhaltungsgebiet"),
        ],
        "abbildungen": ["karte_entwicklung", "typen_entwicklung", "zeitmaschine", "ausblick"],
    },
    {
        "slug": "entsiegelung",
        "repo": "leipzig-entsiegelung",
        "titel": "Entsiegelungspotenziale der Leipziger Ortsteile 2025",
        "untertitel": "Versiegelung, Hitze und Grün in allen 63 Ortsteilen: wo es sich am meisten "
                      "lohnt, Asphalt aufzubrechen und Bäume zu pflanzen",
        "kernaussage": "2.591 Flächen ließen sich entsiegeln, Höfe im Blockinneren bringen am meisten.",
        "pdf": DESKTOP / "Entsiegelung" / "Entsiegelungspotenziale_Leipzig_2026-11.pdf",
        "foto": ("Holzbrücke im Johannapark", "Frank Vincentz", "CC BY-SA 3.0",
                 "https://creativecommons.org/licenses/by-sa/3.0/deed.de"),
        "themen": ["Deep Learning", "Luftbilder", "Hitzemodell", "Optimierung"],
        "steckbrief": [
            ("Frage", "Wo lohnt es sich am meisten, Asphalt aufzubrechen und Bäume zu pflanzen?"),
            ("Daten", "Luftbild Sachsen 2025 auf 20 cm, Oberflächen- und Geländemodell (GeoSN), "
                      "Landsat-Sommeraufnahmen 2018 bis 2025, Stadtgrundkarte, OpenStreetMap."),
            ("Methode", "Ein U-Net erkennt Versiegelung im Luftbild, ein Hitzemodell schätzt die "
                        "Abkühlung, ein Optimierer verteilt 1000 Bäume dorthin, wo sie den meisten "
                        "Menschen nützen."),
            ("Prüfung", "Modell an fremden Kacheln geprüft, Gegenprobe mit Gradient Boosting, "
                        "Steckbriefe der besten Flächen von Hand am Luftbild kontrolliert."),
        ],
        "kacheln": [
            ("26 %", "von Leipzig versiegelt, auf 20 cm genau erkannt"),
            ("2.591", "Flächen mit zusammen 472 ha entsiegelbar"),
            ("−0,7 °C", "im 100-m-Feld, wenn 1.000 m² Asphalt Rasen und Bäumen weichen"),
            ("1,5 ×", "mehr Kühlung durch klug verteilte Bäume"),
        ],
        "abbildungen": ["leipzig_versiegelung", "leipzig_hitze", "nutzen", "baeume"],
    },
    {
        "slug": "naechtliche-erreichbarkeit",
        "repo": "leipzig-oepnv-anbindung",
        "titel": "Nächtliche Erreichbarkeit der Leipziger Ortsteile 2026",
        "untertitel": "Nachts mit Bus und Bahn: Heimwege vom Ausgehen und Wege zu Freunden, Stunde "
                      "für Stunde, und welche Verbesserung im Nachtnetz den meisten Menschen hilft",
        "kernaussage": "Nachts rückt Leipzig auseinander: 38 statt 28 Minuten bis nach Hause.",
        "pdf": DESKTOP / "OEPNV-Anbindung" / "Naechtliche-Erreichbarkeit_Leipzig_2026-11.pdf",
        "foto": ("Straßenbahnen auf dem Augustusplatz", "Frank Vincentz", "CC BY-SA 3.0",
                 "https://creativecommons.org/licenses/by-sa/3.0/deed.de"),
        "themen": ["Erreichbarkeit", "Fahrplandaten", "Szenarien"],
        "steckbrief": [
            ("Frage", "Wie kommt man nachts mit Bus und Bahn nach Hause oder zu Freunden, und "
                      "welche Verbesserung im Nachtnetz hilft den meisten?"),
            ("Daten", "Fahrplan des Mitteldeutschen Verkehrsverbunds (GTFS), Zensus 2022 auf "
                      "100 m, Ortsteile der Stadt, Bars und Clubs aus OpenStreetMap."),
            ("Methode", "Reisezeiten von Tür zu Tür für jede Stunde der Woche, Heimwege aus den "
                        "Ausgehvierteln, durchgerechnete Szenarien für das Nachtnetz."),
            ("Prüfung", "Stichproben von Hand gegen die Fahrplanauskunft geprüft."),
        ],
        "kacheln": [
            ("38 statt 28", "Minuten bis nach Hause, nachts statt tagsüber"),
            ("56 statt 575", "Fahrten pro Stunde um 2 Uhr nachts"),
            ("21 statt 51", "Minuten: Nachts schlägt das Rad den Nachtbus"),
            ("−5,2 Min.", "je Weg mit Nachtbussen alle 30 Minuten"),
        ],
        "abbildungen": ["zeitkarte", "netz_tag_nacht", "schluss_kurve", "massnahmen"],
    },
]

# Projekte, die noch entstehen (Karte ohne eigene Seite)
IN_ARBEIT = [
    {
        "titel": "Luftlage in Leipzig",
        "text": "Ein eigener Feinstaubsensor auf dem Dach und die Bürgersensoren der Stadt, "
                "abgeglichen mit den amtlichen Messstationen.",
        "themen": ["Sensorik", "Zeitreihen", "Kalibrierung"],
        "stand": "erscheint Anfang 2027",
    },
]
