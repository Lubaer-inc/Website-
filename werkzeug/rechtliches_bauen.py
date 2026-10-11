"""Erzeugt impressum.html und datenschutz.html im Stil der Startseite."""
import sys
W = sys.argv[1]
SEITEN = {
 "impressum.html": ("impressum", "Impressum", '<h2>Angaben gemäß § 5 DDG</h2>\n<p>Dr. Lukas Bärmann<br>Erwinstraße 32<br>79102 Freiburg im Breisgau</p>\n<h2>Kontakt</h2>\n<p>E-Mail: <a href="mailto:art@lukasbaermann.de">art@lukasbaermann.de</a></p>\n<h2>Verantwortlich für den Inhalt</h2>\n<p>Dr. Lukas Bärmann, Anschrift wie oben</p>\n<h2>Urheberrecht</h2>\n<p>Alle auf dieser Website gezeigten Werke und Fotografien sind urheberrechtlich geschützt. Jede Verwendung außerhalb der Grenzen des Urheberrechts bedarf der vorherigen schriftlichen Zustimmung.</p>'),
 "datenschutz.html": ("datenschutz", "Datenschutzerklärung", '<h2>1. Verantwortlicher</h2>\n<p>Dr. Lukas Bärmann, Erwinstraße 32, 79102 Freiburg im Breisgau · E-Mail: <a href="mailto:art@lukasbaermann.de">art@lukasbaermann.de</a></p>\n<h2>2. Hosting über GitHub Pages</h2>\n<p>Diese Website wird bei GitHub Pages gehostet, einem Dienst der GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA. Beim Aufruf der Seite verarbeitet GitHub technisch notwendige Daten, insbesondere Ihre IP-Adresse, Datum und Uhrzeit des Zugriffs, die aufgerufene Seite sowie Browser- und Systeminformationen. Diese Daten werden zur Auslieferung und Absicherung der Website benötigt. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse an einer sicheren und zuverlässigen Bereitstellung der Website). Dabei kann eine Übermittlung in die USA erfolgen. Weitere Informationen: <a href="https://docs.github.com/de/site-policy/privacy-policies/github-general-privacy-statement" target="_blank" rel="noopener">Datenschutzerklärung von GitHub</a>.</p>\n<h2>3. Keine Cookies, kein Tracking</h2>\n<p>Diese Website setzt keine Cookies, verwendet keine Analyse- oder Trackingdienste und lädt keine Schriftarten oder Inhalte von Drittanbietern nach.</p>\n<h2>4. Kontakt per E-Mail</h2>\n<p>Wenn Sie mir eine E-Mail schreiben, verarbeite ich Ihre Angaben ausschließlich zur Bearbeitung Ihrer Anfrage (Art. 6 Abs. 1 lit. b bzw. f DSGVO) und lösche sie, sobald sie dafür nicht mehr erforderlich sind und keine gesetzlichen Aufbewahrungspflichten bestehen.</p>\n<h2>5. Externe Links</h2>\n<p>Diese Website enthält Links zu Instagram und Presseartikeln. Erst wenn Sie einen solchen Link anklicken, werden Daten an den jeweiligen Anbieter übertragen.</p>\n<h2>6. Ihre Rechte</h2>\n<p>Sie haben das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit sowie Widerspruch gegen die Verarbeitung (Art. 15–21 DSGVO). Außerdem können Sie sich bei einer Datenschutz-Aufsichtsbehörde beschweren, z. B. beim Landesbeauftragten für den Datenschutz und die Informationsfreiheit Baden-Württemberg.</p>'),
}
for datei, (titel, langtitel, inhalt) in SEITEN.items():
    page = f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<link rel="icon" href="favicon.ico" sizes="48x48">
<link rel="icon" href="favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="favicon-192.png" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<title>{titel} – lukas bärmann</title>
<style>
  :root{{--ink:#141414;--muted:#7a7a7a;--line:#dcdcdc;--sans:"Helvetica Neue",Helvetica,Arial,sans-serif;--mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;--rand:clamp(20px,6.5vw,100px)}}
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{background:#fff;color:var(--ink);font-family:var(--sans);font-weight:300;font-size:18px;line-height:1.6;-webkit-font-smoothing:antialiased}}
  a{{color:inherit;text-decoration:none}}
  .rand{{padding-left:var(--rand);padding-right:var(--rand)}}
  header{{display:flex;justify-content:space-between;align-items:baseline;gap:20px;padding-top:30px;padding-bottom:26px}}
  .logo{{font-size:clamp(1.6rem,2.6vw,2.25rem);font-weight:400;letter-spacing:-.035em}}
  .zurueck{{color:var(--muted);font-size:1rem;font-weight:400}} .zurueck:hover{{color:var(--ink)}}
  main{{padding-top:90px;padding-bottom:100px;max-width:calc(820px + 2 * var(--rand))}}
  h1{{font-size:clamp(2.8rem,6.2vw,6.2rem);font-weight:400;letter-spacing:-.065em;line-height:.95;margin-left:-.04em}}
  .strich{{width:90px;height:1px;background:var(--line);margin:34px 0 22px}}
  h2{{font-size:1.15rem;font-weight:400;margin-top:38px;margin-bottom:6px}}
  p a{{border-bottom:1px solid var(--line)}} p a:hover{{border-color:var(--ink)}}
  footer{{display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px;padding-top:40px;padding-bottom:40px;font-family:var(--mono);font-size:.8rem;color:var(--muted)}}
  footer a{{margin-left:22px}} footer a:hover{{color:var(--ink)}}
  :focus-visible{{outline:1px solid var(--ink);outline-offset:3px}}
  @media (max-width:760px){{ body{{font-size:16px}} header{{padding-top:16px}} main{{padding-top:50px}} footer{{flex-direction:column}} footer a{{margin:0 22px 0 0}} }}
</style>
</head>
<body>
<header class="rand">
  <a href="index.html" class="logo">lukas bärmann</a>
  <a href="index.html" class="zurueck">← zur startseite</a>
</header>
<main class="rand">
  <h1>{titel}</h1>
  <div class="strich"></div>
  {inhalt}
</main>
<footer class="rand">
  <span>© copyright 2026 lukas bärmann</span>
  <span><a href="impressum.html">impressum</a><a href="datenschutz.html">datenschutz</a></span>
</footer>
</body>
</html>
'''
    open(f"{W}/{datei}", "w", encoding="utf-8").write(page)
print("ok")
