"""Setzt das Foto einer neuen Zeichnung (ungerahmt, A3 hochkant) ins Passepartout
und gleicht Weißabgleich/Helligkeit an die bestehenden Montagen an.

Aufruf:
    python3 werkzeug/neues_werk.py FOTO NUMMER [--vorlage MONTAGE.png]

Ergebnis:
    werkzeug/montagen/werk-NN_Passepartout.png   (3000 x 3000, wie die bisherigen Montagen)
    bilder/werke/werk-NN.jpg, werk-NN-klein.jpg  (für die Website)
Danach Titel und Gruppe in werkzeug/seite_bauen.py (GRUPPEN) eintragen und die Seite neu erzeugen.
"""
import sys, os, argparse
import numpy as np
import cv2
from PIL import Image, ImageOps

HIER = os.path.dirname(os.path.abspath(__file__))
WURZEL = os.path.dirname(HIER)

# Geometrie der Montagen (3000 x 3000): Fenster im Passepartout
FX0, FY0, FX1, FY1 = 897, 627, 2105, 2369
# Zuschnitt für die Website (wie bei den bestehenden Werken)
WEB_BOX = (525, 244, 2452, 2779)
# Papierton der bestehenden Montagen (Median des unbemalten Papiers)
PAPIER_ZIEL = np.array([234.0, 229.0, 223.0])
RAND = 28  # Breite des Schattens am Fensterrand, der aus der Vorlage übernommen wird


def blatt_finden(bgr):
    """Findet die vier Ecken des Blatts (größte helle, viereckige Fläche)."""
    h, w = bgr.shape[:2]
    s = 1200 / max(h, w)
    klein = cv2.resize(bgr, (int(w * s), int(h * s)), interpolation=cv2.INTER_AREA)
    grau = cv2.GaussianBlur(cv2.cvtColor(klein, cv2.COLOR_BGR2GRAY), (7, 7), 0)
    _, bin_ = cv2.threshold(grau, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    bin_ = cv2.morphologyEx(bin_, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    konturen, _ = cv2.findContours(bin_, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not konturen:
        raise SystemExit("Kein Blatt gefunden – bitte Foto mit allen vier Ecken auf dunklerem Untergrund.")
    k = max(konturen, key=cv2.contourArea)
    if cv2.contourArea(k) < 0.15 * klein.shape[0] * klein.shape[1]:
        raise SystemExit("Blatt zu klein im Bild – bitte näher heran fotografieren.")
    umfang = cv2.arcLength(k, True)
    for eps in (0.01, 0.02, 0.03, 0.05):
        ecken = cv2.approxPolyDP(k, eps * umfang, True)
        if len(ecken) == 4:
            break
    else:
        ecken = cv2.boxPoints(cv2.minAreaRect(k))
    p = ecken.reshape(4, 2).astype(np.float32) / s
    # sortieren: oben links, oben rechts, unten rechts, unten links
    summe, diff = p.sum(1), np.diff(p, axis=1).ravel()
    return np.array([p[np.argmin(summe)], p[np.argmin(diff)], p[np.argmax(summe)], p[np.argmax(diff)]], np.float32)


def entzerren(bgr, ecken):
    """Zieht das Blatt gerade auf A3-Hochformat, etwas größer als das Fenster (Passepartout deckt den Rand)."""
    fw, fh = FX1 - FX0, FY1 - FY0
    H = int(round(fh * 1.03)); W = int(round(H / 1.4142))
    ziel = np.array([[0, 0], [W - 1, 0], [W - 1, H - 1], [0, H - 1]], np.float32)
    M = cv2.getPerspectiveTransform(ecken, ziel)
    blatt = cv2.warpPerspective(bgr, M, (W, H), flags=cv2.INTER_LANCZOS4)
    x0, y0 = (W - fw) // 2, (H - fh) // 2
    return blatt[y0:y0 + fh, x0:x0 + fw]


def papier_maske(rgb):
    """Unbemaltes Papier: hell, wenig gesättigt, mit Sicherheitsabstand zu Strichen."""
    hsv = cv2.cvtColor(np.clip(rgb, 0, 255).astype(np.uint8), cv2.COLOR_RGB2HSV)
    v, s = hsv[..., 2].astype(float), hsv[..., 1].astype(float)
    # lokal relativ bewerten, damit auch dunkler ausgeleuchtete Bereiche als Papier zählen
    v_lokal = cv2.dilate(cv2.GaussianBlur(v, (0, 0), 6), np.ones((61, 61), np.uint8))
    m = (v > v_lokal * 0.90) & (s < 60)
    m = cv2.erode(m.astype(np.uint8), np.ones((9, 9), np.uint8)) > 0
    return m


def beleuchtungsfeld(rgb, m, zellen=48):
    """Papierfarbe je Kanal großflächig schätzen (Zeichnung ausgespart, Lücken aufgefüllt)."""
    h, w = rgb.shape[:2]
    gw, gh = zellen, int(round(zellen * h / w))
    mk = cv2.resize(m.astype(np.float32), (gw, gh), interpolation=cv2.INTER_AREA)
    feld = np.zeros((gh, gw, 3), np.float32)
    for k in range(3):
        summe = cv2.resize((rgb[..., k] * m).astype(np.float32), (gw, gh), interpolation=cv2.INTER_AREA)
        feld[..., k] = summe / np.maximum(mk, 1e-6)
    luecke = (mk < 0.25).astype(np.uint8)
    for k in range(3):   # Zellen ohne Papier aus der Umgebung auffüllen
        f = feld[..., k]; ok = luecke == 0
        f8 = np.clip(f, 0, 255).astype(np.uint8)
        f[~ok] = cv2.inpaint(f8, luecke, 5, cv2.INPAINT_TELEA)[~ok]
        feld[..., k] = cv2.GaussianBlur(f, (0, 0), 1.0)
    return cv2.resize(feld, (w, h), interpolation=cv2.INTER_CUBIC)


def weissabgleich(rgb):
    """Ausleuchtung und Farbstich pro Kanal glätten, Papier auf den Ton der bestehenden Montagen bringen.
    Feine Papierstruktur und Kreidefarben bleiben erhalten."""
    rgb = rgb.astype(np.float32)
    m = papier_maske(rgb)
    feld = beleuchtungsfeld(rgb, m)
    flach = rgb / np.maximum(feld, 1)            # Papier = 1.0
    out = flach * PAPIER_ZIEL[None, None, :]
    # Feinabgleich auf den Median des Papiers
    m2 = papier_maske(out)
    out *= (PAPIER_ZIEL / np.median(out[m2], axis=0))[None, None, :]
    return np.clip(out, 0, 255)


def auf_fenster_bringen(rgb):
    """Für Fotos, die nur das Blatt zeigen: unten bündig mit dem Fenster (Signatur nah am Passepartout),
    fehlende Höhe nur OBEN ergänzen – mit echter Papierstruktur aus dem oberen Blattrand (gespiegelt)."""
    fw, fh = FX1 - FX0, FY1 - FY0
    h, w = rgb.shape[:2]
    ziel = fw / fh
    if w / h > ziel:
        fehlt = int(round(w / ziel)) - h
        rand = rgb[:min(h, max(fehlt, 1) + 60)]
        # gespiegelter oberer Rand, mehrfach falls nötig, mit weicher Naht
        stuecke = []
        while sum(s.shape[0] for s in stuecke) < fehlt:
            stuecke.append(rand[::-1] if len(stuecke) % 2 == 0 else rand)
        oben = np.concatenate(stuecke, 0)[-fehlt:] if stuecke else rgb[:0]
        oben = oben[::-1][::-1]
        voll = np.concatenate([oben, rgb], 0)
    else:
        # zu hoch: oben abschneiden, unten bleibt bündig
        H = int(round(w / ziel)); voll = rgb[h - H:]
    return cv2.resize(np.clip(voll, 0, 255).astype(np.float32), (fw, fh), interpolation=cv2.INTER_AREA)


# Papierstruktur der bestehenden Montagen (Standardabweichung der Helligkeit im leeren Papier)
STRUKTUR_ZIEL = {"fein": 3.6, "mittel": 0.85, "grob": 0.6}  # Zielwerte im Messfeld: fein ~2.5, mittel ~0.6


def struktur_angleichen(rgb):
    """Körnung des Papiers an die bestehenden Montagen angleichen – aus der eigenen Struktur des Fotos
    verstärkt (kein künstliches Muster), nur auf unbemaltem Papier."""
    rgb = rgb.astype(np.float32)
    g = rgb.mean(2)
    m = papier_maske(rgb)
    # nur deutlich abseits der Striche verändern, sonst entstehen helle Säume an den Konturen
    sicher = cv2.erode(m.astype(np.uint8), np.ones((25, 25), np.uint8)).astype(np.float32)
    weich = cv2.GaussianBlur(sicher, (0, 0), 5)
    b2, b12 = cv2.GaussianBlur(g, (0, 0), 2), cv2.GaussianBlur(g, (0, 0), 12)
    fein, mittel = g - b2, b2 - b12
    zusatz = np.zeros_like(g)
    # feine Körnung ÖRTLICH angleichen (dunkle Fotoecken werden durch den Lichtausgleich sonst körniger)
    lokal = np.sqrt(cv2.GaussianBlur(np.where(m, fein, 0) ** 2, (0, 0), 30) /
                    np.maximum(cv2.GaussianBlur(m.astype(np.float32), (0, 0), 30), 1e-3))
    zusatz += fein * (np.clip(STRUKTUR_ZIEL["fein"] * 0.69 / np.maximum(lokal, 1e-3), 0.4, 3.5) - 1)
    for band, ziel in ((mittel, STRUKTUR_ZIEL["mittel"]),):
        ist = band[m].std()
        faktor = np.clip(ziel / max(ist, 1e-3), 0.4, 3.5)  # auch abschwächen, wenn das Foto körniger ist
        zusatz += band * (faktor - 1)
    # sehr leichte großflächige Wolkigkeit wie bei echten Fotos von Papier
    rng = np.random.default_rng(7)
    wolke = cv2.resize(rng.normal(0, 1, (12, 9)).astype(np.float32), (g.shape[1], g.shape[0]), interpolation=cv2.INTER_CUBIC)
    zusatz += wolke / max(wolke.std(), 1e-3) * STRUKTUR_ZIEL["grob"]
    return np.clip(rgb + (zusatz * weich)[..., None], 0, 255)


def montieren(blatt_rgb, vorlage_pfad):
    vor = np.asarray(Image.open(vorlage_pfad).convert("RGB")).astype(float)
    fenster_alt = vor[FY0:FY1, FX0:FX1]
    # Schatten/Kante am Fensterrand aus der Vorlage übernehmen (Verhältnis zum Papierton)
    papier_alt = np.median(fenster_alt[papier_maske(fenster_alt)], axis=0)
    schatten = np.clip(fenster_alt / papier_alt[None, None, :], 0.3, 1.0).mean(2)
    h, w = schatten.shape
    yy, xx = np.mgrid[0:h, 0:w]
    abstand = np.minimum(np.minimum(xx, w - 1 - xx), np.minimum(yy, h - 1 - yy))
    gewicht = np.clip(1 - abstand / RAND, 0, 1)
    faktor = 1 - gewicht * (1 - schatten)
    neu = vor.copy()
    neu[FY0:FY1, FX0:FX1] = blatt_rgb * faktor[..., None]
    return Image.fromarray(np.clip(neu, 0, 255).astype(np.uint8))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("foto"); ap.add_argument("nummer", type=int)
    ap.add_argument("--vorlage", default=os.path.join(HIER, "montagen", "vorlage_Passepartout.png"))
    ap.add_argument("--zugeschnitten", action="store_true", help="Foto zeigt nur das Blatt (kein Hintergrund)")
    ap.add_argument("--test", metavar="ORDNER", help="nur Testbild in ORDNER speichern, nichts in die Website schreiben")
    a = ap.parse_args()
    foto = ImageOps.exif_transpose(Image.open(a.foto)).convert("RGB")
    bgr = cv2.cvtColor(np.asarray(foto), cv2.COLOR_RGB2BGR)
    if a.zugeschnitten:
        blatt = auf_fenster_bringen(weissabgleich(np.asarray(foto).astype(float)))
    else:
        blatt = entzerren(bgr, blatt_finden(bgr))
        blatt = weissabgleich(cv2.cvtColor(blatt, cv2.COLOR_BGR2RGB))
    blatt = struktur_angleichen(blatt)
    montage = montieren(blatt, a.vorlage)
    if a.test:
        os.makedirs(a.test, exist_ok=True)
        ziel = os.path.join(a.test, f"werk-{a.nummer:02d}_Passepartout.png"); montage.save(ziel)
        print("Testbild:", ziel); return
    os.makedirs(os.path.join(HIER, "montagen"), exist_ok=True)
    nn = f"{a.nummer:02d}"
    montage.save(os.path.join(HIER, "montagen", f"werk-{nn}_Passepartout.png"))
    web = montage.crop(WEB_BOX)
    g = web.copy(); g.thumbnail((1600, 1600), Image.LANCZOS)
    g.save(os.path.join(WURZEL, "bilder", "werke", f"werk-{nn}.jpg"), "JPEG", quality=84, optimize=True, progressive=True)
    k = web.copy(); k.thumbnail((700, 700), Image.LANCZOS)
    k.save(os.path.join(WURZEL, "bilder", "werke", f"werk-{nn}-klein.jpg"), "JPEG", quality=80, optimize=True, progressive=True)
    print(f"fertig: werk-{nn}")


if __name__ == "__main__":
    main()
