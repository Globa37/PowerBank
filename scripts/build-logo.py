#!/usr/bin/env python3
"""
VOLTIQ — Markenzeichen aus dem Portraet erzeugen.

    python3 scripts/build-logo.py

Liest assets/brand/portrait-quelle.jpg und schreibt alle Symbolgroessen.
Braucht Pillow und numpy:  pip install Pillow numpy

Ablauf:
  1. Freistellen per Flutfuellung vom Bildrand. Wichtig: der Hintergrund hat
     exakt dieselbe Farbe wie die Licht-Flaechen auf Stirn und Wange, ein
     globales Ersetzen dieser Farbe wuerde also Loecher ins Gesicht stanzen.
     Nur zusammenhaengende Randflaeche wird entfernt.
  2. Die fuenf Flaechenfarben der Vorlage werden auf die Markenpalette
     abgebildet. Das bindet das Bild an die Seite und buegelt zugleich die
     JPEG-Artefakte glatt.
  3. Rund zuschneiden, Kupferring setzen, Groessen ausgeben.
"""
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import os

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUELLBILD = os.path.join(WURZEL, 'assets/brand/portrait-quelle.jpg')
ARBEIT = 1024

# Flaechenfarben der Vorlage -> Markenpalette.
VORLAGE = np.array([
    [249, 223, 188],   # Licht (auch der Hintergrund)
    [232, 180, 122],   # Haut mittel
    [ 19,  26,  45],   # Haar und Linien
    [123,  85,  64],   # Schatten tief
    [183, 130,  90],   # Schatten mittel
], dtype=np.int32)
MARKE = np.array([
    [255, 238, 222],   # warmes Creme
    [214, 132,  66],   # Kupferhaut
    [ 22,  32,  58],   # Navy, leicht angehoben - sonst verschwindet
    [110,  58,  26],   # das Haar im dunklen Abzeichen
    [170,  96,  48],
], dtype=np.uint8)

ABZEICHEN_BG = (9, 13, 26, 255)
KUPFER = (255, 106, 43, 255)


def freistellen(im):
    """Hintergrund per Flutfuellung vom Rand entfernen."""
    flut = im.copy()
    MARKER = (255, 0, 255)
    b, h = flut.size
    for x in range(0, b, 8):
        for y in (0, h - 1):
            if flut.getpixel((x, y)) != MARKER:
                ImageDraw.floodfill(flut, (x, y), MARKER, thresh=26)
    for y in range(0, h, 8):
        for x in (0, b - 1):
            if flut.getpixel((x, y)) != MARKER:
                ImageDraw.floodfill(flut, (x, y), MARKER, thresh=26)
    treffer = np.all(np.asarray(flut) == np.array(MARKER), axis=2)
    maske = Image.fromarray(np.where(treffer, 0, 255).astype('uint8'), 'L')
    return maske.filter(ImageFilter.GaussianBlur(1.2))


def umfaerben(im, maske):
    """Jede Flaechenfarbe auf ihre Markenfarbe abbilden.

    int32 ist Pflicht: die quadrierten Differenzen werden groesser als 32767
    und liefen unter int16 ueber, was die Zuordnung ins Gegenteil verkehrt.
    """
    rgb = np.asarray(im.convert('RGB')).astype(np.int32)
    abstand = ((rgb[:, :, None, :] - VORLAGE[None, None, :, :]) ** 2).sum(axis=3)
    neu = Image.fromarray(MARKE[abstand.argmin(axis=2)].astype('uint8'), 'RGB')
    neu.putalpha(maske)
    return neu


def kopf_ausschnitt(maske):
    """Ausschnitt vom Haaransatz bis zum Kinn bestimmen.

    Unterhalb des Kinns laeuft die Silhouette in Hals und Schulter aus. Als
    Ende wird die Zeile genommen, ab der die Breite unter ein Fuenftel des
    Maximums faellt - das ist verlaesslicher als ein fester Pixelwert.
    """
    a = np.asarray(maske)
    breite = (a > 128).sum(axis=1)
    zeilen = np.nonzero(breite)[0]
    oben = int(zeilen[0])
    maxb = int(breite.max())
    mitte = (oben + int(zeilen[-1])) // 2
    unten = int(zeilen[-1])
    for y in range(mitte, int(zeilen[-1]) + 1):
        if breite[y] < maxb * 0.20:
            unten = y
            break
    spalten = np.nonzero((a[oben:unten] > 128).sum(axis=0))[0]
    return int(spalten[0]), oben, int(spalten[-1]) + 1, unten


def abzeichen(gesicht, ausschnitt, px, rand=0.10, ring=0.019):
    """Kopf vollstaendig in den Kreis setzen.

    Der Kopf muss ganz hineinpassen - Ohren und Kinn duerfen nicht am Rand
    abgeschnitten werden. Deshalb wird nach der laengeren Seite skaliert und
    ringsum ein Rand freigelassen, statt eine feste Hoehe zu setzen.
    """
    C = px * 4
    b = Image.new('RGBA', (C, C), (0, 0, 0, 0))
    ImageDraw.Draw(b).ellipse([0, 0, C - 1, C - 1], fill=ABZEICHEN_BG)

    f = gesicht.crop(ausschnitt)
    platz = C * (1 - 2 * rand)
    faktor = min(platz / f.width, platz / f.height)
    ww, hh = max(1, int(f.width * faktor)), max(1, int(f.height * faktor))
    b.alpha_composite(f.resize((ww, hh), Image.LANCZOS),
                      ((C - ww) // 2, (C - hh) // 2))

    kreis = Image.new('L', (C, C), 0)
    ImageDraw.Draw(kreis).ellipse([0, 0, C - 1, C - 1], fill=255)
    b.putalpha(Image.composite(b.getchannel('A'), Image.new('L', (C, C), 0), kreis))

    r = max(2, int(C * ring))
    ImageDraw.Draw(b).ellipse([r // 2, r // 2, C - 1 - r // 2, C - 1 - r // 2],
                              outline=KUPFER, width=r)
    return b.resize((px, px), Image.LANCZOS)


im = Image.open(QUELLBILD).convert('RGB').resize((ARBEIT, ARBEIT), Image.LANCZOS)
maske = freistellen(im)
gesicht = umfaerben(im, maske)
AUSSCHNITT = kopf_ausschnitt(maske)
print('Kopf-Ausschnitt:', AUSSCHNITT)

ZIELE = {
    'assets/brand/voltiq-mark-512.png': 512,
    'assets/brand/voltiq-mark-192.png': 192,
    'assets/brand/voltiq-mark-96.png':   96,
    'assets/icon-512.png':              512,
    'assets/icon-192.png':              192,
    'assets/apple-touch-icon.png':      180,
}
for pfad, px in ZIELE.items():
    ziel = os.path.join(WURZEL, pfad)
    abzeichen(gesicht, AUSSCHNITT, px).save(ziel, optimize=True)
    print('%-42s %4d px  %6d B' % (pfad, px, os.path.getsize(ziel)))

# Freigestelltes Gesicht ohne Abzeichen - fuer den Startbildschirm.
frei = gesicht.crop(AUSSCHNITT)
frei.thumbnail((560, 560), Image.LANCZOS)
frei.save(os.path.join(WURZEL, 'assets/brand/voltiq-gesicht.png'), optimize=True)
print('assets/brand/voltiq-gesicht.png           freigestellt')
