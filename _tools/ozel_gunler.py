#!/usr/bin/env python3
"""Özel gün sayfalarını üretir: /ozel-gunler/ ve her gün için /<slug>/index.html.

Ortak üst menü, alt bilgi ve sipariş penceresi index.html'den alınır. Bu dosya
_tools/build.py tarafından çağrılır (index.html güncellendikten sonra import edilir):

    python3 _tools/build.py

Ürünler sayfada products.json'dan yüklenir. Panelde (Pages CMS) bir ürünün
"Özel günler" alanında işaretli günlerin sayfasında o ürün gösterilir; bir güne
hiç ürün işaretlenmemişse o sayfada tüm ürünler görünür.
"""
import html, json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://www.dunyaflowers.com"
WA = "905334222994"

GUNLER = [
  {
    "slug": "ogretmenler-gunu", "ad": "Öğretmenler Günü", "tarih": "24 Kasım 2026, Salı", "sira": "2026-11-24",
    "title": "Öğretmenler Günü Çiçekleri Çekmeköy",
    "desc": "Öğretmenler Günü (24 Kasım) için buket ve saksı çiçekleri. Çekmeköy, Ümraniye ve Sancaktepe'ye teslimat, dükkândan teslim alma. WhatsApp'tan kolay sipariş.",
    "h1": "Öğretmenler Günü çiçekleri",
    "lead": "24 Kasım'da öğretmeninize teşekkür etmenin en zarif yolu: özenle hazırlanmış taze bir buket ya da sınıfında uzun süre yaşayacak bir saksı çiçeği.",
    "metin": [
      ("Öğretmeninize hangi çiçek?", [
        "Öğretmenler Günü'nde en çok tercih edilenler küçük ve orta boy buketler ile saksı çiçekleri. Saksı çiçekleri (orkide, barış çiçeği gibi) sınıfta ya da öğretmenler odasında haftalarca kalır; buketler ise o güne özel, renkli bir sürpriz olur.",
        "Bütçeyi sınıf olarak birleştirip tek ve daha büyük bir tasarım göndermek de sık yapılan bir tercih. Kart notuna öğrencilerin adlarını yazabilirsiniz.",
      ]),
      ("Sipariş verirken", [
        "• 24 Kasım hafta içine denk geldiğinde siparişler yoğunlaşır; birkaç gün önceden sipariş vermenizi öneririz.",
        "• Okula gönderim için adres alanına okulun adını, sınıfı ve öğretmenin adını yazın; teslim saatini WhatsApp'tan birlikte netleştiririz.",
        "• Dükkânımızdan (Çekmeköy, Demokrasi Cd. No:15/A) her gün 08:00–21:00 arasında teslim alabilirsiniz.",
      ]),
    ],
    "sss": [
      ("Okula teslimat yapıyor musunuz?", "Çekmeköy, Ümraniye ve Sancaktepe'deki adreslere teslimat yapıyoruz; okul da bu adreslerden biri olabilir. Teslimat ücreti adrese göre sipariş onayında bildirilir."),
      ("Kart notu ekleyebilir miyim?", "Evet. Sipariş formundaki “Kart notu” alanına yazdığınız mesajı karta yazıp çiçeğe ekliyoruz."),
    ],
  },
  {
    "slug": "yilbasi", "ad": "Yılbaşı", "tarih": "31 Aralık 2026, Perşembe", "sira": "2026-12-31",
    "title": "Yılbaşı Çiçekleri ve Kokina Çekmeköy",
    "desc": "Yılbaşı için kokina, kış temalı buket ve aranjmanlar. Çekmeköy, Ümraniye ve Sancaktepe'ye teslimat. Dünya Flowers'tan WhatsApp ile sipariş.",
    "h1": "Yılbaşı çiçekleri ve kokina",
    "lead": "Kozalak, kurutulmuş portakal, kırmızı meyveler ve kokinayla hazırlanan kış tasarımları; evinize, iş yerinize ya da sevdiklerinize yeni yıl için.",
    "metin": [
      ("Yeni yıla taze bir başlangıç", [
        "Yılbaşı tasarımlarımızda kış bitkileri, kokina ve sıcak renkler öne çıkıyor. Kutuda aranjmanlar masa süsü olarak, buketler ise hediye olarak tercih ediliyor.",
        "Kurumsal hediye ya da birden fazla adrese gönderim için WhatsApp'tan yazın; adet ve bütçeye göre birlikte planlayalım.",
      ]),
      ("Sipariş verirken", [
        "• Aralık'ın son haftası yoğun geçer; teslim tarihini birkaç gün önceden belirlemenizi öneririz.",
        "• Teslimat bölgemiz: Çekmeköy, Ümraniye ve Sancaktepe. Dükkândan teslim almak için her gün 08:00–21:00 açığız.",
      ]),
    ],
    "sss": [
      ("Kokina ne kadar dayanır?", "Kokina dalları serin ve doğrudan güneş almayan bir yerde uzun süre canlılığını korur; aranjmanın suyunu düzenli kontrol etmeniz yeterli."),
      ("Toplu sipariş verebilir miyim?", "Evet. Adet, tarih ve bütçeyi WhatsApp'tan yazmanız yeterli; uygun tasarımları birlikte seçelim."),
    ],
  },
  {
    "slug": "sevgililer-gunu", "ad": "Sevgililer Günü", "tarih": "14 Şubat 2027, Pazar", "sira": "2027-02-14",
    "title": "Sevgililer Günü Çiçekleri ve Kırmızı Gül Çekmeköy",
    "desc": "14 Şubat Sevgililer Günü için kırmızı gül buketleri ve özel tasarımlar. Çekmeköy, Ümraniye ve Sancaktepe'ye teslimat. WhatsApp'tan sipariş.",
    "h1": "Sevgililer Günü çiçekleri",
    "lead": "Klasik kırmızı güllerden gösterişli özel tasarımlara; 14 Şubat'ta sevdiğinize en taze haliyle ulaşan çiçekler.",
    "metin": [
      ("Kırmızı gül mü, farklı bir tasarım mı?", [
        "Sevgililer Günü'nün klasiği kırmızı gül buketleri. Daha farklı bir şey arıyorsanız pembe ve pudra tonlarında karışık buketler ya da kutu tasarımlar da güzel bir seçenek.",
        "Aklınızdaki renk, gül sayısı ya da bütçe için WhatsApp'tan yazın; size özel hazırlayalım.",
      ]),
      ("Sipariş verirken", [
        "• 14 Şubat yılın en yoğun günü; önceden sipariş vermeniz, istediğiniz saatte teslim için en garantili yol.",
        "• Kart notunuzu sipariş formuna yazın, karta biz yazalım.",
        "• Teslimat bölgemiz: Çekmeköy, Ümraniye ve Sancaktepe.",
      ]),
    ],
    "sss": [
      ("Belirli bir saatte teslim mümkün mü?", "Sipariş formunda saat aralığı seçebilirsiniz; yoğun günlerde teslim saatini sipariş onayında birlikte netleştiriyoruz."),
      ("Gül sayısını seçebilir miyim?", "Evet. İstediğiniz gül sayısını ve rengini WhatsApp'tan yazın, fiyatını hemen iletelim."),
    ],
  },
  {
    "slug": "kadinlar-gunu", "ad": "Kadınlar Günü", "tarih": "8 Mart 2027, Pazartesi", "sira": "2027-03-08",
    "title": "8 Mart Kadınlar Günü Çiçekleri Çekmeköy",
    "desc": "8 Mart Dünya Kadınlar Günü için buket ve saksı çiçekleri; iş yerleri için toplu sipariş. Çekmeköy, Ümraniye ve Sancaktepe'ye teslimat.",
    "h1": "Kadınlar Günü çiçekleri",
    "lead": "8 Mart'ta annenize, eşinize, arkadaşınıza ya da iş arkadaşlarınıza taze bir buketle değer verdiğinizi gösterin.",
    "metin": [
      ("Tek bir buket ya da tüm ekip için", [
        "Kadınlar Günü'nde hem tekli hediyeler hem de iş yerleri için toplu siparişler hazırlıyoruz. Toplu siparişlerde aynı tasarımı birden fazla adet hazırlayabilir ya da bütçeye göre farklı boylarda seçenekler sunabiliriz.",
      ]),
      ("Sipariş verirken", [
        "• Toplu siparişlerde adet ve teslim adresini birkaç gün önceden iletmeniz hazırlık için önemli.",
        "• Teslimat bölgemiz: Çekmeköy, Ümraniye ve Sancaktepe. Dükkândan teslim alma her gün 08:00–21:00.",
      ]),
    ],
    "sss": [
      ("İş yerine toplu teslimat yapıyor musunuz?", "Evet, teslimat bölgemizdeki iş yerlerine toplu teslimat yapıyoruz. Adet ve adresi WhatsApp'tan yazın, fiyatı iletelim."),
    ],
  },
  {
    "slug": "anneler-gunu", "ad": "Anneler Günü", "tarih": "9 Mayıs 2027, Pazar", "sira": "2027-05-09",
    "title": "Anneler Günü Çiçekleri Çekmeköy",
    "desc": "Anneler Günü (9 Mayıs 2027) için buket, gül ve saksı çiçekleri. Çekmeköy, Ümraniye ve Sancaktepe'ye teslimat. WhatsApp'tan kolay sipariş.",
    "h1": "Anneler Günü çiçekleri",
    "lead": "Annenize en güzel teşekkür: pembe güller, lilyumlar ve mevsimin en taze çiçekleriyle hazırlanan buketler ya da uzun ömürlü saksı çiçekleri.",
    "metin": [
      ("Annenize hangi çiçek?", [
        "Anneler Günü'nde pembe ve pudra tonlarındaki buketler, lilyum ve gül karışımları en çok tercih edilenler. Bakımı kolay ve uzun ömürlü bir hediye isterseniz orkide ya da barış çiçeği gibi saksı çiçekleri güzel bir seçenek.",
        "Anneler Günü her yıl Mayıs'ın ikinci pazarı kutlanır; 2027'de 9 Mayıs Pazar gününe denk geliyor.",
      ]),
      ("Sipariş verirken", [
        "• Anneler Günü haftası yılın en yoğun dönemlerinden; birkaç gün önceden sipariş verip teslim tarihini seçmenizi öneririz.",
        "• Kart notunuzu formda yazın, el yazısıyla karta geçirelim.",
        "• Teslimat bölgemiz: Çekmeköy, Ümraniye ve Sancaktepe. Dükkândan teslim alma her gün 08:00–21:00.",
      ]),
    ],
    "sss": [
      ("Pazar günü teslimat yapıyor musunuz?", "Dükkânımız her gün 08:00–21:00 açık. Pazar günü teslimat için sipariş verirken tarihi seçin; teslim saatini sipariş onayında birlikte netleştiririz."),
      ("Başka şehre gönderim var mı?", "Şu an Çekmeköy, Ümraniye ve Sancaktepe'ye teslimat yapıyoruz."),
    ],
  },
  {
    "slug": "babalar-gunu", "ad": "Babalar Günü", "tarih": "20 Haziran 2027, Pazar", "sira": "2027-06-20",
    "title": "Babalar Günü Çiçek ve Saksı Bitkileri Çekmeköy",
    "desc": "Babalar Günü (20 Haziran 2027) için saksı bitkileri ve buketler. Çekmeköy, Ümraniye ve Sancaktepe'ye teslimat. WhatsApp'tan sipariş.",
    "h1": "Babalar Günü çiçekleri",
    "lead": "Babanıza evinde ya da ofisinde uzun süre kalacak bir saksı bitkisi ya da sade ve şık bir buket.",
    "metin": [
      ("Babalar için öneriler", [
        "Babalar Günü'nde bakımı kolay saksı bitkileri ve yeşil tonların ağır bastığı sade buketler öne çıkıyor. Saksı bitkileri hem uzun ömürlü hem de ofis masası için uygun.",
        "Babalar Günü her yıl Haziran'ın üçüncü pazarı kutlanır; 2027'de 20 Haziran'a denk geliyor.",
      ]),
      ("Sipariş verirken", [
        "• Teslimat bölgemiz: Çekmeköy, Ümraniye ve Sancaktepe.",
        "• Dükkândan teslim almak için her gün 08:00–21:00 açığız.",
      ]),
    ],
    "sss": [
      ("Saksı bitkisinin bakımı zor mu?", "Seçtiğimiz saksı bitkileri bakımı kolay türlerden; teslimde kısa bakım bilgisini de iletiyoruz."),
    ],
  },
  {
    "slug": "dogum-gunu", "ad": "Doğum Günü", "tarih": "", "sira": "",
    "title": "Doğum Günü Çiçekleri Çekmeköy",
    "desc": "Doğum günü için renkli buketler, güller ve saksı çiçekleri. Çekmeköy, Ümraniye ve Sancaktepe'ye teslimat; kart notu ekleme. WhatsApp'tan sipariş.",
    "h1": "Doğum günü çiçekleri",
    "lead": "Renkli bir buket ve özel bir kart notuyla doğum günü sürprizi; dilediğiniz gün, dilediğiniz adrese.",
    "metin": [
      ("Doğum günü sürprizi", [
        "Doğum günlerinde canlı renkli karışık buketler ve güller en çok tercih edilenler. Kişinin sevdiği rengi ya da çiçeği biliyorsanız WhatsApp'tan yazın, ona göre hazırlayalım.",
        "Sipariş formunda teslim tarihini ve saat aralığını seçebilir, kart notunuzu ekleyebilirsiniz.",
      ]),
      ("Teslimat", [
        "• Teslimat bölgemiz: Çekmeköy, Ümraniye ve Sancaktepe. Teslimat ücreti adrese göre sipariş onayında bildirilir.",
        "• Dükkândan teslim alma her gün 08:00–21:00.",
      ]),
    ],
    "sss": [
      ("Sürpriz teslimat yapabilir misiniz?", "Evet. Alıcının adı ve telefonunu formda yazmanız yeterli; teslimatta göndereni kart notunda belirtiyoruz."),
    ],
  },
  {
    "slug": "acilis-tebrik", "ad": "Açılış ve Tebrik", "tarih": "", "sira": "",
    "title": "Açılış ve Tebrik Çiçekleri Çekmeköy",
    "desc": "Açılış, yeni iş, terfi ve tebrik için aranjman ve saksı çiçekleri. Çekmeköy, Ümraniye ve Sancaktepe'ye teslimat. WhatsApp'tan sipariş.",
    "h1": "Açılış ve tebrik çiçekleri",
    "lead": "Yeni bir iş yeri, terfi ya da başarı… Tebriklerinizi gösterişli bir aranjman ya da uzun ömürlü bir saksı çiçeğiyle iletin.",
    "metin": [
      ("Açılışa ve tebrike uygun tasarımlar", [
        "Açılış ve tebriklerde vazoda ya da kutuda aranjmanlar ve büyük saksı çiçekleri tercih ediliyor; iş yerinde uzun süre kalıyor ve görünür bir yerde duruyor.",
        "Firma adına gönderimlerde kart notuna firma adını ve tebrik mesajınızı yazın. Büyük boy ya da özel bir tasarım için WhatsApp'tan yazın.",
      ]),
      ("Teslimat", [
        "• Teslimat bölgemiz: Çekmeköy, Ümraniye ve Sancaktepe.",
        "• Açılış saatine yetişmesi gereken siparişlerde saati sipariş onayında birlikte netleştiriyoruz.",
      ]),
    ],
    "sss": [
      ("Fatura kesiyor musunuz?", "Fatura bilgileri için sipariş sırasında WhatsApp'tan bize yazın."),
    ],
  },
]

ORTAK_SSS = [
  ("Aynı gün teslimat yapıyor musunuz?", "Evet, Çekmeköy, Ümraniye ve Sancaktepe'ye aynı gün teslimat yapıyoruz. Özel günlerde yoğunluk olduğu için önceden sipariş vermenizi öneririz."),
  ("Ödemeyi nasıl yapabilirim?", "Adrese gönderimde ödeme havale/EFT ile alınır; banka bilgileri sipariş onayında yalnızca 0533 422 29 94 numaralı WhatsApp hattımızdan iletilir. Dükkândan teslim alırken kredi kartı veya nakitle ödeyebilirsiniz."),
]
CARDS = lambda slug: ""  # build.py ürün kartlarını (HTML) buraya verir

idx = (ROOT / "index.html").read_text(encoding="utf-8")
def grab(pattern):
    m = re.search(pattern, idx, re.S)
    assert m, pattern
    return m.group(0)

FONTS = grab(r'<link rel="preconnect" href="https://fonts.googleapis.com">.*?rel="stylesheet">')
HEADER = grab(r"<header>.*?</header>")
FOOTER = grab(r"<footer>.*?</footer>")
AFTER = grab(r'<a class="fab".*?<!-- Order modal -->.*?</form>\s*</div>\s*</div>')
e = html.escape

def wa_link(text):
    from urllib.parse import quote
    return f"https://wa.me/{WA}?text={quote(text)}"

def head(title, desc, path, crumbs):
    url = SITE + path
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(crumbs)]}
    return f'''<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="canonical" href="{url}">
<title>{e(title)} | Dünya Flowers</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#3a1740">
<link rel="icon" type="image/png" href="/images/favicon.png">
<link rel="apple-touch-icon" href="/images/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:locale" content="tr_TR">
<meta property="og:site_name" content="Dünya Flowers">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/images/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
{FONTS}
<link rel="stylesheet" href="/assets/site.css">
<script type="application/ld+json">
{json.dumps(bc, ensure_ascii=False, indent=2)}
</script>
</head>'''

def crumbs_html(crumbs):
    parts = []
    for i, (n, u) in enumerate(crumbs):
        parts.append(f'<span aria-current="page">{e(n)}</span>' if i == len(crumbs) - 1 else f'<a href="{u}">{e(n)}</a> ›')
    return '<nav class="crumbs" aria-label="Konum">' + " ".join(parts) + "</nav>"

def diger(slug):
    out = []
    for g in GUNLER:
        if g["slug"] == slug:
            continue
        tarih = " <small>" + e(g["tarih"].split(",")[0]) + "</small>" if g["tarih"] else ""
        out.append(f'<a href="/{g["slug"]}/">{e(g["ad"])}{tarih}</a>')
    return "".join(out)

def page(g):
    path = f'/{g["slug"]}/'
    crumbs = [("Ana sayfa", "/"), ("Özel Günler", "/ozel-gunler/"), (g["ad"], path)]
    prose = ""
    for h, paras in g["metin"]:
        items = [p for p in paras if p.startswith("• ")]
        prose += f"<h2>{e(h)}</h2>\n"
        prose += "".join(f"<p>{e(p)}</p>\n" for p in paras if not p.startswith("• "))
        if items:
            prose += "<ul>" + "".join(f"<li>{e(p[2:])}</li>" for p in items) + "</ul>\n"
    sss = g["sss"] + ORTAK_SSS
    prose += "<h2>Sık sorulan sorular</h2>\n" + "".join(f"<h3>{e(q)}</h3>\n<p>{e(a)}</p>\n" for q, a in sss)
    wa = wa_link(f'Merhaba, {g["ad"]} için çiçek siparişi vermek istiyorum.')
    eyebrow = f'✿ {e(g["tarih"])}' if g["tarih"] else "✿ Çekmeköy'ün çiçekçisi"
    return f'''{head(g["title"], g["desc"], path, crumbs)}
<body data-gun="{g["slug"]}" data-gun-adi="{e(g["ad"])}">

{HEADER}

<main>
  <section class="occ-hero">
    <div class="wrap">
      {crumbs_html(crumbs)}
      <span class="eyebrow">{eyebrow}</span>
      <h1>{e(g["h1"])}</h1>
      <p class="lead">{e(g["lead"])}</p>
      <div class="hero-cta">
        <a class="btn btn-primary" href="#urunler">Çiçekleri İncele</a>
        <a class="btn btn-ghost" target="_blank" rel="noopener" href="{wa}">WhatsApp'tan Sorun</a>
      </div>
    </div>
  </section>

  <section class="block" id="urunler">
    <div class="wrap">
      <div class="head">
        <h2>{e(g["ad"])} için çiçeklerimiz</h2>
        <p>Tüm tasarımlar o gün taze çiçeklerle hazırlanır. Çekmeköy, Ümraniye ve Sancaktepe'ye aynı gün teslimat; dükkândan teslim alma her gün 08:00–21:00.</p>
      </div>
      <div class="grid" id="grid">{CARDS(g["slug"])}</div>
      <div class="custom">
        <div>
          <h3>Aklınızda başka bir tasarım mı var?</h3>
          <p>Renk, bütçe ya da çiçek türü fark etmez; bize yazın, {e(g["ad"])} için size özel hazırlayalım.</p>
        </div>
        <a class="btn btn-light" target="_blank" rel="noopener" href="{wa}">WhatsApp'tan Yazın</a>
      </div>
    </div>
  </section>

  <section class="block" id="bilgi">
    <div class="wrap">
      <div class="prose">
{prose}      </div>
      <h2 class="sr-only">Diğer özel günler</h2>
      <div class="occ-links">{diger(g["slug"])}</div>
    </div>
  </section>
</main>

{FOOTER}

{AFTER}

<script src="/assets/site.js"></script>
</body>
</html>
'''

def hub():
    path = "/ozel-gunler/"
    crumbs = [("Ana sayfa", "/"), ("Özel Günler", path)]
    dated = sorted([g for g in GUNLER if g["sira"]], key=lambda g: g["sira"])
    cards = "".join(f'<a class="occ-card" href="/{g["slug"]}/"><span>{e(g["tarih"] or "Her zaman")}</span><b>{e(g["ad"])}</b><p>{e(g["lead"])}</p></a>\n'
                    for g in dated + [g for g in GUNLER if not g["sira"]])
    return f'''{head("Özel Gün Çiçekleri Çekmeköy", "Öğretmenler Günü, Anneler Günü, Sevgililer Günü, yılbaşı, doğum günü ve açılış için çiçekler. Çekmeköy, Ümraniye ve Sancaktepe'ye teslimat.", path, crumbs)}
<body>

{HEADER}

<main>
  <section class="occ-hero">
    <div class="wrap">
      {crumbs_html(crumbs)}
      <span class="eyebrow">✿ Çekmeköy'ün çiçekçisi</span>
      <h1>Özel gün çiçekleri</h1>
      <p class="lead">Öğretmenler Günü'nden Anneler Günü'ne, doğum günlerinden açılışlara; her özel gün için taze çiçekler. Çekmeköy, Ümraniye ve Sancaktepe'ye teslimat, dükkândan teslim alma her gün 08:00–21:00.</p>
    </div>
  </section>
  <section class="block">
    <div class="wrap">
      <h2 class="sr-only">Yaklaşan özel günler</h2>
      <div class="occ-grid">
{cards}      </div>
    </div>
  </section>
</main>

{FOOTER}

<script src="/assets/site.js"></script>
</body>
</html>
'''

def main(cards_for):
    global CARDS
    CARDS = cards_for
    (ROOT / "ozel-gunler").mkdir(exist_ok=True)
    (ROOT / "ozel-gunler" / "index.html").write_text(hub(), encoding="utf-8")
    for g in GUNLER:
        (ROOT / g["slug"]).mkdir(exist_ok=True)
        (ROOT / g["slug"] / "index.html").write_text(page(g), encoding="utf-8")
    return ["/ozel-gunler/"] + [f'/{g["slug"]}/' for g in GUNLER]
