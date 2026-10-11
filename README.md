# lukasbaermann.de

Website von Lukas Bärmann, freischaffender Künstler in Freiburg. Reines HTML/CSS/JS: kein Build-Schritt, keine externen Schriften oder Dienste, keine Cookies.

## Inhalte

| Was                         | Wo                                              |
|-----------------------------|-------------------------------------------------|
| Werke (Galerie)             | `index.html`, Abschnitt `#werke`; Bilder in `bilder/werke/` (`werk-XX.jpg` groß, `werk-XX-klein.jpg` Vorschau) |
| Arbeitsweise, Über mich     | `index.html`; Fotos in `bilder/atelier/`, `bilder/portrait.jpg` |
| Ausstellungen, Presse       | `index.html`, Abschnitt `#ausstellungen`        |
| Impressum / Datenschutz     | `impressum.html`, `datenschutz.html`            |

## Seite neu erzeugen

`index.html`, `impressum.html` und `datenschutz.html` werden aus den Skripten in `werkzeug/` erzeugt
(Werkgruppen, Texte, Ausstellungen stehen dort oben im Skript):

```sh
python3 werkzeug/seite_bauen.py .
python3 werkzeug/rechtliches_bauen.py .
python3 werkzeug/englisch_bauen.py .   # en/index.html aus der deutschen Seite
```

Neue deutsche Texte brauchen in `werkzeug/englisch_bauen.py` eine passende Übersetzungszeile,
sonst bricht das Skript mit „nicht gefunden“ ab.

## Veröffentlichen (GitHub Pages)

1. **Settings → Pages**: Source „Deploy from a branch“, Branch `main`, Ordner `/ (root)`.
2. Die Datei `CNAME` enthält `lukasbaermann.de`.
3. DNS bei IONOS:
   - `A`-Records für `@`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `CNAME` für `www`: `lubaer-inc.github.io`
4. Nach der Zertifikatsausstellung „Enforce HTTPS“ aktivieren.

Hinweis: GitHub Pages ist im kostenlosen Tarif nur für öffentliche Repositories verfügbar.
