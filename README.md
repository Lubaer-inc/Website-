# lukasbaermann.de

Website von Lukas Bärmann, freischaffender Künstler. Reines HTML/CSS/JS: kein Build-Schritt, keine externen Abhängigkeiten, keine Cookies.

## Inhalte pflegen

| Was                       | Wo                                     |
|---------------------------|----------------------------------------|
| Werke & Ausstellungen     | `js/content.js`                        |
| Werkbilder                | `images/werke/` (JPG, ca. 2000 px)     |
| Untertitel, Vita, Kontakt | `index.html`                           |
| Impressum / Datenschutz   | `impressum.html`, `datenschutz.html`   |

Platzhalter stehen in eckigen Klammern `[…]` und müssen ersetzt werden.

## Lokal ansehen

`index.html` einfach im Browser öffnen, oder:

```sh
python3 -m http.server 8000
```

## Veröffentlichen (GitHub Pages)

1. Im Repo unter **Settings → Pages** als Quelle den Branch wählen (Ordner `/ (root)`).
2. Die Datei `CNAME` enthält bereits `lukasbaermann.de`.
3. Beim Domain-Anbieter die DNS-Einträge setzen:
   - `A`-Records für `lukasbaermann.de`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `CNAME` für `www`: `<github-benutzername>.github.io`
4. Nach der Zertifikatsausstellung unter **Settings → Pages** „Enforce HTTPS“ aktivieren.

Hinweis: Für GitHub Pages aus einem privaten Repo ist ein kostenpflichtiger GitHub-Plan nötig. Alternativ lässt sich der Ordner per FTP bei jedem Webhoster (z. B. dem Domain-Anbieter) hochladen.
