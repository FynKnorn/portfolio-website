"""Logo: Glas-Kachel mit Sternbild (Farbschleier unter Glas, weiße Sterne als Daten-Graph).

Dieselbe Zeichnung dient als Logo in der Kopfleiste (mit Bewegung über stil.css) und als
Tab-Symbol (Favicon, ohne Bewegung).
"""

DEFS = """<defs>
<radialGradient id="logo-a"><stop offset="0" stop-color="#2a78d6"/><stop offset="1" stop-color="#2a78d6" stop-opacity="0"/></radialGradient>
<radialGradient id="logo-b"><stop offset="0" stop-color="#3d5fd0"/><stop offset="1" stop-color="#3d5fd0" stop-opacity="0"/></radialGradient>
<radialGradient id="logo-c"><stop offset="0" stop-color="#2a8bbd"/><stop offset="1" stop-color="#2a8bbd" stop-opacity="0"/></radialGradient>
<linearGradient id="logo-glanz" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".75"/><stop offset=".5" stop-color="#fff" stop-opacity=".1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<clipPath id="logo-kachel"><rect x="2" y="2" width="28" height="28" rx="8"/></clipPath>
</defs>"""

INHALT = """<g clip-path="url(#logo-kachel)"><rect width="32" height="32" fill="#dbe7f7"/>
<circle class="logo-s1" cx="10" cy="11" r="13" fill="url(#logo-a)"/>
<circle class="logo-s2" cx="24" cy="22" r="13" fill="url(#logo-b)"/>
<circle class="logo-s1" cx="25" cy="7" r="9" fill="url(#logo-c)"/>
<rect width="32" height="32" fill="#fff" opacity=".12"/><rect x="2" y="2" width="28" height="14" fill="url(#logo-glanz)"/></g>
<rect x="2.5" y="2.5" width="27" height="27" rx="7.5" fill="none" stroke="#fff" stroke-opacity=".85"/>
<g stroke="#fff" stroke-width="1.1" opacity=".9"><line x1="8" y1="22" x2="13" y2="12"/><line x1="13" y1="12" x2="19" y2="17"/>
<line x1="19" y1="17" x2="24" y2="9"/><line x1="19" y1="17" x2="23" y2="24"/></g>
<g fill="#fff"><circle class="logo-stern" cx="8" cy="22" r="1.5"/><circle cx="13" cy="12" r="1.8"/><circle cx="19" cy="17" r="2.6"/>
<circle class="logo-stern-2" cx="24" cy="9" r="1.5"/><circle class="logo-stern" cx="23" cy="24" r="1.3"/></g>"""


def logo(groesse: int = 28) -> str:
    """Logo zum Einbetten in die Seite (Bewegung kommt aus stil.css)."""
    return f'<svg class="logo" viewBox="0 0 32 32" width="{groesse}" height="{groesse}" aria-hidden="true">{DEFS}{INHALT}</svg>'


def favicon() -> str:
    """Eigenständige SVG-Datei für den Browser-Tab."""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">{DEFS}{INHALT}</svg>\n'
