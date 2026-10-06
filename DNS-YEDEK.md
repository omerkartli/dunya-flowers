# DNS yedeği — eski site (4 Ekim 2026 itibarıyla)

GitHub'a geçmeden önce Natro'daki kayıtların aynısı. Eski siteye geri dönmek
gerekirse bu tablo birebir geri girilir.

Nerede: Natro → Hosting Yönetimi → Web Hosting Hesapları → Sınırsız Pro Hosting
(dunyaflowers.com) → Yönet → Web Alanı Yönetimi → dunyaflowers.com satırı
"Web Sitesi" menüsü → **DNS Yönetimi**.

## DNS sunucuları (Alan Adı Yönetimi → dunyaflowers.com → DNS simgesi)

| 1.DNS | 2.DNS |
|---|---|
| NS1.NATROHOST.COM | NS2.NATROHOST.COM |

## Kayıtlar

| Tür | Zone | Adres / Data |
|---|---|---|
| A | dunyaflowers.com | 94.73.149.62 |
| CNAME | www.dunyaflowers.com | dunyaflowers.com. |
| CNAME | ftp.dunyaflowers.com | dunyaflowers.com. |
| TXT | dunyaflowers.com | "v=spf1 include:_spfcls.natrohost.com include:_netblockshalon.natrohost.com ~all" |
| MX | — | Kayıt yok (domainde mail kullanılmıyor) |
| SRV | — | Kayıt yok |

Eski site Natro'da Windows 2019 / Plesk hostingde (94.73.149.62) duruyor;
hosting 14 Kasım 2026'da bitiyor. Ondan sonra eskiye dönüş mümkün olmaz.

## Eskiye dönüş

1. GitHub için eklenen 4 A kaydını (185.199.108–111.153) sil.
2. A kaydı ekle: `dunyaflowers.com` → `94.73.149.62`
3. `www` CNAME'ini (`omerkartli.github.io`) sil, yerine
   `www.dunyaflowers.com` → `dunyaflowers.com.` ekle.
4. ftp CNAME ve TXT kaydına dokunulmadı; olduğu gibi kalır.

## GitHub'a geçiş (4 Ekim 2026'da girildi)

| Tür | Zone | Adres |
|---|---|---|
| A | dunyaflowers.com | 185.199.108.153 |
| A | dunyaflowers.com | 185.199.109.153 |
| A | dunyaflowers.com | 185.199.110.153 |
| A | dunyaflowers.com | 185.199.111.153 |
| CNAME | www.dunyaflowers.com | omerkartli.github.io. |

ftp CNAME ve TXT (spf) kaydı değiştirilmedi.

Natro paneli notu: CNAME eklerken "Alt Alan Adı" = `www`, "Server" =
`omerkartli.github.io.` (sonunda nokta). A kaydında "Alt Alan Adı" boş bırakılır.

## Cloudflare'e geçiş (6 Ekim 2026)

DNS yönetimi Natro'dan Cloudflare'e taşındı (Cloudflare hesabı:
Dunya.flowerss@gmail.com, Free plan). Alan adı kaydı hâlâ Natro'da.

Natro → Alan Adı Yönetimi → dunyaflowers.com → DNS Sunucuları:

| 1.DNS | 2.DNS |
|---|---|
| camilo.ns.cloudflare.com | kayleigh.ns.cloudflare.com |

Cloudflare'deki kayıtlar (hepsi **DNS only / gri bulut**; turuncu yapılırsa
GitHub Pages HTTPS sertifikasını yenileyemeyebilir):

| Tür | Ad | Değer |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | omerkartli.github.io |
| TXT | @ | "v=spf1 include:_spfcls.natrohost.com include:_netblockshalon.natrohost.com ~all" |

Eski `ftp` CNAME kaydı silindi.

Geri dönüş: Natro'da DNS sunucularını tekrar NS1.NATROHOST.COM /
NS2.NATROHOST.COM yapmak. Natro hostingi 14 Kasım 2026'da bitince Natro
tarafındaki kayıtlar silinebilir; o tarihten sonra bu yol çalışmaz.

**Dikkat:** Alan adı kaydı da 14 Kasım 2026'da bitiyor. Ondan önce Natro'da
yenilenmeli ya da Cloudflare Registrar'a transfer edilmeli (transfer 1 yıllık
yenilemeyi de içerir).

## Cloudflare Registrar'a transfer (6 Ekim 2026)

Alan adı kaydının Natro'dan Cloudflare Registrar'a transferi başlatıldı
(ücret $10.46, 1 yıllık uzatma dahil, otomatik yenilemeli). Kayıt sahibi:
Ali Rıza Kaçar / Dünya Flowers, e-posta dunya.flowerss@gmail.com.
Transfer en geç 7 gün içinde tamamlanır; tamamlanınca yeni bitiş tarihi
14 Kasım 2027 olur. Natro hostingi yenilenmeyecek.
