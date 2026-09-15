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
- Keine durchgestrichenen „Statt“-Preise ohne echte 30-Tage-Historie (PAngV).

**Nach dem Deploy prüfen:**

- [ ] Rich Results Test — https://search.google.com/test/rich-results
- [ ] OG-Vorschau — https://developers.facebook.com/tools/debug
- [ ] Server liefert `404.html` wirklich als 404 aus
