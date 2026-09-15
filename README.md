# VOLTIQ MAG — Landingpage

Statische Verkaufsseite für eine magnetische 5000-mAh-Powerbank. Kein Build,
kein Framework, keine Abhängigkeiten: HTML, CSS und etwas Vanilla-JS. Der
Ordner lässt sich unverändert auf jeden Webspace oder zu Netlify, Cloudflare
Pages und GitHub Pages hochladen.

```
python3 -m http.server 8000   # lokal ansehen: http://localhost:8000
```

## Aufbau

| Datei | Zweck |
| --- | --- |
| `index.html` | Landingpage. Der Hero *ist* der Konfigurator — Farbwahl, Preis und Kaufbutton stehen über der Falz. CSS und JS liegen inline. |
| `assets/checkout.js` | Anbindung an den Zahlungsanbieter. Einzige Stelle mit Preis und Artikeldaten. |
| `index.html` → `#material` | Zwei Detailaufnahmen (Makro 07, Magnetring 04). Echte Produktfotos tragen den Eindruck von Wertigkeit weiter als jeder Effekt. |
| `assets/page.css` | Stylesheet der Unterseiten. Gleiche Tokens wie `index.html`. |
| `assets/fonts/` | Inter, Inter Tight, JetBrains Mono — lokal, damit keine Besucher-IP an Google geht. |
| `assets/img/` | Produktbilder in mehreren Breiten als WebP, mit JPG/PNG als Rückfall. |
| `versand`, `rueckgabe`, `garantie`, `batterien`, `kontakt` | Serviceseiten, `index,follow`. |
| `impressum`, `datenschutz`, `agb`, `widerruf` | Pflichttexte, `noindex,follow`. |
| `robots.txt`, `sitemap.xml` | Nur die indexierbaren Seiten stehen in der Sitemap. |
| `404.html` | Fehlerseite. Muss der Server aktiv ausliefern — siehe Hinweis auf der Seite selbst. |

### Farbwechsel

Die gewählte Farbe setzt `--glow` auf dem `<html>`-Element. Daran hängen
Aurora, Magnetringe, Partikel und Akzentkanten. Der Kaufbutton bleibt
absichtlich immer kupfern: ein Button, der die Farbe wechselt, verliert seine
Signalwirkung.

### Bilder

`assets/img/` enthält die fertigen Ableitungen. Ungenutzt und als Reserve
vorhanden sind noch 05 (Hero iPhone), 06 (Desk) und 09 (Travel). Die Erzeugungsskripte (`scripts/build-images.py`,
`scripts/fetch-fonts.py`) sind in älteren Kommentaren erwähnt, aber nie ins
Repo gelangt — wer die Bilder neu ableiten will, muss sie neu schreiben.

## Markenzeichen

Das Zeichen ist ein Portraet — dasselbe soll ueber alle Shops hinweg
wiederkehren. Es wird nicht von Hand gepflegt, sondern erzeugt:

```
pip install Pillow numpy
python3 scripts/build-logo.py
```

Quelle ist `assets/brand/portrait-quelle.jpg`. Das Skript stellt den Kopf frei,
bildet die fuenf Flaechenfarben der Vorlage auf die Markenpalette ab und
schreibt alle Symbolgroessen (`assets/brand/`, `assets/icon-*.png`,
`assets/apple-touch-icon.png`).

Zwei Dinge, die beim Nachbauen leicht schiefgehen:

- **Nicht per Farbe freistellen.** Der Hintergrund hat exakt denselben Ton wie
  die Licht-Flaechen auf Stirn und Wange. Ein globales Ersetzen dieser Farbe
  stanzt Loecher ins Gesicht. Das Skript flutet deshalb nur vom Bildrand.
- **Groesse.** Unter etwa 30 px zerfaellt ein Gesicht zu Matsch. Deshalb steht
  das Zeichen in der Kopfzeile auf 34 px und nicht kleiner.
- **Einpassung nicht schaetzen.** Der Kopf muss ganz in den Kreis passen,
  Ohren und Kinn duerfen nicht am Rand abgeschnitten werden. Das Skript
  bestimmt den Ausschnitt aus der Silhouette (Ende dort, wo die Breite unter
  ein Fuenftel des Maximums faellt - also am Hals) und skaliert nach der
  laengeren Seite mit 10 Prozent Rand. Feste Prozentwerte hatten das Kinn
  um ein halbes Prozent ueber den Kreisrand geschoben.

Fuer den Browser-Tab bleibt es beim Blitz (`assets/favicon.svg`): bei 16 px
ist ein Gesicht nicht mehr lesbar, ein Blitz schon. Beide gehoeren zum selben
System — das Portraet ist das Zeichen, der Blitz das Signet, und er steht auch
an der Stelle des I in VOLT*I*Q.

### Startbildschirm

`index.html` zeigt beim ersten Aufruf je Sitzung einen Vorhang mit Portraet,
Ladungsring und Schriftzug (`#intro`). Er blendet sich per CSS-Animation aus,
damit er auch ohne JavaScript verschwindet, **und** wird zusaetzlich per
`setTimeout` nach 2,6 s entfernt. Die Doppelung ist Absicht: bliebe der
Vollbild-Layer stehen, waere der Shop unbedienbar — das ist zu teuer, um es
einer Animation allein zu ueberlassen. Bei `prefers-reduced-motion` entfaellt
er ganz, und ein Klick schliesst ihn sofort.

### Herkunft der Bilder

Die Originale liegen auf dem Higgsfield-CDN und waren in der ersten Fassung
direkt verlinkt. Die lokalen Ableitungen im Repo stammen von dort. Falls je
eine größere Auflösung gebraucht wird, sind das die Quellen:

```
https://d8j0ntlcm91z4.cloudfront.net/user_3JGnRZcljS9ZEfmpThKsT6DATn2/hf_20260914_223113_<ID>.png
```

| Datei | ID |
| --- | --- |
| 01-silber-freigestellt | `e62443dc-bb8e-4de2-a4f7-c129291cdac5` |
| 02-orange-freigestellt | `5acfb82c-1314-4ef0-9de0-42fe4595c6cc` |
| 03-blau-freigestellt | `ef09bf6f-ac7c-4806-abcf-0299af2ef2e9` |
| 04-rueckseite-magnetring | `c7f361ab-771b-4021-876a-7ec947a84fbe` |
| 05-hero-iphone | `1c15a848-6137-47a3-a574-debdc499ebe7` |
| 06-desk-szene | `b01a6945-5210-4ab1-afa8-a6ffc04792ad` |
| 07-makro-detail | `243c4c86-647f-4fbb-9723-028b4805207e` |
| 08-nacht-lifestyle | `2e3182b9-440b-4a33-afb6-3780c946ecfa` |
| 09-travel-flatlay | `ccc81738-caf2-45b2-afc5-c4009d02dcd7` |
| 10-lineup-3-farben | `3f1032ed-1207-4a40-9004-b2191896d0ad` |

Fremdes Hosting ist kein Dauerzustand — die lokalen Kopien im Repo sind die
maßgeblichen. Die CDN-Links stehen hier nur als Rückfallebene.

## Deploy zu Vercel

Der Ordner ist eine statische Seite ohne Build. Vercel erkennt das von selbst.

1. [vercel.com/new](https://vercel.com/new) öffnen und dieses GitHub-Repo importieren.
2. Framework Preset: **Other**. Build Command und Output Directory leer lassen.
3. Deploy. Nach etwa einer Minute steht die Seite unter
   `https://<projektname>.vercel.app` — dieser Link ist öffentlich und lässt
   sich weitergeben.

Jeder Push auf `main` erzeugt danach ein neues Produktiv-Deployment, jeder
Push auf einen anderen Branch eine Preview-URL.

### Was `vercel.json` festlegt

- **Schriften** ein Jahr `immutable` — die Dateinamen tragen einen Hash, sie
  ändern sich nie unbemerkt.
- **Bilder** 30 Tage mit `stale-while-revalidate`, falls doch ein Motiv
  getauscht wird.
- **HTML** ohne Cache. Sonst sehen Besucher nach einer Preisänderung noch
  tagelang den alten Preis.
- `cleanUrls` steht bewusst auf `false`. Es würde `/versand.html` auf
  `/versand` umleiten — die `canonical`-Tags und die `sitemap.xml` nennen aber
  die `.html`-Adressen. Wer die kurzen URLs will, muss beides mitziehen.

Die `404.html` liefert Vercel bei statischen Projekten automatisch als
Fehlerseite aus; dafür ist keine Konfiguration nötig.

## Vor dem Livegang

Der Code ist fertig; offen sind fast nur noch Geschäftsentscheidungen.

**Ohne diese drei Registrierungen darf nicht verkauft werden.** Eine Powerbank
ist gleichzeitig Batterie, Elektrogerät und kommt in einer Verpackung:

- [ ] Batterien (BattDG) und Elektrogeräte (ElektroG) bei der Stiftung EAR
- [ ] Verpackungen bei LUCID, dazu ein Vertrag mit einem dualen System
- [ ] UN38.3-Prüfnachweis vom Lieferanten; Akkuversand (UN 3481, Gefahrgut)
      mit dem Versanddienstleister klären

**Lieferant und Herkunft:**

Smilelink, Modell SML-MB1, Guangdong (China). OEM/ODM mit eigenem Logo
möglich. Vor dem Import zu klären: MOQ und Stückpreis, CE/RoHS, der
UN38.3-Prüfnachweis.

> **Achtung, Widerspruch:** Die Startseite wirbt mit „Versand aus
> Deutschland", der Footer mit „Entwickelt in Deutschland". Beides gilt nur,
> wenn wirklich aus einem deutschen Lager versendet wird. Bei Direktversand
> aus Guangdong sind beide Aussagen falsch und abmahnfähig — dann müssen
> stattdessen die echte Herkunft, eine realistische Laufzeit und ein Hinweis
> auf mögliche Einfuhrabgaben auf der Seite stehen. Das ist vor dem ersten
> Verkauf zu entscheiden, nicht danach.

**Daten eintragen:**

- [ ] Domain: alle `https://voltiq.de` ersetzen — HTML (`canonical`, `og:url`,
      JSON-LD), `robots.txt`, `sitemap.xml`
- [ ] Preis an *einer* Stelle: `PRODUCT.priceCents` in `assets/checkout.js`.
      `renderPrices()` schreibt ihn in jedes `[data-price]`. Zusätzlich der
      `price` im JSON-LD von `index.html`
- [ ] Zahlungsanbieter: `PRODUCT.provider` auf `stripe` oder `shopify`,
      Varianten-IDs je Farbe nachtragen
- [ ] Versandkosten, Lieferzeit und Versandherkunft in `versand.html` — und
      erst dann die Zusagen im Kaufblock von `index.html` stehen lassen
- [ ] Alle `<mark class="ph">`-Platzhalter in den Rechtstexten füllen
      (Impressum 13, Versand 8, Datenschutz 7, …), Texte juristisch prüfen
      lassen und danach die `data-placeholder-notice`-Kästen löschen

**Rechtliche Fallstricke, die im Code schon berücksichtigt sind:**

- Kein Cookie-Banner nötig, solange kein Tracking eingebunden ist. Sobald
  Analyse- oder Zahlungs-Skripte dazukommen, greift § 25 TDDDG.
- Auf der Startseite steht „Gewährleistung“, nicht „Garantie“. Eine Garantie
  ist eine freiwillige Zusage und müsste nach § 479 BGB vollständig in
  Textform mitgeliefert werden.
- Beworben werden nur die gesetzlichen 14 Tage Widerruf. Eine längere
  freiwillige Frist wird mit der Werbung verbindlich.
- **Der Streichpreis ist scharf gestellt.** `PRODUCT.listPriceCents` in
  `assets/checkout.js` steht auf 3500, die Seite wirbt also mit „statt
  35,00 €“. Nach § 11 PAngV darf eine Preisermäßigung nur mit dem
  **niedrigsten Preis der letzten 30 Tage** beworben werden. Wurde das Gerät
  nie zu 35 € angeboten, ist das ein Mondpreis und abmahnfähig. Auf `0`
  setzen, dann verschwindet die gesamte Angebots-Auszeichnung von der Seite —
  Badge, Streichpreis und Prozentangabe.

**Nach dem Deploy prüfen:**

- [ ] Rich Results Test — https://search.google.com/test/rich-results
- [ ] OG-Vorschau — https://developers.facebook.com/tools/debug
- [ ] Server liefert `404.html` wirklich als 404 aus
