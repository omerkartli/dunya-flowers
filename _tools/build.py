#!/usr/bin/env python3
"""Sitenin otomatik üretilen kısımlarını günceller.

- index.html: ürün kartları (#grid içinde) ve ürün bilgisi etiketi (JSON-LD),
  fiyat aralığı rozeti
- özel gün sayfaları (_tools/ozel_gunler.py)
- sitemap.xml (sayfalar ve ürün fotoğrafları)

Panelde products.json değişince GitHub Actions (.github/workflows/build.yml) bu
betiği kendiliğinden çalıştırır. Elle çalıştırmak için:

    python3 _tools/build.py
"""
import html, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://www.dunyaflowers.com"
e = html.escape


def load_products():
    data = json.loads((ROOT / "products.json").read_text(encoding="utf-8"))
    items = data if isinstance(data, list) else data.get("urunler", [])
    out = []
    for p in items:
        try:
            price = float(p.get("price") or 0)
        except (TypeError, ValueError):
            price = 0
        if p.get("active") is False or not p.get("name") or not p.get("img") or price <= 0:
            continue
        p = dict(p, price=int(price) if price == int(price) else price)
        out.append(p)
    return out


def img_path(v):
    return v if re.match(r"^(https?:)?/", v) else "/" + v


def tr_num(n):
    return f"{n:,}".replace(",", ".")


def cards(products):
    # assets/site.js'deki renderGrid ile aynı yapı; sayfa açılınca JS yeniden çizer
    out = []
    for i, p in enumerate(products):
        tag = f'<span class="tag">{e(p["tag"])}</span>' if p.get("tag") else ""
        out.append(f'''
      <article class="card">
        <div class="ph">
          <img loading="lazy" decoding="async" src="{e(img_path(p["img"]))}" alt="{e(p["name"])} çiçek buketi">
          {tag}
        </div>
        <div class="body">
          <h3>{e(p["name"])}</h3>
          <p class="desc">{e(p.get("desc", ""))}</p>
          <div class="row">
            <span class="price">{tr_num(p["price"])}<small>₺</small></span>
            <button class="btn btn-primary" data-order="{i}">Sipariş Ver</button>
          </div>
        </div>
      </article>''')
    return "".join(out) + "\n      "


def schema(products):
    data = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Dünya Flowers çiçekleri",
        "itemListElement": [{
            "@type": "ListItem",
            "position": i + 1,
            "item": {
                "@type": "Product",
                "name": p["name"],
                "image": SITE + img_path(p["img"]),
                "description": p.get("desc") or p["name"],
                "brand": {"@type": "Brand", "name": "Dünya Flowers"},
                "offers": {
                    "@type": "Offer",
                    "price": str(p["price"]),
                    "priceCurrency": "TRY",
                    "availability": "https://schema.org/InStock",
                    "url": SITE + "/#urunler",
                    "seller": {"@type": "Organization", "name": "Dünya Flowers"},
                },
            },
        } for i, p in enumerate(products)],
    }
    return '<script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False, indent=2) + "\n</script>"


def between(text, start, end, inner):
    pat = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    if not pat.search(text):
        sys.exit(f"index.html içinde {start} … {end} işaretleri bulunamadı")
    return pat.sub(lambda m: start + inner + end, text, count=1)


def main():
    products = load_products()
    idx_path = ROOT / "index.html"
    idx = idx_path.read_text(encoding="utf-8")
    idx = between(idx, "<!-- urunler:basla -->", "<!-- urunler:bitir -->", cards(products))
    idx = between(idx, "<!-- urun-sema:basla -->", "<!-- urun-sema:bitir -->", "\n" + schema(products) + "\n")
    if products:
        prices = [p["price"] for p in products]
        idx = re.sub(r'(<b id="priceRange">).*?(</b>)',
                     lambda m: f"{m.group(1)}{tr_num(min(prices))} – {tr_num(max(prices))} ₺{m.group(2)}", idx, count=1)
    idx_path.write_text(idx, encoding="utf-8")

    sys.path.insert(0, str(ROOT / "_tools"))
    import ozel_gunler  # index.html güncellendikten sonra (ortak üst menü/alt bilgi için)

    def cards_for(slug):
        sec = [p for p in products if slug in (p.get("gunler") or [])]
        return cards(sec or products)

    pages = ["/"] + ozel_gunler.main(cards_for)

    # Site haritası: sayfalar + ana sayfadaki ürün fotoğrafları
    imgs = "".join(f"\n    <image:image><image:loc>{e(SITE + img_path(p['img']))}</image:loc></image:image>" for p in products)
    rows = []
    for u in pages:
        extra = imgs if u == "/" else ""
        rows.append(f"  <url><loc>{SITE}{u}</loc>{extra}</url>")
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
        + "\n".join(rows) + "\n</urlset>\n", encoding="utf-8")
    print(f"{len(products)} ürün, {len(pages)} sayfa güncellendi")


if __name__ == "__main__":
    main()
