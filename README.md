# Dünya Flowers

Çekmeköy'deki Dünya Flowers çiçekçisinin sitesi: https://www.dunyaflowers.com

Düz HTML/CSS/JS, build adımı yok. GitHub Pages'te `main` dalının kökünden yayınlanır.

- `index.html` — sayfanın tamamı
- `products.json` — ürünler ve fiyatlar (yönetim panelinden düzenlenir)
- `.pages.yml` — yönetim paneli (Pages CMS) ayarları
- `images/` — ürün fotoğrafları
- `CNAME` — özel domain (`www.dunyaflowers.com`)

Sipariş formu dükkânın WhatsApp hattına (0533 422 29 94) mesaj açar.

## Yönetim paneli

Ürün, fiyat ve fotoğraflar https://app.pagescms.org üzerinden düzenlenir:
GitHub hesabıyla giriş yapılır, `dunya-flowers` deposu seçilir, "Ürünler"
açılır. Kaydedilen her değişiklik `main` dalına commit olur ve site birkaç
dakika içinde güncellenir. "Sitede göster" kapatılan ürün silinmeden gizlenir.

## Domain (Natro DNS)

| Tür | Ad | Değer |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | omerkartli.github.io |

Eski siteyi gösteren A/CNAME kayıtları silinir; MX ve TXT kayıtlarına dokunulmaz.
DNS yayıldıktan sonra Settings → Pages → "Enforce HTTPS" işaretlenir.
