"""Erzeugt en/index.html aus der deutschen index.html (vorher seite_bauen.py ausführen)."""
import sys, os
W = sys.argv[1]
t = open(f"{W}/index.html", encoding="utf-8").read()

def ersetze(alt, neu, mindestens=1):
    global t
    n = t.count(alt)
    assert n >= mindestens, f"nicht gefunden: {alt[:70]!r}"
    t = t.replace(alt, neu)

# --- Kopf, Sprache, Meta ---
ersetze('<html lang="de">', '<html lang="en">')
ersetze('<link rel="canonical" href="https://lukasbaermann.de/">', '<link rel="canonical" href="https://lukasbaermann.de/en/">')
ersetze('content="Lukas Bärmann – freischaffender Künstler in Freiburg im Breisgau. Figurative Zeichnungen in Ölpastellkreide."',
        'content="Lukas Bärmann – independent artist based in Freiburg, Germany. Figurative drawings in oil pastel."')
ersetze('<meta property="og:locale" content="de_DE">', '<meta property="og:locale" content="en_GB">')
ersetze('<meta property="og:url" content="https://lukasbaermann.de/">', '<meta property="og:url" content="https://lukasbaermann.de/en/">')
ersetze('content="Figurative Zeichnungen in Ölpastell. Freischaffender Künstler in Freiburg im Breisgau."',
        'content="Figurative drawings in oil pastel. Independent artist based in Freiburg, Germany."')

# --- Pfade: Seite liegt eine Ebene tiefer ---
for a, b in [('src="bilder/', 'src="../bilder/'), ('"src": "bilder/', '"src": "../bilder/'), ('"th": "bilder/', '"th": "../bilder/'),
             ('href="favicon', 'href="../favicon'), ('href="apple-touch-icon', 'href="../apple-touch-icon'),
             ('href="impressum.html"', 'href="../impressum.html"'), ('href="datenschutz.html"', 'href="../datenschutz.html"')]:
    ersetze(a, b)

# --- Menü ---
ersetze('<a href="#werke">werke</a>', '<a href="#werke">works</a>')
ersetze('<a href="#arbeitsweise">arbeitsweise</a>', '<a href="#arbeitsweise">process</a>')
ersetze('<a href="#ausstellungen">ausstellungen</a>', '<a href="#ausstellungen">exhibitions</a>')
ersetze('<a href="#presse">presse</a>', '<a href="#presse">press</a>')
ersetze('<a href="#kontakt">kontakt</a>', '<a href="#kontakt">contact</a>')
ersetze('<a href="en/" class="sprache" lang="en" hreflang="en">en</a>', '<a href="../" class="sprache" lang="de" hreflang="de">de</a>')
ersetze('aria-label="menü öffnen"', 'aria-label="open menu"')
ersetze("burger.setAttribute('aria-label',auf?'menü schließen':'menü öffnen')", "burger.setAttribute('aria-label',auf?'close menu':'open menu')")

# --- Abschnitte ---
ersetze('<section id="werke" aria-label="werke">', '<section id="werke" aria-label="works">')
ersetze('<h2 class="titel">arbeitsweise</h2>', '<h2 class="titel">process</h2>')
ersetze('<p class="unterzeile">motive und vorgehen.</p>', '<p class="unterzeile">motifs and approach.</p>')
ersetze('Ausgangspunkt meiner Arbeiten sind häufig beiläufige Situationen und Körperhaltungen, die ich im Alltag beobachte oder fotografisch festhalte. In der Zeichnung löse ich die Figuren zunehmend aus ihrem ursprünglichen Umfeld. Dabei geht es mir weniger um eine genaue Wiedergabe als um die Haltung, die Beziehung der Personen zueinander und die Stimmung des beobachteten Moments. Aus dieser Reduktion entwickelt sich anschließend die malerische Arbeit. Meine Werke entstehen in unterschiedlichen Techniken. Neben Acryl- und Ölmalereien bilden Zeichnungen mit Ölpastellkreide auf Leinwand oder Malkarton einen besonderen Schwerpunkt.',
        'My work often begins with incidental situations and postures that I observe in everyday life or capture in photographs. In the drawing, I gradually detach the figures from their original surroundings. I am less interested in exact depiction than in posture, in the relationships between the people, and in the mood of the observed moment. The painterly work then develops out of this reduction. My works are made in a range of techniques: alongside acrylic and oil paintings, drawings in oil pastel on canvas or painting board are a particular focus.')
ersetze('<h2 class="titel">ausstellungen</h2>', '<h2 class="titel">exhibitions</h2>')
ersetze('<p class="unterzeile">seit 2023 freischaffender künstler in freiburg.</p>', '<p class="unterzeile">independent artist in freiburg since 2023.</p>')
ersetze('<h2 class="titel">presse</h2>', '<h2 class="titel">press</h2>')
ersetze('<span>Pressemitteilung</span>', '<span>Press release</span>')
ersetze('<span>Ausgabe Kaiserslautern, 8. Januar 2026</span>', '<span>Kaiserslautern edition, 8 January 2026</span>')
ersetze('<span>5. Januar 2026</span>', '<span>5 January 2026</span>')
ersetze('<span>Ausgabe Freiburg, 25. Juni 2025</span>', '<span>Freiburg edition, 25 June 2025</span>')
ersetze('<h2 class="titel">kontakt</h2>', '<h2 class="titel">contact</h2>')
ersetze('Für Anfragen zu Werken, Ankäufen, Aufträgen oder Ausstellungen freue ich mich über eine Nachricht.',
        'For enquiries about works, purchases, commissions or exhibitions, I look forward to hearing from you.')

# --- Werkangaben, Großansicht, Anfrage ---
ersetze('Ölpastell auf Malpapier, A3', 'Oil pastel on drawing paper, A3')
ersetze('>schließen</button>', '>close</button>')
ersetze('aria-label="bild groß"', 'aria-label="large view"')
ersetze('aria-label="vorheriges bild"', 'aria-label="previous image"')
ersetze('aria-label="nächstes bild"', 'aria-label="next image"')
ersetze('data-anfragen="anfragen" data-verkauft="verkauft"', 'data-anfragen="enquire" data-verkauft="sold"')
ersetze('>anfragen</a>', '>enquire</a>')
ersetze("encodeURIComponent('Anfrage: '+w.t)", "encodeURIComponent('Enquiry: '+w.t)")
ersetze("encodeURIComponent('Hallo Lukas,\\n\\nich interessiere mich für dein Werk „'+w.t+'“ (Oil pastel on drawing paper, A3).\\n\\n')",
        "encodeURIComponent('Hello Lukas,\\n\\nI am interested in your work “'+w.t+'” (oil pastel on drawing paper, A3).\\n\\n')")
ersetze("' groß ansehen'", "' – view large'")
ersetze(' groß ansehen"', ' – view large"')
ersetze('aria-label="vorherige werke"', 'aria-label="previous works"')
ersetze('aria-label="nächste werke"', 'aria-label="next works"')
ersetze('aria-label="vorherige fotos"', 'aria-label="previous photos"')
ersetze('aria-label="nächste fotos"', 'aria-label="next photos"')
ersetze('aria-label="gruppe ${', 'aria-label="group ${')

# --- Fußzeile (rechtliche Seiten bleiben deutsch, wie vom deutschen Recht verlangt) ---
ersetze('>impressum</a>', ' lang="de">legal notice (impressum)</a>')
ersetze('>datenschutz</a>', ' lang="de">privacy (datenschutz)</a>')

# --- Bildbeschreibungen ---
ersetze('alt="Lukas Bärmann mit Blumenvase in der Ausstellung"', 'alt="Lukas Bärmann with a vase of flowers in the exhibition"')
ersetze('alt="Lukas Bärmann im Türrahmen"', 'alt="Lukas Bärmann in a doorway"')
ersetze('alt="Lukas Bärmann läuft durch die Ausstellung"', 'alt="Lukas Bärmann walking through the exhibition"')
ersetze('Arbeitsprozess ', 'Process ')

# --- Suchmaschinen ---
ersetze('<title>Lukas Bärmann – Künstler in Freiburg · Zeichnungen in Ölpastell</title>', '<title>Lukas Bärmann – Artist in Freiburg · Oil Pastel Drawings</title>')
ersetze('<meta property="og:title" content="Lukas Bärmann – Künstler in Freiburg">', '<meta property="og:title" content="Lukas Bärmann – Artist in Freiburg">')
ersetze('"jobTitle":"Bildender Künstler","description":"Freischaffender Künstler in Freiburg im Breisgau, figurative Zeichnungen in Ölpastell."',
        '"jobTitle":"Visual artist","description":"Independent artist based in Freiburg, Germany, making figurative drawings in oil pastel."')
ersetze('"url":"https://lukasbaermann.de/",', '"url":"https://lukasbaermann.de/en/",')

os.makedirs(f"{W}/en", exist_ok=True)
open(f"{W}/en/index.html", "w", encoding="utf-8").write(t)
print("ok")
