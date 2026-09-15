/* ==========================================================================
   VOLTIQ — Checkout-Anbindung
   --------------------------------------------------------------------------
   Die Landingpage kennt keinen Zahlungsanbieter. Sie ruft nur VOLTIQ.checkout()
   auf; welcher Anbieter dahinter steckt, entscheidet PRODUCT.provider.

   Anbinden in drei Schritten:
     1. PRODUCT unten ausfuellen (Preis, SKU, Farben).
     2. provider auf 'stripe' oder 'shopify' setzen.
     3. Im passenden Adapter die zwei bis drei markierten Werte eintragen.

   Bis dahin laeuft provider 'none': der Button zeigt einen Hinweis statt
   eines kaputten Checkouts.

   Jeder Button mit  data-checkout  wird automatisch verdrahtet. Die aktuell
   gewaehlte Farbe kommt aus dem Farbwaehler (.sw.on) der Startseite.
   ========================================================================== */
(function () {
  'use strict';

  /* ----------------------------------------------------------------------
     PRODUKT — einzige Stelle, an der Preis und Artikeldaten stehen.
     Der sichtbare Preis im HTML muss dazu passen; renderPrices() unten
     schreibt ihn auf Wunsch automatisch.
     ---------------------------------------------------------------------- */
  var PRODUCT = {
    provider: 'none',            // 'none' | 'stripe' | 'shopify' | 'custom'
    sku: 'VQ-MAG-5000',
    name: 'VOLTIQ MAG',
    priceCents: 2999,            // Verkaufspreis in Cent
    currency: 'EUR',
    colors: {
      silber: { label: 'Titan Silber',   variant: null },  // TODO: Varianten-ID
      orange: { label: 'Copper Orange',  variant: null },
      blau:   { label: 'Midnight Navy',  variant: null }
    }
  };

  /* ----------------------------------------------------------------------
     ADAPTER
     Jeder bekommt (order) und ist selbst fuer die Weiterleitung zustaendig.
     order = { sku, name, color, colorLabel, variant, quantity, priceCents, currency }
     ---------------------------------------------------------------------- */
  var adapters = {

    /* Platzhalter, solange kein Anbieter feststeht. */
    none: function (order) {
      notify(
        'Der Checkout ist noch nicht angebunden.\n\n' +
        order.quantity + '× ' + order.name + ' — ' + order.colorLabel +
        ' — ' + formatPrice(order.priceCents * order.quantity) + '\n\n' +
        'Anbieter in assets/checkout.js setzen (PRODUCT.provider).'
      );
      console.info('[VOLTIQ] Checkout angefordert:', order);
    },

    /* --------------------------------------------------------------------
       STRIPE CHECKOUT
       Zwei Wege:
       (a) Payment Link  — kein Backend noetig. Link in stripe.paymentLinks
           je Farbe eintragen; Stripe uebernimmt Kasse, Steuer und Versand.
       (b) Session ueber eigene Route — stripe.endpoint setzen. Die Route
           erzeugt serverseitig eine Checkout Session und gibt { url } zurueck.
           Der Secret Key darf NIE im Frontend stehen.
       -------------------------------------------------------------------- */
    stripe: function (order) {
      var cfg = PRODUCT.stripe || {};
      var link = cfg.paymentLinks && cfg.paymentLinks[order.color];

      if (link) {
        window.location.href = link;
        return;
      }

      if (!cfg.endpoint) {
        return fail('Stripe ist gewaehlt, aber weder paymentLinks noch endpoint gesetzt.');
      }

      return fetch(cfg.endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(order)
      })
        .then(function (r) {
          if (!r.ok) throw new Error('HTTP ' + r.status);
          return r.json();
        })
        .then(function (data) {
          if (!data.url) throw new Error('Antwort ohne url');
          window.location.href = data.url;
        })
        .catch(function (err) {
          fail('Checkout konnte nicht gestartet werden.', err);
        });
    },

    /* --------------------------------------------------------------------
       SHOPIFY
       Der Permalink-Weg braucht kein SDK: /cart/<variantId>:<menge>
       shopify.domain und die Varianten-IDs in PRODUCT.colors eintragen.
       -------------------------------------------------------------------- */
    shopify: function (order) {
      var cfg = PRODUCT.shopify || {};
      if (!cfg.domain) return fail('Shopify ist gewaehlt, aber shopify.domain fehlt.');
      if (!order.variant) return fail('Fuer die Farbe "' + order.color + '" fehlt die Varianten-ID.');

      window.location.href =
        'https://' + cfg.domain + '/cart/' + order.variant + ':' + order.quantity;
    },

    /* Eigenes Backend, eigener Warenkorb. */
    custom: function (order) {
      fail('Adapter "custom" ist noch nicht implementiert.', order);
    }
  };

  /* ----------------------------------------------------------------------
     Hilfsfunktionen
     ---------------------------------------------------------------------- */
  function formatPrice(cents) {
    return new Intl.NumberFormat('de-DE', {
      style: 'currency',
      currency: PRODUCT.currency
    }).format(cents / 100);
  }

  function selectedColor() {
    var on = document.querySelector('.sw.on');
    var key = (on && on.dataset.c) || Object.keys(PRODUCT.colors)[0];
    var color = PRODUCT.colors[key] || {};
    return {
      color: key,
      colorLabel: color.label || (on && on.dataset.name) || key,
      variant: color.variant || null
    };
  }

  function buildOrder(opts) {
    var sel = selectedColor();
    return {
      sku: PRODUCT.sku,
      name: PRODUCT.name,
      color: sel.color,
      colorLabel: sel.colorLabel,
      variant: sel.variant,
      quantity: (opts && opts.quantity) || 1,
      priceCents: PRODUCT.priceCents,
      currency: PRODUCT.currency
    };
  }

  function notify(message) {
    window.alert(message);
  }

  function fail(message, detail) {
    console.error('[VOLTIQ] ' + message, detail || '');
    notify('Da ist etwas schiefgelaufen. Bitte spaeter erneut versuchen.');
  }

  /* ----------------------------------------------------------------------
     Oeffentliche API
     ---------------------------------------------------------------------- */
  var VOLTIQ = {
    product: PRODUCT,

    checkout: function (opts) {
      var adapter = adapters[PRODUCT.provider];
      if (!adapter) return fail('Unbekannter Anbieter: ' + PRODUCT.provider);
      return adapter(buildOrder(opts));
    },

    /* Schreibt den Preis aus PRODUCT in jedes [data-price] — damit HTML und
       Konfiguration nicht auseinanderlaufen koennen. */
    renderPrices: function () {
      var text = formatPrice(PRODUCT.priceCents);
      document.querySelectorAll('[data-price]').forEach(function (el) {
        el.textContent = text;
      });
    }
  };

  window.VOLTIQ = VOLTIQ;

  /* ----------------------------------------------------------------------
     Buttons verdrahten
     ---------------------------------------------------------------------- */
  document.addEventListener('DOMContentLoaded', function () {
    VOLTIQ.renderPrices();

    document.querySelectorAll('[data-checkout]').forEach(function (el) {
      el.addEventListener('click', function (ev) {
        ev.preventDefault();
        VOLTIQ.checkout({ quantity: Number(el.dataset.quantity) || 1 });
      });
    });
  });
})();
